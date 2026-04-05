import httpx
import logging
from typing import Dict, Any, Optional, List
from app.core.config import settings

logger = logging.getLogger(__name__)

# Java Core Engine HTTP client
JAVA_BASE_URL = f"http://{settings.JAVA_GRPC_HOST}:{settings.JAVA_GRPC_PORT}"


class JavaBridge:
    """
    Bridge to Java Core Engine via HTTP REST.
    Falls back gracefully if Java engine is not available.
    """
    
    def __init__(self):
        self._available: Optional[bool] = None
        self._client = httpx.AsyncClient(timeout=10.0)
    
    async def is_available(self) -> bool:
        """Check if Java Core Engine is running"""
        if self._available is not None:
            return self._available
        
        try:
            response = await self._client.get(f"{JAVA_BASE_URL}/health")
            self._available = response.status_code == 200
            if self._available:
                logger.info("✅ Java Core Engine connected")
            return self._available
        except Exception:
            self._available = False
            logger.info("ℹ️  Java Core Engine not available — using Python-only mode")
            return False
    
    async def run_matching(
        self,
        user_id: str,
        skill_name: str,
        candidates: List[Dict],
        strategy: str = "direct"
    ) -> Optional[Dict]:
        """
        Run matching through Java engine's Strategy + Chain patterns
        Returns None if Java is unavailable
        """
        if not await self.is_available():
            return None
        
        try:
            payload = {
                "user_id": user_id,
                "skill_name": skill_name,
                "candidates": candidates,
                "strategy": strategy
            }
            
            response = await self._client.post(f"{JAVA_BASE_URL}/match", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Java matching: {result.get('matches_found', 0)} matches, "
                          f"confidence: {result.get('confidence', 0):.2f}")
                return result
            else:
                logger.warning(f"Java matching failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.warning(f"Java bridge error (matching): {e}")
            self._available = None  # Re-check next time
            return None
    
    async def validate_exchange(
        self,
        skill1: Dict,
        skill2: Dict
    ) -> Optional[Dict]:
        """
        Validate exchange fairness using Java Command pattern
        Returns None if Java is unavailable
        """
        if not await self.is_available():
            return None
        
        try:
            payload = {
                "skill1": skill1,
                "skill2": skill2
            }
            
            response = await self._client.post(f"{JAVA_BASE_URL}/exchange/validate", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Java validation: fair={result.get('is_fair')}, "
                          f"score={result.get('fairness_score', 0)}")
                return result
            return None
                
        except Exception as e:
            logger.warning(f"Java bridge error (validation): {e}")
            self._available = None
            return None
    
    async def get_patterns_info(self) -> Optional[Dict]:
        """Get design patterns status from Java engine"""
        if not await self.is_available():
            return None
        
        try:
            response = await self._client.get(f"{JAVA_BASE_URL}/patterns/demo")
            if response.status_code == 200:
                return response.json()
            return None
        except Exception:
            return None
    
    async def close(self):
        """Close HTTP client"""
        await self._client.aclose()


# Singleton instance
_bridge: Optional[JavaBridge] = None


def get_java_bridge() -> JavaBridge:
    global _bridge
    if _bridge is None:
        _bridge = JavaBridge()
    return _bridge
