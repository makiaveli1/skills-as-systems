from __future__ import annotations

import sqlite3
from pathlib import Path


SCHEMA_PATH = Path(__file__).resolve().parents[2] / "config" / "schema.sql"


def connect(path: str | Path) -> sqlite3.Connection:
    connection = sqlite3.connect(path, timeout=5, isolation_level=None)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA journal_mode = WAL")
    return connection


def initialize(path: str | Path) -> None:
    connection = connect(path)
    try:
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    finally:
        connection.close()
