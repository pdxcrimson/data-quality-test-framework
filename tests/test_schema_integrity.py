"""
test_schema_integrity.py

Validates nullability, allowed values, and basic ranges on core tables.
"""

from src.validators import schema_checks


def test_no_orders_with_null_required_fields():
    violations = schema_checks.find_orders_with_null_required_fields()
    assert violations == [], f"Found orders with null required fields: {violations}"


def test_no_orders_with_invalid_status():
    violations = schema_checks.find_orders_with_invalid_status()
    assert violations == [], f"Found orders with invalid status: {violations}"


def test_no_negative_order_amounts():
    violations = schema_checks.find_negative_order_amounts()
    assert violations == [], f"Found orders with negative amounts: {violations}"
