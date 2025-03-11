"""Tools for analyzing Terraform code"""
from typing import List, Dict, Any
from crewai import tools
import glob
import os

class TerraformTools:
    """Tools for analyzing Terraform code"""

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

    @tools.tool("Analyze infrastructure architecture and design")
    def analyze_architecture(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze infrastructure architecture in Terraform files"""
        findings = {
            'components': [],
            'relationships': [],
            'patterns': []
        }
        return findings

    @tools.tool("Review infrastructure design patterns")
    def review_design(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Review infrastructure design in Terraform files"""
        findings = {
            'modularity': [],
            'reusability': [],
            'maintainability': []
        }
        return findings

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

    @tools.tool("Check infrastructure scalability patterns")
    def check_scalability(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Check scalability configurations in Terraform files"""
        findings = {
            'compute': [],
            'storage': [],
            'network': []
        }
        return findings
