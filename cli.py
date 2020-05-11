"""Reflector OpenAPI generator

This script uses SQLAlchemy's reflection capabilities to auto-generate OpenAPI
specifications and implement simple REST CRUD API endpoints for the discovered
relations.
"""

import click

from db import Reflector, DEPENDENT_ONLY


@click.group()
@click.option('--sql-driver', help='SQL driver to use for connections (currently only Postgres)')
@click.option('-a', '--host', required=True, help='DB hostname')
@click.option('-p', '--port', required=True, type=int, help='DB listener port')
@click.option('-u', '--user', required=True, help='username to connect as')
@click.option('-P', '--password', required=True, prompt=True, hide_input=True,
              confirmation_prompt=True, help='DB user password')
@click.option('-d', '--database', required=True, help='DB to reflect')
@click.pass_context
def context(ctx, host, port, user, password, database, sql_driver):
    if sql_driver is None:
        sql_driver = 'postgres'
    context_dict = {
        'host': host,
        'port': port,
        'user': user,
        'password': password,
        'database': database,
        'sql_driver': sql_driver,
    }
    reflector = Reflector(**context_dict)
    context_dict['reflector'] = reflector
    ctx.obj = context_dict


@context.command()
@click.pass_context
def inspect(ctx, **kwargs):
    """run reflection on target schema"""
    print(f"DEBUG: running cli.inspect with config: {ctx}")
    print(f"DEBUG: running Reflector")
    r = ctx.obj['reflector']
    r.reflect()
    for table_name, table in r.get_tables():
        print(f"Found table {table_name} with {len(table['columns'])} columns, "
              f"{len(table['foreign_keys'])} foreign keys")
    for view_name, view in r.get_views():
        print(f"Found view {view_name} with {len(view['columns'])} columns")


@context.command()
@click.pass_context
@click.option('-o', '--spec-output', type=str, help='file to write spec to')
def emit(ctx, spec_output, **kwargs):
    """build OpenAPI spec"""
    ctx.forward(inspect)
    # TODO: emit stuff...
    pass


@context.command()
@click.pass_context
@click.option('-o', '--spec-output', type=str, help='file to write spec to')
@click.option('-O', '--impl-output', type=str, help='file to write implementation to')
def implement(ctx, spec_output, impl_output, **kwargs):
    """build REST API"""
    ctx.forward(emit)
    # TODO: implement stuff...
    pass


@context.command()
def run(**kwargs):
    """inspect, emit, implement"""
    pass


if __name__ == '__main__':
    context()
