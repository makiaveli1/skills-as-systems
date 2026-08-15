from __future__ import annotations

import sqlite3
import sys
from pathlib import Path


SCHEMA = """
CREATE TABLE jobs (
    id TEXT PRIMARY KEY,
    payload TEXT NOT NULL,
    state TEXT NOT NULL CHECK (state IN ('queued', 'leased', 'done', 'cancelled')),
    lease_owner TEXT,
    lease_until INTEGER,
    result TEXT
);
CREATE INDEX jobs_ready ON jobs(state, lease_until, id);
CREATE TABLE deliveries (
    job_id TEXT PRIMARY KEY REFERENCES jobs(id),
    worker TEXT NOT NULL,
    delivered_at INTEGER NOT NULL,
    result TEXT NOT NULL
);
PRAGMA user_version = 1;
"""


def main() -> None:
    path = Path(sys.argv[1])
    connection = sqlite3.connect(path)
    try:
        connection.executescript(SCHEMA)
        connection.execute(
            "INSERT INTO jobs(id, payload, state) VALUES ('queued-old', '{}', 'queued')"
        )
        connection.execute(
            "INSERT INTO jobs(id, payload, state, lease_owner, lease_until) "
            "VALUES ('leased-old', '{}', 'leased', 'worker-old', 999)"
        )
        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
