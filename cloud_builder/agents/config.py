"""LLM and Agent Configuration"""
import os
from typing import Dict, Any
from crewai.agent import Agent
from litellm import completion

def get_llm_config() -> Dict[str, Any]:
    """Get LLM configuration based on environment"""
    env = os.getenv('ENVIRONMENT', 'prod').lower()
    timeout = int(os.getenv('ANALYSIS_TIMEOUT', '300'))
    
    if env == 'dev':
        # Use local Ollama in development
        if not os.getenv('OLLAMA_HOST'):
            raise ValueError("OLLAMA_HOST must be set in development environment")
        if not os.getenv('OLLAMA_MODEL'):
            raise ValueError("OLLAMA_MODEL must be set in development environment")
            
        return {
            "config_list": [{
                "model": f"ollama/{os.getenv('OLLAMA_MODEL')}",
                "api_base": os.getenv('OLLAMA_HOST'),
                "api_type": "ollama",
                "api_key": "not-needed"  # Ollama doesn't need an API key
            }],
            "temperature": 0.1,  # Lower temperature for more focused responses
            "request_timeout": timeout
        }
    else:
        # Use OpenAI in production
        if not os.getenv('OPENAI_API_KEY'):
            raise ValueError("OPENAI_API_KEY must be set in production environment")
            
        return {
            "config_list": [{
                "model": "gpt-4",
                "api_key": os.getenv('OPENAI_API_KEY')
            }],
            "temperature": 0.1,
            "request_timeout": timeout
        }

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
            'allow_delegation': False,
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
            'allow_delegation': False,
            'verbose': True
        }
    }
    return configs.get(role, {})
