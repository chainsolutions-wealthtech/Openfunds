from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migrations" / "manifest.json"
MIGRATION = ROOT / "schemas" / "fund" / "023_listing_identifier_subject.sql"


class ListingIdentifierSubjectContractTests(unittest.TestCase):
    def test_migration_023_is_registered_forward_only(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        entries = [m for m in manifest["migrations"] if m["id"] == "023_LISTING_IDENTIFIER_SUBJECT"]
        self.assertEqual(1, len(entries))
        self.assertEqual(230, entries[0]["order"])
        self.assertEqual("schemas/fund/023_listing_identifier_subject.sql", entries[0]["path"])

    def test_identifier_subject_distinguishes_listing_from_inav(self) -> None:
        self.assertTrue(MIGRATION.is_file(), "migration 023 must exist")
        sql = MIGRATION.read_text(encoding="utf-8").upper()
        self.assertIn("ALTER TABLE FUND.LISTING_IDENTIFIER", sql)
        self.assertIn("IDENTIFIER_SUBJECT TEXT", sql)
        self.assertIn("DEFAULT 'LISTING'", sql)
        self.assertIn("'LISTING'", sql)
        self.assertIn("'INAV'", sql)
        self.assertNotIn("ALTER TABLE FUND.ENTITY_IDENTIFIER", sql)

    def test_current_identifier_uniqueness_is_listing_scoped_and_subject_aware(self) -> None:
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertIn("drop index if exists fund.ux_fund_listing_identifier_current_scheme_value", sql)
        self.assertIn("listing_id, identifier_subject, identifier_scheme, normalized_value", sql)
        self.assertIn("where is_current", sql)
        self.assertNotIn("delete from", sql)
        self.assertNotIn("truncate", sql)
        self.assertNotIn("drop table", sql)


if __name__ == "__main__":
    unittest.main()
