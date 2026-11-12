from tunguskas.paths import EXPORT_DIR
from tunguskas.warehouse import get_connection


def export_data() -> None:
    with get_connection(read_only=True) as conn:
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
