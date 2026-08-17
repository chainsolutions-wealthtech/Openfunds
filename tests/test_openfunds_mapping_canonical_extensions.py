from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "data" / "dictionary" / "spec_v1"
LISTING = ROOT / "data" / "dictionary" / "extensions" / "listing_v1"


class OpenfundsMappingCanonicalExtensionTests(unittest.TestCase):
    def setUp(self):
        from scripts.validate_openfunds_mapping_registry import load_canonical_inventory
        self.load_canonical_inventory = load_canonical_inventory

    def test_core_and_listing_extension_are_unioned_without_rewriting_core(self):
        ids, entities, counts = self.load_canonical_inventory(CORE, [LISTING])
        self.assertEqual(143, counts["core"])
        self.assertEqual(34, counts["extensions"])
        self.assertEqual(177, counts["total"])
        self.assertEqual(177, len(ids))
        self.assertEqual("LISTING_IDENTIFIER", entities["OF_FUND_LISTING_IDENTIFIER_IDENTIFIER_VALUE"])
        self.assertEqual("LISTING", entities["OF_FUND_LISTING_VENUE_MIC"])

    def test_extension_collision_with_core_field_id_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            (path / "00_metadata.json").write_text(json.dumps({
                "dictionary_id": "TEST_COLLISION",
                "dictionary_version": "1.0.0",
                "status": "VALIDATED_LISTING_EXTENSION_SCOPE",
                "field_count": 1,
            }), encoding="utf-8")
            (path / "10_fields.json").write_text(json.dumps({"fields": [{
                "field_id": "OF_FUND_FUND_ENTITY_CANONICAL_CODE",
                "entity_code": "LISTING",
            }]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate canonical FIELD_ID"):
                self.load_canonical_inventory(CORE, [path])

    def test_extension_declared_count_must_match_payload(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            (path / "00_metadata.json").write_text(json.dumps({
                "dictionary_id": "TEST_COUNT",
                "dictionary_version": "1.0.0",
                "status": "VALIDATED_LISTING_EXTENSION_SCOPE",
                "field_count": 2,
            }), encoding="utf-8")
            (path / "10_fields.json").write_text(json.dumps({"fields": [{
                "field_id": "OF_FUND_LISTING_TEST_FIELD",
                "entity_code": "LISTING",
            }]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "field_count mismatch"):
                self.load_canonical_inventory(CORE, [path])


if __name__ == "__main__":
    unittest.main()
