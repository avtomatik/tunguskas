from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"

RAW_DIR = DATA_DIR / "external"
WAREHOUSE_DIR = DATA_DIR / "warehouse"
EXPORT_DIR = DATA_DIR / "exports"

SQL_DIR = BASE_DIR / "sql"

WAREHOUSE_PATH = WAREHOUSE_DIR / "tunguska.duckdb"

FILE_NAME = "archive.zip"
