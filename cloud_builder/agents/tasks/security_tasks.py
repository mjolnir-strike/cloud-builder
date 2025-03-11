"""Security analysis tasks for Terraform code"""
from typing import Dict, Any, List
from crewai import Task
from ..tools.read_terraform import read_terraform_files

def analyze_security(directory: str) -> Dict[str, Any]:
    """Analyze security configurations in Terraform code
    
    Args:
        directory: Path to directory containing Terraform code
        
    Returns:
        Dictionary containing security analysis results
    """
    # Read Terraform files
    files = read_terraform_files(directory)
    
    # Analyze each file for security concerns
    findings = []
    for file in files:
        findings.extend(_analyze_file_security(file))
    
    return {
        'findings': findings,
        'file_count': len(files)
    }

def _analyze_file_security(file: Dict[str, str]) -> List[Dict[str, Any]]:
    """Analyze security configuration in a single file
    
    Args:
        file: Dictionary containing file path and content
        
    Returns:
        List of security findings
    """
    findings = []
    content = file['content'].lower()
    path = file['path']
    
    # Check for common security issues
    if 'public_access' in content:
        findings.append({
            'severity': 'HIGH',
            'file': path,
            'issue': 'Public access may be enabled',
            'recommendation': 'Review and restrict public access settings'
        })
    
    if '*' in content and ('allow' in content or 'policy' in content):
        findings.append({
            'severity': 'HIGH',
            'file': path,
            'issue': 'Overly permissive IAM policy detected',
            'recommendation': 'Use principle of least privilege'
        })
    
    if 'encryption' in content and ('false' in content or 'disabled' in content):
        findings.append({
            'severity': 'HIGH',
            'file': path,
            'issue': 'Encryption may be disabled',
            'recommendation': 'Enable encryption for sensitive data'
        })
    
    return findings
