import click
from typing import Optional
from .agents import AgentFactory
import os
import glob
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def _contains_terraform_files(directory: str) -> bool:
    """Check if directory contains Terraform files"""
    tf_files = glob.glob(os.path.join(directory, "**/*.tf"), recursive=True)
    return len(tf_files) > 0

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
        # Ensure OpenAI API key is set
        if not os.getenv('OPENAI_API_KEY'):
            raise click.ClickException(
                "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable "
                "or add it to your .env file."
            )

        # Validate directory contains Terraform files
        if not _contains_terraform_files(directory):
            raise click.ClickException(
                f"No Terraform files (*.tf) found in {directory}. "
                "Please provide a directory containing Terraform code."
            )

        # Create and run the appropriate agent
        agent_instance = AgentFactory.create_agent(agent)
        analysis = agent_instance.analyze_terraform(directory)
        click.echo(agent_instance.generate_summary(analysis))
    except Exception as e:
        click.echo(f"Error analyzing directory: {str(e)}")
        raise click.Abort()

if __name__ == '__main__':
    cli()
