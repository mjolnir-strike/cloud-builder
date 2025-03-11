"""CrewAI-based agent for analyzing Terraform code"""
import os
from typing import Dict, Any, Optional
from functools import partial
from crewai import Agent, Task, Crew, Process
from langchain_ollama import OllamaLLM
from .base import BaseAgent
from .config import get_llm_config, get_agent_config
from .tools import TerraformTools

class CrewAgent(BaseAgent):
    """CrewAI implementation of infrastructure analysis agent"""
    
    def __init__(self):
        """Initialize CrewAgent with LLM configuration"""
        # Initialize Ollama LLM
        llm = OllamaLLM(
            model=f"ollama/{os.getenv('OLLAMA_MODEL')}",  # Specify provider
            base_url=os.getenv('OLLAMA_HOST'),
            temperature=0.1,
            timeout=int(os.getenv('ANALYSIS_TIMEOUT', '300'))
        )
        
        # Initialize tools
        tools = TerraformTools()
        
        # Create agents with their specialized tools
        self.terraform_expert = Agent(
            **get_agent_config('terraform_expert'),
            llm=llm,  # Pass Ollama instance directly
            tools=[
                tools.read_terraform_files,
                tools.analyze_security,
                tools.check_best_practices,
                tools.optimize_costs
            ]
        )
        
        self.architect = Agent(
            **get_agent_config('solution_architect'),
            llm=llm,  # Pass Ollama instance directly
            tools=[
                tools.analyze_architecture,
                tools.review_design,
                tools.suggest_improvements,
                tools.check_scalability
            ]
        )
    
    def analyze_terraform(self, directory: str) -> Dict[str, Any]:
        """Analyze Terraform code in the specified directory"""
        if not os.path.exists(directory):
            raise ValueError(f"Directory {directory} does not exist")
        
        # Create tasks for analysis
        terraform_task = Task(
            description="""
            Analyze the Terraform code in the specified directory for:
            1. Resource configuration best practices
            2. Security standards (access, network, endpoints)
            3. Infrastructure design patterns
            4. Cost optimization opportunities
            
            Provide detailed findings and recommendations.
            """,
            expected_output="""A comprehensive analysis report containing:
            1. Resource configuration details and recommendations
            2. Security compliance findings and potential issues
            3. Infrastructure design patterns and improvements
            4. Cost optimization opportunities and suggestions
            """,
            agent=self.terraform_expert,
            context=[{
                "directory": directory,
                "description": "Terraform infrastructure analysis task",
                "expected_output": "Analysis of infrastructure code"
            }],
            context_vars=["directory"],
            tools=[
                self.terraform_expert.tools[0],  # read_terraform_files
                self.terraform_expert.tools[1],  # analyze_security
                self.terraform_expert.tools[2],  # check_best_practices
                self.terraform_expert.tools[3]   # optimize_costs
            ]
        )
        
        architect_task = Task(
            description="""
            Review the infrastructure design and provide:
            1. Architecture review and recommendations
            2. Best practices alignment
            3. Improvement areas for scalability and maintainability
            4. Design pattern suggestions
            
            Focus on provider-agnostic patterns and practices.
            """,
            expected_output="""A detailed architecture review report containing:
            1. Architecture assessment and patterns analysis
            2. Best practices evaluation and gaps
            3. Specific recommendations for improvements
            4. Actionable steps for implementation
            """,
            agent=self.architect,
            context=[{
                "directory": directory,
                "description": "Architecture review task",
                "expected_output": "Review of infrastructure design"
            }],
            context_vars=["directory"],
            tools=[
                self.architect.tools[0],  # analyze_architecture
                self.architect.tools[1],  # review_design
                self.architect.tools[2],  # suggest_improvements
                self.architect.tools[3]   # check_scalability
            ]
        )
        
        # Create crew for analysis
        crew = Crew(
            agents=[self.terraform_expert, self.architect],
            tasks=[terraform_task, architect_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Run analysis
        result = crew.kickoff()
        return {"analysis": result}
    
    def generate_summary(self, analysis: Dict[str, Any]) -> str:
        """Generate a summary of the analysis results"""
        if not analysis:
            return "No analysis available"
        return analysis.get("analysis", "No analysis available")
