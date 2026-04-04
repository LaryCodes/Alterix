from typing import Any, Dict, List
import logging
import asyncio
from .matching_agent import MatchingAgent
from .optimization_agent import OptimizationAgent
from .fairness_agent import FairnessAgent

logger = logging.getLogger(__name__)


class AgentMediator:
    """
    MEDIATOR PATTERN
    Coordinates communication between multiple AI agents
    Orchestrates complex workflows involving multiple agents
    """
    
    def __init__(self):
        self.agents = {
            "matching": MatchingAgent(),
            "optimization": OptimizationAgent(),
            "fairness": FairnessAgent()
        }
        logger.info(f"AgentMediator initialized with {len(self.agents)} agents")
    
    async def find_optimal_match(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinate agents to find optimal match
        1. Matching agent finds candidates
        2. Optimization agent finds best paths
        3. Fairness agent validates exchanges
        """
        logger.info("Starting optimal match workflow")
        
        # Step 1: Find matches
        matching_result = await self.agents["matching"].execute(context)
        
        if not matching_result["success"]:
            return {
                "success": False,
                "error": "Matching agent failed",
                "details": matching_result
            }
        
        matches = matching_result["result"]["matches"]
        
        if not matches:
            return {
                "success": True,
                "matches": [],
                "message": "No matches found"
            }
        
        # Step 2: Find optimal paths (including multi-hop)
        optimization_context = {
            **context,
            "matches": matches
        }
        optimization_result = await self.agents["optimization"].execute(optimization_context)
        
        # Step 3: Validate fairness for top matches
        validated_matches = []
        for match in matches[:5]:  # Validate top 5
            fairness_context = {
                "exchange_type": "DIRECT_SWAP",
                "participants": [
                    {"id": context["user_id"]},
                    {"id": match["user_id"]}
                ],
                "offerings": {
                    context["user_id"]: context.get("offered_skill", {}),
                    match["user_id"]: match.get("offered_skills", [{}])[0]
                }
            }
            fairness_result = await self.agents["fairness"].execute(fairness_context)
            
            match["fairness"] = fairness_result["result"]
            validated_matches.append(match)
        
        return {
            "success": True,
            "direct_matches": validated_matches,
            "multi_hop_paths": optimization_result["result"]["optimal_paths"],
            "recommendation": self._generate_final_recommendation(
                validated_matches,
                optimization_result["result"]["optimal_paths"]
            )
        }
    
    async def validate_exchange(self, exchange_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate an exchange using fairness agent
        """
        logger.info("Validating exchange")
        
        result = await self.agents["fairness"].execute(exchange_data)
        
        return {
            "success": result["success"],
            "validation": result["result"],
            "approved": result["result"].get("is_fair", False)
        }
    
    async def get_recommendations(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get personalized recommendations using all agents
        """
        logger.info("Generating recommendations for user")
        
        # Run agents in parallel
        tasks = [
            self.agents["matching"].execute(user_context),
            self.agents["optimization"].execute(user_context)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        matching_result = results[0] if not isinstance(results[0], Exception) else None
        optimization_result = results[1] if not isinstance(results[1], Exception) else None
        
        recommendations = {
            "direct_matches": matching_result["result"]["matches"] if matching_result else [],
            "multi_hop_opportunities": optimization_result["result"]["optimal_paths"] if optimization_result else [],
            "suggested_actions": self._generate_action_suggestions(matching_result, optimization_result)
        }
        
        return {
            "success": True,
            "recommendations": recommendations
        }
    
    def _generate_final_recommendation(self, direct_matches: List[Dict], multi_hop_paths: List[Dict]) -> str:
        """Generate final recommendation based on all agent results"""
        fair_direct_matches = [m for m in direct_matches if m.get("fairness", {}).get("is_fair", False)]
        
        if fair_direct_matches:
            return f"Found {len(fair_direct_matches)} fair direct matches. Recommend starting with highest scored match."
        elif multi_hop_paths:
            best_path = multi_hop_paths[0]
            return f"No direct matches, but found {len(multi_hop_paths)} multi-hop paths. Best path has {best_path['hops']} hops."
        else:
            return "No suitable matches found. Consider broadening your search criteria or adding more skills."
    
    def _generate_action_suggestions(self, matching_result: Dict, optimization_result: Dict) -> List[str]:
        """Generate actionable suggestions for user"""
        suggestions = []
        
        if matching_result and matching_result.get("result", {}).get("matches"):
            suggestions.append("Review your top direct matches and initiate contact")
        
        if optimization_result and optimization_result.get("result", {}).get("optimal_paths"):
            suggestions.append("Consider multi-hop exchanges for skills not directly available")
        
        if not suggestions:
            suggestions.extend([
                "Add more skills to your profile to increase match opportunities",
                "Improve your trust score by completing exchanges",
                "Adjust your skill level requirements"
            ])
        
        return suggestions
    
    def get_agent_stats(self) -> Dict[str, Any]:
        """Get statistics for all agents"""
        return {
            agent_name: agent.get_stats()
            for agent_name, agent in self.agents.items()
        }
