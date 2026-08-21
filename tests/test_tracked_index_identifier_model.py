import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migrations" / "manifest.json"
MIGRATION = ROOT / "schemas" / "fund" / "038_tracked_index_identifiers.sql"


class TrackedIndexIdentifierModelTests(unittest.TestCase):
    def test_migration_038_is_registered_forward_only(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        row = next((m for m in manifest["migrations"] if m["id"] == "038_TRACKED_INDEX_IDENTIFIERS"), None)
        self.assertIsNotNone(row)
        self.assertEqual(380, row["order"])
        self.assertEqual("schemas/fund/038_tracked_index_identifiers.sql", row["path"])

    def test_identifier_relation_is_versioned_and_vendor_specific(self):
        self.assertTrue(MIGRATION.is_file())
        lower = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertIn("create table if not exists fund.tracked_index_identifier", lower)
        for token in (
            "share_class_tracked_index_id uuid not null",
            "identifier_scheme text not null",
            "identifier_value text not null",
            "normalized_value text not null",
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
        self.assertIn("references fund.share_class_tracked_index", lower)
        compact = "".join(lower.split())
        self.assertIn("identifier_schemein('bloomberg','ric')", compact)
        self.assertNotIn("upper(identifier_value)", lower)
        self.assertNotIn("lower(identifier_value)", lower)

    def test_one_current_identifier_per_scheme_per_tracked_index(self):
        lower = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertIn("(share_class_tracked_index_id, identifier_scheme)", lower)
        self.assertIn("where is_current", lower)


if __name__ == "__main__":
    unittest.main()
