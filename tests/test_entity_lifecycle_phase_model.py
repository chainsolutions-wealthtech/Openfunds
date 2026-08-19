import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migrations" / "manifest.json"
MIGRATION = ROOT / "schemas" / "fund" / "029_entity_lifecycle_phase.sql"
EXPECTED = {"PROJECTED", "TO_BE_LAUNCHED", "OFFERING_PERIOD", "ACTIVE", "DORMANT", "IN_LIQUIDATION", "TERMINATED"}


class EntityLifecyclePhaseModelTests(unittest.TestCase):
    def test_migration_029_is_registered_forward_only(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        row = next((m for m in manifest["migrations"] if m["id"] == "029_ENTITY_LIFECYCLE_PHASE"), None)
        self.assertIsNotNone(row)
        self.assertEqual(290, row["order"])
        self.assertEqual("schemas/fund/029_entity_lifecycle_phase.sql", row["path"])

    def test_precise_phase_is_additive_to_broad_lifecycle_status(self):
        self.assertTrue(MIGRATION.is_file())
        sql = MIGRATION.read_text(encoding="utf-8")
        lower = sql.lower()
        self.assertIn("alter table fund.entity_state", lower)
        self.assertIn("add column if not exists lifecycle_phase text", lower)
        self.assertNotIn("drop column lifecycle_status", lower)
        self.assertNotIn("rename column lifecycle_status", lower)
        self.assertNotIn("update fund.entity_state", lower)
        for value in EXPECTED:
            self.assertIn(f"'{value}'", sql)


if __name__ == "__main__":
    unittest.main()
