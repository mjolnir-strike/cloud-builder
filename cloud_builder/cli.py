"""CLI for cloud-builder"""
import os
import click
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from .agents.crew_agent import CrewAgent
import sys

def find_terraform_files(directory: str) -> List[str]:
    """Find Terraform files in directory
    
    Args:
        directory: Directory to search
        
    Returns:
        List of Terraform files
    """
    terraform_files = []
    for path in Path(directory).rglob('*.tf'):
        terraform_files.append(str(path.relative_to(directory)))
    return terraform_files

@click.group()
def cli():
    """Cloud Builder CLI"""
    # Load environment variables
    load_dotenv()
    pass

@cli.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def analyze(directory: str):
    """Analyze Terraform code in directory"""
    try:
        # Find Terraform files
        terraform_files = find_terraform_files(directory)
        if not terraform_files:
            click.echo("No Terraform files found")
            sys.exit(1)
        
        click.echo("Found {} Terraform-related files:".format(len(terraform_files)))
        for file in terraform_files:
            click.echo(f"  - {file}")
        click.echo()
        
        # Get model from environment
        model = os.getenv('OLLAMA_MODEL', 'qwen2.5')
        click.echo(f"Using Ollama model {model} for analysis")
        
        # Create agent and run analysis
        agent = CrewAgent(directory)
        results = agent.analyze()
        
        # Print results
        click.echo("\nSecurity Analysis:")
        click.echo("-" * 20)
        click.echo(results['security_analysis'])
        
        click.echo("\nCost Analysis:")
        click.echo("-" * 20)
        click.echo(results['cost_analysis'])
        
    except ValueError as e:
        click.echo(f"Configuration error: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error analyzing directory: {str(e)}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli()
