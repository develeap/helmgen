import click
from helmgen.bs.backend_service_adapter import BackendServiceAdapter
from helmgen.bs.parser import Parser


@click.group()
def apply():
    """Apply the generated objects"""
    pass


@apply.command()
@click.option("--value-file", required=True, help="cluster endpoint")
def apply(value_file):
    """apply helm on cluster"""
    parser = Parser(value_file)
    print(parser.read_file())
