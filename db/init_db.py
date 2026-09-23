"""
init_db.py

Spins up a fresh SQLite database from schema.sql and seed_data.sql.
Run directly to (re)build the local test database:

    python db/init_db.py
"""

import sqlite3
from pathlib import Path

DB_DIR = Path(__file__).parent
DB_PATH = DB_DIR / "test_data.db"
SCHEMA_PATH = DB_DIR / "schema.sql"
SEED_PATH = DB_DIR / "seed_data.sql"


def build_database(db_path: Path = DB_PATH) -> Path:
    """Create (or recreate) the SQLite database and load schema + seed data."""
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(SCHEMA_PATH.read_text())
        conn.executescript(SEED_PATH.read_text())
        conn.commit()
    finally:
        conn.close()

    return db_path


if __name__ == "__main__":
    path = build_database()
    print(f"Database built at: {path}")
