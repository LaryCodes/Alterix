from typing import Any, Dict, List
import logging
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class FairnessAgent(BaseAgent):
    """
    AI Agent responsible for ensuring fair value exchange
    Validates that exchanges are balanced and equitable
    """
    
    def __init__(self):
        super().__init__("fairness_agent", "Fairness Agent")
        self.fairness_threshold = 0.7
        
    async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate fairness of an exchange or exchange chain
        """
        exchange_type = context.get("exchange_type")
        participants = context.get("participants", [])
        offerings = context.get("offerings", {})
        
        logger.info(f"Evaluating fairness for {exchange_type} exchange")
        
        if exchange_type == "DIRECT_SWAP":
            result = self._evaluate_direct_swap(participants, offerings)
        elif exchange_type == "MULTI_PARTY_CHAIN":
            result = self._evaluate_chain(participants, offerings)
        else:
            result = self._evaluate_paid_learning(participants, offerings)
        
        return result
    
    def _evaluate_direct_swap(self, participants: List[Dict], offerings: Dict) -> Dict[str, Any]:
        """Evaluate fairness of 1:1 swap"""
        if len(participants) != 2:
            return {
                "is_fair": False,
                "fairness_score": 0.0,
                "reason": "Direct swap requires exactly 2 participants"
            }
        
        user1_id = participants[0]["id"]
        user2_id = participants[1]["id"]
        
        skill1 = offerings.get(user1_id, {})
        skill2 = offerings.get(user2_id, {})
        
        value1 = self._calculate_skill_value(skill1)
        value2 = self._calculate_skill_value(skill2)
        
        # Calculate fairness score
        if value1 == 0 or value2 == 0:
            fairness_score = 0.0
        else:
            ratio = min(value1, value2) / max(value1, value2)
            fairness_score = ratio
        
        is_fair = fairness_score >= self.fairness_threshold
        
        return {
            "is_fair": is_fair,
            "fairness_score": fairness_score,
            "value_difference": abs(value1 - value2),
            "skill1_value": value1,
            "skill2_value": value2,
            "recommendation": self._generate_fairness_recommendation(fairness_score, value1, value2)
        }
    
    def _evaluate_chain(self, participants: List[Dict], offerings: Dict) -> Dict[str, Any]:
        """Evaluate fairness of multi-party chain"""
        values = []
        for participant in participants:
            skill = offerings.get(participant["id"], {})
            values.append(self._calculate_skill_value(skill))
        
        if not values or min(values) == 0:
            return {
                "is_fair": False,
                "fairness_score": 0.0,
                "reason": "Invalid skill values in chain"
            }
        
        # Calculate variance in values
        avg_value = sum(values) / len(values)
        variance = sum((v - avg_value) ** 2 for v in values) / len(values)
        normalized_variance = variance / (avg_value ** 2) if avg_value > 0 else 1.0
        
        # Lower variance = more fair
        fairness_score = max(0.0, 1.0 - normalized_variance)
        is_fair = fairness_score >= self.fairness_threshold
        
        return {
            "is_fair": is_fair,
            "fairness_score": fairness_score,
            "average_value": avg_value,
            "value_variance": variance,
            "participant_values": values,
            "recommendation": "Chain is balanced" if is_fair else "Consider adjusting skill levels or adding compensation"
        }
    
    def _evaluate_paid_learning(self, participants: List[Dict], offerings: Dict) -> Dict[str, Any]:
        """Evaluate fairness of paid learning exchange"""
        teacher = participants[0]
        learner = participants[1]
        
        skill = offerings.get(teacher["id"], {})
        payment = offerings.get(learner["id"], {}).get("payment_amount", 0)
        
        skill_value = self._calculate_skill_value(skill)
        fair_price = skill_value * 10  # $10 per value point
        
        price_ratio = payment / fair_price if fair_price > 0 else 0
        fairness_score = min(1.0, price_ratio) if price_ratio <= 1.5 else 1.0 / price_ratio
        
        is_fair = fairness_score >= self.fairness_threshold
        
        return {
            "is_fair": is_fair,
            "fairness_score": fairness_score,
            "suggested_price": fair_price,
            "actual_price": payment,
            "price_difference": abs(payment - fair_price),
            "recommendation": f"Suggested price range: ${fair_price * 0.8:.2f} - ${fair_price * 1.2:.2f}"
        }
    
    def _calculate_skill_value(self, skill: Dict) -> float:
        """Calculate monetary value of a skill"""
        base_values = {
            "BEGINNER": 10,
            "INTERMEDIATE": 25,
            "ADVANCED": 50,
            "EXPERT": 100
        }
        
        category_multipliers = {
            "Technology": 1.5,
            "Business": 1.4,
            "Creative": 1.3,
            "Language": 1.2,
            "Other": 1.0
        }
        
        level = skill.get("level", "BEGINNER")
        category = skill.get("category", "Other")
        hours = skill.get("estimated_hours", 1)
        
        base_value = base_values.get(level, 10)
        multiplier = category_multipliers.get(category, 1.0)
        
        return base_value * multiplier * hours
    
    def _generate_fairness_recommendation(self, score: float, value1: float, value2: float) -> str:
        """Generate recommendation based on fairness score"""
        if score >= 0.9:
            return "Excellent match! Values are well balanced."
        elif score >= 0.7:
            return "Good match. Exchange is fair."
        elif score >= 0.5:
            diff = abs(value1 - value2)
            return f"Consider adding ${diff:.2f} compensation to balance the exchange."
        else:
            return "Significant value imbalance. Consider finding a different match."
    
    def get_capabilities(self) -> List[str]:
        return [
            "value_assessment",
            "fairness_scoring",
            "exchange_validation",
            "price_recommendation"
        ]
