import click
from helmgen.bs.backend_service_adapter import BackendServiceAdapter

@click.group()
def generate():
    """ something Backend Service related commands"""
    pass

@generate.command()
@click.option('--option',
                required=True,
                help='cluster endpoint')
def generate(option):
    """ generate helm on cluster """
    bs_adapter = BackendServiceAdapter(option)
    bs_adapter.demo()
    
