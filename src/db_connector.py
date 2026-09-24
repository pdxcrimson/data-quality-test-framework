"""
db_connector.py

Lightweight connection helper. Uses plain sqlite3 (no ORM) to keep the
framework easy to read and to swap for Postgres later (see README).
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path

DEFAULT_DB_PATH = Path(__file__).parent.parent / "db" / "test_data.db"


@contextmanager
def get_connection(db_path: Path = DEFAULT_DB_PATH):
    """Yield a sqlite3 connection with row access by column name."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def run_query(query: str, db_path: Path = DEFAULT_DB_PATH) -> list[sqlite3.Row]:
    """Run a read-only query and return all rows."""
    with get_connection(db_path) as conn:
        cursor = conn.execute(query)
        return cursor.fetchall()
