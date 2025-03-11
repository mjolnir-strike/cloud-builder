"""Configuration for agents and LLM"""
from typing import Dict, Any
from langchain_ollama import OllamaLLM
import os

def get_llm_config() -> Dict[str, Any]:
    """Get LLM configuration for Ollama
    
    Returns:
        LLM configuration
    """
    model = os.getenv('OLLAMA_MODEL', 'llama3.2')
    base_url = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    
    # Configure model settings based on type
    if model == 'gpt-4-0-mini':
        temperature = 0.1  # More precise for analysis
        timeout = 600     # Longer timeout for complex analysis
    else:
        temperature = 0.2  # Default for other models
        timeout = 300     # Default timeout
    
    return {
        'model': f"ollama/{model}",  # Specify ollama as the provider
        'base_url': base_url,
        'temperature': temperature,
        'request_timeout': int(os.getenv('ANALYSIS_TIMEOUT', str(timeout)))
    }

def get_agent_config(role: str) -> dict:
    """Get agent configuration
    
    Args:
        role: Agent role (security_expert, cost_expert)
        
    Returns:
        Agent configuration
    """
    # Get LLM configuration
    llm_config = get_llm_config()
    
    # Base configuration
    base_config = {
        'llm': OllamaLLM(**llm_config),
        'verbose': True,
        'allow_delegation': False,
        'memory': False
    }
    
    # Role-specific configurations
    configs = {
        'security_expert': {
            **base_config,
            'role': 'Security Expert',
            'goal': 'Analyze Terraform code for security vulnerabilities and best practices',
            'backstory': 'You are a cloud security expert with deep knowledge of infrastructure security best practices. Your task is to identify potential security issues and suggest improvements in IAM configurations, network security, data protection, and compliance.'
        },
        'cost_expert': {
            **base_config,
            'role': 'Cost Expert',
            'goal': 'Analyze Terraform code for cost optimization opportunities',
            'backstory': 'You are a cloud cost optimization expert with experience in identifying cost-saving opportunities. Your task is to review resource sizing, retention policies, backup configurations, and suggest cost-effective alternatives.'
        }
    }
    
    return configs.get(role, {})
