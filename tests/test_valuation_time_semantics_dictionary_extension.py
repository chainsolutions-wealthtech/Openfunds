import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "data" / "dictionary" / "extensions" / "valuation_time_semantics_v1"
EXPECTED = {
    "OF_FUND_FUND_PROFILE_VALUATION_POINT_TIME",
    "OF_FUND_FUND_PROFILE_VALUATION_TIMEZONE_LABEL",
    "OF_FUND_FUND_PROFILE_VALUATION_TIMEZONE_IANA",
    "OF_FUND_SHARE_CLASS_PROFILE_NAV_PUBLICATION_TIME",
}


class ValuationTimeSemanticsDictionaryExtensionTests(unittest.TestCase):
    def test_extension_declares_exactly_four_fields(self):
        metadata = json.loads((PACKAGE / "00_metadata.json").read_text(encoding="utf-8"))
        payload = json.loads((PACKAGE / "10_fields.json").read_text(encoding="utf-8"))
        self.assertEqual(4, metadata["field_count"])
        self.assertEqual(4, len(payload["fields"]))
        self.assertEqual(EXPECTED, {field["field_id"] for field in payload["fields"]})

    def test_timezone_label_and_iana_have_distinct_automation_semantics(self):
        payload = json.loads((PACKAGE / "10_fields.json").read_text(encoding="utf-8"))
        by_id = {field["field_id"]: field for field in payload["fields"]}
        label = by_id["OF_FUND_FUND_PROFILE_VALUATION_TIMEZONE_LABEL"]
        iana = by_id["OF_FUND_FUND_PROFILE_VALUATION_TIMEZONE_IANA"]
        self.assertIn("NOT_AUTOMATION_SAFE", label["validation_rule"])
        self.assertIn("IANA_TZ_DATABASE_IDENTIFIER", iana["validation_rule"])


if __name__ == "__main__":
    unittest.main()
