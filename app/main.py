#!/usr/bin/env python

import click
from cet.commands.backend_service import bs
from cet.commands.octopus import octopus
import logging

@click.group()
def main():
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

main.add_command(bs)
main.add_command(octopus)

if __name__ == '__main__':
    main()
