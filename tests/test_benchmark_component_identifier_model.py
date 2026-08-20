import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migrations" / "manifest.json"
MIGRATION = ROOT / "schemas" / "fund" / "036_benchmark_component_identifiers.sql"


class BenchmarkComponentIdentifierModelTests(unittest.TestCase):
    def test_migration_036_is_registered_forward_only(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        row = next((m for m in manifest["migrations"] if m["id"] == "036_BENCHMARK_COMPONENT_IDENTIFIERS"), None)
        self.assertIsNotNone(row)
        self.assertEqual(360, row["order"])
        self.assertEqual("schemas/fund/036_benchmark_component_identifiers.sql", row["path"])

    def test_identifier_relation_is_additive_and_vendor_specific(self):
        self.assertTrue(MIGRATION.is_file())
        sql = MIGRATION.read_text(encoding="utf-8")
        lower = sql.lower()
        self.assertIn("create table if not exists fund.benchmark_component_identifier", lower)
        self.assertIn("benchmark_component_id uuid not null", lower)
        self.assertIn("identifier_scheme text not null", lower)
        self.assertIn("identifier_value text not null", lower)
        self.assertIn("normalized_value text not null", lower)
        self.assertIn("'BLOOMBERG'", sql)
        self.assertIn("'RIC'", sql)
        self.assertIn("references fund.share_class_benchmark_component(benchmark_component_id)", lower)
        self.assertNotIn("alter table fund.share_class_benchmark_component", lower)

    def test_relation_is_versioned_and_source_lineaged(self):
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        for token in (
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
            self.assertIn(token, sql)
        self.assertIn("where is_current", sql)


if __name__ == "__main__":
    unittest.main()
