DROP TABLE IF EXISTS staging.hydrology_clean;
 
CREATE TABLE staging.hydrology_clean AS

SELECT
    TRIM(location) AS location,
    TRIM(river_post) AS river_post,
    post_id,

    TRY_CAST(gauge_zero AS DOUBLE) AS gauge_zero,

    CASE
        WHEN TRY_CAST(day AS INTEGER) IS NULL THEN NULL

        ELSE
            MAKE_DATE(year, month, 1)
            + (CAST(day AS INTEGER) - 1)
    END AS date,

    TRY_CAST(
        REGEXP_EXTRACT(
            raw_value,
            '(\d+)',
            1
        ) AS INTEGER
    ) AS value,

    NULLIF(
        TRIM(
            REGEXP_EXTRACT(
                raw_value,
                '([^\d]+)',
                1
            )
        ),
        ''
    ) AS legend

FROM raw.hydrology

WHERE raw_value IS NOT NULL;
