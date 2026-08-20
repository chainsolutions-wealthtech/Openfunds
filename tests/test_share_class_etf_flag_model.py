import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migrations" / "manifest.json"
MIGRATION = ROOT / "schemas" / "fund" / "032_share_class_etf_flag.sql"


class ShareClassEtfFlagModelTests(unittest.TestCase):
    def test_migration_032_is_registered_forward_only(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        row = next((m for m in manifest["migrations"] if m["id"] == "032_SHARE_CLASS_ETF_FLAG"), None)
        self.assertIsNotNone(row)
        self.assertEqual(320, row["order"])
        self.assertEqual("schemas/fund/032_share_class_etf_flag.sql", row["path"])

    def test_etf_flag_is_share_class_level_and_additive(self):
        self.assertTrue(MIGRATION.is_file())
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertIn("alter table fund.share_class_profile", sql)
        self.assertIn("is_etf boolean", sql)
        self.assertNotIn("alter table fund.fund_profile", sql)
        self.assertNotIn("update fund.share_class_profile", sql)
        self.assertNotIn("delete from", sql)
        self.assertNotIn("truncate", sql)
        self.assertNotIn("drop table", sql)


if __name__ == "__main__":
    unittest.main()
