from fastapi import APIRouter, HTTPException, Depends
from app.core.database import get_supabase
from app.core.auth import get_current_user

router = APIRouter()


@router.get("/users/{user_id}")
async def get_user(user_id: str, current_user: dict = Depends(get_current_user)):
    """Get user profile"""
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    result = supabase.table('users').select('id, name, email, trust_score, total_exchanges, created_at').eq('id', user_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"success": True, "user": result.data[0]}


@router.get("/users/{user_id}/stats")
async def get_user_stats(user_id: str, current_user: dict = Depends(get_current_user)):
    """Get user statistics"""
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    # Get user
    user_result = supabase.table('users').select('*').eq('id', user_id).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = user_result.data[0]
    
    # Get offered skills count
    offered_skills = supabase.table('user_offered_skills').select('id').eq('user_id', user_id).execute()
    
    # Get requested skills count
    requested_skills = supabase.table('user_requested_skills').select('id').eq('user_id', user_id).execute()
    
    # Get exchanges
    exchanges = supabase.table('exchange_participants').select('exchange_id, exchanges(*)').eq('user_id', user_id).execute()
    
    active_exchanges = [e for e in exchanges.data if e.get('exchanges', {}).get('status') in ['PENDING', 'IN_PROGRESS', 'SCHEDULED', 'NEGOTIATING']]
    completed_exchanges = [e for e in exchanges.data if e.get('exchanges', {}).get('status') == 'COMPLETED']
    
    return {
        "success": True,
        "stats": {
            "skills_offered": len(offered_skills.data),
            "skills_requested": len(requested_skills.data),
            "active_exchanges": len(active_exchanges),
            "completed_exchanges": len(completed_exchanges),
            "trust_score": user['trust_score'],
            "total_exchanges": user['total_exchanges']
        }
    }
