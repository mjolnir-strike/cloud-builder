"""Task definitions for infrastructure analysis"""
from typing import Dict, Any
from crewai import Task

def get_analysis_task(directory: str, agent: Any) -> Task:
    """Get task for analyzing Terraform code"""
    return Task(
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
        agent=agent
    )

def get_review_task(agent: Any) -> Task:
    """Get task for reviewing infrastructure design"""
    return Task(
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
        agent=agent
    )
