import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "data" / "dictionary" / "extensions" / "share_class_multicurrency_dealing_v1"


class ShareClassMulticurrencyDictionaryExtensionTests(unittest.TestCase):
    def test_extension_matches_migration_028_physical_surface(self):
        metadata = json.loads((PACKAGE / "00_metadata.json").read_text(encoding="utf-8"))
        payload = json.loads((PACKAGE / "10_fields.json").read_text(encoding="utf-8"))
        self.assertEqual(16, metadata["field_count"])
        self.assertEqual(16, len(payload["fields"]))
        ids = {field["field_id"] for field in payload["fields"]}
        self.assertIn("OF_FUND_SHARE_CLASS_PROFILE_IS_MULTICURRENCY", ids)
        self.assertIn("OF_FUND_SHARE_CLASS_DEALING_CURRENCY_CURRENCY_ID", ids)
        self.assertEqual(len(ids), len(payload["fields"]))

    def test_reference_currency_and_additional_dealing_currency_are_distinct(self):
        payload = json.loads((PACKAGE / "10_fields.json").read_text(encoding="utf-8"))
        by_id = {field["field_id"]: field for field in payload["fields"]}
        additional = by_id["OF_FUND_SHARE_CLASS_DEALING_CURRENCY_CURRENCY_ID"]
        self.assertEqual("share_class_dealing_currency", additional["physical_table"])
        self.assertIn("distinct from the Share Class reference/NAV currency", additional["definition_en"])


if __name__ == "__main__":
    unittest.main()
