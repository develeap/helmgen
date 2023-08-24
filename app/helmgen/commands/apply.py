import click
from helmgen.bs.backend_service_adapter import BackendServiceAdapter

@click.group()
def apply():
    """ something Backend Service related commands"""
    pass

@apply.command()
@click.option('--cluster',
                required=True,
                help='cluster endpoint')
@click.option('--value-file',
                required=True,
                help='cluster endpoint')
def apply(cluster, value_file):
    """ apply helm on cluster """
    bs_adapter = BackendServiceAdapter(cluster, value_file)
    
