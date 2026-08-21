import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "data" / "dictionary" / "extensions" / "share_class_tracked_index_v1"


class ShareClassTrackedIndexDictionaryExtensionTests(unittest.TestCase):
    def test_extension_has_exact_physical_field_count(self):
        metadata = json.loads((EXT / "00_metadata.json").read_text(encoding="utf-8"))
        fields = json.loads((EXT / "10_fields.json").read_text(encoding="utf-8"))["fields"]
        self.assertEqual(18, metadata["field_count"])
        self.assertEqual(18, len(fields))
        self.assertEqual(18, len({f["field_id"] for f in fields}))

    def test_mapping_targets_are_present(self):
        fields = json.loads((EXT / "10_fields.json").read_text(encoding="utf-8"))["fields"]
        ids = {f["field_id"] for f in fields}
        self.assertTrue({
            "OF_FUND_SHARE_CLASS_TRACKED_INDEX_INDEX_NAME",
            "OF_FUND_SHARE_CLASS_TRACKED_INDEX_INDEX_CURRENCY_ID",
            "OF_FUND_SHARE_CLASS_TRACKED_INDEX_INDEX_CURRENCY_MODE",
            "OF_FUND_SHARE_CLASS_TRACKED_INDEX_INDEX_TYPE",
        }.issubset(ids))

    def test_all_fields_point_to_migration_037_table(self):
        fields = json.loads((EXT / "10_fields.json").read_text(encoding="utf-8"))["fields"]
        for field in fields:
            self.assertEqual("SHARE_CLASS_TRACKED_INDEX", field["entity_code"])
            self.assertEqual("fund", field["physical_schema"])
            self.assertEqual("share_class_tracked_index", field["physical_table"])
            self.assertEqual("schemas/fund/037_share_class_tracked_index.sql", field["provenance_path"])


if __name__ == "__main__":
    unittest.main()
