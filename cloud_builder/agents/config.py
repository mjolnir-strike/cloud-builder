"""LLM and Agent Configuration"""
import os
from typing import Dict, Any
from crewai.agent import Agent
from langchain_ollama import OllamaLLM

def get_llm_config() -> OllamaLLM:
    """Get LLM configuration for Ollama"""
    # Validate required environment variables
    if not os.getenv('OLLAMA_HOST'):
        raise ValueError("OLLAMA_HOST must be set (e.g. http://localhost:11434)")
    if not os.getenv('OLLAMA_MODEL'):
        raise ValueError("OLLAMA_MODEL must be set (e.g. qwen2.5-coder)")
    
    return OllamaLLM(
        model=f"ollama/{os.getenv('OLLAMA_MODEL')}",  # Specify provider
        base_url=os.getenv('OLLAMA_HOST'),
        temperature=0.1,
        timeout=int(os.getenv('ANALYSIS_TIMEOUT', '300'))
    )

def get_agent_config(role: str) -> Dict[str, Any]:
    """Get agent configuration by role"""
    configs = {
        'terraform_expert': {
            'role': 'Infrastructure Expert',
            'goal': 'Analyze Terraform code for best practices and security',
            'backstory': """Senior DevOps engineer with expertise in infrastructure as code.
            Specializes in:
            - Infrastructure best practices
            - Security configurations
            - Resource management
            - Cost optimization""",
            'memory': True,  # Enable memory for better context retention
            'max_iterations': 3,  # Limit iterations for focused analysis
            'verbose': True
        },
        'solution_architect': {
            'role': 'Solution Architect',
            'goal': 'Review infrastructure design and suggest improvements',
            'backstory': """Cloud architect specializing in infrastructure design.
            Expert in:
            - Infrastructure architecture
            - Security best practices
            - Resource organization
            - Cost optimization""",
            'memory': True,  # Enable memory for better context retention
            'max_iterations': 3,  # Limit iterations for focused analysis
            'verbose': True
        }
    }
    return configs.get(role, {})
