from typing import Any, Dict, List
import logging
from .base_agent import BaseAgent
from app.services.openrouter_service import openrouter_service

logger = logging.getLogger(__name__)


class MatchingAgent(BaseAgent):
    """
    AI Agent responsible for finding optimal skill matches
    Uses AI and algorithms to find direct and indirect matches
    """
    
    def __init__(self):
        super().__init__("matching_agent", "Matching Agent")
        self.match_threshold = 0.6
        
    async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Find matches for a user based on their requested skills
        Uses AI to enhance matching quality
        """
        user_id = context.get("user_id")
        requested_skill = context.get("requested_skill")
        candidates = context.get("candidates", [])
        
        logger.info(f"Finding matches for user {user_id}, skill: {requested_skill}")
        
        # Calculate match scores using algorithm
        matches = []
        for candidate in candidates:
            score_metrics = self._calculate_match_score(context, candidate)
            final_score = score_metrics["final_score"]
            
            if final_score >= self.match_threshold:
                matches.append({
                    "user_id": candidate.get("id"),
                    "score": final_score,
                    "metrics": score_metrics,
                    "match_type": "direct" if final_score > 0.8 else "potential",
                    "offered_skills": candidate.get("offered_skills", []),
                    "trust_score": candidate.get("trust_score", 50)
                })
        
        # Sort by score
        matches.sort(key=lambda x: x["score"], reverse=True)
        
        # Use AI to enhance top matches with insights
        if matches and openrouter_service.client:
            top_match = matches[0]
            ai_insight = await self._get_ai_match_insight(requested_skill, top_match)
            if ai_insight:
                matches[0]["ai_insight"] = ai_insight
        
        return {
            "matches": matches[:10],
            "total_candidates": len(candidates),
            "matches_found": len(matches),
            "algorithm": "hybrid_ai_matching"
        }
    
    async def _get_ai_match_insight(self, requested_skill: Dict, match: Dict) -> str:
        """Get AI insight about why this is a good match"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are a skill matching expert. Provide a brief insight about why this match is good."
                },
                {
                    "role": "user",
                    "content": f"User wants to learn: {requested_skill.get('name')}\nMatch offers: {match.get('offered_skills', [])}\nMatch score: {match.get('score')}\n\nProvide a brief insight (1-2 sentences)."
                }
            ]
            
            insight = await openrouter_service.generate_completion(messages, max_tokens=100)
            return insight or ""
        except Exception as e:
            logger.error(f"Failed to get AI insight: {e}")
            return ""
    
    def _calculate_match_score(self, context: Dict[str, Any], candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate match score between requester and candidate.
        Returns a metrics dictionary with detailed breakdown.
        """
        requested_skill = context.get("requested_skill", {})
        offered_skills = candidate.get("offered_skills", [])
        
        # Skill match (50%)
        skill_score = 0.0
        best_level_match = 0.0
        for skill in offered_skills:
            if skill.get("name", "").lower() == requested_skill.get("name", "").lower():
                level_match = self._compare_skill_levels(
                    requested_skill.get("level"),
                    skill.get("level")
                )
                skill_score = 1.0  # Name matched exactly
                best_level_match = max(best_level_match, level_match)
        
        # Sub-score for skill match
        final_skill_subscore = skill_score * best_level_match
        
        # Trust score (30%)
        trust_score_raw = float(candidate.get("trust_score", 50))
        trust_score_norm = trust_score_raw / 100.0
        
        # Reciprocal interest (20%)
        reciprocal_score = 0.0
        requester_skills = context.get("requester_skills", [])
        candidate_requests = candidate.get("requested_skills", [])
        
        for req_skill in requester_skills:
            for cand_req in candidate_requests:
                if req_skill.get("name", "").lower() == cand_req.get("name", "").lower():
                    reciprocal_score = 1.0
                    break
        
        # Weighted combination
        final_score = (final_skill_subscore * 0.5) + (trust_score_norm * 0.3) + (reciprocal_score * 0.2)
        
        return {
            "skill_match": round(final_skill_subscore, 2),
            "trust_score": round(trust_score_norm, 2),
            "reciprocal_match": round(reciprocal_score, 2),
            "final_score": round(final_score, 2)
        }
    
    def _compare_skill_levels(self, requested: str, offered: str) -> float:
        """Compare skill levels and return match score"""
        levels = {"BEGINNER": 1, "INTERMEDIATE": 2, "ADVANCED": 3, "EXPERT": 4}
        req_level = levels.get(requested, 1)
        off_level = levels.get(offered, 1)
        
        if off_level >= req_level:
            return 1.0
        else:
            return off_level / req_level
    
    def get_capabilities(self) -> List[str]:
        return [
            "direct_matching",
            "skill_level_comparison",
            "trust_based_filtering",
            "reciprocal_matching",
            "ai_enhanced_insights"
        ]
