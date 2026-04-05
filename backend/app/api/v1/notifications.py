from fastapi import APIRouter, Depends, HTTPException
from app.core.auth import get_current_user
from app.core.database import get_supabase
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/notifications/{user_id}")
async def get_notifications(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get user notifications (recent activity)"""
    if current_user['id'] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    try:
        result = supabase.table('notifications')\
            .select('*')\
            .eq('user_id', user_id)\
            .order('created_at', desc=True)\
            .limit(20)\
            .execute()
        
        return {
            "success": True,
            "notifications": result.data
        }
    
    except Exception as e:
        logger.error(f"Get notifications error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/notifications/{notification_id}/read")
async def mark_notification_read(
    notification_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Mark a notification as read"""
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    try:
        # Verify ownership
        check = supabase.table('notifications').select('user_id').eq('id', notification_id).execute()
        if not check.data or check.data[0]['user_id'] != current_user['id']:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        supabase.table('notifications').update({'is_read': True}).eq('id', notification_id).execute()
        
        return {"success": True}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Mark read error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/notifications/{user_id}/read-all")
async def mark_all_read(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Mark all notifications as read"""
    if current_user['id'] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    try:
        supabase.table('notifications')\
            .update({'is_read': True})\
            .eq('user_id', user_id)\
            .eq('is_read', False)\
            .execute()
        
        return {"success": True}
    
    except Exception as e:
        logger.error(f"Mark all read error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
