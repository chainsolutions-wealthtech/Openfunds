import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migrations" / "manifest.json"
MIGRATION = ROOT / "schemas" / "fund" / "028_share_class_multicurrency_dealing.sql"


class ShareClassMulticurrencyModelTests(unittest.TestCase):
    def test_migration_028_is_registered_forward_only(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        row = next((m for m in manifest["migrations"] if m["id"] == "028_SHARE_CLASS_MULTICURRENCY_DEALING"), None)
        self.assertIsNotNone(row)
        self.assertEqual(280, row["order"])
        self.assertEqual("schemas/fund/028_share_class_multicurrency_dealing.sql", row["path"])

    def test_reference_currency_is_not_made_multivalued(self):
        self.assertTrue(MIGRATION.is_file())
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertIn("add column if not exists is_multicurrency boolean", sql)
        self.assertIn("create table if not exists fund.share_class_dealing_currency", sql)
        self.assertIn("currency_id uuid not null references ref.currency", sql)
        self.assertNotIn("drop column currency_id", sql)
        self.assertNotIn("rename column currency_id", sql)
        self.assertNotIn("update fund.share_class_profile", sql)

    def test_additional_dealing_currencies_are_versioned_and_source_lineaged(self):
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        for token in ["effective_from", "effective_from_status", "effective_to", "effective_to_status", "recorded_at", "superseded_at", "is_current", "validation_status", "source_artifact_id", "source_locator", "source_note"]:
            self.assertIn(token, sql)
        self.assertIn("where is_current", sql)


if __name__ == "__main__":
    unittest.main()
