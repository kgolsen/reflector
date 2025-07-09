# reflector

This package provides utilities for inspecting SQL databases and generating
REST API definitions.  The current focus is on introspecting PostgreSQL
schemas and producing a structured representation of the tables, columns,
primary keys and foreign key relationships.

The `reflect` CLI exposes an `inspect` subcommand that outputs the detected
structure as JSON given a SQLAlchemy connection URL.
