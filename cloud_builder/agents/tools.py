"""Tools for analyzing Terraform code"""
from typing import List, Dict, Any
from functools import wraps
from crewai import tools
import glob
import os

def bind_tool(func):
    """Decorator to ensure tool methods are properly bound"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except TypeError as e:
            if "missing 1 required positional argument: 'self'" in str(e):
                raise RuntimeError(
                    f"Tool method {func.__name__} not properly bound to instance. "
                    "Make sure to initialize TerraformTools as an instance variable."
                ) from e
            raise
    return wrapper

class TerraformTools:
    """Tools for analyzing Terraform code"""

    @bind_tool
    @tools.tool("Read Terraform files from a directory")
    def read_terraform_files(self, directory: str) -> List[Dict[str, Any]]:
        """Read and parse Terraform files from a directory"""
        files = []
        if os.path.exists(directory):
            for tf_file in glob.glob(os.path.join(directory, "**/*.tf"), recursive=True):
                try:
                    with open(tf_file, 'r') as f:
                        files.append({
                            'path': tf_file,
                            'content': f.read()
                        })
                except Exception as e:
                    print(f"Error reading file {tf_file}: {e}")
        return files

    @bind_tool
    @tools.tool("Analyze security configurations in Terraform code")
    def analyze_security(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze security configurations in Terraform files"""
        findings = {
            'iam': [],
            'network': [],
            'encryption': [],
            'access': []
        }
        return findings

    @bind_tool
    @tools.tool("Check infrastructure code against best practices")
    def check_best_practices(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Check Terraform files against best practices"""
        findings = {
            'modularity': [],
            'naming': [],
            'variables': [],
            'state': []
        }
        return findings

    @bind_tool
    @tools.tool("Analyze and optimize infrastructure costs")
    def optimize_costs(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze cost optimization opportunities in Terraform files"""
        findings = {
            'compute': [],
            'storage': [],
            'network': [],
            'unused': []
        }
        return findings

    @bind_tool
    @tools.tool("Analyze infrastructure architecture and design")
    def analyze_architecture(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze infrastructure architecture in Terraform files"""
        findings = {
            'components': [],
            'relationships': [],
            'patterns': []
        }
        return findings

    @bind_tool
    @tools.tool("Review infrastructure design patterns")
    def review_design(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Review infrastructure design in Terraform files"""
        findings = {
            'modularity': [],
            'reusability': [],
            'maintainability': []
        }
        return findings

    @bind_tool
    @tools.tool("Suggest infrastructure improvements")
    def suggest_improvements(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Suggest improvements for Terraform infrastructure"""
        suggestions = {
            'security': [],
            'performance': [],
            'cost': [],
            'maintainability': []
        }
        return suggestions

    @bind_tool
    @tools.tool("Check infrastructure scalability patterns")
    def check_scalability(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Check scalability configurations in Terraform files"""
        findings = {
            'compute': [],
            'storage': [],
            'network': []
        }
        return findings
