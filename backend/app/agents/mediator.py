from typing import Any, Dict, List
import logging
import asyncio
import uuid
import time
import json
from .matching_agent import MatchingAgent
from .optimization_agent import OptimizationAgent
from .fairness_agent import FairnessAgent
from .reputation_agent import ReputationAgent
from app.core.database import get_supabase

logger = logging.getLogger(__name__)


class AgentMediator:
    """
    MEDIATOR PATTERN
    Acts as the Central Decision Engine.
    Enforces strict threshold logic and trace logging.
    """
    
    def __init__(self):
        self.agents = {
            "matching": MatchingAgent(),
            "optimization": OptimizationAgent(),
            "fairness": FairnessAgent(),
            "reputation": ReputationAgent()
        }
        logger.info(f"AgentMediator initialized with {len(self.agents)} agents")
        
    async def _write_trace_async(self, exchange_id: str, agent_name: str, input_data: dict, output_data: dict, metrics: dict, reasoning: str, execution_time_ms: int):
        # We handle this asynchronously to not block
        try:
            supabase = get_supabase()
            if not supabase:
                return
                
            trace_record = {
                "exchange_id": exchange_id,
                "agent_name": agent_name,
                "input_data": input_data,
                "output_data": output_data,
                "metrics": metrics,
                "decision_reasoning": reasoning,
                "execution_time_ms": execution_time_ms
            }
            supabase.table('agent_traces').insert(trace_record).execute()
            logger.info(f"Wrote trace log for {agent_name}")
        except Exception as e:
            logger.error(f"Failed to write trace log: {e}")
            
    def _write_trace(self, exchange_id: str, agent_name: str, input_data: dict, output_data: dict, metrics: dict, reasoning: str, execution_time_ms: int):
        # Fire and forget if inside async event loop
        asyncio.create_task(self._write_trace_async(exchange_id, agent_name, input_data, output_data, metrics, reasoning, execution_time_ms))
    
    async def find_optimal_match(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinate agents to find optimal match
        Enforces thresholds: if score too low -> stop.
        """
        logger.info("Starting optimal match workflow")
        start_time = time.time()
        
        # We need an exchange/session ID for tracing even if it's just a match request
        session_id = str(uuid.uuid4()) 
        
        # Step 1: Find matches
        matching_result = await self.agents["matching"].execute(context)
        exec_ms = int((time.time() - start_time) * 1000)
        
        if not matching_result["success"]:
            return {
                "success": False,
                "error": "Matching agent failed",
                "details": matching_result
            }
        
        matches = matching_result["result"]["matches"]
        
        # Log Trace for Matching
        best_match_metrics = matches[0]["metrics"] if matches else {}
        self._write_trace(
            exchange_id=session_id,
            agent_name="MatchingAgent",
            input_data={"requested_skill": context.get("requested_skill")},
            output_data={"match_count": len(matches)},
            metrics=best_match_metrics,
            reasoning=f"Found {len(matches)} suitable matches based on exact skill and trust.",
            execution_time_ms=exec_ms
        )
        
        if not matches:
            return {
                "success": True,
                "matches": [],
                "message": "No matches found. Pipeline stopped."
            }
            
        # Threshold control logic: if the best match score is < 0.3, abort pipeline
        if matches[0]["score"] < 0.3:
            logger.warning("Best match score too low. Aborting subsequent agents.")
            return {
                "success": True,
                "matches": matches,
                "message": "Matches found but scores are below optimization threshold. Pipeline stopped."
            }
        
        # Step 2: Optimization agent (only if strict thresholds met)
        opt_start = time.time()
        optimization_context = {
            **context,
            "matches": matches
        }
        optimization_result = await self.agents["optimization"].execute(optimization_context)
        opt_ms = int((time.time() - opt_start) * 1000)
        
        self._write_trace(
            exchange_id=session_id,
            agent_name="OptimizationAgent",
            input_data={"candidates": len(matches)},
            output_data={"paths_found": len(optimization_result.get("result", {}).get("optimal_paths", []))},
            metrics={"max_hops": 4},
            reasoning="Attempted to find multi-hop optimized paths for fallback.",
            execution_time_ms=opt_ms
        )
        
        # Step 3: Validate fairness for top match
        validated_matches = []
        for match in matches[:3]:  # Validate top 3
            fair_start = time.time()
            fairness_context = {
                "exchange_type": "DIRECT_SWAP",
                "participants": [
                    {"id": context["user_id"]},
                    {"id": match["user_id"]}
                ],
                "offerings": {
                    context["user_id"]: context.get("offered_skill", {}),
                    match["user_id"]: match.get("offered_skills", [{}])[0] if match.get("offered_skills") else {}
                }
            }
            fairness_result = await self.agents["fairness"].execute(fairness_context)
            fairness_metrics = fairness_result.get("result", {})
            fair_ms = int((time.time() - fair_start) * 1000)
            
            # Write trace for this match evaluation
            self._write_trace(
                exchange_id=session_id,
                agent_name="FairnessAgent",
                input_data={"participants": [context["user_id"], match["user_id"]]},
                output_data={"is_fair": fairness_metrics.get("is_fair", False)},
                metrics={"fairness_score": fairness_metrics.get("fairness_score", 0.0)},
                reasoning=fairness_metrics.get("recommendation", "Evaluated fairness base points."),
                execution_time_ms=fair_ms
            )
            
            match["fairness"] = fairness_metrics
            
            # Control Logic: Only allow matches that are deemed vaguely fair (> 0.4 score)
            if fairness_metrics.get("fairness_score", 0.0) >= 0.4:
                validated_matches.append(match)
        
        return {
            "success": True,
            "trace_id": session_id,
            "direct_matches": validated_matches,
            "multi_hop_paths": optimization_result["result"]["optimal_paths"],
            "recommendation": "Pipeline completed successfully with hard thresholds applied."
        }
    
    async def validate_exchange(self, exchange_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate an exchange using fairness agent
        """
        start_time = time.time()
        result = await self.agents["fairness"].execute(exchange_data)
        metrics = result.get("result", {})
        
        # Decide if approved based on rigorous threshold
        approved = metrics.get("is_fair", False) and metrics.get("fairness_score", 0.0) > 0.6
        
        return {
            "success": result["success"],
            "validation": metrics,
            "approved": approved
        }
        
    async def evaluate_exchange_completion(self, exchange_id: str, user_id: str, prev_trust: float, rating: float, fairness_score: float) -> Dict[str, Any]:
        """
        Run ReputationAgent upon exchange completion.
        """
        start_time = time.time()
        context = {
            "user_id": user_id,
            "previous_trust_score": prev_trust,
            "rating_received": rating,
            "fairness_score": fairness_score
        }
        
        result = await self.agents["reputation"].execute(context)
        out = result.get("result", {})
        ext_ms = int((time.time() - start_time) * 1000)
        
        self._write_trace(
            exchange_id=exchange_id,
            agent_name="ReputationAgent",
            input_data={"rating": rating, "prev_trust": prev_trust, "fairness": fairness_score},
            output_data={"new_trust": out.get("metrics", {}).get("new_trust_score", prev_trust)},
            metrics=out.get("metrics", {}),
            reasoning=out.get("reasoning", ""),
            execution_time_ms=ext_ms
        )
        
        return out
    
    async def get_recommendations(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get personalized recommendations using all agents
        """
        # Kept lightweight
        tasks = [
            self.agents["matching"].execute(user_context),
            self.agents["optimization"].execute(user_context)
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return {"success": True, "recommendations": {}}
    
    def get_agent_stats(self) -> Dict[str, Any]:
        """Get statistics for all agents"""
        return {
            agent_name: agent.get_stats()
            for agent_name, agent in self.agents.items()
        }
