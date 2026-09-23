-- seed_data.sql
-- Mostly clean data, with a handful of intentionally "dirty" records
-- so the test suite has real problems to catch (not just green checkmarks).

INSERT INTO customers (customer_id, name, status) VALUES
    (1, 'Acme Corp', 'active'),
    (2, 'Globex LLC', 'active'),
    (3, 'Initech', 'inactive'),
    (4, 'Umbrella Inc', 'active'),
    (5, 'Soylent Co', 'pending');

INSERT INTO orders (order_id, customer_id, amount, order_date, status) VALUES
    (100, 1, 500.00, '2026-01-05', 'closed'),
    (101, 2, 1200.50, '2026-01-06', 'closed'),
    (102, 3, 75.00,  '2026-01-07', 'open'),
    (103, 4, 300.00, '2026-01-08', 'closed'),
    (104, 5, 950.00, '2026-01-09', 'open'),
    -- BAD: customer_id 99 does not exist in customers -> orphaned order
    (105, 99, 200.00, '2026-01-10', 'open');

INSERT INTO rebates (rebate_id, order_id, rebate_amount, rebate_pct, applied_date) VALUES
    (200, 100, 50.00, 10.0, '2026-01-06'),
    (201, 101, 120.05, 10.0, '2026-01-07'),
    -- BAD: rebate_amount (400) exceeds the order's amount (75) -> business rule violation
    (202, 102, 400.00, 20.0, '2026-01-08'),
    (203, 103, 30.00, 10.0, NULL),
    -- BAD: rebate_pct is 150, outside the valid 0-100 range
    (204, 104, 90.00, 150.0, '2026-01-10'),
    -- BAD: order_id 999 does not exist in orders -> orphaned rebate
    (205, 999, 25.00, 5.0, '2026-01-11');

INSERT INTO batch_runs (batch_id, run_date, status, records_processed) VALUES
    (1, '2026-01-06', 'completed', 6),
    (2, '2026-01-07', 'completed', 5),
    -- BAD: status is 'completed' but 0 records were processed
    (3, '2026-01-08', 'completed', 0),
    (4, '2026-01-09', 'failed', 0);
