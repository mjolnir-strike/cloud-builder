"""Configuration for agents and LLM"""
from typing import Dict, Any
from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI
import os

def get_llm_config() -> Dict[str, Any]:
    """Get LLM configuration based on model type
    
    Returns:
        LLM configuration and instance
    """
    model = os.getenv('OLLAMA_MODEL', 'llama3.2')
    
    # Configure model settings based on type
    if model == 'gpt-4o-mini':
        # Use OpenAI for GPT-4-0-mini
        llm = ChatOpenAI(
            model='gpt-4o-mini',
            temperature=0.1,  # More precise for analysis
            request_timeout=600  # Longer timeout for complex analysis
        )
    else:
        # Use Ollama for other models
        base_url = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        llm = OllamaLLM(
            model=model,
            base_url=base_url,
            temperature=0.2,  # Default for other models
            request_timeout=int(os.getenv('ANALYSIS_TIMEOUT', '300'))
        )
    
    return llm

def get_agent_config(role: str) -> dict:
    """Get agent configuration
    
    Args:
        role: Agent role (security_expert, cost_expert)
        
    Returns:
        Agent configuration
    """
    # Get LLM instance
    llm = get_llm_config()
    
    # Base configuration
    base_config = {
        'llm': llm,
        'verbose': True,
        'allow_delegation': False,
        'memory': False
    }
    
    # Role-specific configurations
    configs = {
        'security_expert': {
            **base_config,
            'role': 'Security Expert',
            'goal': 'Provide a single, comprehensive security analysis of Terraform code and stop',
            'backstory': (
                'You are a cloud security expert who performs focused, one-time security assessments. '
                'You analyze infrastructure code for security best practices, identify vulnerabilities, '
                'and provide clear, actionable recommendations. You focus on provider-agnostic patterns '
                'and deliver a single, comprehensive report.'
            )
        },
        'cost_expert': {
            **base_config,
            'role': 'Cost Expert',
            'goal': 'Provide a single, comprehensive cost analysis of Terraform code and stop',
            'backstory': (
                'You are a cloud cost optimization expert who performs focused, one-time cost assessments. '
                'You analyze infrastructure code for cost-saving opportunities, resource efficiency, '
                'and provide clear, actionable recommendations. You focus on provider-agnostic patterns '
                'and deliver a single, comprehensive report.'
            )
        }
    }
    
    return configs.get(role, {})
