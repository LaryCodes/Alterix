from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.auth import get_current_user
from app.core.database import get_supabase
import uuid
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


class SendMessageRequest(BaseModel):
    exchange_id: str
    content: str


@router.post("/messages/send")
async def send_message(
    request: SendMessageRequest,
    current_user: dict = Depends(get_current_user)
):
    """Send a message in an exchange context"""
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    try:
        # Verify user is participant in this exchange
        participant = supabase.table('exchange_participants')\
            .select('id')\
            .eq('exchange_id', request.exchange_id)\
            .eq('user_id', current_user['id'])\
            .execute()
        
        if not participant.data:
            raise HTTPException(status_code=403, detail="Not a participant in this exchange")
        
        message_data = {
            'id': str(uuid.uuid4()),
            'exchange_id': request.exchange_id,
            'sender_id': current_user['id'],
            'content': request.content,
            'is_read': False
        }
        
        result = supabase.table('messages').insert(message_data).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to send message")
        
        logger.info(f"Message sent in exchange {request.exchange_id} by {current_user['id']}")
        
        return {
            "success": True,
            "message": result.data[0]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Send message error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/messages/exchange/{exchange_id}")
async def get_exchange_messages(
    exchange_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get all messages for an exchange"""
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    try:
        # Verify user is participant
        participant = supabase.table('exchange_participants')\
            .select('id')\
            .eq('exchange_id', exchange_id)\
            .eq('user_id', current_user['id'])\
            .execute()
        
        if not participant.data:
            raise HTTPException(status_code=403, detail="Not a participant in this exchange")
        
        # Get messages with sender info
        result = supabase.table('messages')\
            .select('*, users:sender_id(id, name, email)')\
            .eq('exchange_id', exchange_id)\
            .order('created_at', desc=False)\
            .execute()
        
        # Mark unread messages as read
        unread_ids = [
            m['id'] for m in result.data
            if not m['is_read'] and m['sender_id'] != current_user['id']
        ]
        
        if unread_ids:
            for msg_id in unread_ids:
                supabase.table('messages').update({'is_read': True}).eq('id', msg_id).execute()
        
        return {
            "success": True,
            "messages": result.data
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get messages error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
