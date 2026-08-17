from __future__ import annotations

import json
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "data" / "dictionary" / "extensions" / "listing_v1"
METADATA = PACKAGE / "00_metadata.json"
FIELDS = PACKAGE / "10_fields.json"
MIGRATION = ROOT / "schemas" / "fund" / "019_share_class_listing_core.sql"
FIELD_ID_RE = re.compile(r"^OF_FUND_(LISTING|LISTING_IDENTIFIER)_[A-Z0-9_]+$")

EXPECTED_LISTING_COLUMNS = {
    "listing_id", "share_class_id", "entity_type", "exchange_organization_id",
    "venue_mic", "trading_currency_id", "is_primary", "valid_from",
    "valid_from_status", "valid_to", "valid_to_status", "recorded_at",
    "superseded_at", "is_current", "validation_status", "source_artifact_id",
    "source_locator", "source_note",
}
EXPECTED_IDENTIFIER_COLUMNS = {
    "listing_identifier_id", "listing_id", "identifier_scheme", "identifier_value",
    "normalized_value", "effective_from", "effective_from_status", "effective_to",
    "effective_to_status", "recorded_at", "superseded_at", "is_current",
    "validation_status", "source_artifact_id", "source_locator", "source_note",
}


class ListingDictionaryExtensionTests(unittest.TestCase):
    def load(self):
        metadata = json.loads(METADATA.read_text(encoding="utf-8"))
        fields = json.loads(FIELDS.read_text(encoding="utf-8"))["fields"]
        return metadata, fields

    def test_package_is_versioned_and_declares_migration_019_scope(self):
        metadata, fields = self.load()
        self.assertEqual("OPENFUNDS_CANONICAL_LISTING_EXTENSION", metadata["dictionary_id"])
        self.assertEqual("1.0.0", metadata["dictionary_version"])
        self.assertEqual("VALIDATED_LISTING_EXTENSION_SCOPE", metadata["status"])
        self.assertEqual("schemas/fund/019_share_class_listing_core.sql", metadata["provenance_path"])
        self.assertEqual(34, metadata["field_count"])
        self.assertEqual(34, len(fields))

    def test_all_019_physical_columns_are_represented_once(self):
        _, fields = self.load()
        listing = {f["physical_column"] for f in fields if f["physical_table"] == "listing"}
        identifiers = {f["physical_column"] for f in fields if f["physical_table"] == "listing_identifier"}
        self.assertEqual(EXPECTED_LISTING_COLUMNS, listing)
        self.assertEqual(EXPECTED_IDENTIFIER_COLUMNS, identifiers)
        ids = [f["field_id"] for f in fields]
        names = [f["technical_name"] for f in fields]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(names), len(set(names)))
        self.assertTrue(all(FIELD_ID_RE.fullmatch(v) for v in ids))

    def test_sedol_mapping_targets_exist_at_listing_identifier_level(self):
        _, fields = self.load()
        by_column = {f["physical_column"]: f for f in fields if f["physical_table"] == "listing_identifier"}
        self.assertEqual("OF_FUND_LISTING_IDENTIFIER_IDENTIFIER_VALUE", by_column["identifier_value"]["field_id"])
        self.assertEqual("OF_FUND_LISTING_IDENTIFIER_IDENTIFIER_SCHEME", by_column["identifier_scheme"]["field_id"])
        self.assertEqual("OF_FUND_LISTING_IDENTIFIER_NORMALIZED_VALUE", by_column["normalized_value"]["field_id"])
        for column in ("identifier_value", "identifier_scheme", "normalized_value"):
            self.assertEqual("LISTING_IDENTIFIER", by_column[column]["entity_code"])

    def test_every_field_has_governed_minimum_semantics_and_real_sql_column(self):
        _, fields = self.load()
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        required = {
            "field_id", "technical_name", "entity_code", "physical_schema",
            "physical_table", "physical_column", "data_type", "nullable",
            "definition_fr", "definition_en", "history_method", "source_role",
            "validation_rule", "normalization_rule", "provenance_path", "status",
        }
        for field in fields:
            self.assertTrue(required.issubset(field), field.get("field_id"))
            self.assertEqual("fund", field["physical_schema"])
            self.assertEqual("schemas/fund/019_share_class_listing_core.sql", field["provenance_path"])
            self.assertEqual("VALIDATED", field["status"])
            self.assertIn(field["physical_column"].lower(), sql)


if __name__ == "__main__":
    unittest.main()
