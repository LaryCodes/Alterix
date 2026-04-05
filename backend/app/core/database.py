from supabase import create_client, Client
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class SupabaseClient:
    """Singleton Supabase client"""
    _instance: Client = None
    
    @classmethod
    def get_client(cls) -> Client:
        if cls._instance is None:
            if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
                logger.warning("Supabase credentials not configured. Using mock client.")
                return None
            
            try:
                cls._instance = create_client(
                    settings.SUPABASE_URL,
                    settings.SUPABASE_KEY
                )
                logger.info("Supabase client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
                return None
        
        return cls._instance


def get_supabase() -> Client:
    """Dependency to get Supabase client"""
    return SupabaseClient.get_client()
