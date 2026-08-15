from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ledgerbox import CreditEvent, LedgerRepository, connect, initialize, process_credit


class LedgerboxServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.database = Path(self.temporary.name) / "ledger.db"
        self.connection = connect(self.database)
        initialize(self.connection)
        self.repository = LedgerRepository(self.connection)

    def tearDown(self) -> None:
        self.connection.close()
        self.temporary.cleanup()

    def test_applies_credit(self) -> None:
        event = CreditEvent("evt-1", "acct-1", 2500)

        self.assertEqual(process_credit(self.repository, event), "applied")
        self.assertEqual(self.repository.balance("acct-1"), 2500)
        self.assertEqual(self.repository.entry_count("evt-1"), 1)

    def test_sequential_duplicate_is_ignored(self) -> None:
        event = CreditEvent("evt-2", "acct-1", 1800)

        self.assertEqual(process_credit(self.repository, event), "applied")
        self.assertEqual(process_credit(self.repository, event), "duplicate")
        self.assertEqual(self.repository.balance("acct-1"), 1800)

    def test_distinct_events_apply_independently(self) -> None:
        self.assertEqual(
            process_credit(self.repository, CreditEvent("evt-3", "acct-1", 700)),
            "applied",
        )
        self.assertEqual(
            process_credit(self.repository, CreditEvent("evt-4", "acct-1", 900)),
            "applied",
        )
        self.assertEqual(self.repository.balance("acct-1"), 1600)

    def test_rejects_unsupported_currency(self) -> None:
        with self.assertRaisesRegex(ValueError, "EUR"):
            process_credit(
                self.repository,
                CreditEvent("evt-5", "acct-1", 500, currency="USD"),
            )


if __name__ == "__main__":
    unittest.main()
