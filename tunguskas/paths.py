from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
WAREHOUSE_DIR = DATA_DIR / "warehouse"
EXPORT_DIR = DATA_DIR / "exports"
SQL_DIR = BASE_DIR / "sql"
RAW_ARCHIVE_PATH = DATA_DIR / "external" / "archive.zip"
WAREHOUSE_PATH = WAREHOUSE_DIR / "tunguska.duckdb"

for directory in (WAREHOUSE_DIR, EXPORT_DIR):
    directory.mkdir(parents=True, exist_ok=True)
