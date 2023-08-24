#!/usr/bin/env python

import click
from helmgen.commands.apply import apply

import logging

@click.group()
def main():
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

main.add_command(apply)

if __name__ == '__main__':
    main()
