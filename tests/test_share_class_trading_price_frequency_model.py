from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migrations" / "manifest.json"
MIGRATION = ROOT / "schemas" / "fund" / "025_share_class_trading_price_frequency.sql"


class ShareClassTradingPriceFrequencyModelContractTests(unittest.TestCase):
    def test_migration_025_is_registered_forward_only(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        entries = [item for item in manifest["migrations"] if item["id"] == "025_SHARE_CLASS_TRADING_PRICE_FREQUENCY"]
        self.assertEqual(1, len(entries))
        self.assertEqual(250, entries[0]["order"])
        self.assertEqual("schemas/fund/025_share_class_trading_price_frequency.sql", entries[0]["path"])

    def test_trading_price_frequency_is_distinct_from_nav_frequency(self) -> None:
        self.assertTrue(MIGRATION.exists(), "migration 025 must exist")
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertIn("alter table fund.share_class_profile", sql)
        self.assertIn("trading_price_frequency", sql)
        self.assertIn(" text", sql)
        self.assertNotIn("rename column nav_frequency", sql)
        self.assertNotIn("drop column nav_frequency", sql)

    def test_migration_is_additive_and_does_not_rewrite_existing_profiles(self) -> None:
        self.assertTrue(MIGRATION.exists(), "migration 025 must exist")
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertNotIn("update fund.share_class_profile", sql)
        self.assertNotIn("delete from", sql)
        self.assertNotIn("truncate", sql)
        self.assertNotIn("drop table", sql)


if __name__ == "__main__":
    unittest.main()
