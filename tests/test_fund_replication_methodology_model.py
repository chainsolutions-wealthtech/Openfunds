import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migrations" / "manifest.json"
MIGRATION = ROOT / "schemas" / "fund" / "034_fund_replication_methodology.sql"
FIRST_LEVEL = {"PHYSICAL", "SYNTHETICAL", "HYBRID", "OTHERS"}
DETAILS = {
    "FULL",
    "OPTIMIZED_EQUITIES_SAMPLED_BONDS",
    "PHYSICALLY_BACKED",
    "UNFUNDED_SWAP",
    "FUNDED_SWAP",
    "COMBINATION_UNFUNDED_AND_FUNDED_SWAP",
    "FUTURES",
}


class FundReplicationMethodologyModelTests(unittest.TestCase):
    def test_migration_034_is_registered_forward_only(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        row = next((m for m in manifest["migrations"] if m["id"] == "034_FUND_REPLICATION_METHODOLOGY"), None)
        self.assertIsNotNone(row)
        self.assertEqual(340, row["order"])
        self.assertEqual("schemas/fund/034_fund_replication_methodology.sql", row["path"])

    def test_first_level_and_normalized_detail_relation_are_additive(self):
        self.assertTrue(MIGRATION.is_file())
        sql = MIGRATION.read_text(encoding="utf-8")
        lower = sql.lower()
        self.assertIn("alter table fund.fund_profile", lower)
        self.assertIn("add column if not exists replication_methodology_first_level text", lower)
        self.assertIn("create table if not exists fund.replication_methodology_detail", lower)
        self.assertIn("fund_id uuid not null", lower)
        self.assertIn("detail_code text not null", lower)
        self.assertIn("references fund.entity(entity_id, entity_type)", lower)
        self.assertNotIn("replication_methodology_second_level text", lower)
        self.assertNotIn("update fund.fund_profile", lower)
        for value in FIRST_LEVEL | DETAILS:
            self.assertIn(f"'{value}'", sql)

    def test_detail_relation_is_versioned_and_source_lineaged(self):
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
        self.assertIn("where is_current", lower)


if __name__ == "__main__":
    unittest.main()
