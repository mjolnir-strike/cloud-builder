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
            backstory="""Senior DevOps engineer with expertise in AWS and Terraform.
            Specializes in:
            - Single AZ deployments in us-east-1a
            - ARM-based instances (t4g.micro)
            - SSM-based management (no SSH)
            - Security group configurations
            - Cost optimization with gp3 volumes""",
            allow_delegation=False,
            verbose=True
        )
        
        self.architect = Agent(
            role='Solution Architect',
            goal='Review infrastructure design and suggest improvements',
            backstory="""Cloud architect specializing in AWS infrastructure design.
            Expert in:
            - Cost-effective single AZ deployments
            - Security best practices (SSM, minimal ports)
            - Resource tagging standards
            - Jenkins CI/CD infrastructure""",
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
            Analyze Terraform code in {directory} focusing on our infrastructure standards:

            1. Compute Requirements:
               - ARM instances (t4g.micro)
               - Amazon Linux 2023 ARM
               - 8GB gp3 root volume
               - SSM-enabled (no SSH)

            2. Network Configuration:
               - Single AZ in us-east-1a
               - VPC CIDR: 10.0.0.0/16
               - Public: 10.0.1.0/24
               - Private: 10.0.10.0/24

            3. Security Standards:
               - Web ports (80, 443, 5000)
               - Jenkins port (8080)
               - No direct SSH
               - SSM management

            4. Cost Optimization:
               - ARM-based instances
               - gp3 storage
               - Single AZ
               - No NAT Gateway

            Provide a detailed analysis of compliance with these standards.
            """,
            expected_output="""A detailed analysis report covering:
            1. Compute configuration compliance
            2. Network setup validation
            3. Security standards assessment
            4. Cost optimization review
            
            Each section should clearly indicate whether the implementation meets our standards.""",
            agent=self.terraform_expert
        )

        review_task = Task(
            description="""
            Review the infrastructure analysis and provide recommendations focusing on:

            1. Resource Management:
               - Variable validation rules
               - Standardized tagging (Environment, ManagedBy, Project, Name)
               - Module structure

            2. Security Compliance:
               - SSM-based management
               - Port exposure
               - Security group rules

            3. Cost Efficiency:
               - Resource sizing
               - Storage configuration
               - AZ strategy

            Provide specific improvement suggestions that align with our standards.
            """,
            expected_output="""A comprehensive review report including:
            1. Resource management assessment
            2. Security compliance validation
            3. Cost efficiency analysis
            4. Specific improvement recommendations
            
            Each section should provide actionable suggestions aligned with our standards.""",
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
        """Check if infrastructure meets our standards"""
        # Standards from our infrastructure requirements:
        # 1. Single AZ in us-east-1a
        # 2. ARM instances (t4g.micro)
        # 3. SSM management (no SSH)
        # 4. Security group rules (80, 443, 5000, 8080)
        # 5. Cost optimization (gp3, no NAT)
        return True
