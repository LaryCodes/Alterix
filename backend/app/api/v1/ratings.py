from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.auth import get_current_user
from app.core.database import get_supabase
from app.agents.mediator import AgentMediator
from typing import Optional
import uuid
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

_mediator: Optional[AgentMediator] = None

def set_mediator(mediator: AgentMediator):
    global _mediator
    _mediator = mediator

def get_mediator() -> AgentMediator:
    if _mediator is None:
        raise HTTPException(status_code=500, detail="Mediator not initialized")
    return _mediator


class RatingCreateRequest(BaseModel):
    exchange_id: str
    rated_id: str
    rating: int
    feedback: str = ""

@router.post("/ratings")
async def create_rating(
    request: RatingCreateRequest,
    current_user: dict = Depends(get_current_user),
    mediator: AgentMediator = Depends(get_mediator)
):
    """Rate a completed exchange"""
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    if request.rating < 1 or request.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    try:
        # Verify exchange is completed
        exchange = supabase.table('exchanges').select('status').eq('id', request.exchange_id).execute()
        if not exchange.data:
            raise HTTPException(status_code=404, detail="Exchange not found")
        if exchange.data[0]['status'] != 'COMPLETED':
            raise HTTPException(status_code=400, detail="Can only rate completed exchanges")
        
        # Verify user is participant
        participant = supabase.table('exchange_participants')\
            .select('id')\
            .eq('exchange_id', request.exchange_id)\
            .eq('user_id', current_user['id'])\
            .execute()
        
        if not participant.data:
            raise HTTPException(status_code=403, detail="Not a participant in this exchange")
        
        # Check for existing rating
        existing = supabase.table('ratings')\
            .select('id')\
            .eq('exchange_id', request.exchange_id)\
            .eq('rater_id', current_user['id'])\
            .eq('rated_id', request.rated_id)\
            .execute()
        
        if existing.data:
            raise HTTPException(status_code=400, detail="You have already rated this exchange")
        
        rating_data = {
            'id': str(uuid.uuid4()),
            'exchange_id': request.exchange_id,
            'rater_id': current_user['id'],
            'rated_id': request.rated_id,
            'rating': request.rating,
            'feedback': request.feedback
        }
        
        result = supabase.table('ratings').insert(rating_data).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to save rating")
        
        # Call ReputationAgent via Mediator
        all_ratings = supabase.table('ratings').select('rating').eq('rated_id', request.rated_id).execute()
        avg = 3.0
        if all_ratings.data:
            avg = sum(r['rating'] for r in all_ratings.data) / len(all_ratings.data)
            
        # Get fairness score for this exchange
        exchange_meta = supabase.table('exchanges').select('fairness_score').eq('id', request.exchange_id).execute()
        fairness_score = exchange_meta.data[0]['fairness_score'] if exchange_meta.data else 0.5
        
        user = supabase.table('users').select('trust_score').eq('id', request.rated_id).execute()
        if user.data:
            prev_trust = float(user.data[0]['trust_score'])
            
            # Delegate to ReputationAgent
            reputation_result = await mediator.evaluate_exchange_completion(
                exchange_id=request.exchange_id,
                user_id=request.rated_id,
                prev_trust=prev_trust,
                rating=float(request.rating),
                fairness_score=float(fairness_score)
            )
            
            new_trust = reputation_result.get("metrics", {}).get("new_trust_score", prev_trust)
            
            supabase.table('users').update({
                'average_rating': round(avg, 2),
                'trust_score': new_trust
            }).eq('id', request.rated_id).execute()
        
        logger.info(f"Rating created: {current_user['id']} rated {request.rated_id} with {request.rating}")
        
        return {
            "success": True,
            "rating": result.data[0]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create rating error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ratings/exchange/{exchange_id}")
async def get_exchange_ratings(
    exchange_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get ratings for an exchange"""
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    try:
        result = supabase.table('ratings')\
            .select('*, rater:rater_id(id, name), rated:rated_id(id, name)')\
            .eq('exchange_id', exchange_id)\
            .execute()
        
        return {
            "success": True,
            "ratings": result.data
        }
    
    except Exception as e:
        logger.error(f"Get ratings error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
