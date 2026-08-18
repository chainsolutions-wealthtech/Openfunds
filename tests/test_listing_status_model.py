from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migrations" / "manifest.json"
MIGRATION = ROOT / "schemas" / "fund" / "021_listing_business_status.sql"


class ListingBusinessStatusModelContractTests(unittest.TestCase):
    def test_migration_021_is_registered_forward_only(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        entries = [m for m in manifest["migrations"] if m["id"] == "021_LISTING_BUSINESS_STATUS"]
        self.assertEqual(1, len(entries))
        self.assertEqual(210, entries[0]["order"])
        self.assertEqual("schemas/fund/021_listing_business_status.sql", entries[0]["path"])

    def test_listing_status_is_a_separate_nullable_business_attribute(self) -> None:
        self.assertTrue(MIGRATION.is_file(), "migration 021 must exist")
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertIn("alter table fund.listing", sql)
        self.assertIn("listing_status text", sql)
        self.assertNotIn("listing_status text not null", sql)
        self.assertIn("'planned'", sql)
        self.assertIn("'active'", sql)
        self.assertIn("'suspended'", sql)
        self.assertIn("'delisted'", sql)
        self.assertNotIn("default 'active'", sql)

    def test_business_status_is_not_repurposed_as_bitemporal_is_current(self) -> None:
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertNotIn("rename column is_current", sql)
        self.assertNotIn("drop column is_current", sql)
        self.assertNotIn("update fund.listing set is_current", sql)
        self.assertNotIn("delete from", sql)
        self.assertNotIn("truncate", sql)
        self.assertNotIn("drop table", sql)


if __name__ == "__main__":
    unittest.main()
