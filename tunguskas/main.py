from tunguskas.export import export_data
from tunguskas.ingest import ingest_archive
from tunguskas.paths import SQL_DIR
from tunguskas.warehouse import get_connection, run_sql_file


def main():

    conn = get_connection()

    run_sql_file(
        conn,
        SQL_DIR / "ddl" / "schemas.sql",
    )

    conn.close()

    ingest_archive()

    conn = get_connection()

    run_sql_file(
        conn,
        SQL_DIR / "transforms" / "raw_to_staging.sql",
    )

    run_sql_file(
        conn,
        SQL_DIR / "transforms" / "staging_to_mart.sql",
    )

    conn.close()

    export_data()


if __name__ == "__main__":
    main()
