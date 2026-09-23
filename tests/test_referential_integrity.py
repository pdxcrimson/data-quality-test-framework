"""
test_referential_integrity.py

The seed data intentionally includes a couple of orphaned records
(see db/seed_data.sql) so these tests verify the validators actually
catch them. In a real pipeline you'd point these validators at a live
or staging database and assert an EMPTY result instead.
"""

from src.validators import referential_integrity


def test_orphaned_orders_are_detected():
    orphans = referential_integrity.find_orphaned_orders()
    orphan_ids = {row["order_id"] for row in orphans}
    assert orphan_ids == {105}, f"Expected only order 105 to be orphaned, got: {orphan_ids}"


def test_orphaned_rebates_are_detected():
    orphans = referential_integrity.find_orphaned_rebates()
    orphan_ids = {row["rebate_id"] for row in orphans}
    assert orphan_ids == {205}, f"Expected only rebate 205 to be orphaned, got: {orphan_ids}"
