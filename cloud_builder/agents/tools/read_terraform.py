"""Tool for reading Terraform files"""
import os
from typing import List
from pathlib import Path
from crewai import tools

@tools.tool("Read Terraform files from directory")
def read_terraform_files(directory: str) -> List[str]:
    """Read Terraform files from directory
    
    Args:
        directory: Directory containing Terraform files
        
    Returns:
        List of file contents
    """
    contents = []
    
    # Find all .tf files
    for path in Path(directory).rglob('*.tf'):
        try:
            with open(path, 'r') as f:
                contents.append({
                    'file': str(path.relative_to(directory)),
                    'content': f.read()
                })
        except Exception as e:
            print(f"Error reading {path}: {e}")
    
    if not contents:
        return ["No Terraform files found"]
    
    # Format contents for analysis
    formatted_contents = []
    for item in contents:
        formatted_contents.append(
            f"File: {item['file']}\n"
            f"Content:\n{item['content']}\n"
            f"{'-' * 80}\n"
        )
    
    return formatted_contents
