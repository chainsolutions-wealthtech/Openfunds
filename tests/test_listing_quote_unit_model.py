from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migrations" / "manifest.json"
MIGRATION = ROOT / "schemas" / "fund" / "020_listing_quote_unit_semantics.sql"
CURRENCIES = ROOT / "data" / "reference" / "CURRENCIES.csv"


class ListingQuoteUnitModelContractTests(unittest.TestCase):
    def migration_sql(self) -> str:
        self.assertTrue(MIGRATION.is_file(), "migration 020 SQL must exist")
        return MIGRATION.read_text(encoding="utf-8").lower()

    def test_migration_020_is_registered_forward_only(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        entries = [
            item
            for item in manifest["migrations"]
            if item["id"] == "020_LISTING_QUOTE_UNIT_SEMANTICS"
        ]
        self.assertEqual(1, len(entries))
        self.assertEqual(200, entries[0]["order"])
        self.assertEqual(
            "schemas/fund/020_listing_quote_unit_semantics.sql",
            entries[0]["path"],
        )

    def test_quote_unit_is_separate_from_economic_currency(self) -> None:
        sql = self.migration_sql()
        self.assertIn("alter table fund.listing", sql)
        self.assertIn("trading_quote_unit_code", sql)
        self.assertIn("trading_quote_unit_factor", sql)
        self.assertIn("trading_currency_id", sql)
        self.assertIn("check", sql)
        self.assertIn("trading_quote_unit_factor > 0", sql)
        self.assertNotIn("insert into ref.currency", sql)
        self.assertNotIn("delete from", sql)
        self.assertNotIn("truncate", sql)
        self.assertNotIn("drop table", sql)

    def test_quote_unit_code_is_exact_three_uppercase_characters_when_present(self) -> None:
        sql = self.migration_sql()
        self.assertIn("char_length(trading_quote_unit_code) = 3", sql)
        self.assertIn("trading_quote_unit_code = upper(trading_quote_unit_code)", sql)
        self.assertIn("trading_quote_unit_code ~ '^[a-z]{3}$'", sql)

    def test_factor_cannot_exist_without_quote_unit_code(self) -> None:
        sql = self.migration_sql()
        self.assertIn(
            "trading_quote_unit_factor is null or trading_quote_unit_code is not null",
            sql,
        )

    def test_minor_unit_codes_are_not_injected_into_currency_registry(self) -> None:
        currencies = CURRENCIES.read_text(encoding="utf-8")
        for pseudo_code in ("GBX", "EUX", "USX"):
            self.assertNotIn(f"\n{pseudo_code};", currencies)


if __name__ == "__main__":
    unittest.main()
