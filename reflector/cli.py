"""Reflector OpenAPI generator

This script uses SQLAlchemy's reflection capabilities to auto-generate OpenAPI
specifications and implement simple REST CRUD API endpoints for the discovered
relations.
"""

import click


@click.group()
def reflect():
    pass


@reflect.command()
def config():
    pass


@reflect.command()
def inspect(**kwargs):
    pass


@reflect.command()
def emit(**kwargs):
    pass


@reflect.command()
def implement(**kwargs):
    pass


if __name__ == '__main__':
    reflect()
