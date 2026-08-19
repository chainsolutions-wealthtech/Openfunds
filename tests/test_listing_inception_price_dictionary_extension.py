from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "data" / "dictionary" / "extensions" / "listing_inception_price_v1"
METADATA = PACKAGE / "00_metadata.json"
FIELDS = PACKAGE / "10_fields.json"
MIGRATION = ROOT / "schemas" / "fund" / "024_listing_inception_price.sql"


class ListingInceptionPriceDictionaryExtensionTests(unittest.TestCase):
    def test_extension_is_one_field_and_tracks_migration_024(self) -> None:
        metadata = json.loads(METADATA.read_text(encoding="utf-8"))
        fields = json.loads(FIELDS.read_text(encoding="utf-8"))["fields"]
        self.assertEqual(1, metadata["field_count"])
        self.assertEqual(1, len(fields))
        self.assertEqual("schemas/fund/024_listing_inception_price.sql", metadata["provenance_path"])
        field = fields[0]
        self.assertEqual("OF_FUND_LISTING_INCEPTION_PRICE", field["field_id"])
        self.assertEqual("LISTING", field["entity_code"])
        self.assertEqual("listing", field["physical_table"])
        self.assertEqual("inception_price", field["physical_column"])
        self.assertEqual("numeric", field["data_type"])
        self.assertEqual("NULL_OR_GREATER_THAN_ZERO", field["validation_rule"])
        self.assertIn("inception_price", MIGRATION.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
