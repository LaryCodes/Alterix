from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.core.config import settings
from app.core.database import get_supabase
from typing import Optional

security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify JWT token and return current user
    """
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        
        # Get user from database
        supabase = get_supabase()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database not configured")
        
        result = supabase.table('users').select('id, name, email, trust_score, total_exchanges').eq('id', user_id).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        return result.data[0]
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )


async def get_current_user_optional(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    """
    Optional authentication - returns None if no token provided
    """
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None
