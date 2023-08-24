import click
from helmgen.bs.backend_service_adapter import BackendServiceAdapter

@click.group()
def template():
    """ something Backend Service related commands"""
    pass

@template.command()
@click.option('--option',
                required=True,
                help='cluster endpoint')
def template(option):
    """ template helm on cluster """
    bs_adapter = BackendServiceAdapter(option)
    bs_adapter.demo()
    
