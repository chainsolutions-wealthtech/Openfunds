from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "data" / "dictionary" / "extensions" / "listing_quote_unit_v1"
METADATA = PACKAGE / "00_metadata.json"
FIELDS = PACKAGE / "10_fields.json"
MIGRATION = ROOT / "schemas" / "fund" / "020_listing_quote_unit_semantics.sql"
CORE = ROOT / "data" / "dictionary" / "spec_v1"
LISTING = ROOT / "data" / "dictionary" / "extensions" / "listing_v1"

EXPECTED = {
    "OF_FUND_LISTING_TRADING_QUOTE_UNIT_CODE": "trading_quote_unit_code",
    "OF_FUND_LISTING_TRADING_QUOTE_UNIT_FACTOR": "trading_quote_unit_factor",
}


class ListingQuoteUnitDictionaryExtensionTests(unittest.TestCase):
    def test_extension_declares_exact_migration_020_scope(self) -> None:
        self.assertTrue(METADATA.is_file(), "listing_quote_unit_v1 metadata must exist")
        self.assertTrue(FIELDS.is_file(), "listing_quote_unit_v1 fields must exist")
        metadata = json.loads(METADATA.read_text(encoding="utf-8"))
        fields = json.loads(FIELDS.read_text(encoding="utf-8"))["fields"]
        self.assertEqual("OPENFUNDS_CANONICAL_LISTING_QUOTE_UNIT_EXTENSION", metadata["dictionary_id"])
        self.assertEqual("1.0.0", metadata["dictionary_version"])
        self.assertEqual("VALIDATED_LISTING_QUOTE_UNIT_EXTENSION_SCOPE", metadata["status"])
        self.assertEqual("schemas/fund/020_listing_quote_unit_semantics.sql", metadata["provenance_path"])
        self.assertEqual(2, metadata["field_count"])
        self.assertEqual(2, len(fields))

    def test_extension_exposes_only_the_two_new_020_columns(self) -> None:
        fields = json.loads(FIELDS.read_text(encoding="utf-8"))["fields"]
        by_id = {field["field_id"]: field for field in fields}
        self.assertEqual(set(EXPECTED), set(by_id))
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        for field_id, physical_column in EXPECTED.items():
            field = by_id[field_id]
            self.assertEqual("LISTING", field["entity_code"])
            self.assertEqual("fund", field["physical_schema"])
            self.assertEqual("listing", field["physical_table"])
            self.assertEqual(physical_column, field["physical_column"])
            self.assertEqual("schemas/fund/020_listing_quote_unit_semantics.sql", field["provenance_path"])
            self.assertEqual("VALIDATED", field["status"])
            self.assertIn(physical_column, sql)

    def test_core_listing_and_quote_unit_extensions_union_to_179_fields(self) -> None:
        from scripts.validate_openfunds_mapping_registry import load_canonical_inventory

        ids, entities, counts = load_canonical_inventory(CORE, [LISTING, PACKAGE])
        self.assertEqual(143, counts["core"])
        self.assertEqual(36, counts["extensions"])
        self.assertEqual(179, counts["total"])
        self.assertEqual(179, len(ids))
        for field_id in EXPECTED:
            self.assertEqual("LISTING", entities[field_id])

    def test_listing_v1_remains_immutable_at_34_fields(self) -> None:
        metadata = json.loads((LISTING / "00_metadata.json").read_text(encoding="utf-8"))
        fields = json.loads((LISTING / "10_fields.json").read_text(encoding="utf-8"))["fields"]
        self.assertEqual(34, metadata["field_count"])
        self.assertEqual(34, len(fields))


if __name__ == "__main__":
    unittest.main()
