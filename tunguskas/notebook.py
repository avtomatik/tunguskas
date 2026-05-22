import duckdb

from tunguskas.paths import WAREHOUSE_PATH


def get_dataframe(query: str):
    conn = duckdb.connect(str(WAREHOUSE_PATH))
    return conn.execute(query).df()
