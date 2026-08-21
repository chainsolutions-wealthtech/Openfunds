import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migrations" / "manifest.json"
MIGRATION = ROOT / "schemas" / "fund" / "037_share_class_tracked_index.sql"


class ShareClassTrackedIndexModelTests(unittest.TestCase):
    def test_migration_037_is_registered_forward_only(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        row = next((m for m in manifest["migrations"] if m["id"] == "037_SHARE_CLASS_TRACKED_INDEX"), None)
        self.assertIsNotNone(row)
        self.assertEqual(370, row["order"])
        self.assertEqual("schemas/fund/037_share_class_tracked_index.sql", row["path"])

    def test_tracked_index_is_versioned_and_source_lineaged(self):
        self.assertTrue(MIGRATION.is_file())
        lower = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertIn("create table if not exists fund.share_class_tracked_index", lower)
        for token in (
            "share_class_id uuid not null",
            "index_name text not null",
            "index_currency_id uuid",
            "index_currency_mode text not null",
            "index_type text",
            "effective_from_status",
            "effective_to_status",
            "recorded_at",
            "superseded_at",
            "is_current",
            "validation_status",
            "source_artifact_id",
            "source_locator",
            "source_note",
        ):
            self.assertIn(token, lower)
        self.assertIn("references fund.entity(entity_id, entity_type)", lower)
        self.assertIn("references ref.currency(currency_id)", lower)
        self.assertIn("'explicit_iso4217','local_currency','unknown'", lower.replace(" ", ""))
        for token in ("'price'", "'performance'", "'performance_net_dividends'", "'performance_gross_dividends'"):
            self.assertIn(token, lower)

    def test_local_currency_mode_never_requires_or_infers_currency_id(self):
        lower = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertIn("index_currency_mode = 'explicit_iso4217' and index_currency_id is not null", lower)
        self.assertIn("index_currency_mode in ('local_currency','unknown') and index_currency_id is null", lower)
        self.assertNotIn("update fund.share_class_profile", lower)
        self.assertNotIn("coalesce", lower)

    def test_only_one_current_tracked_index_exists_per_share_class(self):
        lower = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertIn("on fund.share_class_tracked_index (share_class_id)", lower)
        self.assertIn("where is_current", lower)


if __name__ == "__main__":
    unittest.main()
