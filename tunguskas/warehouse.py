from pathlib import Path

import duckdb

from tunguskas.paths import WAREHOUSE_PATH


def get_connection(read_only: bool = False) -> duckdb.DuckDBPyConnection:
    return duckdb.connect(str(WAREHOUSE_PATH), read_only=read_only)


def run_sql_file(conn: duckdb.DuckDBPyConnection, path: Path) -> None:
    with open(path, "r", encoding="utf-8") as f:
        conn.execute(f.read())
