from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migrations" / "manifest.json"
MIGRATION = ROOT / "schemas" / "fund" / "024_listing_inception_price.sql"


class ListingInceptionPriceModelContractTests(unittest.TestCase):
    def test_migration_024_is_registered_forward_only(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        entries = [item for item in manifest["migrations"] if item["id"] == "024_LISTING_INCEPTION_PRICE"]
        self.assertEqual(1, len(entries))
        self.assertEqual(240, entries[0]["order"])
        self.assertEqual("schemas/fund/024_listing_inception_price.sql", entries[0]["path"])

    def test_inception_price_is_a_listing_attribute(self) -> None:
        self.assertTrue(MIGRATION.exists(), "migration 024 must exist")
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertIn("alter table fund.listing", sql)
        self.assertIn("inception_price", sql)
        self.assertIn("numeric", sql)
        self.assertIn("inception_price > 0", sql)

    def test_price_does_not_duplicate_currency_or_quote_unit_semantics(self) -> None:
        self.assertTrue(MIGRATION.exists(), "migration 024 must exist")
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertNotIn("insert into ref.currency", sql)
        self.assertNotIn("trading_currency_id", sql)
        self.assertNotIn("trading_quote_unit_code", sql)
        self.assertNotIn("trading_quote_unit_factor", sql)
        self.assertNotIn("delete from", sql)
        self.assertNotIn("truncate", sql)
        self.assertNotIn("drop table", sql)


if __name__ == "__main__":
    unittest.main()
