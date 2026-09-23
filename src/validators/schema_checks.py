"""
schema_checks.py

Lower-level checks on nullability, allowed value sets, and ranges --
the kind of thing a schema/constraint *should* catch but that's worth
testing explicitly, since constraints can be missing, weakened by a
migration, or bypassed by direct writes.
"""

from src.db_connector import run_query


def find_orders_with_null_required_fields() -> list[dict]:
    """Orders missing a value in a field that should never be null."""
    query = """
        SELECT order_id
        FROM orders
        WHERE customer_id IS NULL OR amount IS NULL OR order_date IS NULL
    """
    return [dict(row) for row in run_query(query)]


def find_orders_with_invalid_status() -> list[dict]:
    """Orders with a status outside the allowed value set."""
    query = """
        SELECT order_id, status
        FROM orders
        WHERE status NOT IN ('open', 'closed', 'cancelled')
    """
    return [dict(row) for row in run_query(query)]


def find_negative_order_amounts() -> list[dict]:
    """Orders with a negative amount, which should never be valid."""
    query = """
        SELECT order_id, amount
        FROM orders
        WHERE amount < 0
    """
    return [dict(row) for row in run_query(query)]
