from tunguskas.paths import EXPORT_DIR
from tunguskas.warehouse import get_connection


def export_data():

    conn = get_connection()

    conn.execute(
        f"""
        COPY mart.daily_levels_enriched
        TO '{EXPORT_DIR / "dataset.parquet"}'
        (FORMAT PARQUET)
    """
    )

    conn.execute(
        f"""
        COPY mart.daily_levels_enriched
        TO '{EXPORT_DIR / "dataset.csv"}'
        (HEADER, DELIMITER ',')
    """
    )

    conn.close()
