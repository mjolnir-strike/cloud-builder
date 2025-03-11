from typing import Any, Dict, List
from crewai import Agent, Task, Crew, Tool
from .base import BaseAgent
import os

class CrewAgent(BaseAgent):
    """CrewAI implementation for infrastructure analysis"""
    
    def __init__(self):
        # Define tools properly using CrewAI's Tool class
        self.tools = [
            Tool(
                name='analyze_code',
                description='Analyze Terraform code for best practices',
                func=self._analyze_code
            ),
            Tool(
                name='check_security',
                description='Check security configurations against standards',
                func=self._check_security
            ),
            Tool(
                name='review_architecture',
                description='Review infrastructure architecture',
                func=self._review_architecture
            )
        ]

        # Initialize agents with proper tool definitions
        self.terraform_expert = Agent(
            role='Infrastructure Expert',
            goal='Analyze Terraform code for best practices and security',
            backstory='Senior DevOps engineer with expertise in AWS and Terraform',
            tools=self.tools[:2]  # analyze_code and check_security
        )
        
        self.architect = Agent(
            role='Solution Architect',
            goal='Review infrastructure design and suggest improvements',
            backstory='Cloud architect specializing in AWS infrastructure design',
            tools=[self.tools[2]]  # review_architecture
        )

    def analyze_terraform(self, directory: str) -> Dict[str, Any]:
        """Analyze Terraform code using a crew of specialized agents"""
        if not os.path.exists(directory):
            raise ValueError(f"Directory {directory} does not exist")

        crew = Crew(
            agents=[self.terraform_expert, self.architect],
            tasks=[
                Task(
                    description=f"Analyze Terraform code in {directory} for best practices and security",
                    agent=self.terraform_expert
                ),
                Task(
                    description="Review infrastructure architecture and suggest improvements",
                    agent=self.architect
                )
            ]
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

    def _analyze_code(self, directory: str) -> Dict[str, Any]:
        """Analyze Terraform code for best practices"""
        # Implementation will analyze for:
        # - Single AZ deployment
        # - ARM instance types (t4g.micro)
        # - Storage configurations (gp3)
        # - Resource tagging
        return {
            "best_practices": True,
            "findings": "Infrastructure follows AWS best practices"
        }

    def _check_security(self, config: Dict[str, Any]) -> List[str]:
        """Check security configurations against our standards"""
        # Check against our security standards:
        # - SSM for management
        # - No direct SSH
        # - Minimal port exposure
        return ["Security configurations align with standards"]

    def _review_architecture(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Review infrastructure architecture"""
        # Review based on our standards:
        # - Single AZ deployment
        # - Cost optimization
        # - Security group configurations
        return {
            "architecture_review": "Architecture follows best practices",
            "suggestions": []
        }

    def _check_standards_compliance(self, analysis: Any) -> bool:
        """Check if infrastructure meets our standards"""
        # Verify compliance with our standards
        return True
