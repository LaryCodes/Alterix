from typing import Any, Dict, List
import logging
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class ReputationAgent(BaseAgent):
    """
    Evaluates exchange completions to update global Trust Scores.
    Uses deterministic scoring with structural output.
    """
    
    def __init__(self):
        super().__init__("reputation_agent", "Reputation Agent")
        
    async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate and output the reputation deltas for a participant after an exchange.
        Expects context to have: 'user_id', 'previous_trust_score', 'rating_received', 'fairness_score'
        """
        user_id = context.get("user_id")
        prev_trust = float(context.get("previous_trust_score", 50.0))
        rating = float(context.get("rating_received", 3.0)) # 1 to 5
        fairness = float(context.get("fairness_score", 0.5)) # 0 to 1
        
        logger.info(f"Evaluating reputation update for user {user_id}")
        
        # 1. Base rating impact: Centered around 3.0 (neutral)
        # Rating 5 -> +10, Rating 1 -> -10
        rating_impact = (rating - 3.0) * 5.0
        
        # 2. Fairness multiplier: Adjusts impact based on how fair the exchange was
        # Highly fair exchanges (close to 1.0) grant the full positive impact but cushion negative impact slightly.
        # Unfair exchanges punish negative ratings harder and reduce positive rating rewards.
        if rating_impact > 0:
            adjusted_impact = rating_impact * fairness
        else:
            # Unfair exchanges get penalized more if the rating is bad
            adjusted_impact = rating_impact * (2.0 - fairness)
            
        # 3. Trust Score Inertia: Harder to change at the extremes (closer to 0 or 100)
        inertia = 1.0
        if prev_trust > 80 and adjusted_impact > 0:
            inertia = 0.5 # Diminishing returns above 80
        elif prev_trust < 20 and adjusted_impact < 0:
            inertia = 0.5 # Diminishing penalties below 20
            
        final_adjustment = adjusted_impact * inertia
        new_trust_score = max(0.0, min(100.0, prev_trust + final_adjustment))
        
        # Determine risk assessment
        high_risk = False
        if rating <= 2.0 and prev_trust < 40.0:
            high_risk = True
            
        reasoning = (
            f"Base trust score was {prev_trust:.1f}. "
            f"Received rating {rating}/5 resulted in a base adjustment. "
            f"Fairness context of {fairness:.2f} altered the impact multiplier. "
            f"Final adjustment: {final_adjustment:+.1f} points."
        )

        return {
            "metrics": {
                "previous_trust_score": prev_trust,
                "rating_received": rating,
                "fairness_score": fairness,
                "adjustment_applied": round(final_adjustment, 2),
                "new_trust_score": round(new_trust_score, 2)
            },
            "reasoning": reasoning,
            "high_risk": high_risk
        }
    
    def get_capabilities(self) -> List[str]:
        return [
            "trust_score_computation",
            "risk_assessment"
        ]
