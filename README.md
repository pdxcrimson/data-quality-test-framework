# Data Quality Test Automation Framework

[![Data Quality Tests](https://github.com/pdxcrimson/data-quality-test-framework/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/pdxcrimson/data-quality-test-framework/actions/workflows/tests.yml)

A pytest-based framework for validating data integrity in a SQL database —
schema checks, referential integrity, business-rule enforcement, and
duplicate detection. Built to demonstrate SDET-style test automation
applied to a data layer rather than a UI or API.

The target dataset models a simplified rebates/payments-processing domain
(customers, orders, rebates, batch runs), seeded with a handful of
**intentional data quality problems** so the test suite has real issues
to catch, not just green checkmarks.

## Why this exists

Most QA/SDET portfolios show UI or API test automation. Verifying that
data is *correct* after it lands in a database — not just that an API
returned 200 — is an equally common (and often under-tested) part of the
job: batch jobs, ETL pipelines, and backend processing can all silently
produce bad data even when every request "succeeds."

## Project structure

```
data-quality-test-framework/
├── db/
│   ├── schema.sql          # table definitions
│   ├── seed_data.sql       # sample data, including intentional bad records
│   └── init_db.py          # builds a fresh SQLite DB from schema + seed data
├── src/
│   ├── db_connector.py     # connection handling
│   └── validators/         # reusable data validation logic
│       ├── schema_checks.py
│       ├── referential_integrity.py
│       ├── business_rules.py
│       └── duplicate_detection.py
├── tests/                  # pytest test suite covering each validator
├── .github/workflows/      # CI: runs the suite on every push
└── reports/                # generated HTML test report (git-ignored)
```

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/pdxcrimson/data-quality-test-framework.git
   cd data-quality-test-framework
   ```

2. **Initialize the environment**:
   ```bash
   uv sync
   ```
   This creates a `.venv`, installs Python 3.14, and syncs dependencies (pytest and pytest-html).

## Running the tests

```bash
# Builds a fresh SQLite DB automatically via the conftest fixture

# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_business_rules.py

# Run all tests verbosely
uv run pytest -v

# With an HTML report
uv run pytest tests/ --html=reports/report.html --self-contained-html
```

## What the tests actually check

| Category | Example check |
|---|---|
| Schema checks | No null required fields, status values are within the allowed set, no negative order amounts |
| Referential integrity | Every order's `customer_id` exists in `customers`; every rebate's `order_id` exists in `orders` |
| Business rules | A rebate can't exceed its order's amount; `rebate_pct` must be 0–100; a "completed" batch can't show 0 records processed |
| Duplicate detection | No duplicate `order_id`/`rebate_id`; no duplicate order submissions (same customer, date, amount) |

The referential-integrity and business-rule tests are written to assert
the validators correctly flag the *known* bad records seeded in
`seed_data.sql` — in other words, these are tests of the validators
themselves. Point `src/db_connector.py` at a real staging/production
database and flip those assertions to expect an **empty** result, and
this becomes a data quality gate you can run in CI against real data.

## Swapping SQLite for Postgres

The framework uses plain `sqlite3` for zero-setup local development.
To point it at Postgres instead:
1. Replace `src/db_connector.py`'s connection logic with `psycopg2` (or
   SQLAlchemy) connecting to your Postgres instance.
2. Adjust `db/schema.sql` for any Postgres-specific syntax (types,
   constraints).
3. Everything in `src/validators/` and `tests/` is pure SQL + Python and
   needs no changes.

## Extending this

- Add new validators under `src/validators/` following the existing
  pattern (a module of functions, each returning a list of violation
  rows).
- Add a corresponding test module under `tests/`.
- The GitHub Actions workflow (`.github/workflows/tests.yml`) already
  runs the full suite and uploads the HTML report as a build artifact
  on every push.
