"""
referential_integrity.py

Checks for orphaned records: rows whose foreign key points to a parent
row that doesn't exist. In production systems this usually means a
failed cascade, a bad migration, or a race condition during writes.
"""

from src.db_connector import run_query


def find_orphaned_orders() -> list[dict]:
    """Orders whose customer_id has no matching row in customers."""
    query = """
        SELECT o.order_id, o.customer_id
        FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
    """
    return [dict(row) for row in run_query(query)]


def find_orphaned_rebates() -> list[dict]:
    """Rebates whose order_id has no matching row in orders."""
    query = """
        SELECT r.rebate_id, r.order_id
        FROM rebates r
        LEFT JOIN orders o ON r.order_id = o.order_id
        WHERE o.order_id IS NULL
    """
    return [dict(row) for row in run_query(query)]
