"""Base task classes for Terraform analysis"""
from typing import Dict, Any, List
from ..tools.read_terraform import read_terraform_files

class BaseTask:
    """Base class for all Terraform analysis tasks"""
    
    def _read_files(self, directory: str) -> List[Dict[str, Any]]:
        """Read Terraform files from directory
        
        Args:
            directory: Path to directory containing Terraform code
            
        Returns:
            List of dictionaries containing file paths and contents
        """
        return read_terraform_files(directory)
