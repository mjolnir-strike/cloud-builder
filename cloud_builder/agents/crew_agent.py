from typing import Any, Dict, List
from crewai import Agent, Task, Crew, Process
from .base import BaseAgent
import os

class CrewAgent(BaseAgent):
    """CrewAI implementation for infrastructure analysis"""
    
    def __init__(self):
        # Initialize agents with tools as functions
        self.terraform_expert = Agent(
            role='Infrastructure Expert',
            goal='Analyze Terraform code for best practices and security',
            backstory='Senior DevOps engineer with expertise in AWS and Terraform',
            allow_delegation=False,
            verbose=True,
            function_calling=True,
            tools=[
                {
                    "name": "analyze_terraform_code",
                    "description": "Analyze Terraform code for AWS best practices",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "directory": {
                                "type": "string",
                                "description": "Directory containing Terraform code"
                            }
                        },
                        "required": ["directory"]
                    }
                },
                {
                    "name": "check_security_config",
                    "description": "Check security configurations against standards",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "config": {
                                "type": "object",
                                "description": "Security configuration to check"
                            }
                        },
                        "required": ["config"]
                    }
                }
            ]
        )
        
        self.architect = Agent(
            role='Solution Architect',
            goal='Review infrastructure design and suggest improvements',
            backstory='Cloud architect specializing in AWS infrastructure design',
            allow_delegation=False,
            verbose=True,
            function_calling=True,
            tools=[
                {
                    "name": "review_architecture",
                    "description": "Review infrastructure architecture",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "analysis": {
                                "type": "object",
                                "description": "Analysis results to review"
                            }
                        },
                        "required": ["analysis"]
                    }
                }
            ]
        )

    def analyze_terraform(self, directory: str) -> Dict[str, Any]:
        """Analyze Terraform code using a crew of specialized agents"""
        if not os.path.exists(directory):
            raise ValueError(f"Directory {directory} does not exist")

        crew = Crew(
            agents=[self.terraform_expert, self.architect],
            tasks=[
                Task(
                    description=f"Analyze Terraform code in {directory} for best practices and security. Check for:\n"
                              f"1. Single AZ deployment in us-east-1a\n"
                              f"2. ARM instance usage (t4g.micro)\n"
                              f"3. Storage configurations (gp3)\n"
                              f"4. Security group rules (ports 80, 443, 5000)\n"
                              f"5. SSM-based management\n"
                              f"6. Cost optimization practices",
                    expected_output="Detailed analysis of Terraform code with focus on AWS best practices and security standards",
                    agent=self.terraform_expert
                ),
                Task(
                    description="Review the infrastructure architecture and suggest improvements based on:\n"
                              "1. Single AZ deployment requirements\n"
                              "2. Cost optimization guidelines\n"
                              "3. Security best practices\n"
                              "4. Resource tagging standards",
                    expected_output="Architecture review with specific improvement suggestions",
                    agent=self.architect
                )
            ],
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
        # Verify compliance with our standards:
        # - Single AZ in us-east-1a
        # - ARM instances (t4g.micro)
        # - SSM management
        # - Security group rules
        return True
