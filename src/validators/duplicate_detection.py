"""
duplicate_detection.py

Finds duplicate records that should be unique per business rules
(e.g., a customer should not have two orders logged for the exact
same order_date + amount, which usually signals a double-submission).
"""

from src.db_connector import run_query


def find_duplicate_orders_by_customer_and_date() -> list[dict]:
    """Orders where the same customer has two orders with the same
    amount on the same date -- a common signal of duplicate submission."""
    query = """
        SELECT customer_id, order_date, amount, COUNT(*) AS occurrences
        FROM orders
        GROUP BY customer_id, order_date, amount
        HAVING COUNT(*) > 1
    """
    return [dict(row) for row in run_query(query)]


def find_duplicate_rebate_ids() -> list[dict]:
    """Sanity check: rebate_id should be unique (primary key), but this
    validator demonstrates how you'd catch it even without the constraint."""
    query = """
        SELECT rebate_id, COUNT(*) AS occurrences
        FROM rebates
        GROUP BY rebate_id
        HAVING COUNT(*) > 1
    """
    return [dict(row) for row in run_query(query)]
