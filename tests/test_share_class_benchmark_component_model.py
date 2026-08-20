import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migrations" / "manifest.json"
MIGRATION = ROOT / "schemas" / "fund" / "035_share_class_benchmark_components.sql"


class ShareClassBenchmarkComponentModelTests(unittest.TestCase):
    def test_migration_035_is_registered_forward_only(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        row = next((m for m in manifest["migrations"] if m["id"] == "035_SHARE_CLASS_BENCHMARK_COMPONENTS"), None)
        self.assertIsNotNone(row)
        self.assertEqual(350, row["order"])
        self.assertEqual("schemas/fund/035_share_class_benchmark_components.sql", row["path"])

    def test_benchmark_is_normalized_as_ordered_components(self):
        self.assertTrue(MIGRATION.is_file())
        sql = MIGRATION.read_text(encoding="utf-8")
        lower = sql.lower()
        self.assertIn("create table if not exists fund.share_class_benchmark_component", lower)
        for token in (
            "share_class_id uuid not null",
            "component_order integer not null",
            "component_name text not null",
            "component_weight numeric",
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
        self.assertIn("component_order > 0", lower)
        self.assertIn("component_weight is null or component_weight >= 0", lower)
        self.assertNotIn("benchmark text", lower)
        self.assertNotIn("update fund.share_class_profile", lower)

    def test_current_component_order_is_unique_per_share_class(self):
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertIn("(share_class_id, component_order)", lower)
        self.assertIn("where is_current", lower)


if __name__ == "__main__":
    unittest.main()
