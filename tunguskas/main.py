from tunguskas.export import export_data
from tunguskas.ingest import ingest_archive
from tunguskas.paths import SQL_DIR
from tunguskas.warehouse import get_connection, run_sql_file


def main() -> None:
    with get_connection() as conn:
        run_sql_file(conn, SQL_DIR / "ddl" / "schemas.sql")

    ingest_archive()

    with get_connection() as conn:
        run_sql_file(conn, SQL_DIR / "transforms" / "raw_to_staging.sql")
        run_sql_file(conn, SQL_DIR / "transforms" / "staging_to_mart.sql")

    export_data()
