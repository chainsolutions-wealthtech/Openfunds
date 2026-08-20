import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "data" / "dictionary" / "extensions" / "fund_replication_methodology_v1"


class FundReplicationMethodologyDictionaryExtensionTests(unittest.TestCase):
    def test_extension_has_one_profile_field_and_fifteen_relation_fields(self):
        meta = json.loads((PKG / "00_metadata.json").read_text(encoding="utf-8"))
        fields = json.loads((PKG / "10_fields.json").read_text(encoding="utf-8"))["fields"]
        self.assertEqual(16, meta["field_count"])
        self.assertEqual(16, len(fields))
        ids = {f["field_id"] for f in fields}
        self.assertIn("OF_FUND_FUND_PROFILE_REPLICATION_METHODOLOGY_FIRST_LEVEL", ids)
        self.assertIn("OF_FUND_REPLICATION_METHODOLOGY_DETAIL_DETAIL_CODE", ids)
        self.assertEqual(16, len(ids))

    def test_second_level_is_a_relation_not_a_pipe_string_field(self):
        fields = json.loads((PKG / "10_fields.json").read_text(encoding="utf-8"))["fields"]
        detail = next(f for f in fields if f["field_id"] == "OF_FUND_REPLICATION_METHODOLOGY_DETAIL_DETAIL_CODE")
        self.assertEqual("REPLICATION_METHODOLOGY_DETAIL", detail["entity_code"])
        self.assertEqual("replication_methodology_detail", detail["physical_table"])
        self.assertEqual("detail_code", detail["physical_column"])
        self.assertNotIn("pipe", detail["technical_name"].lower())


if __name__ == "__main__":
    unittest.main()
