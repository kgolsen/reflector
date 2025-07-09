from dataclasses import dataclass, field
from typing import Dict, List, Optional

from sqlalchemy import create_engine, inspect


@dataclass
class ColumnSchema:
    name: str
    type: str
    nullable: bool
    default: Optional[str]


@dataclass
class ForeignKeySchema:
    constrained_columns: List[str]
    referred_table: str
    referred_columns: List[str]


@dataclass
class TableSchema:
    name: str
    columns: List[ColumnSchema] = field(default_factory=list)
    primary_key: List[str] = field(default_factory=list)
    foreign_keys: List[ForeignKeySchema] = field(default_factory=list)


@dataclass
class DatabaseSchema:
    tables: Dict[str, TableSchema] = field(default_factory=dict)


class Introspector:
    """Read database metadata using SQLAlchemy."""

    def __init__(self, url: str):
        self.engine = create_engine(url)
        self.inspector = inspect(self.engine)

    def introspect(self) -> DatabaseSchema:
        schema = DatabaseSchema()
        for table_name in self.inspector.get_table_names():
            columns = []
            for c in self.inspector.get_columns(table_name):
                columns.append(
                    ColumnSchema(
                        name=c["name"],
                        type=str(c["type"]),
                        nullable=c.get("nullable", True),
                        default=str(c.get("default")) if c.get("default") is not None else None,
                    )
                )
            pk = self.inspector.get_pk_constraint(table_name).get("constrained_columns", [])
            fks = []
            for fk in self.inspector.get_foreign_keys(table_name):
                fks.append(
                    ForeignKeySchema(
                        constrained_columns=fk.get("constrained_columns", []),
                        referred_table=fk.get("referred_table"),
                        referred_columns=fk.get("referred_columns", []),
                    )
                )
            schema.tables[table_name] = TableSchema(
                name=table_name,
                columns=columns,
                primary_key=list(pk),
                foreign_keys=fks,
            )
        return schema
