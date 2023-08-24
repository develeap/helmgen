import click
from helmgen.bs.backend_service_adapter import BackendServiceAdapter
from helmgen.bs.parser import Parser

@click.group()
def template():
    """ template the generated objects """
    pass
