from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class BaseAgent(ABC):
    """Base agent interface that can be implemented by both CrewAI and LangChain"""
    
    @abstractmethod
    def analyze_terraform(self, directory: str) -> Dict[str, Any]:
        """Analyze Terraform code in the specified directory"""
        pass

    @abstractmethod
    def generate_summary(self, analysis: Dict[str, Any]) -> str:
        """Generate a human-readable summary of the analysis"""
        pass

class AgentFactory:
    """Factory to create appropriate agent based on configuration"""
    
    @staticmethod
    def create_agent(agent_type: str = "crew") -> BaseAgent:
        if agent_type == "crew":
            from .crew_agent import CrewAgent
            return CrewAgent()
        elif agent_type == "langchain":
            from .langchain_agent import LangChainAgent
            return LangChainAgent()
        else:
            raise ValueError(f"Unsupported agent type: {agent_type}")
