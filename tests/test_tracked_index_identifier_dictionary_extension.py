import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "data" / "dictionary" / "extensions" / "tracked_index_identifier_v1"


class TrackedIndexIdentifierDictionaryExtensionTests(unittest.TestCase):
    def test_extension_has_exact_physical_field_count(self):
        metadata = json.loads((EXT / "00_metadata.json").read_text(encoding="utf-8"))
        fields = json.loads((EXT / "10_fields.json").read_text(encoding="utf-8"))["fields"]
        self.assertEqual(16, metadata["field_count"])
        self.assertEqual(16, len(fields))
        self.assertEqual(16, len({f["field_id"] for f in fields}))

    def test_mapping_targets_are_present(self):
        fields = json.loads((EXT / "10_fields.json").read_text(encoding="utf-8"))["fields"]
        ids = {f["field_id"] for f in fields}
        self.assertTrue({
            "OF_FUND_TRACKED_INDEX_IDENTIFIER_IDENTIFIER_VALUE",
            "OF_FUND_TRACKED_INDEX_IDENTIFIER_IDENTIFIER_SCHEME",
            "OF_FUND_TRACKED_INDEX_IDENTIFIER_NORMALIZED_VALUE",
        }.issubset(ids))

    def test_all_fields_point_to_migration_038_table(self):
        fields = json.loads((EXT / "10_fields.json").read_text(encoding="utf-8"))["fields"]
        for field in fields:
            self.assertEqual("TRACKED_INDEX_IDENTIFIER", field["entity_code"])
            self.assertEqual("fund", field["physical_schema"])
            self.assertEqual("tracked_index_identifier", field["physical_table"])
            self.assertEqual("schemas/fund/038_tracked_index_identifiers.sql", field["provenance_path"])


if __name__ == "__main__":
    unittest.main()
