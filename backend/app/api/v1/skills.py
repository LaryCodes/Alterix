from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from app.core.database import get_supabase
from app.core.auth import get_current_user
import uuid
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Seed data for skills catalog
SEED_SKILLS = [
    # Technology
    {"name": "Python", "category": "Technology", "level": "BEGINNER", "description": "Python programming fundamentals", "estimated_hours": 20},
    {"name": "Python", "category": "Technology", "level": "INTERMEDIATE", "description": "Python web frameworks, data science basics", "estimated_hours": 40},
    {"name": "Python", "category": "Technology", "level": "ADVANCED", "description": "Advanced Python, async programming, ML", "estimated_hours": 80},
    {"name": "JavaScript", "category": "Technology", "level": "BEGINNER", "description": "JavaScript basics and DOM manipulation", "estimated_hours": 20},
    {"name": "JavaScript", "category": "Technology", "level": "INTERMEDIATE", "description": "React, Node.js, modern JS", "estimated_hours": 40},
    {"name": "JavaScript", "category": "Technology", "level": "ADVANCED", "description": "Full-stack JS, TypeScript, architecture", "estimated_hours": 80},
    {"name": "Java", "category": "Technology", "level": "BEGINNER", "description": "Java programming fundamentals", "estimated_hours": 25},
    {"name": "Java", "category": "Technology", "level": "INTERMEDIATE", "description": "OOP, Spring Boot basics", "estimated_hours": 50},
    {"name": "Java", "category": "Technology", "level": "ADVANCED", "description": "Design patterns, microservices, JVM tuning", "estimated_hours": 100},
    {"name": "React", "category": "Technology", "level": "INTERMEDIATE", "description": "React components, hooks, state management", "estimated_hours": 30},
    {"name": "Machine Learning", "category": "Technology", "level": "INTERMEDIATE", "description": "ML fundamentals, scikit-learn, neural networks", "estimated_hours": 60},
    {"name": "Data Science", "category": "Technology", "level": "INTERMEDIATE", "description": "Data analysis, visualization, pandas", "estimated_hours": 40},
    {"name": "DevOps", "category": "Technology", "level": "INTERMEDIATE", "description": "Docker, CI/CD, cloud deployment", "estimated_hours": 40},
    {"name": "Mobile Development", "category": "Technology", "level": "INTERMEDIATE", "description": "React Native or Flutter development", "estimated_hours": 50},
    {"name": "Cybersecurity", "category": "Technology", "level": "INTERMEDIATE", "description": "Security fundamentals, ethical hacking", "estimated_hours": 45},
    # Business
    {"name": "Digital Marketing", "category": "Business", "level": "BEGINNER", "description": "Social media, SEO basics", "estimated_hours": 15},
    {"name": "Digital Marketing", "category": "Business", "level": "INTERMEDIATE", "description": "PPC, analytics, content strategy", "estimated_hours": 30},
    {"name": "Project Management", "category": "Business", "level": "INTERMEDIATE", "description": "Agile, Scrum, project planning", "estimated_hours": 25},
    {"name": "Financial Analysis", "category": "Business", "level": "INTERMEDIATE", "description": "Financial modeling, valuation", "estimated_hours": 35},
    {"name": "Public Speaking", "category": "Business", "level": "BEGINNER", "description": "Presentation skills, confidence building", "estimated_hours": 10},
    {"name": "Entrepreneurship", "category": "Business", "level": "INTERMEDIATE", "description": "Business planning, startup fundamentals", "estimated_hours": 30},
    # Creative
    {"name": "UI/UX Design", "category": "Creative", "level": "BEGINNER", "description": "Design principles, Figma basics", "estimated_hours": 20},
    {"name": "UI/UX Design", "category": "Creative", "level": "INTERMEDIATE", "description": "User research, prototyping, design systems", "estimated_hours": 40},
    {"name": "UI/UX Design", "category": "Creative", "level": "ADVANCED", "description": "Advanced interaction design, accessibility", "estimated_hours": 60},
    {"name": "Graphic Design", "category": "Creative", "level": "INTERMEDIATE", "description": "Adobe suite, branding, visual design", "estimated_hours": 35},
    {"name": "Photography", "category": "Creative", "level": "BEGINNER", "description": "Camera basics, composition, lighting", "estimated_hours": 15},
    {"name": "Video Editing", "category": "Creative", "level": "INTERMEDIATE", "description": "Premiere Pro, After Effects, storytelling", "estimated_hours": 30},
    {"name": "Music Production", "category": "Creative", "level": "BEGINNER", "description": "DAW basics, beat making, mixing", "estimated_hours": 20},
    {"name": "Creative Writing", "category": "Creative", "level": "INTERMEDIATE", "description": "Fiction, non-fiction, storytelling techniques", "estimated_hours": 25},
    # Language
    {"name": "English", "category": "Language", "level": "INTERMEDIATE", "description": "Conversational English, grammar", "estimated_hours": 30},
    {"name": "Spanish", "category": "Language", "level": "BEGINNER", "description": "Basic Spanish conversation", "estimated_hours": 25},
    {"name": "French", "category": "Language", "level": "BEGINNER", "description": "Basic French conversation", "estimated_hours": 25},
    {"name": "Mandarin", "category": "Language", "level": "BEGINNER", "description": "Basic Mandarin, characters, tones", "estimated_hours": 40},
    {"name": "Japanese", "category": "Language", "level": "BEGINNER", "description": "Hiragana, Katakana, basic conversation", "estimated_hours": 35},
    {"name": "Arabic", "category": "Language", "level": "BEGINNER", "description": "Basic Arabic script and conversation", "estimated_hours": 35},
]


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
async def get_all_skills():
    """Get all available skills (public catalog — no auth required)"""
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    result = supabase.table('skills').select('*').order('category').order('name').execute()
    return {"success": True, "skills": result.data}


@router.post("/skills/seed")
async def seed_skills():
    """Seed the skills catalog with default skills. Only inserts if catalog is empty."""
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    try:
        existing = supabase.table('skills').select('id').limit(1).execute()
        if existing.data:
            return {"success": True, "message": "Skills already seeded", "count": 0}
        
        skills_to_insert = []
        for skill in SEED_SKILLS:
            skills_to_insert.append({
                'id': str(uuid.uuid4()),
                **skill,
                'valuation_score': 0.0
            })
        
        # Insert in batches
        batch_size = 10
        for i in range(0, len(skills_to_insert), batch_size):
            batch = skills_to_insert[i:i + batch_size]
            supabase.table('skills').insert(batch).execute()
        
        logger.info(f"Seeded {len(skills_to_insert)} skills")
        return {"success": True, "message": f"Seeded {len(skills_to_insert)} skills", "count": len(skills_to_insert)}
    
    except Exception as e:
        logger.error(f"Seed skills error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


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
    
    try:
        # Check for duplicate
        existing = supabase.table('user_offered_skills')\
            .select('id')\
            .eq('user_id', user_id)\
            .eq('skill_id', skill.skill_id)\
            .execute()
        
        if existing.data:
            raise HTTPException(status_code=400, detail="You already offer this skill")
        
        data = {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'skill_id': skill.skill_id,
            'proficiency_level': skill.proficiency_level
        }
        
        result = supabase.table('user_offered_skills').insert(data).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to add skill")
        
        return {"success": True, "data": result.data[0]}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Add offered skill error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/skills/user/{user_id}/request")
async def add_requested_skill(user_id: str, skill: UserSkillRequest, current_user: dict = Depends(get_current_user)):
    """Add a skill that user wants to learn"""
    if current_user['id'] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    try:
        # Check for duplicate
        existing = supabase.table('user_requested_skills')\
            .select('id')\
            .eq('user_id', user_id)\
            .eq('skill_id', skill.skill_id)\
            .execute()
        
        if existing.data:
            raise HTTPException(status_code=400, detail="You already requested this skill")
        
        data = {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'skill_id': skill.skill_id,
            'desired_level': skill.desired_level
        }
        
        result = supabase.table('user_requested_skills').insert(data).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to add skill")
        
        return {"success": True, "data": result.data[0]}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Add requested skill error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/skills/user/offered/{skill_id}")
async def remove_offered_skill(skill_id: str, current_user: dict = Depends(get_current_user)):
    """Remove an offered skill"""
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    check = supabase.table('user_offered_skills').select('user_id').eq('id', skill_id).execute()
    if not check.data or check.data[0]['user_id'] != current_user['id']:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    supabase.table('user_offered_skills').delete().eq('id', skill_id).execute()
    return {"success": True}


@router.delete("/skills/user/requested/{skill_id}")
async def remove_requested_skill(skill_id: str, current_user: dict = Depends(get_current_user)):
    """Remove a requested skill"""
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    check = supabase.table('user_requested_skills').select('user_id').eq('id', skill_id).execute()
    if not check.data or check.data[0]['user_id'] != current_user['id']:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    supabase.table('user_requested_skills').delete().eq('id', skill_id).execute()
    return {"success": True}
