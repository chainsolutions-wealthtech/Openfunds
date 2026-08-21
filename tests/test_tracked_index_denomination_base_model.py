import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migrations" / "manifest.json"
MIGRATION = ROOT / "schemas" / "fund" / "039_tracked_index_denomination_base.sql"


class TrackedIndexDenominationBaseModelTests(unittest.TestCase):
    def test_migration_039_is_registered_forward_only(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        row = next((m for m in manifest["migrations"] if m["id"] == "039_TRACKED_INDEX_DENOMINATION_BASE"), None)
        self.assertIsNotNone(row)
        self.assertEqual(390, row["order"])
        self.assertEqual("schemas/fund/039_tracked_index_denomination_base.sql", row["path"])

    def test_denomination_base_is_positive_nullable_tracked_index_attribute(self):
        self.assertTrue(MIGRATION.is_file())
        lower = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertIn("alter table fund.share_class_tracked_index", lower)
        self.assertIn("add column if not exists denomination_base numeric", lower)
        self.assertIn("denomination_base is null or denomination_base > 0", lower)
        self.assertNotIn("update fund.share_class_tracked_index", lower)
        self.assertNotIn("update fund.share_class_profile", lower)
        self.assertNotIn("index_level", lower)
        self.assertNotIn("fund_price", lower)


if __name__ == "__main__":
    unittest.main()
