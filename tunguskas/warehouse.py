import duckdb

from tunguskas.paths import WAREHOUSE_PATH


def get_connection() -> duckdb.DuckDBPyConnection:
    return duckdb.connect(str(WAREHOUSE_PATH))


def run_sql_file(conn, path):
    with open(path, "r", encoding="utf-8") as f:
        conn.execute(f.read())
