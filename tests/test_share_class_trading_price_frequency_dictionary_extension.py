import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "data" / "dictionary" / "extensions" / "share_class_trading_price_frequency_v1"


class ShareClassTradingPriceFrequencyDictionaryExtensionTests(unittest.TestCase):
    def test_extension_declares_exactly_one_additive_field(self):
        metadata = json.loads((PACKAGE / "00_metadata.json").read_text(encoding="utf-8"))
        payload = json.loads((PACKAGE / "10_fields.json").read_text(encoding="utf-8"))
        self.assertEqual(1, metadata["field_count"])
        self.assertEqual(1, len(payload["fields"]))
        field = payload["fields"][0]
        self.assertEqual("OF_FUND_SHARE_CLASS_PROFILE_TRADING_PRICE_FREQUENCY", field["field_id"])
        self.assertEqual("SHARE_CLASS_PROFILE", field["entity_code"])
        self.assertEqual("share_class_profile", field["physical_table"])
        self.assertEqual("trading_price_frequency", field["physical_column"])
        self.assertEqual("schemas/fund/025_share_class_trading_price_frequency.sql", field["provenance_path"])

    def test_extension_keeps_nav_and_trading_price_frequencies_distinct(self):
        payload = json.loads((PACKAGE / "10_fields.json").read_text(encoding="utf-8"))
        field = payload["fields"][0]
        self.assertNotEqual("nav_frequency", field["physical_column"])
        self.assertIn("distinct from NAV", field["definition_en"])


if __name__ == "__main__":
    unittest.main()
