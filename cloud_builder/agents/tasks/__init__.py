"""Tasks for Terraform analysis"""
from .security_tasks import analyze_security
from .cost_tasks import analyze_costs

__all__ = [
    'analyze_security',
    'analyze_costs'
]
