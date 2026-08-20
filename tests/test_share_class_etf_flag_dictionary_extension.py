import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "data" / "dictionary" / "extensions" / "share_class_etf_flag_v1"


class ShareClassEtfFlagDictionaryExtensionTests(unittest.TestCase):
    def test_extension_contains_exactly_one_share_class_field(self):
        metadata = json.loads((EXT / "00_metadata.json").read_text(encoding="utf-8"))
        fields = json.loads((EXT / "10_fields.json").read_text(encoding="utf-8"))["fields"]
        self.assertEqual(1, metadata["field_count"])
        self.assertEqual(1, len(fields))
        field = fields[0]
        self.assertEqual("OF_FUND_SHARE_CLASS_PROFILE_IS_ETF", field["field_id"])
        self.assertEqual("share_class_profile", field["physical_table"])
        self.assertEqual("is_etf", field["physical_column"])
        self.assertEqual("boolean", field["data_type"])


if __name__ == "__main__":
    unittest.main()
