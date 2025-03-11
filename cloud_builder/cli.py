"""CLI for cloud-builder"""
import os
import click
from typing import Optional
from .agents.crew_agent import CrewAgent
from dotenv import load_dotenv

@click.group()
def cli():
    """Cloud Builder CLI"""
    # Load environment variables
    load_dotenv()
    pass

@cli.command()
@click.argument('directory', type=click.Path(exists=True))
@click.option('--agent', type=click.Choice(['crew', 'langchain']), default='crew', help='Agent type to use')
def analyze(directory: str, agent: Optional[str] = 'crew'):
    """Analyze Terraform code in directory"""
    # Find Terraform files
    tf_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.tf') or file.endswith('.tfvars'):
                tf_files.append(os.path.join(root, file))
    
    if not tf_files:
        click.echo('No Terraform files found in directory')
        return
    
    # Display found files
    click.echo('Found {} Terraform-related files:'.format(len(tf_files)))
    for file in tf_files:
        click.echo('  - {}'.format(os.path.basename(file)))
    click.echo()

    # Display model being used
    model = os.getenv('OLLAMA_MODEL', 'llama3.2')
    click.echo(f'Using Ollama model {model} for analysis\n')

    # Run analysis
    try:
        if agent == 'crew':
            agent = CrewAgent(directory)
            result = agent.analyze()
            
            # Parse and display the analysis results
            if isinstance(result['analysis'], str):
                # Find the final answers in the output
                security_analysis = ""
                cost_analysis = ""
                
                # Extract security analysis
                if "Security Expert\n## Final Answer:" in result['analysis']:
                    security_analysis = result['analysis'].split("Security Expert\n## Final Answer:")[1].split("Cost Expert")[0].strip()
                
                # Extract cost analysis
                if "Cost Expert\n## Final Answer:" in result['analysis']:
                    cost_analysis = result['analysis'].split("Cost Expert\n## Final Answer:")[1].split("[")[0].strip()
                
                # Display security analysis
                if security_analysis:
                    click.echo('\nSecurity Analysis')
                    click.echo('-----------------')
                    click.echo(security_analysis)
                
                # Display cost analysis
                if cost_analysis:
                    click.echo('\nCost Analysis')
                    click.echo('-------------')
                    click.echo(cost_analysis)
            else:
                click.echo('\nAnalysis Results')
                click.echo('----------------')
                click.echo(str(result['analysis']))
        else:
            click.echo('LangChain agent not yet implemented')
    except Exception as e:
        click.echo(f'Error analyzing directory: {str(e)}')

if __name__ == '__main__':
    cli()
