from __future__ import annotations

import tempfile
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from parcelhouse import cancel, claim_next, complete, connect, create_job, get_job, initialize, recover_expired


class ParcelhouseTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temporary.name) / "jobs.db"
        initialize(self.db_path)
        self.connection = connect(self.db_path)

    def tearDown(self):
        self.connection.close()
        self.temporary.cleanup()

    def test_create_and_claim(self):
        create_job(self.connection, "job-1", {"address": "North Quay"})
        claimed = claim_next(self.connection, "worker-a", now=100, lease_seconds=20)
        self.assertEqual(claimed["id"], "job-1")
        self.assertEqual(claimed["state"], "leased")
        self.assertEqual(claimed["lease_owner"], "worker-a")

    def test_complete_records_result(self):
        create_job(self.connection, "job-1", {"address": "North Quay"})
        claim_next(self.connection, "worker-a", now=100)
        self.assertTrue(complete(self.connection, "job-1", "worker-a", "left safely", 110))
        self.assertEqual(get_job(self.connection, "job-1")["state"], "done")

    def test_cancel_queued(self):
        create_job(self.connection, "job-1", {})
        self.assertTrue(cancel(self.connection, "job-1"))
        self.assertEqual(get_job(self.connection, "job-1")["state"], "cancelled")

    def test_recover_expired(self):
        create_job(self.connection, "job-1", {})
        claim_next(self.connection, "worker-a", now=100, lease_seconds=10)
        self.assertEqual(recover_expired(self.connection, now=111), 1)
        self.assertEqual(get_job(self.connection, "job-1")["state"], "queued")


if __name__ == "__main__":
    unittest.main()
