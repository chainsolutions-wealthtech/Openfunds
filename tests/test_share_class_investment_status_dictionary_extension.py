import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "data" / "dictionary" / "extensions" / "share_class_investment_status_v1"
EXPECTED = {
    "OF_FUND_SHARE_CLASS_PROFILE_INVESTMENT_STATUS",
    "OF_FUND_SHARE_CLASS_PROFILE_INVESTMENT_STATUS_DESCRIPTION",
    "OF_FUND_SHARE_CLASS_PROFILE_INVESTMENT_STATUS_DATE",
    "OF_FUND_SHARE_CLASS_PROFILE_INVESTMENT_STATUS_DATE_STATUS",
}


class ShareClassInvestmentStatusDictionaryExtensionTests(unittest.TestCase):
    def test_extension_contains_exactly_four_fields(self):
        metadata = json.loads((EXT / "00_metadata.json").read_text(encoding="utf-8"))
        fields = json.loads((EXT / "10_fields.json").read_text(encoding="utf-8"))["fields"]
        self.assertEqual(4, metadata["field_count"])
        self.assertEqual(4, len(fields))
        self.assertEqual(EXPECTED, {f["field_id"] for f in fields})
        self.assertTrue(all(f["physical_table"] == "share_class_profile" for f in fields))


if __name__ == "__main__":
    unittest.main()
