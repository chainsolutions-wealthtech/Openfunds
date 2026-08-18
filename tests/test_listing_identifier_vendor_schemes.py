from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migrations" / "manifest.json"
MIGRATION = ROOT / "schemas" / "fund" / "022_listing_vendor_identifier_schemes.sql"


class ListingVendorIdentifierSchemeContractTests(unittest.TestCase):
    def test_migration_022_is_registered_forward_only(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        entries = [m for m in manifest["migrations"] if m["id"] == "022_LISTING_VENDOR_IDENTIFIER_SCHEMES"]
        self.assertEqual(1, len(entries))
        self.assertEqual(220, entries[0]["order"])
        self.assertEqual("schemas/fund/022_listing_vendor_identifier_schemes.sql", entries[0]["path"])

    def test_listing_identifier_scheme_is_extended_without_rebuilding_table(self) -> None:
        self.assertTrue(MIGRATION.is_file(), "migration 022 must exist")
        sql = MIGRATION.read_text(encoding="utf-8").upper()
        for scheme in ("SEDOL", "TICKER", "LOCAL_CODE", "OTHER", "BLOOMBERG", "RIC"):
            self.assertIn(f"'{scheme}'", sql)
        self.assertIn("ALTER TABLE FUND.LISTING_IDENTIFIER", sql)
        self.assertIn("ADD CONSTRAINT", sql)
        self.assertNotIn("DROP TABLE", sql)
        self.assertNotIn("TRUNCATE", sql)
        self.assertNotIn("DELETE FROM", sql)

    def test_vendor_schemes_are_not_added_to_share_class_entity_identifier(self) -> None:
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertNotIn("alter table fund.entity_identifier", sql)


if __name__ == "__main__":
    unittest.main()
