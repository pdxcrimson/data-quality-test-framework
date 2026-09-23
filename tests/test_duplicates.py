"""
test_duplicates.py

Seed data has no duplicate orders or rebate IDs, so these tests
confirm the validators correctly report a clean result.
"""

from src.validators import duplicate_detection


def test_no_duplicate_orders_by_customer_and_date():
    duplicates = duplicate_detection.find_duplicate_orders_by_customer_and_date()
    assert duplicates == [], f"Found unexpected duplicate orders: {duplicates}"


def test_no_duplicate_rebate_ids():
    duplicates = duplicate_detection.find_duplicate_rebate_ids()
    assert duplicates == [], f"Found unexpected duplicate rebate IDs: {duplicates}"
