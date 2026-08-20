import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migrations" / "manifest.json"
MIGRATION = ROOT / "schemas" / "fund" / "030_entity_lifecycle_event_types.sql"
EXPECTED_NEW = {
    "SUBSCRIPTION_PERIOD_START",
    "SUBSCRIPTION_PERIOD_END",
    "DORMANCY_START",
    "DORMANCY_END",
    "LIQUIDATION_START",
    "TERMINATION",
}
EXPECTED_EXISTING = {
    "LAUNCH",
    "RENAME",
    "MERGER",
    "ABSORPTION",
    "SPLIT",
    "MANAGEMENT_TRANSFER",
    "DOMICILE_TRANSFER",
    "LEGAL_FORM_CHANGE",
    "SUSPENSION",
    "REACTIVATION",
    "CLOSURE",
    "LIQUIDATION",
    "OTHER",
}


class EntityLifecycleEventTypesModelTests(unittest.TestCase):
    def test_migration_030_is_registered_forward_only(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        row = next((m for m in manifest["migrations"] if m["id"] == "030_ENTITY_LIFECYCLE_EVENT_TYPES"), None)
        self.assertIsNotNone(row)
        self.assertEqual(300, row["order"])
        self.assertEqual("schemas/fund/030_entity_lifecycle_event_types.sql", row["path"])

    def test_event_type_constraint_is_extended_without_rewriting_rows(self):
        self.assertTrue(MIGRATION.is_file())
        sql = MIGRATION.read_text(encoding="utf-8")
        lower = sql.lower()
        self.assertIn("alter table fund.entity_event", lower)
        self.assertNotIn("update fund.entity_event", lower)
        self.assertNotIn("delete from fund.entity_event", lower)
        self.assertNotIn("truncate fund.entity_event", lower)
        self.assertNotIn("drop table fund.entity_event", lower)
        for value in EXPECTED_NEW | EXPECTED_EXISTING:
            self.assertIn(f"'{value}'", sql)


if __name__ == "__main__":
    unittest.main()
