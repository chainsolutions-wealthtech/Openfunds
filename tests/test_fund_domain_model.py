from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migrations/manifest.json"
CORE_MIGRATION = ROOT / "schemas/fund/015_fund_subfund_shareclass_core.sql"
EXTENSION_MIGRATION = ROOT / "schemas/fund/018_extended_security_identifier_schemes.sql"


class FundDomainModelTests(unittest.TestCase):
    def test_manifest_keeps_015_as_foundation_and_allows_forward_extensions(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        fund_migrations = [
            item
            for item in manifest["migrations"]
            if item["path"].startswith("schemas/fund/")
        ]
        by_id = {item["id"]: item for item in fund_migrations}
        self.assertIn("015_FUND_SUBFUND_SHARECLASS_CORE", by_id)
        canonical = by_id["015_FUND_SUBFUND_SHARECLASS_CORE"]
        self.assertEqual(canonical["order"], 150)
        self.assertEqual(
            canonical["path"],
            "schemas/fund/015_fund_subfund_shareclass_core.sql",
        )
        if "018_EXTENDED_SECURITY_IDENTIFIER_SCHEMES" in by_id:
            extension = by_id["018_EXTENDED_SECURITY_IDENTIFIER_SCHEMES"]
            self.assertGreater(extension["order"], canonical["order"])
            self.assertEqual(
                extension["path"],
                "schemas/fund/018_extended_security_identifier_schemes.sql",
            )

        excluded = {
            entry["path"]: entry["reason"]
            for entry in manifest["excluded_sql"]
        }
        proposal = "schemas/taxonomy/fund_relationship_information_model_v0.1.sql"
        self.assertIn(proposal, excluded)
        self.assertIn("SUPERSEDED_DRAFT", excluded[proposal])
        self.assertIn("015", excluded[proposal])

    def test_migration_contains_the_required_canonical_contract(self) -> None:
        sql = CORE_MIGRATION.read_text(encoding="utf-8")
        required = (
            "create table if not exists fund.entity (",
            "create table if not exists fund.entity_state (",
            "create table if not exists fund.fund_profile (",
            "create table if not exists fund.subfund_profile (",
            "create table if not exists fund.share_class_profile (",
            "create table if not exists fund.entity_name (",
            "create table if not exists fund.entity_identifier (",
            "create table if not exists fund.structure_relationship (",
            "create table if not exists fund.entity_event (",
            "create table if not exists fund.event_participant (",
            "create or replace view fund.current_share_class_path as",
            "create or replace view fund.structure_quality_issue as",
            "create or replace function fund.enforce_structure_relationship()",
        )
        for fragment in required:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, sql)

    def test_foundational_migration_does_not_activate_legacy_draft_tables(self) -> None:
        sql = CORE_MIGRATION.read_text(encoding="utf-8").lower()
        self.assertNotIn("create table if not exists fund.fund (", sql)
        self.assertNotIn("create table if not exists fund.share_class (", sql)
        self.assertNotIn("drop table", sql)
        self.assertNotIn("delete from", sql)
        self.assertNotIn("truncate", sql)

    def test_standalone_and_umbrella_paths_are_explicit(self) -> None:
        sql = CORE_MIGRATION.read_text(encoding="utf-8")
        self.assertIn("'STANDALONE','UMBRELLA'", sql)
        self.assertIn("'FUND_HAS_SUBFUND'", sql)
        self.assertIn("'FUND_HAS_SHARE_CLASS'", sql)
        self.assertIn("'SUBFUND_HAS_SHARE_CLASS'", sql)
        self.assertIn("No synthetic subfund is required", sql)

    def test_identity_names_identifiers_and_events_are_separate(self) -> None:
        sql = CORE_MIGRATION.read_text(encoding="utf-8")
        self.assertIn("name_role text not null", sql)
        self.assertIn("identifier_scheme text not null", sql)
        self.assertIn("event_type text not null", sql)
        self.assertIn("'RENAME'", sql)
        self.assertIn("'MERGER'", sql)
        self.assertIn("'MANAGEMENT_TRANSFER'", sql)
        self.assertIn("'LIQUIDATION'", sql)


if __name__ == "__main__":
    unittest.main()
