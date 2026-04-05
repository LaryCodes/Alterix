from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.core.config import settings
from app.core.database import get_supabase
import uuid
import logging

router = APIRouter()
logger = logging.getLogger(__name__)
ph = PasswordHasher()


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
    logger.info(f"📝 Registration attempt for: {request.email}")
    
    supabase = get_supabase()
    
    if not supabase:
        logger.error("❌ Database not configured")
        raise HTTPException(status_code=500, detail="Database not configured")
    
    # Validate password length
    if len(request.password) < 8:
        logger.warning(f"⚠️ Password too short for: {request.email}")
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    
    try:
        # Check if user exists
        existing = supabase.table('users').select('*').eq('email', request.email).execute()
        if existing.data:
            logger.warning(f"⚠️ Email already registered: {request.email}")
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash password with argon2
        password_hash = ph.hash(request.password)
        
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
            logger.error(f"❌ Failed to create user: {request.email}")
            raise HTTPException(status_code=500, detail="Failed to create user")
        
        user = result.data[0]
        token = create_access_token({"sub": user['id'], "email": user['email']})
        
        logger.info(f"✅ User registered successfully: {request.email}")
        
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
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.post("/login")
async def login(request: LoginRequest):
    logger.info(f"🔐 Login attempt for: {request.email}")
    
    supabase = get_supabase()
    
    if not supabase:
        logger.error("❌ Database not configured")
        raise HTTPException(status_code=500, detail="Database not configured")
    
    try:
        # Get user
        result = supabase.table('users').select('*').eq('email', request.email).execute()
        
        if not result.data:
            logger.warning(f"⚠️ User not found: {request.email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        user = result.data[0]
        
        # Verify password with argon2
        try:
            ph.verify(user['password_hash'], request.password)
        except VerifyMismatchError:
            logger.warning(f"⚠️ Invalid password for: {request.email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        token = create_access_token({"sub": user['id'], "email": user['email']})
        
        logger.info(f"✅ Login successful: {request.email}")
        
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
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Login error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")
