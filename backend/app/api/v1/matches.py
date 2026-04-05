from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.agents.mediator import AgentMediator
from app.core.auth import get_current_user
from app.core.database import get_supabase
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Global mediator instance - will be set by main.py
_mediator: Optional[AgentMediator] = None

def set_mediator(mediator: AgentMediator):
    global _mediator
    _mediator = mediator

def get_mediator() -> AgentMediator:
    if _mediator is None:
        raise HTTPException(status_code=500, detail="Mediator not initialized")
    return _mediator


class SkillModel(BaseModel):
    name: str
    category: str
    level: str
    estimated_hours: int = 1


class MatchRequest(BaseModel):
    user_id: str
    requested_skill: SkillModel
    offered_skill: Optional[SkillModel] = None
    requester_skills: List[SkillModel] = []
    max_distance: int = 50
    min_trust_score: float = 30.0


def _fetch_candidates(supabase, user_id: str, requested_skill_name: str) -> List[Dict]:
    """Fetch real candidates from Supabase who offer the requested skill"""
    try:
        # Find skill IDs matching the requested skill name
        skill_result = supabase.table('skills').select('id, name, category, level').ilike('name', f'%{requested_skill_name}%').execute()
        
        if not skill_result.data:
            logger.info(f"No skills found matching: {requested_skill_name}")
            return []
        
        skill_ids = [s['id'] for s in skill_result.data]
        
        # Find users offering those skills (excluding the requester)
        offered_result = supabase.table('user_offered_skills')\
            .select('user_id, skill_id, proficiency_level, skills(id, name, category, level)')\
            .in_('skill_id', skill_ids)\
            .neq('user_id', user_id)\
            .execute()
        
        if not offered_result.data:
            logger.info("No users found offering the requested skill")
            return []
        
        # Build candidate profiles
        candidate_ids = list(set(item['user_id'] for item in offered_result.data))
        
        # Fetch user details
        users_result = supabase.table('users')\
            .select('id, name, email, trust_score, total_exchanges, is_active')\
            .in_('id', candidate_ids)\
            .eq('is_active', True)\
            .execute()
        
        user_map = {u['id']: u for u in users_result.data}
        
        # Fetch requested skills for candidates (for reciprocal matching)
        requested_result = supabase.table('user_requested_skills')\
            .select('user_id, skill_id, desired_level, skills(id, name, category, level)')\
            .in_('user_id', candidate_ids)\
            .execute()
        
        # Build full candidate objects
        candidates = []
        for uid in candidate_ids:
            user_data = user_map.get(uid)
            if not user_data:
                continue
            
            offered_skills = [
                {
                    "name": item['skills']['name'],
                    "category": item['skills']['category'],
                    "level": item['proficiency_level'],
                    "skill_id": item['skill_id']
                }
                for item in offered_result.data
                if item['user_id'] == uid and item.get('skills')
            ]
            
            requested_skills = [
                {
                    "name": item['skills']['name'],
                    "category": item['skills']['category'],
                    "level": item['desired_level'],
                    "skill_id": item['skill_id']
                }
                for item in requested_result.data
                if item['user_id'] == uid and item.get('skills')
            ]
            
            candidates.append({
                "id": uid,
                "name": user_data['name'],
                "email": user_data['email'],
                "trust_score": float(user_data.get('trust_score', 50)),
                "total_exchanges": user_data.get('total_exchanges', 0),
                "offered_skills": offered_skills,
                "requested_skills": requested_skills
            })
        
        logger.info(f"Found {len(candidates)} candidates for skill: {requested_skill_name}")
        return candidates
        
    except Exception as e:
        logger.error(f"Error fetching candidates: {e}")
        return []


def _fetch_all_users(supabase, user_id: str) -> List[Dict]:
    """Fetch all active users with their skills for multi-hop pathfinding"""
    try:
        users_result = supabase.table('users')\
            .select('id, name, email, trust_score, total_exchanges')\
            .eq('is_active', True)\
            .limit(100)\
            .execute()
        
        if not users_result.data:
            return []
        
        user_ids = [u['id'] for u in users_result.data]
        
        # Batch fetch all offered skills
        offered_result = supabase.table('user_offered_skills')\
            .select('user_id, skill_id, proficiency_level, skills(id, name, category, level)')\
            .in_('user_id', user_ids)\
            .execute()
        
        # Batch fetch all requested skills
        requested_result = supabase.table('user_requested_skills')\
            .select('user_id, skill_id, desired_level, skills(id, name, category, level)')\
            .in_('user_id', user_ids)\
            .execute()
        
        all_users = []
        for user in users_result.data:
            uid = user['id']
            
            offered_skills = [
                {
                    "name": item['skills']['name'],
                    "category": item['skills']['category'],
                    "level": item['proficiency_level']
                }
                for item in offered_result.data
                if item['user_id'] == uid and item.get('skills')
            ]
            
            requested_skills = [
                {
                    "name": item['skills']['name'],
                    "category": item['skills']['category'],
                    "level": item['desired_level']
                }
                for item in requested_result.data
                if item['user_id'] == uid and item.get('skills')
            ]
            
            all_users.append({
                "id": uid,
                "name": user['name'],
                "trust_score": float(user.get('trust_score', 50)),
                "offered_skills": offered_skills,
                "requested_skills": requested_skills
            })
        
        return all_users
        
    except Exception as e:
        logger.error(f"Error fetching all users: {e}")
        return []


@router.post("/matches/find")
async def find_matches(
    request: MatchRequest,
    current_user: dict = Depends(get_current_user),
    mediator: AgentMediator = Depends(get_mediator)
):
    """
    Find optimal matches for a user
    Uses AI agents with REAL data from database
    """
    if current_user['id'] != request.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    try:
        # Fetch REAL candidates from database
        candidates = _fetch_candidates(supabase, request.user_id, request.requested_skill.name)
        
        # Fetch all users for multi-hop pathfinding
        all_users = _fetch_all_users(supabase, request.user_id)
        
        # Also fetch requester's offered skills for reciprocal matching
        requester_offered = supabase.table('user_offered_skills')\
            .select('*, skills(*)')\
            .eq('user_id', request.user_id)\
            .execute()
        
        requester_skills = [
            {
                "name": item['skills']['name'],
                "category": item['skills']['category'],
                "level": item['proficiency_level']
            }
            for item in requester_offered.data
            if item.get('skills')
        ]
        
        # Prepare context with REAL data
        context = {
            "user_id": request.user_id,
            "requested_skill": request.requested_skill.dict(),
            "offered_skill": request.offered_skill.dict() if request.offered_skill else {},
            "requester_skills": requester_skills,
            "candidates": candidates,
            "all_users": all_users
        }
        
        logger.info(f"Match context: {len(candidates)} candidates, {len(all_users)} total users, {len(requester_skills)} requester skills")
        
        # Use mediator to coordinate agents
        result = await mediator.find_optimal_match(context)
        
        return {
            "success": True,
            "data": result
        }
    
    except Exception as e:
        logger.error(f"Match finding error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/matches/recommendations/{user_id}")
async def get_recommendations(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    mediator: AgentMediator = Depends(get_mediator)
):
    """Get personalized recommendations with REAL data"""
    if current_user['id'] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    try:
        # Fetch user's requested skills
        requested_result = supabase.table('user_requested_skills')\
            .select('*, skills(*)')\
            .eq('user_id', user_id)\
            .execute()
        
        requested_skill = {}
        if requested_result.data and requested_result.data[0].get('skills'):
            first_skill = requested_result.data[0]['skills']
            requested_skill = {
                "name": first_skill['name'],
                "category": first_skill['category'],
                "level": requested_result.data[0]['desired_level']
            }
        
        # Fetch real data
        candidates = _fetch_candidates(supabase, user_id, requested_skill.get('name', '')) if requested_skill else []
        all_users = _fetch_all_users(supabase, user_id)
        
        context = {
            "user_id": user_id,
            "requested_skill": requested_skill,
            "candidates": candidates,
            "all_users": all_users
        }
        
        result = await mediator.get_recommendations(context)
        
        return {
            "success": True,
            "data": result
        }
    
    except Exception as e:
        logger.error(f"Recommendations error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/matches/stats")
async def get_matching_stats(
    current_user: dict = Depends(get_current_user),
    mediator: AgentMediator = Depends(get_mediator)
):
    """Get matching system statistics"""
    return {
        "success": True,
        "stats": mediator.get_agent_stats()
    }
