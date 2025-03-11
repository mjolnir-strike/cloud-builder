"""CrewAgent for Terraform analysis"""
from typing import Dict, Any, List
from crewai import Agent, Crew, Task, Process
from .config import get_agent_config
from .tools.read_terraform import read_terraform_files

class CrewAgent:
    """Agent for analyzing Terraform code using a provider-agnostic approach"""
    
    def __init__(self, directory: str):
        """Initialize CrewAgent
        
        Args:
            directory: Directory containing Terraform files
        """
        self.directory = directory
        self.tools = [read_terraform_files]
    
    def create_agent(self, role: str) -> Agent:
        """Create an agent with the specified role
        
        Args:
            role: Agent role (security_expert, cost_expert)
            
        Returns:
            Agent instance
        """
        config = get_agent_config(role)
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            llm=config['llm'],
            verbose=config['verbose'],
            allow_delegation=config['allow_delegation'],
            memory=config['memory'],
            tools=self.tools
        )
    
    def analyze(self) -> Dict[str, Any]:
        """Analyze Terraform code in the directory using specialized agents
        
        Returns:
            Analysis results containing security and cost recommendations
        """
        # Create specialized agents
        security_agent = self.create_agent('security_expert')
        cost_agent = self.create_agent('cost_expert')
        
        # Create analysis tasks with single-run focus
        tasks = [
            Task(
                description=(
                    f"Perform a ONE-TIME security analysis of Terraform files in {self.directory}. Focus on:\n"
                    "1. IAM and access control best practices\n"
                    "2. Network security and data protection\n"
                    "3. Compliance with security standards\n"
                    "4. Provider-agnostic security patterns\n"
                    "Provide a SINGLE comprehensive analysis and stop."
                ),
                agent=security_agent,
                expected_output=(
                    "A single, comprehensive security analysis including:\n"
                    "1. Security vulnerabilities and risks\n"
                    "2. Best practices recommendations\n"
                    "3. Compliance findings\n"
                    "4. Specific improvement suggestions\n"
                    "Return results in a clear, structured format."
                )
            ),
            Task(
                description=(
                    f"Perform a ONE-TIME cost analysis of Terraform files in {self.directory}. Focus on:\n"
                    "1. Resource sizing and utilization\n"
                    "2. Cost-effective configurations\n"
                    "3. Resource lifecycle management\n"
                    "4. Provider-agnostic optimization patterns\n"
                    "Provide a SINGLE comprehensive analysis and stop."
                ),
                agent=cost_agent,
                expected_output=(
                    "A single, comprehensive cost analysis including:\n"
                    "1. Cost optimization opportunities\n"
                    "2. Resource efficiency recommendations\n"
                    "3. Lifecycle management suggestions\n"
                    "4. Specific cost-saving measures\n"
                    "Return results in a clear, structured format."
                )
            )
        ]
        
        # Create crew for sequential analysis
        crew = Crew(
            agents=[security_agent, cost_agent],
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        # Run analysis and process results
        result = crew.kickoff()
        # Handle new CrewAI output format
        return {
            'analysis': result
        }
