from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None


class User(UserBase):
    id: UUID
    is_active: bool = True
    is_verified: bool = False
    trust_score: float = 50.0
    total_exchanges: int = 0
    successful_exchanges: int = 0
    average_rating: float = 0.0
    report_count: int = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserInDB(User):
    password_hash: str
