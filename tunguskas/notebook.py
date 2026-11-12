import pandas as pd

from tunguskas.warehouse import get_connection


def get_dataframe(query: str) -> pd.DataFrame:
    with get_connection(read_only=True) as conn:
        return conn.execute(query).df()
