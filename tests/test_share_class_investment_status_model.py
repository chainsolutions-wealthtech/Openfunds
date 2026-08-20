import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migrations" / "manifest.json"
MIGRATION = ROOT / "schemas" / "fund" / "031_share_class_investment_status.sql"
EXPECTED = {
    "OPEN",
    "SOFT_CLOSED",
    "HARD_CLOSED",
    "CLOSED_FOR_REDEMPTION",
    "CLOSED_FOR_SUBSCRIPTION_AND_REDEMPTION",
}


class ShareClassInvestmentStatusModelTests(unittest.TestCase):
    def test_migration_031_is_registered_forward_only(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        row = next((m for m in manifest["migrations"] if m["id"] == "031_SHARE_CLASS_INVESTMENT_STATUS"), None)
        self.assertIsNotNone(row)
        self.assertEqual(310, row["order"])
        self.assertEqual("schemas/fund/031_share_class_investment_status.sql", row["path"])

    def test_investment_status_is_distinct_from_lifecycle_phase(self):
        self.assertTrue(MIGRATION.is_file())
        sql = MIGRATION.read_text(encoding="utf-8")
        lower = sql.lower()
        self.assertIn("alter table fund.share_class_profile", lower)
        for column in ("investment_status", "investment_status_description", "investment_status_date", "investment_status_date_status"):
            self.assertIn(column, lower)
        self.assertNotIn("alter table fund.entity_state", lower)
        self.assertNotIn("update fund.share_class_profile", lower)
        for value in EXPECTED:
            self.assertIn(f"'{value}'", sql)

    def test_date_knowledge_status_prevents_synthetic_dates(self):
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertIn("investment_status_date_status", sql)
        self.assertIn("'known'", sql)
        self.assertIn("'unknown'", sql)
        self.assertIn("investment_status_date is not null", sql)
        self.assertIn("investment_status_date is null", sql)


if __name__ == "__main__":
    unittest.main()
