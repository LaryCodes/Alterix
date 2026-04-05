from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.agents.mediator import AgentMediator
from app.core.auth import get_current_user
from app.core.database import get_supabase
import uuid
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


class ExchangeValidationRequest(BaseModel):
    exchange_type: str
    participants: List[Dict[str, Any]]
    offerings: Dict[str, Any]


class ExchangeCreateRequest(BaseModel):
    type: str = "DIRECT_SWAP"
    partner_id: str
    offered_skill_id: str
    requested_skill_id: str


class ExchangeStatusUpdate(BaseModel):
    status: str


@router.post("/exchanges/validate")
async def validate_exchange(
    request: ExchangeValidationRequest,
    current_user: dict = Depends(get_current_user),
    mediator: AgentMediator = Depends(get_mediator)
):
    """Validate an exchange for fairness using AI agents"""
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
        logger.error(f"Exchange validation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/exchanges/create")
async def create_exchange(
    request: ExchangeCreateRequest,
    current_user: dict = Depends(get_current_user)
):
    """Create a new exchange — writes to real database"""
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    try:
        user_id = current_user['id']
        exchange_id = str(uuid.uuid4())
        
        # Verify partner exists
        partner_result = supabase.table('users').select('id, name').eq('id', request.partner_id).execute()
        if not partner_result.data:
            raise HTTPException(status_code=404, detail="Partner user not found")
        
        # Create the exchange
        exchange_data = {
            'id': exchange_id,
            'type': request.type,
            'status': 'PENDING',
            'fairness_score': 0.0
        }
        
        exchange_result = supabase.table('exchanges').insert(exchange_data).execute()
        if not exchange_result.data:
            raise HTTPException(status_code=500, detail="Failed to create exchange")
        
        # Add participants
        participants = [
            {
                'id': str(uuid.uuid4()),
                'exchange_id': exchange_id,
                'user_id': user_id,
                'role': 'initiator'
            },
            {
                'id': str(uuid.uuid4()),
                'exchange_id': exchange_id,
                'user_id': request.partner_id,
                'role': 'responder'
            }
        ]
        
        supabase.table('exchange_participants').insert(participants).execute()
        
        # Add offerings
        offerings = [
            {
                'id': str(uuid.uuid4()),
                'exchange_id': exchange_id,
                'user_id': user_id,
                'skill_id': request.offered_skill_id,
                'hours_committed': 0,
                'payment_amount': 0.0
            },
            {
                'id': str(uuid.uuid4()),
                'exchange_id': exchange_id,
                'user_id': request.partner_id,
                'skill_id': request.requested_skill_id,
                'hours_committed': 0,
                'payment_amount': 0.0
            }
        ]
        
        supabase.table('exchange_offerings').insert(offerings).execute()
        
        # Create notifications for both parties
        notifications = [
            {
                'id': str(uuid.uuid4()),
                'user_id': user_id,
                'type': 'exchange_created',
                'title': 'Exchange Created',
                'message': f'You initiated a skill exchange with {partner_result.data[0]["name"]}',
                'related_exchange_id': exchange_id,
                'is_read': False
            },
            {
                'id': str(uuid.uuid4()),
                'user_id': request.partner_id,
                'type': 'exchange_request',
                'title': 'New Exchange Request',
                'message': f'{current_user.get("name", "Someone")} wants to exchange skills with you!',
                'related_exchange_id': exchange_id,
                'is_read': False
            }
        ]
        
        supabase.table('notifications').insert(notifications).execute()
        
        logger.info(f"Exchange created: {exchange_id} between {user_id} and {request.partner_id}")
        
        return {
            "success": True,
            "exchange_id": exchange_id,
            "status": "PENDING",
            "message": "Exchange created successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Exchange creation error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create exchange: {str(e)}")


@router.get("/exchanges/{exchange_id}")
async def get_exchange(
    exchange_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get exchange details from database"""
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    try:
        # Get exchange
        exchange_result = supabase.table('exchanges').select('*').eq('id', exchange_id).execute()
        if not exchange_result.data:
            raise HTTPException(status_code=404, detail="Exchange not found")
        
        exchange = exchange_result.data[0]
        
        # Get participants
        participants_result = supabase.table('exchange_participants')\
            .select('*, users(id, name, email, trust_score)')\
            .eq('exchange_id', exchange_id)\
            .execute()
        
        exchange['participants'] = [
            {**p['users'], 'role': p['role']}
            for p in participants_result.data
            if p.get('users')
        ]
        
        # Get offerings
        offerings_result = supabase.table('exchange_offerings')\
            .select('*, skills(id, name, category, level), users(id, name)')\
            .eq('exchange_id', exchange_id)\
            .execute()
        
        exchange['offerings'] = offerings_result.data
        
        # Verify user is participant
        participant_ids = [p['users']['id'] for p in participants_result.data if p.get('users')]
        if current_user['id'] not in participant_ids:
            raise HTTPException(status_code=403, detail="Not authorized to view this exchange")
        
        return {
            "success": True,
            "exchange": exchange
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get exchange error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/exchanges/{exchange_id}/status")
async def update_exchange_status(
    exchange_id: str,
    update: ExchangeStatusUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update exchange status"""
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    valid_statuses = ['PENDING', 'NEGOTIATING', 'SCHEDULED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED']
    if update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
    
    try:
        # Verify user is participant
        participant_check = supabase.table('exchange_participants')\
            .select('id')\
            .eq('exchange_id', exchange_id)\
            .eq('user_id', current_user['id'])\
            .execute()
        
        if not participant_check.data:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        # Update status
        update_data = {'status': update.status}
        if update.status == 'COMPLETED':
            from datetime import datetime
            update_data['completed_at'] = datetime.utcnow().isoformat()
        
        result = supabase.table('exchanges').update(update_data).eq('id', exchange_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Exchange not found")
        
        # Update user stats if completed
        if update.status == 'COMPLETED':
            participants = supabase.table('exchange_participants')\
                .select('user_id')\
                .eq('exchange_id', exchange_id)\
                .execute()
            
            for p in participants.data:
                user = supabase.table('users').select('total_exchanges, trust_score').eq('id', p['user_id']).execute()
                if user.data:
                    current = user.data[0]
                    supabase.table('users').update({
                        'total_exchanges': current['total_exchanges'] + 1,
                        'trust_score': min(100, float(current['trust_score']) + 2.0)
                    }).eq('id', p['user_id']).execute()
        
        logger.info(f"Exchange {exchange_id} status updated to {update.status}")
        
        return {
            "success": True,
            "exchange_id": exchange_id,
            "status": update.status
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Status update error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/exchanges/user/{user_id}")
async def get_user_exchanges(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get all exchanges for a user"""
    if current_user['id'] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    try:
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
                    .select('*, users(id, name, email, trust_score)')\
                    .eq('exchange_id', exchange['id'])\
                    .neq('user_id', user_id)\
                    .execute()
                
                exchange['participants'] = [p['users'] for p in participants.data if p.get('users')]
                exchanges.append(exchange)
        
        return {
            "success": True,
            "exchanges": exchanges
        }
    
    except Exception as e:
        logger.error(f"Get user exchanges error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
