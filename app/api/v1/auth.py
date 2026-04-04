from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.core.config import settings
from app.core.database import get_supabase
import uuid

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


@router.post("/register")
async def register(request: RegisterRequest):
    supabase = get_supabase()
    
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    # Validate password length
    if len(request.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    
    # Check if user exists
    existing = supabase.table('users').select('*').eq('email', request.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Truncate password to 72 bytes for bcrypt (bcrypt limitation)
    password_bytes = request.password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # Hash password
    password_hash = pwd_context.hash(password_bytes.decode('utf-8'))
    
    # Create user
    user_data = {
        'id': str(uuid.uuid4()),
        'name': request.name,
        'email': request.email,
        'password_hash': password_hash,
        'is_active': True,
        'trust_score': 50.0,
        'total_exchanges': 0
    }
    
    result = supabase.table('users').insert(user_data).execute()
    
    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to create user")
    
    user = result.data[0]
    token = create_access_token({"sub": user['id'], "email": user['email']})
    
    return {
        "success": True,
        "token": token,
        "user": {
            "id": user['id'],
            "name": user['name'],
            "email": user['email'],
            "trust_score": user['trust_score']
        }
    }


@router.post("/login")
async def login(request: LoginRequest):
    supabase = get_supabase()
    
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    # Get user
    result = supabase.table('users').select('*').eq('email', request.email).execute()
    
    if not result.data:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = result.data[0]
    
    # Truncate password to 72 bytes for bcrypt verification
    password_bytes = request.password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # Verify password
    if not pwd_context.verify(password_bytes.decode('utf-8'), user['password_hash']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user['id'], "email": user['email']})
    
    return {
        "success": True,
        "token": token,
        "user": {
            "id": user['id'],
            "name": user['name'],
            "email": user['email'],
            "trust_score": user['trust_score'],
            "total_exchanges": user['total_exchanges']
        }
    }
