DROP TABLE IF EXISTS mart.stations;
 
CREATE TABLE mart.stations AS
 
SELECT DISTINCT
    post_id,
    location,
    river_post,
    gauge_zero
FROM staging.hydrology_clean;
 
 
 
DROP TABLE IF EXISTS mart.daily_levels;
 
CREATE TABLE mart.daily_levels AS
 
SELECT
    ROW_NUMBER() OVER () AS observation_id,
 
    post_id,
 
    date,
 
    value,
 
    legend
 
FROM staging.hydrology_clean
 
WHERE date IS NOT NULL
AND value IS NOT NULL
 
ORDER BY
    post_id,
    date;
