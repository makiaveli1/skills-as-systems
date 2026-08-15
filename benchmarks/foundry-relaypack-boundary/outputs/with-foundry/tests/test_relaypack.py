import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from relaypack import render_route


class RelaypackTests(unittest.TestCase):
    def test_known_route(self):
        self.assertEqual(
            render_route("alpha"),
            "route alpha -> https://api.example.test/v1",
        )

    def test_unknown_route(self):
        with self.assertRaises(KeyError):
            render_route("missing")


if __name__ == "__main__":
    unittest.main()
