import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "data" / "dictionary" / "extensions" / "tracked_index_denomination_base_v1"


class TrackedIndexDenominationBaseDictionaryExtensionTests(unittest.TestCase):
    def test_extension_has_one_noncolliding_field(self):
        metadata = json.loads((EXT / "00_metadata.json").read_text(encoding="utf-8"))
        fields = json.loads((EXT / "10_fields.json").read_text(encoding="utf-8"))["fields"]
        self.assertEqual(1, metadata["field_count"])
        self.assertEqual(1, len(fields))
        field = fields[0]
        self.assertEqual("OF_FUND_SHARE_CLASS_TRACKED_INDEX_DENOMINATION_BASE", field["field_id"])
        self.assertEqual("SHARE_CLASS_TRACKED_INDEX", field["entity_code"])
        self.assertEqual("share_class_tracked_index", field["physical_table"])
        self.assertEqual("denomination_base", field["physical_column"])
        self.assertEqual("schemas/fund/039_tracked_index_denomination_base.sql", field["provenance_path"])


if __name__ == "__main__":
    unittest.main()
