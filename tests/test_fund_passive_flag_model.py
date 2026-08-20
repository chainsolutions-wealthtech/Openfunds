import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migrations" / "manifest.json"
MIGRATION = ROOT / "schemas" / "fund" / "033_fund_passive_flag.sql"


class FundPassiveFlagModelTests(unittest.TestCase):
    def test_migration_033_is_registered_forward_only(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        row = next((m for m in manifest["migrations"] if m["id"] == "033_FUND_PASSIVE_FLAG"), None)
        self.assertIsNotNone(row)
        self.assertEqual(330, row["order"])
        self.assertEqual("schemas/fund/033_fund_passive_flag.sql", row["path"])

    def test_passive_flag_is_fund_level_and_additive(self):
        self.assertTrue(MIGRATION.is_file())
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertIn("alter table fund.fund_profile", sql)
        self.assertIn("add column if not exists is_passive boolean", sql)
        self.assertNotIn("alter table fund.share_class_profile", sql)
        self.assertNotIn("drop column", sql)
        self.assertNotIn("update fund.fund_profile", sql)


if __name__ == "__main__":
    unittest.main()
