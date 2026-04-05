from abc import ABC, abstractmethod
from typing import Any, Dict, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Base class for all AI agents in the system
    Provides common functionality and interface
    """
    
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.created_at = datetime.utcnow()
        self.execution_count = 0
        self.last_execution = None
        
    @abstractmethod
    async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the given context and return results
        Must be implemented by concrete agents
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities"""
        pass
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent with logging and metrics
        """
        logger.info(f"Agent {self.name} starting execution")
        self.execution_count += 1
        self.last_execution = datetime.utcnow()
        
        try:
            result = await self.process(context)
            logger.info(f"Agent {self.name} completed successfully")
            return {
                "agent_id": self.agent_id,
                "agent_name": self.name,
                "success": True,
                "result": result,
                "executed_at": self.last_execution.isoformat()
            }
        except Exception as e:
            logger.error(f"Agent {self.name} failed: {str(e)}")
            return {
                "agent_id": self.agent_id,
                "agent_name": self.name,
                "success": False,
                "error": str(e),
                "executed_at": self.last_execution.isoformat()
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "execution_count": self.execution_count,
            "last_execution": self.last_execution.isoformat() if self.last_execution else None,
            "created_at": self.created_at.isoformat()
        }
