import click

@click.group()
def cli():
    """Cloud Builder CLI tool"""
    pass

@cli.command()
@click.argument('text', nargs=-1)
def print(text):
    """Print the given text"""
    click.echo(' '.join(text))

if __name__ == '__main__':
    cli()
