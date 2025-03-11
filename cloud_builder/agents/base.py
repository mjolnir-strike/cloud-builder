"""Base agent interface for infrastructure analysis"""
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    """Base agent interface for infrastructure analysis"""
    
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
        else:
            raise ValueError(f"Unsupported agent type: {agent_type}")
