from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from enum import Enum


class SkillLevel(str, Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    EXPERT = "EXPERT"


class SkillCategory(str, Enum):
    TECHNOLOGY = "Technology"
    BUSINESS = "Business"
    CREATIVE = "Creative"
    LANGUAGE = "Language"
    OTHER = "Other"


class SkillBase(BaseModel):
    name: str
    category: SkillCategory
    level: SkillLevel
    description: Optional[str] = None
    estimated_hours: int = 1


class SkillCreate(SkillBase):
    pass


class Skill(SkillBase):
    id: UUID
    valuation_score: float = 0.0
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserSkillOffered(BaseModel):
    id: UUID
    user_id: UUID
    skill_id: UUID
    proficiency_level: SkillLevel
    years_experience: int = 0
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserSkillRequested(BaseModel):
    id: UUID
    user_id: UUID
    skill_id: UUID
    desired_level: SkillLevel
    priority: int = 1
    created_at: datetime
    
    class Config:
        from_attributes = True
