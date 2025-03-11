import click
from typing import Optional, List
from .agents import AgentFactory
import os
import glob
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def _find_terraform_files(directory: str) -> List[str]:
    """Find all Terraform files in directory"""
    patterns = [
        "**/*.tf",           # Terraform files
        "**/variables.tf",   # Variable definitions
        "**/outputs.tf",     # Output definitions
        "**/terraform.tfvars",  # Variable values
        "**/modules/**/*/",  # Module directories
    ]
    
    files = []
    for pattern in patterns:
        files.extend(glob.glob(os.path.join(directory, pattern), recursive=True))
    return list(set(files))  # Remove duplicates

def _contains_terraform_files(directory: str) -> bool:
    """Check if directory contains Terraform files"""
    return len(_find_terraform_files(directory)) > 0

def _validate_environment() -> None:
    """Validate environment configuration"""
    env = os.getenv('ENVIRONMENT', 'prod').lower()
    
    if env == 'dev':
        # Validate Ollama configuration
        if not os.getenv('OLLAMA_HOST'):
            raise click.ClickException(
                "OLLAMA_HOST must be set in development environment. "
                "Please set it in your .env file."
            )
        if not os.getenv('OLLAMA_MODEL'):
            raise click.ClickException(
                "OLLAMA_MODEL must be set in development environment. "
                "Please set it in your .env file."
            )
        click.echo(f"Using Ollama model {os.getenv('OLLAMA_MODEL')} for analysis")
    else:
        # Validate OpenAI configuration
        if not os.getenv('OPENAI_API_KEY'):
            raise click.ClickException(
                "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable "
                "or add it to your .env file."
            )
        click.echo("Using OpenAI for analysis")

@click.group()
def cli():
    """Cloud Builder CLI for analyzing infrastructure code"""
    pass

@cli.command()
@click.argument('text', nargs=-1)
def print(text):
    """Print the provided text"""
    click.echo(' '.join(text))

@cli.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--agent', type=click.Choice(['crew', 'langchain']), default='crew',
              help='Agent to use for analysis (default: crew)')
def analyze(directory: str, agent: str):
    """Analyze Terraform code in the specified directory"""
    try:
        # Validate environment configuration
        _validate_environment()

        # Validate directory contains Terraform files
        tf_files = _find_terraform_files(directory)
        if not tf_files:
            raise click.ClickException(
                f"No Terraform files found in {directory}. "
                "Please provide a directory containing Terraform code."
            )

        # Log found Terraform files
        click.echo(f"Found {len(tf_files)} Terraform-related files:")
        for file in sorted(tf_files):
            click.echo(f"  - {os.path.relpath(file, directory)}")
        click.echo()

        # Create and run the appropriate agent
        agent_instance = AgentFactory.create_agent(agent)
        analysis = agent_instance.analyze_terraform(directory)
        click.echo(agent_instance.generate_summary(analysis))
    except Exception as e:
        click.echo(f"Error analyzing directory: {str(e)}")
        raise click.Abort()

if __name__ == '__main__':
    cli()
