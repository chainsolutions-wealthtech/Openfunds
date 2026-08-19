import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migrations" / "manifest.json"
MIGRATION = ROOT / "schemas" / "fund" / "027_valuation_time_semantics.sql"


class ValuationTimeSemanticsModelTests(unittest.TestCase):
    def test_migration_027_is_registered_forward_only(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        row = next((m for m in manifest["migrations"] if m["id"] == "027_VALUATION_TIME_SEMANTICS"), None)
        self.assertIsNotNone(row)
        self.assertEqual(270, row["order"])
        self.assertEqual("schemas/fund/027_valuation_time_semantics.sql", row["path"])

    def test_fund_and_share_class_time_fields_are_modelled_together(self):
        self.assertTrue(MIGRATION.is_file())
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertIn("alter table fund.fund_profile", sql)
        self.assertIn("valuation_point_time time", sql)
        self.assertIn("valuation_timezone_label text", sql)
        self.assertIn("valuation_timezone_iana text", sql)
        self.assertIn("alter table fund.share_class_profile", sql)
        self.assertIn("nav_publication_time time", sql)

    def test_timezone_label_is_not_treated_as_automation_safe_iana_zone(self):
        self.assertTrue(MIGRATION.is_file())
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertIn("source-preserving", sql)
        self.assertIn("iana", sql)
        self.assertNotIn("update fund.fund_profile", sql)
        self.assertNotIn("update fund.share_class_profile", sql)
        self.assertNotIn("drop column", sql)


if __name__ == "__main__":
    unittest.main()
