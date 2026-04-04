from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.agents.mediator import AgentMediator
from app.core.auth import get_current_user

router = APIRouter()

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
    min_trust_score: float = 50.0


@router.post("/matches/find")
async def find_matches(
    request: MatchRequest,
    current_user: dict = Depends(get_current_user),
    mediator: AgentMediator = Depends(get_mediator)
):
    """
    Find optimal matches for a user
    Uses AI agents to find direct and multi-hop matches
    """
    # Verify user can only search for themselves
    if current_user['id'] != request.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    try:
        # Prepare context for agents
        context = {
            "user_id": request.user_id,
            "requested_skill": request.requested_skill.dict(),
            "offered_skill": request.offered_skill.dict() if request.offered_skill else {},
            "requester_skills": [s.dict() for s in request.requester_skills],
            "candidates": [],  # Would be fetched from database
            "all_users": []  # Would be fetched from database
        }
        
        # Use mediator to coordinate agents
        result = await mediator.find_optimal_match(context)
        
        return {
            "success": True,
            "data": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/matches/recommendations/{user_id}")
async def get_recommendations(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    mediator: AgentMediator = Depends(get_mediator)
):
    """
    Get personalized recommendations for a user
    """
    # Verify user can only get their own recommendations
    if current_user['id'] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    try:
        context = {
            "user_id": user_id,
            "requested_skill": {},
            "candidates": [],
            "all_users": []
        }
        
        result = await mediator.get_recommendations(context)
        
        return {
            "success": True,
            "data": result
        }
    
    except Exception as e:
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
