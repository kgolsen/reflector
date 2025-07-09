import json
import click

from .introspector import Introspector


@click.group()
def cli():
    """Utilities for working with database schemas."""


@cli.command()
@click.option('--url', required=True, help='SQLAlchemy database URL')
def inspect(url):
    """Output database structure as JSON."""
    inspector = Introspector(url)
    schema = inspector.introspect()
    click.echo(json.dumps(schema, default=lambda o: o.__dict__, indent=2))


if __name__ == '__main__':
    cli()
