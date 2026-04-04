from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from app.core.database import get_supabase
from app.core.auth import get_current_user
import uuid

router = APIRouter()


class SkillCreate(BaseModel):
    name: str
    category: str
    level: str


class UserSkillCreate(BaseModel):
    skill_id: str
    proficiency_level: str


class UserSkillRequest(BaseModel):
    skill_id: str
    desired_level: str


@router.get("/skills")
async def get_all_skills(current_user: dict = Depends(get_current_user)):
    """Get all available skills"""
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    result = supabase.table('skills').select('*').execute()
    return {"success": True, "skills": result.data}


@router.get("/skills/user/{user_id}/offered")
async def get_user_offered_skills(user_id: str, current_user: dict = Depends(get_current_user)):
    """Get skills offered by a user"""
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    result = supabase.table('user_offered_skills')\
        .select('*, skills(*)')\
        .eq('user_id', user_id)\
        .execute()
    
    return {"success": True, "skills": result.data}


@router.get("/skills/user/{user_id}/requested")
async def get_user_requested_skills(user_id: str, current_user: dict = Depends(get_current_user)):
    """Get skills requested by a user"""
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    result = supabase.table('user_requested_skills')\
        .select('*, skills(*)')\
        .eq('user_id', user_id)\
        .execute()
    
    return {"success": True, "skills": result.data}


@router.post("/skills/user/{user_id}/offer")
async def add_offered_skill(user_id: str, skill: UserSkillCreate, current_user: dict = Depends(get_current_user)):
    """Add a skill that user offers"""
    if current_user['id'] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    data = {
        'id': str(uuid.uuid4()),
        'user_id': user_id,
        'skill_id': skill.skill_id,
        'proficiency_level': skill.proficiency_level
    }
    
    result = supabase.table('user_offered_skills').insert(data).execute()
    return {"success": True, "data": result.data[0]}


@router.post("/skills/user/{user_id}/request")
async def add_requested_skill(user_id: str, skill: UserSkillRequest, current_user: dict = Depends(get_current_user)):
    """Add a skill that user wants to learn"""
    if current_user['id'] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    data = {
        'id': str(uuid.uuid4()),
        'user_id': user_id,
        'skill_id': skill.skill_id,
        'desired_level': skill.desired_level
    }
    
    result = supabase.table('user_requested_skills').insert(data).execute()
    return {"success": True, "data": result.data[0]}


@router.delete("/skills/user/offered/{skill_id}")
async def remove_offered_skill(skill_id: str, current_user: dict = Depends(get_current_user)):
    """Remove an offered skill"""
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    # Verify ownership
    check = supabase.table('user_offered_skills').select('user_id').eq('id', skill_id).execute()
    if not check.data or check.data[0]['user_id'] != current_user['id']:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    result = supabase.table('user_offered_skills').delete().eq('id', skill_id).execute()
    return {"success": True}


@router.delete("/skills/user/requested/{skill_id}")
async def remove_requested_skill(skill_id: str, current_user: dict = Depends(get_current_user)):
    """Remove a requested skill"""
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    # Verify ownership
    check = supabase.table('user_requested_skills').select('user_id').eq('id', skill_id).execute()
    if not check.data or check.data[0]['user_id'] != current_user['id']:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    result = supabase.table('user_requested_skills').delete().eq('id', skill_id).execute()
    return {"success": True}
