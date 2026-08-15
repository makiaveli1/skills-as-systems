#!/usr/bin/env python3
"""Hidden behavioural checks for a completed Parcelhouse candidate."""

from __future__ import annotations

import inspect
import json
import sqlite3
import sys
import tempfile
import threading
import unittest
from pathlib import Path


CANDIDATE = Path(sys.argv.pop(1)).resolve()
sys.path.insert(0, str(CANDIDATE / "src"))

import parcelhouse  # noqa: E402


V1_SCHEMA = """
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


class HiddenAcceptance(unittest.TestCase):
    def fresh(self):
        temporary = tempfile.TemporaryDirectory()
        path = Path(temporary.name) / "jobs.db"
        parcelhouse.initialize(path)
        return temporary, path

    def test_public_signatures_remain_compatible(self):
        expected = {
            "claim_next": ["connection", "worker", "now", "lease_seconds", "_after_select"],
            "complete": ["connection", "job_id", "worker", "result", "now"],
            "cancel": ["connection", "job_id"],
            "recover_expired": ["connection", "now"],
        }
        for name, parameters in expected.items():
            self.assertEqual(list(inspect.signature(getattr(parcelhouse, name)).parameters), parameters)

    def test_claim_is_atomic_under_competing_connections(self):
        for iteration in range(24):
            temporary, path = self.fresh()
            try:
                connection = parcelhouse.connect(path)
                parcelhouse.create_job(connection, f"job-{iteration}", {"iteration": iteration})
                connection.close()
                gate = threading.Barrier(2)
                results = []
                errors = []

                def claim(worker):
                    current = parcelhouse.connect(path)
                    try:
                        gate.wait(timeout=3)
                        results.append(parcelhouse.claim_next(current, worker, 100, 30))
                    except Exception as error:  # noqa: BLE001 - evidence surface
                        errors.append(f"{type(error).__name__}: {error}")
                    finally:
                        current.close()

                threads = [threading.Thread(target=claim, args=(f"worker-{number}",)) for number in range(2)]
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join(timeout=5)
                self.assertFalse(any(thread.is_alive() for thread in threads), "claim threads did not finish")
                self.assertEqual(errors, [])
                claimed = [item for item in results if item is not None]
                self.assertEqual(len(claimed), 1)
                self.assertEqual(claimed[0]["id"], f"job-{iteration}")
            finally:
                temporary.cleanup()

    def test_leased_cancellation_wins_without_delivery(self):
        temporary, path = self.fresh()
        try:
            connection = parcelhouse.connect(path)
            parcelhouse.create_job(connection, "job-1", {})
            parcelhouse.claim_next(connection, "worker-a", 100, 30)
            self.assertTrue(parcelhouse.cancel(connection, "job-1"))
            self.assertEqual(parcelhouse.get_job(connection, "job-1")["state"], "cancel_requested")
            self.assertFalse(parcelhouse.complete(connection, "job-1", "worker-a", "delivered", 110))
            self.assertEqual(parcelhouse.get_job(connection, "job-1")["state"], "cancelled")
            count = connection.execute("SELECT COUNT(*) FROM deliveries WHERE job_id = 'job-1'").fetchone()[0]
            self.assertEqual(count, 0)
            connection.close()
        finally:
            temporary.cleanup()

    def test_wrong_worker_cannot_create_delivery(self):
        temporary, path = self.fresh()
        try:
            connection = parcelhouse.connect(path)
            parcelhouse.create_job(connection, "job-1", {})
            parcelhouse.claim_next(connection, "worker-a", 100, 30)
            self.assertFalse(parcelhouse.complete(connection, "job-1", "worker-b", "delivered", 110))
            self.assertEqual(parcelhouse.get_job(connection, "job-1")["state"], "leased")
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM deliveries").fetchone()[0], 0)
            connection.close()
        finally:
            temporary.cleanup()

    def test_expired_cancel_request_never_requeues(self):
        temporary, path = self.fresh()
        try:
            connection = parcelhouse.connect(path)
            parcelhouse.create_job(connection, "job-1", {})
            parcelhouse.claim_next(connection, "worker-a", 100, 10)
            parcelhouse.cancel(connection, "job-1")
            parcelhouse.recover_expired(connection, 111)
            self.assertEqual(parcelhouse.get_job(connection, "job-1")["state"], "cancelled")
            connection.close()
        finally:
            temporary.cleanup()

    def test_version_one_database_migrates_idempotently(self):
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "v1.db"
            connection = sqlite3.connect(path)
            connection.executescript(V1_SCHEMA)
            connection.execute("INSERT INTO jobs(id, payload, state) VALUES ('queued-old', '{}', 'queued')")
            connection.execute(
                "INSERT INTO jobs(id, payload, state, lease_owner, lease_until) VALUES ('leased-old', '{}', 'leased', 'worker-old', 999)"
            )
            connection.commit()
            connection.close()
            parcelhouse.initialize(path)
            parcelhouse.initialize(path)
            migrated = parcelhouse.connect(path)
            self.assertEqual(migrated.execute("SELECT COUNT(*) FROM jobs").fetchone()[0], 2)
            self.assertGreaterEqual(migrated.execute("PRAGMA user_version").fetchone()[0], 2)
            self.assertTrue(parcelhouse.cancel(migrated, "leased-old"))
            self.assertEqual(parcelhouse.get_job(migrated, "leased-old")["state"], "cancel_requested")
            migrated.close()


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]], verbosity=2)
