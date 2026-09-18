import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured")

    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row,
    )


def find_trade(trade_id: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
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
                FROM trades
                WHERE trade_id = %s
                """,
                (trade_id,),
            )

            return cur.fetchone()


def find_settlement_status(trade_id: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    trade_id,
                    status,
                    reason_code,
                    message
                FROM settlement_status
                WHERE trade_id = %s
                """,
                (trade_id,),
            )

            return cur.fetchone()


def find_ssi(trade_id: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    trade_id,

                    internal_custodian,
                    internal_bic,
                    internal_account,
                    internal_currency,

                    counterparty_custodian,
                    counterparty_bic,
                    counterparty_account,
                    counterparty_currency

                FROM ssi
                WHERE trade_id = %s
                """,
                (trade_id,),
            )

            return cur.fetchone()


def find_error_logs(trade_id: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    id,
                    trade_id,
                    system,
                    event_timestamp,
                    error_code,
                    severity,
                    message,
                    retry_count,
                    last_retry_status
                FROM error_logs
                WHERE trade_id = %s
                ORDER BY event_timestamp DESC
                """,
                (trade_id,),
            )

            return cur.fetchall()
