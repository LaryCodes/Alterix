from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
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


class ExchangeValidationRequest(BaseModel):
    exchange_type: str  # DIRECT_SWAP, PAID_LEARNING, MULTI_PARTY_CHAIN
    participants: List[Dict[str, Any]]
    offerings: Dict[str, Any]


@router.post("/exchanges/validate")
async def validate_exchange(
    request: ExchangeValidationRequest,
    current_user: dict = Depends(get_current_user),
    mediator: AgentMediator = Depends(get_mediator)
):
    """
    Validate an exchange for fairness
    Uses Fairness Agent to ensure balanced value
    """
    try:
        context = {
            "exchange_type": request.exchange_type,
            "participants": request.participants,
            "offerings": request.offerings
        }
        
        result = await mediator.validate_exchange(context)
        
        return {
            "success": True,
            "data": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/exchanges/create")
async def create_exchange(
    exchange_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new exchange
    In production, this would integrate with Java core engine via gRPC
    """
    # This would call Java ExchangeService via gRPC
    return {
        "success": True,
        "exchange_id": "exc_" + exchange_data.get("id", "unknown"),
        "status": "PENDING",
        "message": "Exchange created successfully"
    }


@router.get("/exchanges/{exchange_id}")
async def get_exchange(
    exchange_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get exchange details"""
    # Would fetch from database
    return {
        "success": True,
        "exchange": {
            "id": exchange_id,
            "status": "PENDING",
            "type": "DIRECT_SWAP"
        }
    }


@router.get("/exchanges/user/{user_id}")
async def get_user_exchanges(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get all exchanges for a user"""
    from app.core.database import get_supabase
    
    # Verify user can only access their own exchanges
    if current_user['id'] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    # Get exchange participants for this user
    result = supabase.table('exchange_participants')\
        .select('*, exchanges(*)')\
        .eq('user_id', user_id)\
        .execute()
    
    exchanges = []
    for item in result.data:
        if item.get('exchanges'):
            exchange = item['exchanges']
            # Get other participants
            participants = supabase.table('exchange_participants')\
                .select('*, users(id, name, email)')\
                .eq('exchange_id', exchange['id'])\
                .neq('user_id', user_id)\
                .execute()
            
            exchange['participants'] = [p['users'] for p in participants.data if p.get('users')]
            exchanges.append(exchange)
    
    return {
        "success": True,
        "exchanges": exchanges
    }
