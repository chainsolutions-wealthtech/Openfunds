import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "data" / "dictionary" / "extensions" / "share_class_benchmark_component_v1"


class ShareClassBenchmarkComponentDictionaryExtensionTests(unittest.TestCase):
    def test_extension_contains_seventeen_unique_relation_fields(self):
        meta = json.loads((PKG / "00_metadata.json").read_text(encoding="utf-8"))
        fields = json.loads((PKG / "10_fields.json").read_text(encoding="utf-8"))["fields"]
        self.assertEqual(17, meta["field_count"])
        self.assertEqual(17, len(fields))
        ids = {f["field_id"] for f in fields}
        self.assertEqual(17, len(ids))
        self.assertIn("OF_FUND_SHARE_CLASS_BENCHMARK_COMPONENT_COMPONENT_ORDER", ids)
        self.assertIn("OF_FUND_SHARE_CLASS_BENCHMARK_COMPONENT_COMPONENT_NAME", ids)
        self.assertIn("OF_FUND_SHARE_CLASS_BENCHMARK_COMPONENT_COMPONENT_WEIGHT", ids)
        self.assertTrue(all(f["entity_code"] == "SHARE_CLASS_BENCHMARK_COMPONENT" for f in fields))


if __name__ == "__main__":
    unittest.main()
