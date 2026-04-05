from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from app.core.auth import get_current_user
from app.core.database import get_supabase
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/traces/{exchange_id}")
async def get_agent_traces(
    exchange_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Fetch the AI trace logs for a specific exchange or match session.
    Provides the data powering the 'AI Explainability Panel'.
    """
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
        
    try:
        # Fetch the traces ordered by execution time
        result = supabase.table('agent_traces')\
            .select('*')\
            .eq('exchange_id', exchange_id)\
            .order('created_at', desc=False)\
            .execute()
            
        return {
            "success": True,
            "traces": result.data
        }
        
    except Exception as e:
        logger.error(f"Error fetching traces: {e}")
        raise HTTPException(status_code=500, detail=str(e))
