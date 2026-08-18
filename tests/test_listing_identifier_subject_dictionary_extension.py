from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "data" / "dictionary" / "extensions" / "listing_identifier_subject_v1"
METADATA = PACKAGE / "00_metadata.json"
FIELDS = PACKAGE / "10_fields.json"
MIGRATION = ROOT / "schemas" / "fund" / "023_listing_identifier_subject.sql"
CORE = ROOT / "data" / "dictionary" / "spec_v1"
LISTING = ROOT / "data" / "dictionary" / "extensions" / "listing_v1"
QUOTE_UNIT = ROOT / "data" / "dictionary" / "extensions" / "listing_quote_unit_v1"
STATUS = ROOT / "data" / "dictionary" / "extensions" / "listing_status_v1"
FIELD_ID = "OF_FUND_LISTING_IDENTIFIER_IDENTIFIER_SUBJECT"


class ListingIdentifierSubjectDictionaryExtensionTests(unittest.TestCase):
    def test_extension_declares_exact_migration_023_scope(self) -> None:
        self.assertTrue(METADATA.is_file(), "listing_identifier_subject_v1 metadata must exist")
        self.assertTrue(FIELDS.is_file(), "listing_identifier_subject_v1 fields must exist")
        metadata = json.loads(METADATA.read_text(encoding="utf-8"))
        fields = json.loads(FIELDS.read_text(encoding="utf-8"))["fields"]
        self.assertEqual("OPENFUNDS_CANONICAL_LISTING_IDENTIFIER_SUBJECT_EXTENSION", metadata["dictionary_id"])
        self.assertEqual("1.0.0", metadata["dictionary_version"])
        self.assertEqual("VALIDATED_LISTING_IDENTIFIER_SUBJECT_EXTENSION_SCOPE", metadata["status"])
        self.assertEqual("schemas/fund/023_listing_identifier_subject.sql", metadata["provenance_path"])
        self.assertEqual(1, metadata["field_count"])
        self.assertEqual(1, len(fields))

    def test_extension_exposes_identifier_subject_only(self) -> None:
        field = json.loads(FIELDS.read_text(encoding="utf-8"))["fields"][0]
        self.assertEqual(FIELD_ID, field["field_id"])
        self.assertEqual("fund.listing_identifier.identifier_subject", field["technical_name"])
        self.assertEqual("LISTING_IDENTIFIER", field["entity_code"])
        self.assertEqual("fund", field["physical_schema"])
        self.assertEqual("listing_identifier", field["physical_table"])
        self.assertEqual("identifier_subject", field["physical_column"])
        self.assertFalse(field["nullable"])
        self.assertEqual("schemas/fund/023_listing_identifier_subject.sql", field["provenance_path"])
        self.assertEqual("VALIDATED", field["status"])

    def test_all_extensions_union_to_181_fields(self) -> None:
        from scripts.validate_openfunds_mapping_registry import load_canonical_inventory

        ids, entities, counts = load_canonical_inventory(CORE, [LISTING, QUOTE_UNIT, STATUS, PACKAGE])
        self.assertEqual(143, counts["core"])
        self.assertEqual(38, counts["extensions"])
        self.assertEqual(181, counts["total"])
        self.assertEqual(181, len(ids))
        self.assertEqual("LISTING_IDENTIFIER", entities[FIELD_ID])


if __name__ == "__main__":
    unittest.main()
