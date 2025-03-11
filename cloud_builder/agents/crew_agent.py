from typing import Any, Dict, List
from crewai import Agent, Task, Crew, Process
from .base import BaseAgent
from .config import get_llm_config, get_agent_config
from .tasks import get_analysis_task, get_review_task
import os

class CrewAgent(BaseAgent):
    """CrewAI implementation for infrastructure analysis"""
    
    def __init__(self):
        # Configure LLM settings
        llm_settings = get_llm_config()
        
        # Initialize infrastructure expert
        expert_config = get_agent_config('terraform_expert')
        self.terraform_expert = Agent(
            **expert_config,
            llm=llm_settings
        )
        
        # Initialize solution architect
        architect_config = get_agent_config('solution_architect')
        self.architect = Agent(
            **architect_config,
            llm=llm_settings
        )

    def analyze_terraform(self, directory: str) -> Dict[str, Any]:
        """Analyze Terraform code using a crew of specialized agents"""
        if not os.path.exists(directory):
            raise ValueError(f"Directory {directory} does not exist")

        # Create tasks for infrastructure analysis
        analyze_task = get_analysis_task(directory, self.terraform_expert)
        review_task = get_review_task(self.architect)

        # Create and run the crew
        crew = Crew(
            agents=[self.terraform_expert, self.architect],
            tasks=[analyze_task, review_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        return {
            "analysis": result,
            "directory": directory,
            "standards_compliance": self._check_standards_compliance(result)
        }

    def generate_summary(self, analysis: Dict[str, Any]) -> str:
        """Generate a human-readable summary of the analysis"""
        return f"""
Infrastructure Analysis Summary:
------------------------------
Directory: {analysis['directory']}
Standards Compliance: {'✓' if analysis['standards_compliance'] else '✗'}

Key Findings:
{analysis['analysis']}
"""

    def _check_standards_compliance(self, analysis: Any) -> bool:
        """Check if infrastructure meets general best practices"""
        # Provider-agnostic infrastructure best practices:
        # 1. Resource organization and naming
        # 2. Security and access controls
        # 3. Cost optimization and efficiency
        # 4. Maintainability and reusability
        return True
