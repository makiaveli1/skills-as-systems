from __future__ import annotations

import json
import sqlite3
from collections.abc import Callable
from typing import Any


def create_job(connection: sqlite3.Connection, job_id: str, payload: dict[str, Any]) -> None:
    connection.execute(
        "INSERT INTO jobs(id, payload, state) VALUES (?, ?, 'queued')",
        (job_id, json.dumps(payload, sort_keys=True)),
    )


def get_job(connection: sqlite3.Connection, job_id: str) -> dict[str, Any] | None:
    row = connection.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    return dict(row) if row else None


def claim_next(
    connection: sqlite3.Connection,
    worker: str,
    now: int,
    lease_seconds: int = 30,
    _after_select: Callable[[], None] | None = None,
) -> dict[str, Any] | None:
    row = connection.execute(
        "SELECT * FROM jobs WHERE state = 'queued' ORDER BY id LIMIT 1"
    ).fetchone()
    if row is None:
        return None
    if _after_select is not None:
        _after_select()
    connection.execute(
        "UPDATE jobs SET state = 'leased', lease_owner = ?, lease_until = ? WHERE id = ?",
        (worker, now + lease_seconds, row["id"]),
    )
    return get_job(connection, row["id"])


def complete(
    connection: sqlite3.Connection,
    job_id: str,
    worker: str,
    result: str,
    now: int,
) -> bool:
    connection.execute(
        "INSERT INTO deliveries(job_id, worker, delivered_at, result) VALUES (?, ?, ?, ?)",
        (job_id, worker, now, result),
    )
    updated = connection.execute(
        "UPDATE jobs SET state = 'done', result = ?, lease_owner = NULL, lease_until = NULL "
        "WHERE id = ? AND state = 'leased' AND lease_owner = ?",
        (result, job_id, worker),
    )
    return updated.rowcount == 1


def cancel(connection: sqlite3.Connection, job_id: str) -> bool:
    updated = connection.execute(
        "UPDATE jobs SET state = 'cancelled' WHERE id = ? AND state = 'queued'",
        (job_id,),
    )
    return updated.rowcount == 1


def recover_expired(connection: sqlite3.Connection, now: int) -> int:
    updated = connection.execute(
        "UPDATE jobs SET state = 'queued', lease_owner = NULL, lease_until = NULL "
        "WHERE state = 'leased' AND lease_until <= ?",
        (now,),
    )
    return updated.rowcount
