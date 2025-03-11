import click
from typing import Optional
from .agents import AgentFactory
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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

        # Create and run the appropriate agent
        agent_instance = AgentFactory.create_agent(agent)
        analysis = agent_instance.analyze_terraform(directory)
        click.echo(agent_instance.generate_summary(analysis))
    except Exception as e:
        click.echo(f"Error analyzing directory: {str(e)}")
        raise click.Abort()

if __name__ == '__main__':
    cli()
