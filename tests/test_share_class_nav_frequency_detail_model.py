import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migrations" / "manifest.json"
MIGRATION = ROOT / "schemas" / "fund" / "026_share_class_nav_frequency_detail.sql"


class ShareClassNavFrequencyDetailModelTests(unittest.TestCase):
    def test_migration_026_is_registered_forward_only(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        row = next((m for m in manifest["migrations"] if m["id"] == "026_SHARE_CLASS_NAV_FREQUENCY_DETAIL"), None)
        self.assertIsNotNone(row)
        self.assertEqual(260, row["order"])
        self.assertEqual("schemas/fund/026_share_class_nav_frequency_detail.sql", row["path"])

    def test_migration_adds_optional_detail_without_rewriting_frequency(self):
        self.assertTrue(MIGRATION.is_file())
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertIn("alter table fund.share_class_profile", sql)
        self.assertIn("add column if not exists nav_frequency_detail text", sql)
        self.assertNotIn("drop column nav_frequency", sql)
        self.assertNotIn("rename column nav_frequency", sql)
        self.assertNotIn("update fund.share_class_profile", sql)


if __name__ == "__main__":
    unittest.main()
