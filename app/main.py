#!/usr/bin/env python

import click
from helmgen.commands.apply import apply
from helmgen.commands.generate import generate
from helmgen.commands.template import template


import logging

@click.group()
def main():
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

main.add_command(apply)
main.add_command(generate)
main.add_command(template)



if __name__ == '__main__':
    main()
