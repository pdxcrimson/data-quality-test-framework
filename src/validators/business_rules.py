"""
business_rules.py

Domain-specific checks that go beyond schema/type validity -- these
encode "what does correct data actually look like" for this business.
"""

from src.db_connector import run_query


def find_rebates_exceeding_order_amount() -> list[dict]:
    """Rebates where rebate_amount is greater than the parent order's amount."""
    query = """
        SELECT r.rebate_id, r.order_id, r.rebate_amount, o.amount AS order_amount
        FROM rebates r
        JOIN orders o ON r.order_id = o.order_id
        WHERE r.rebate_amount > o.amount
    """
    return [dict(row) for row in run_query(query)]


def find_invalid_rebate_percentages() -> list[dict]:
    """Rebates where rebate_pct falls outside the valid 0-100 range."""
    query = """
        SELECT rebate_id, rebate_pct
        FROM rebates
        WHERE rebate_pct < 0 OR rebate_pct > 100
    """
    return [dict(row) for row in run_query(query)]


def find_empty_completed_batches() -> list[dict]:
    """Batch runs marked 'completed' but with zero records processed."""
    query = """
        SELECT batch_id, run_date, records_processed
        FROM batch_runs
        WHERE status = 'completed' AND records_processed <= 0
    """
    return [dict(row) for row in run_query(query)]
