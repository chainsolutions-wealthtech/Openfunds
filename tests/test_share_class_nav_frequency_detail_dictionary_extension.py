import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "data" / "dictionary" / "extensions" / "share_class_nav_frequency_detail_v1"


class ShareClassNavFrequencyDetailDictionaryExtensionTests(unittest.TestCase):
    def test_extension_declares_exactly_one_field(self):
        metadata = json.loads((PACKAGE / "00_metadata.json").read_text(encoding="utf-8"))
        payload = json.loads((PACKAGE / "10_fields.json").read_text(encoding="utf-8"))
        self.assertEqual(1, metadata["field_count"])
        self.assertEqual(1, len(payload["fields"]))
        field = payload["fields"][0]
        self.assertEqual("OF_FUND_SHARE_CLASS_PROFILE_NAV_FREQUENCY_DETAIL", field["field_id"])
        self.assertEqual("SHARE_CLASS_PROFILE", field["entity_code"])
        self.assertEqual("share_class_profile", field["physical_table"])
        self.assertEqual("nav_frequency_detail", field["physical_column"])
        self.assertEqual("schemas/fund/026_share_class_nav_frequency_detail.sql", field["provenance_path"])

    def test_detail_is_source_preserving_and_not_a_second_frequency_code(self):
        payload = json.loads((PACKAGE / "10_fields.json").read_text(encoding="utf-8"))
        field = payload["fields"][0]
        self.assertEqual("text", field["data_type"])
        self.assertIn("PRESERVE_SOURCE_TEXT", field["normalization_rule"])
        self.assertNotEqual("nav_frequency", field["physical_column"])


if __name__ == "__main__":
    unittest.main()
