from typing import Any, Dict, List
import logging
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class OptimizationAgent(BaseAgent):
    """
    AI Agent responsible for finding optimal multi-hop exchange paths
    Implements graph traversal algorithms to find A → B → C → D chains
    """
    
    def __init__(self):
        super().__init__("optimization_agent", "Optimization Agent")
        self.max_hop_depth = 4
        
    async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Find optimal exchange paths including multi-hop chains
        """
        user_id = context.get("user_id")
        requested_skill = context.get("requested_skill")
        all_users = context.get("all_users", [])
        
        logger.info(f"Finding optimal paths for user {user_id}")
        
        # Build connection graph
        graph = self._build_connection_graph(all_users)
        
        # Find users with requested skill
        target_users = self._find_users_with_skill(all_users, requested_skill)
        
        # Find all paths
        all_paths = []
        for target in target_users:
            paths = self._find_paths(user_id, target["id"], graph, self.max_hop_depth)
            for path in paths:
                path_score = self._calculate_path_score(path, all_users)
                all_paths.append({
                    "path": path,
                    "target_user": target["id"],
                    "hops": len(path) - 1,
                    "score": path_score,
                    "estimated_time": (len(path) - 1) * 7  # days
                })
        
        # Sort by score
        all_paths.sort(key=lambda x: x["score"], reverse=True)
        
        return {
            "optimal_paths": all_paths[:5],  # Top 5 paths
            "total_paths_found": len(all_paths),
            "max_hops": self.max_hop_depth,
            "recommendation": self._generate_recommendation(all_paths)
        }
    
    def _build_connection_graph(self, users: List[Dict]) -> Dict[str, List[str]]:
        """Build graph of user connections based on skill compatibility"""
        graph = {}
        
        for user in users:
            connections = []
            for other in users:
                if user["id"] != other["id"] and self._has_connection(user, other):
                    connections.append(other["id"])
            graph[user["id"]] = connections
        
        return graph
    
    def _has_connection(self, user1: Dict, user2: Dict) -> bool:
        """Check if two users have compatible skills"""
        user1_offers = {s["name"].lower() for s in user1.get("offered_skills", [])}
        user2_requests = {s["name"].lower() for s in user2.get("requested_skills", [])}
        return bool(user1_offers & user2_requests)
    
    def _find_users_with_skill(self, users: List[Dict], skill: Dict) -> List[Dict]:
        """Find users offering the requested skill"""
        skill_name = skill.get("name", "").lower()
        return [
            user for user in users
            if any(s["name"].lower() == skill_name for s in user.get("offered_skills", []))
        ]
    
    def _find_paths(self, start: str, end: str, graph: Dict, max_depth: int) -> List[List[str]]:
        """Find all paths from start to end using DFS"""
        all_paths = []
        
        def dfs(current: str, target: str, path: List[str], visited: set, depth: int):
            if depth <= 0:
                return
            
            if current == target:
                all_paths.append(path.copy())
                return
            
            for neighbor in graph.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    dfs(neighbor, target, path, visited, depth - 1)
                    path.pop()
                    visited.remove(neighbor)
        
        dfs(start, end, [start], {start}, max_depth)
        return all_paths
    
    def _calculate_path_score(self, path: List[str], all_users: List[Dict]) -> float:
        """Calculate quality score for a path"""
        if len(path) < 2:
            return 0.0
        
        # Shorter paths are better
        length_score = 1.0 / len(path)
        
        # Average trust score of path
        user_map = {u["id"]: u for u in all_users}
        trust_scores = [user_map.get(uid, {}).get("trust_score", 50) for uid in path]
        avg_trust = sum(trust_scores) / len(trust_scores) / 100.0
        
        return (length_score * 0.4) + (avg_trust * 0.6)
    
    def _generate_recommendation(self, paths: List[Dict]) -> str:
        """Generate human-readable recommendation"""
        if not paths:
            return "No exchange paths found. Try adjusting your criteria."
        
        best_path = paths[0]
        hops = best_path["hops"]
        
        if hops == 0:
            return "Direct match available! This is the fastest option."
        elif hops == 1:
            return f"2-hop exchange recommended. Estimated completion: {best_path['estimated_time']} days."
        else:
            return f"{hops + 1}-hop chain found. Consider direct matches for faster completion."
    
    def get_capabilities(self) -> List[str]:
        return [
            "multi_hop_pathfinding",
            "graph_optimization",
            "path_scoring",
            "exchange_chain_building"
        ]
