"""
conftest.py

Session-scoped fixture that (re)builds the SQLite test database once
before the suite runs, so every test works against the same known
dataset defined in db/seed_data.sql.
"""

import sys
from pathlib import Path

# Make the repo root importable (so `from src...` works when running
# pytest from anywhere).
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from db.init_db import build_database


@pytest.fixture(scope="session", autouse=True)
def test_database():
    """Build the SQLite database once before any tests run."""
    db_path = build_database()
    yield db_path
