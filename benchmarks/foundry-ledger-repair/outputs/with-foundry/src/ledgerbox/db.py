"""SQLite persistence for Ledgerbox."""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


def connect(path: str | Path) -> sqlite3.Connection:
    connection = sqlite3.connect(path, isolation_level=None, timeout=5)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA busy_timeout = 5000")
    return connection


def initialize(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS ledger_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id TEXT NOT NULL,
            account_id TEXT NOT NULL,
            amount_cents INTEGER NOT NULL,
            currency TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS processed_events (
            event_id TEXT PRIMARY KEY,
            processed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
    )


class LedgerRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    @contextmanager
    def transaction(self) -> Iterator[None]:
        self.connection.execute("BEGIN IMMEDIATE")
        try:
            yield
            self.connection.commit()
        except BaseException:
            self.connection.rollback()
            raise

    def has_processed(self, event_id: str) -> bool:
        row = self.connection.execute(
            "SELECT 1 FROM processed_events WHERE event_id = ?", (event_id,)
        ).fetchone()
        return row is not None

    def append_credit(
        self, event_id: str, account_id: str, amount_cents: int, currency: str
    ) -> None:
        self.connection.execute(
            """
            INSERT INTO ledger_entries(event_id, account_id, amount_cents, currency)
            VALUES (?, ?, ?, ?)
            """,
            (event_id, account_id, amount_cents, currency),
        )

    def mark_processed(self, event_id: str) -> None:
        self.connection.execute(
            "INSERT INTO processed_events(event_id) VALUES (?)", (event_id,)
        )

    def balance(self, account_id: str, currency: str = "EUR") -> int:
        row = self.connection.execute(
            """
            SELECT COALESCE(SUM(amount_cents), 0) AS balance
            FROM ledger_entries
            WHERE account_id = ? AND currency = ?
            """,
            (account_id, currency),
        ).fetchone()
        return int(row["balance"])

    def entry_count(self, event_id: str) -> int:
        row = self.connection.execute(
            "SELECT COUNT(*) AS count FROM ledger_entries WHERE event_id = ?",
            (event_id,),
        ).fetchone()
        return int(row["count"])
