import zipfile
from datetime import datetime, timezone

import duckdb
import pandas as pd

from tunguskas.constants import LOCATIONS, YEARS
from tunguskas.enums import Shape
from tunguskas.paths import FILE_NAME, RAW_DIR
from tunguskas.warehouse import get_connection


def ingest_file(
    conn: duckdb.DuckDBPyConnection,
    archive: zipfile.ZipFile,
    location: str,
    year: int,
) -> None:

    with archive.open(f"{location} {year}.xls") as f:

        df_pack = pd.read_html(f)

        post_id = None
        river_post = None
        gauge_zero = None

        for chunk in df_pack:

            if chunk.shape == Shape.STAMPS.value:

                post_id, _, river_post, gauge_zero, _ = chunk.iloc[:, -1]

            elif chunk.shape == Shape.DATA.value:

                chunk.drop(range(2), inplace=True)
                chunk.drop(chunk.tail(7).index, inplace=True)

                melted = pd.melt(
                    chunk,
                    id_vars=chunk.columns[0],
                    value_vars=chunk.columns[1:],
                    ignore_index=False,
                )

                melted.columns = [
                    "day",
                    "month",
                    "raw_value",
                ]

                melted["year"] = year
                melted["location"] = location
                melted["river_post"] = river_post
                melted["post_id"] = post_id
                melted["gauge_zero"] = gauge_zero
                melted["ingested_at"] = datetime.now(timezone.utc)

                melted = melted[
                    [
                        "location",
                        "river_post",
                        "post_id",
                        "gauge_zero",
                        "day",
                        "month",
                        "year",
                        "raw_value",
                        "ingested_at",
                    ]
                ]

                conn.register("temp_df", melted)

                conn.execute(
                    """
                    INSERT INTO raw.hydrology
                    SELECT *
                    FROM temp_df
                """
                )


def ingest_archive() -> None:

    conn = get_connection()

    archive_path = RAW_DIR / FILE_NAME

    with zipfile.ZipFile(archive_path) as archive:

        for location in LOCATIONS:

            for year in YEARS:

                ingest_file(conn, archive, location, year)

    conn.close()
