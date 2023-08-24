import click
from helmgen.bs.backend_service_adapter import BackendServiceAdapter
from helmgen.bs.parser import Parser

@click.group()
def apply():
    """ Apply the generated objects """
    pass

@apply.command()
@click.argument('value_file')
def apply(value_file):
    """ apply helm on cluster """
    bs_adapter = BackendServiceAdapter(value_file)
    parser = Parser(value_file)
    print(parser.read_file())
