import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "data" / "dictionary" / "extensions" / "fund_passive_flag_v1"


class FundPassiveFlagDictionaryExtensionTests(unittest.TestCase):
    def test_extension_contains_exactly_one_fund_profile_field(self):
        meta = json.loads((PKG / "00_metadata.json").read_text(encoding="utf-8"))
        fields = json.loads((PKG / "10_fields.json").read_text(encoding="utf-8"))["fields"]
        self.assertEqual(1, meta["field_count"])
        self.assertEqual(1, len(fields))
        field = fields[0]
        self.assertEqual("OF_FUND_FUND_PROFILE_IS_PASSIVE", field["field_id"])
        self.assertEqual("FUND_PROFILE", field["entity_code"])
        self.assertEqual("fund_profile", field["physical_table"])
        self.assertEqual("is_passive", field["physical_column"])
        self.assertEqual("boolean", field["data_type"])
        self.assertTrue(field["nullable"])


if __name__ == "__main__":
    unittest.main()
