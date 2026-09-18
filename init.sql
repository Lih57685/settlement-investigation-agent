CREATE TABLE trades (
    trade_id VARCHAR(20) PRIMARY KEY,
    security VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL,
    quantity INTEGER NOT NULL,
    currency VARCHAR(3) NOT NULL,
    market VARCHAR(20),
    counterparty VARCHAR(20),
    account VARCHAR(30),
    settlement_date DATE,
    status VARCHAR(20) NOT NULL
);


CREATE TABLE settlement_status (
    trade_id VARCHAR(20) PRIMARY KEY,
    status VARCHAR(20) NOT NULL,
    reason_code VARCHAR(50),
    message TEXT,

    CONSTRAINT fk_settlement_trade
        FOREIGN KEY (trade_id)
        REFERENCES trades(trade_id)
);


CREATE TABLE ssi (
    trade_id VARCHAR(20) PRIMARY KEY,

    internal_custodian VARCHAR(50),
    internal_bic VARCHAR(20),
    internal_account VARCHAR(50),
    internal_currency VARCHAR(3),

    counterparty_custodian VARCHAR(50),
    counterparty_bic VARCHAR(20),
    counterparty_account VARCHAR(50),
    counterparty_currency VARCHAR(3),

    CONSTRAINT fk_ssi_trade
        FOREIGN KEY (trade_id)
        REFERENCES trades(trade_id)
);


CREATE TABLE error_logs (
    id SERIAL PRIMARY KEY,
    trade_id VARCHAR(20) NOT NULL,
    system VARCHAR(100),
    event_timestamp TIMESTAMP,
    error_code VARCHAR(50),
    severity VARCHAR(20),
    message TEXT,
    retry_count INTEGER,
    last_retry_status VARCHAR(20),

    CONSTRAINT fk_error_trade
        FOREIGN KEY (trade_id)
        REFERENCES trades(trade_id)
);


INSERT INTO trades
(
    trade_id,
    security,
    side,
    quantity,
    currency,
    market,
    counterparty,
    account,
    settlement_date,
    status
)
VALUES
(
    'TX1001',
    'JP0000000001',
    'BUY',
    1000,
    'JPY',
    'JAPAN',
    'CP001',
    'ACC-JP-001',
    '2026-09-10',
    'PENDING'
),
(
    'TX1002',
    'US0000000002',
    'SELL',
    500,
    'USD',
    'USA',
    'CP002',
    'ACC-US-001',
    '2026-09-11',
    'SETTLED'
),
(
    'TX1003',
    'JP0000000003',
    'SELL',
    2000,
    'JPY',
    'JAPAN',
    'CP003',
    'ACC-JP-003',
    '2026-09-11',
    'PENDING'
);


INSERT INTO settlement_status
(
    trade_id,
    status,
    reason_code,
    message
)
VALUES
(
    'TX1001',
    'FAILED',
    'SSI_MISMATCH',
    'Counterparty settlement instruction does not match.'
),
(
    'TX1002',
    'SETTLED',
    NULL,
    'Settlement completed successfully.'
),
(
    'TX1003',
    'FAILED',
    'SYSTEM_ERROR',
    'Settlement instruction failed during outbound processing.'
);


INSERT INTO ssi
(
    trade_id,

    internal_custodian,
    internal_bic,
    internal_account,
    internal_currency,

    counterparty_custodian,
    counterparty_bic,
    counterparty_account,
    counterparty_currency
)
VALUES
(
    'TX1001',

    'MUFG',
    'BOTKJPJT',
    '12345678',
    'JPY',

    'MUFG',
    'BOTKJPJT',
    '87654321',
    'JPY'
);


INSERT INTO error_logs
(
    trade_id,
    system,
    event_timestamp,
    error_code,
    severity,
    message,
    retry_count,
    last_retry_status
)
VALUES
(
    'TX1003',
    'Settlement Gateway',
    '2026-09-11 14:32:10',
    'GW_TIMEOUT_504',
    'ERROR',
    'Timeout while sending settlement instruction to custodian gateway.',
    3,
    'FAILED'
);