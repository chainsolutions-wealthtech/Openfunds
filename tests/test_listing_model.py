from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migrations" / "manifest.json"
MIGRATION = ROOT / "schemas" / "fund" / "019_share_class_listing_core.sql"


class ListingModelContractTests(unittest.TestCase):
    def test_migration_019_is_registered_forward_only(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        entries = [m for m in manifest["migrations"] if m["id"] == "019_SHARE_CLASS_LISTING_CORE"]
        self.assertEqual(1, len(entries))
        self.assertEqual(190, entries[0]["order"])
        self.assertEqual("schemas/fund/019_share_class_listing_core.sql", entries[0]["path"])

    def test_listing_schema_separates_share_class_from_listing_identity(self) -> None:
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertIn("create table if not exists fund.listing", sql)
        self.assertIn("create table if not exists fund.listing_identifier", sql)
        self.assertIn("share_class_id uuid not null", sql)
        self.assertIn("entity_type text not null default 'share_class'", sql)
        self.assertIn("foreign key (share_class_id, entity_type)", sql)
        self.assertIn("references fund.entity(entity_id, entity_type)", sql)
        self.assertIn("exchange_organization_id uuid references ref.organization", sql)
        self.assertIn("venue_mic", sql)
        self.assertIn("trading_currency_id uuid references ref.currency", sql)
        self.assertIn("listing_id uuid not null references fund.listing", sql)
        self.assertIn("identifier_scheme", sql)
        self.assertIn("'sedol'", sql)
        self.assertIn("'ticker'", sql)
        self.assertNotIn("delete from", sql)
        self.assertNotIn("truncate", sql)
        self.assertNotIn("drop table", sql)

    def test_listing_requires_a_venue_locator_and_has_source_lineage(self) -> None:
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertIn("exchange_organization_id is not null or venue_mic is not null", sql)
        self.assertIn("source_artifact_id uuid references source.raw_artifact", sql)
        self.assertIn("source_locator jsonb", sql)
        self.assertIn("validation_status", sql)


if __name__ == "__main__":
    unittest.main()
