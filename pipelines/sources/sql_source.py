from __future__ import annotations

from dlt.sources.sql_database import sql_database


def build_sql_database_source(source_dsn: str, table_names: list[str]):
    return sql_database(source_dsn, table_names=table_names)
