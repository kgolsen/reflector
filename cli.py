"""Reflector OpenAPI generator

This script uses SQLAlchemy's reflection capabilities to auto-generate OpenAPI
specifications and implement simple REST CRUD API endpoints for the discovered
relations.
"""

import click

from db import Reflector


@click.group()
@click.option('--sql-driver', help='SQL driver to use for connections (currently only Postgres)')
@click.option('-a', '--host', required=True, help='DB hostname')
@click.option('-p', '--port', required=True, type=int, help='DB listener port')
@click.option('-u', '--user', required=True, help='username to connect as')
@click.option('-P', '--password', required=True, prompt=True, hide_input=True,
              confirmation_prompt=True, help='DB user password')
@click.option('-d', '--database', required=True, help='DB to reflect')
@click.pass_context
def reflect(ctx, host, port, user, password, database, sql_driver):
    if sql_driver is None:
        sql_driver = 'postgres'
    ctx.obj = {
        'host': host,
        'port': port,
        'user': user,
        'password': password,
        'database': database,
        'sql_driver': sql_driver,
    }


@reflect.command()
@click.pass_obj
def inspect(config):
    """run reflection on target schema"""
    print(f"DEBUG: running cli.inspect with config: {config}")
    r = Reflector(**config)
    print(f"DEBUG: built Reflector: {r}")
    r.reflect()
    for table_name, table in r.tables.items():
        print(f"Found table {table_name} with {len(table['columns'])} columns, "
              f"{len(table['foreign_keys'])} foreign keys")
    for view_name, view in r.views.items():
        print(f"Found view {view_name} with {len(view['columns'])} columns")


@reflect.command()
@click.option('-o', '--output', type=str, help='file to write spec to')
def emit(**kwargs):
    """build OpenAPI spec"""
    pass


@reflect.command()
@click.pass_obj
def implement(**kwargs):
    """build REST API"""
    pass


@reflect.command()
def run(**kwargs):
    """inspect, emit, implement"""
    pass


if __name__ == '__main__':
    reflect()
