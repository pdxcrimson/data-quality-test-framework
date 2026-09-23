"""
test_business_rules.py

Verifies the business-rule validators correctly flag the intentional
violations seeded in db/seed_data.sql.
"""

from src.validators import business_rules


def test_rebates_exceeding_order_amount_are_detected():
    violations = business_rules.find_rebates_exceeding_order_amount()
    violation_ids = {row["rebate_id"] for row in violations}
    assert violation_ids == {202}, f"Expected only rebate 202 to violate this rule, got: {violation_ids}"


def test_invalid_rebate_percentages_are_detected():
    violations = business_rules.find_invalid_rebate_percentages()
    violation_ids = {row["rebate_id"] for row in violations}
    assert violation_ids == {204}, f"Expected only rebate 204 to have an invalid pct, got: {violation_ids}"


def test_empty_completed_batches_are_detected():
    violations = business_rules.find_empty_completed_batches()
    violation_ids = {row["batch_id"] for row in violations}
    assert violation_ids == {3}, f"Expected only batch 3 to be flagged, got: {violation_ids}"
