from typing import Dict, Any, List
from crewai import Task
from ..tools.read_terraform import read_terraform_files

def analyze_costs(directory: str) -> Dict[str, Any]:
    """Analyze cost implications in Terraform code
    
    Args:
        directory: Path to directory containing Terraform code
        
    Returns:
        Dictionary containing cost analysis results
    """
    # Read Terraform files
    files = read_terraform_files(directory)
    
    # Analyze each file for cost concerns
    findings = []
    for file in files:
        findings.extend(_analyze_file_costs(file))
    
    return {
        'findings': findings,
        'file_count': len(files)
    }

def _analyze_file_costs(file: Dict[str, str]) -> List[Dict[str, Any]]:
    """Analyze cost implications in a single file
    
    Args:
        file: Dictionary containing file path and content
        
    Returns:
        List of cost findings
    """
    findings = []
    content = file['content'].lower()
    path = file['path']
    
    # Check for common cost-related patterns
    if 'instance_type' in content:
        findings.append({
            'severity': 'INFO',
            'file': path,
            'issue': 'Instance type configuration detected',
            'recommendation': 'Review instance sizing for cost optimization'
        })
    
    if 'retention' in content:
        findings.append({
            'severity': 'INFO',
            'file': path,
            'issue': 'Data retention configuration found',
            'recommendation': 'Review retention periods for cost efficiency'
        })
    
    if 'backup' in content:
        findings.append({
            'severity': 'INFO',
            'file': path,
            'issue': 'Backup configuration detected',
            'recommendation': 'Review backup frequency and retention'
        })
    
    # Check for potential cost optimizations
    if 'auto_scaling' not in content and ('instance' in content or 'cluster' in content):
        findings.append({
            'severity': 'MEDIUM',
            'file': path,
            'issue': 'No auto-scaling configuration found',
            'recommendation': 'Consider adding auto-scaling for cost optimization'
        })
    
    if 'lifecycle' not in content:
        findings.append({
            'severity': 'LOW',
            'file': path,
            'issue': 'No lifecycle rules found',
            'recommendation': 'Consider adding lifecycle rules for resource cleanup'
        })
    
    return findings
