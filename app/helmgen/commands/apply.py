import click
from helmgen.bs.backend_service_adapter import BackendServiceAdapter
from helmgen.bs.parser import Parser

@click.group()
def apply():
    """ something Backend Service related commands"""
    pass

@apply.command()
@click.option('--value-file',
                required=True,
                help='cluster endpoint')
def apply(value_file):
    """ apply helm on cluster """
    bs_adapter = BackendServiceAdapter(value_file)
    parser = Parser(value_file)

    print(parser.read_file())
    
    
