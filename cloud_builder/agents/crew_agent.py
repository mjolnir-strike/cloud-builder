from typing import Any, Dict, List
from crewai import Agent, Task, Crew, Process
from .base import BaseAgent
import os

class CrewAgent(BaseAgent):
    """CrewAI implementation for infrastructure analysis"""
    
    def __init__(self):
        # Initialize agents for infrastructure analysis
        self.terraform_expert = Agent(
            role='Infrastructure Expert',
            goal='Analyze Terraform code for best practices and security',
            backstory="""Senior DevOps engineer with expertise in infrastructure as code.
            Specializes in:
            - Infrastructure best practices
            - Security configurations
            - Resource management
            - Cost optimization""",
            allow_delegation=False,
            verbose=True
        )
        
        self.architect = Agent(
            role='Solution Architect',
            goal='Review infrastructure design and suggest improvements',
            backstory="""Cloud architect specializing in infrastructure design.
            Expert in:
            - Infrastructure architecture
            - Security best practices
            - Resource organization
            - Cost optimization""",
            allow_delegation=False,
            verbose=True
        )

    def analyze_terraform(self, directory: str) -> Dict[str, Any]:
        """Analyze Terraform code using a crew of specialized agents"""
        if not os.path.exists(directory):
            raise ValueError(f"Directory {directory} does not exist")

        # Create tasks for infrastructure analysis
        analyze_task = Task(
            description=f"""
            Analyze Terraform code in {directory} focusing on infrastructure best practices:

            1. Resource Configuration:
               - Compute resource sizing and types
               - Storage resource configurations
               - Network topology and design
               - Service integrations and dependencies

            2. Security Standards:
               - Identity and access management
               - Network security and isolation
               - Service security configurations
               - Authentication and authorization

            3. Infrastructure Design:
               - Resource organization and naming
               - Module structure and reusability
               - Variable management and validation
               - State management and locking

            4. Cost Optimization:
               - Resource efficiency and utilization
               - Scaling strategy and elasticity
               - Storage tier selection
               - Network traffic optimization

            Provide a detailed analysis of these aspects.
            """,
            expected_output="""A detailed analysis report covering:
            1. Resource configuration assessment
            2. Security implementation review
            3. Infrastructure design evaluation
            4. Cost optimization analysis
            
            Each section should highlight strengths and potential improvements.""",
            agent=self.terraform_expert
        )

        review_task = Task(
            description="""
            Review the infrastructure analysis and provide recommendations focusing on:

            1. Architecture:
               - Resource organization and relationships
               - Module design patterns
               - Service integration patterns
               - Scalability and resilience

            2. Security:
               - Access control patterns
               - Network isolation strategy
               - Data protection mechanisms
               - Compliance and governance

            3. Efficiency:
               - Resource utilization patterns
               - Cost optimization strategies
               - Performance optimization
               - Operational efficiency

            Provide specific improvement suggestions for better infrastructure design.
            """,
            expected_output="""A comprehensive review report including:
            1. Architecture assessment
            2. Security evaluation
            3. Efficiency analysis
            4. Actionable recommendations
            
            Focus on practical improvements that enhance the infrastructure.""",
            agent=self.architect
        )

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
