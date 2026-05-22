CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS mart;
 
DROP TABLE IF EXISTS raw.hydrology;
 
CREATE TABLE raw.hydrology (
    location TEXT,
    river_post TEXT,
    post_id TEXT,
    gauge_zero TEXT,
    day TEXT,
    month INTEGER,
    year INTEGER,
    raw_value TEXT,
    ingested_at TIMESTAMP
);
