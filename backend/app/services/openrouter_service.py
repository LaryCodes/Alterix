from openai import OpenAI
from app.core.config import settings
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class OpenRouterService:
    """Service for interacting with OpenRouter API"""
    
    def __init__(self):
        self.client = None
        if settings.OPENROUTER_API_KEY:
            self.client = OpenAI(
                base_url=settings.OPENROUTER_BASE_URL,
                api_key=settings.OPENROUTER_API_KEY,
            )
            logger.info("OpenRouter client initialized")
        else:
            logger.warning("OpenRouter API key not configured")
    
    async def generate_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Optional[str]:
        """Generate completion using OpenRouter"""
        if not self.client:
            logger.warning("OpenRouter client not initialized")
            return None
        
        if model is None:
            model = settings.OPENROUTER_DEFAULT_MODEL
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"OpenRouter API error: {e}")
            return None
    
    async def generate_skill_recommendations(
        self,
        user_skills: List[str],
        user_interests: List[str]
    ) -> List[str]:
        """Generate personalized skill recommendations"""
        if not self.client:
            return []
        
        messages = [
            {
                "role": "system",
                "content": "You are a skill recommendation expert. Suggest 5 relevant skills to learn based on user's current skills and interests."
            },
            {
                "role": "user",
                "content": f"Current skills: {', '.join(user_skills)}\nInterests: {', '.join(user_interests)}\n\nSuggest 5 skills to learn next."
            }
        ]
        
        response = await self.generate_completion(messages, max_tokens=500)
        
        if response:
            # Parse response into list
            skills = [s.strip() for s in response.split('\n') if s.strip() and not s.strip().startswith('#')]
            return skills[:5]
        
        return []
    
    async def generate_negotiation_suggestion(
        self,
        exchange_context: Dict[str, Any]
    ) -> Optional[str]:
        """Generate AI negotiation suggestions for exchanges"""
        if not self.client:
            return None
        
        messages = [
            {
                "role": "system",
                "content": "You are a negotiation expert for skill exchanges. Provide fair and balanced suggestions."
            },
            {
                "role": "user",
                "content": f"Exchange context: {exchange_context}\n\nProvide a brief negotiation suggestion to make this exchange fair."
            }
        ]
        
        return await self.generate_completion(messages, max_tokens=300)
    
    async def analyze_skill_match(
        self,
        user1_skills: List[str],
        user2_skills: List[str]
    ) -> Dict[str, Any]:
        """Analyze compatibility between two users' skills"""
        if not self.client:
            return {"compatibility_score": 0.5, "analysis": "OpenRouter not configured"}
        
        messages = [
            {
                "role": "system",
                "content": "You are a skill matching analyst. Analyze compatibility between two users."
            },
            {
                "role": "user",
                "content": f"User 1 skills: {', '.join(user1_skills)}\nUser 2 skills: {', '.join(user2_skills)}\n\nProvide compatibility score (0-1) and brief analysis."
            }
        ]
        
        response = await self.generate_completion(messages, max_tokens=200)
        
        # Simple parsing - in production, use structured output
        return {
            "compatibility_score": 0.7,
            "analysis": response or "Analysis unavailable"
        }


# Global instance
openrouter_service = OpenRouterService()
