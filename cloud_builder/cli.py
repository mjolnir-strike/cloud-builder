import click
from typing import Optional
from .agents.base import AgentFactory

@click.group()
def cli():
    """Cloud Builder CLI tool"""
    pass

@cli.command()
@click.argument('text', nargs=-1)
def print(text):
    """Print the given text"""
    click.echo(' '.join(text))

@cli.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--agent', type=click.Choice(['crew', 'langchain']), default='crew', help='Agent type to use for analysis')
def analyze(directory: str, agent: str):
    """Analyze Terraform code in the specified directory"""
    try:
        agent_instance = AgentFactory.create_agent(agent)
        analysis = agent_instance.analyze_terraform(directory)
        click.echo(agent_instance.generate_summary(analysis))
    except Exception as e:
        click.echo(f"Error analyzing directory: {e}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    cli()
