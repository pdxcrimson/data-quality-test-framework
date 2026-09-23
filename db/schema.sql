-- Rebates/payments-processing schema used as the target for data quality tests.

CREATE TABLE IF NOT EXISTS customers (
    customer_id     INTEGER PRIMARY KEY,
    name            TEXT NOT NULL,
    status          TEXT NOT NULL CHECK (status IN ('active', 'inactive', 'pending'))
);

CREATE TABLE IF NOT EXISTS orders (
    order_id        INTEGER PRIMARY KEY,
    customer_id     INTEGER NOT NULL,
    amount          NUMERIC NOT NULL,
    order_date      TEXT NOT NULL,
    status          TEXT NOT NULL CHECK (status IN ('open', 'closed', 'cancelled')),
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);

CREATE TABLE IF NOT EXISTS rebates (
    rebate_id       INTEGER PRIMARY KEY,
    order_id        INTEGER NOT NULL,
    rebate_amount   NUMERIC NOT NULL,
    rebate_pct      NUMERIC NOT NULL,
    applied_date    TEXT,
    FOREIGN KEY (order_id) REFERENCES orders (order_id)
);

CREATE TABLE IF NOT EXISTS batch_runs (
    batch_id            INTEGER PRIMARY KEY,
    run_date            TEXT NOT NULL,
    status              TEXT NOT NULL CHECK (status IN ('completed', 'failed', 'running')),
    records_processed   INTEGER NOT NULL DEFAULT 0
);
