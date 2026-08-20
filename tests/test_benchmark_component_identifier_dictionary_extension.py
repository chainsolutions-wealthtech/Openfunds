import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "data" / "dictionary" / "extensions" / "benchmark_component_identifier_v1"


class BenchmarkComponentIdentifierDictionaryExtensionTests(unittest.TestCase):
    def test_extension_contains_sixteen_unique_relation_fields(self):
        meta = json.loads((PKG / "00_metadata.json").read_text(encoding="utf-8"))
        fields = json.loads((PKG / "10_fields.json").read_text(encoding="utf-8"))["fields"]
        self.assertEqual(16, meta["field_count"])
        self.assertEqual(16, len(fields))
        ids = {f["field_id"] for f in fields}
        self.assertEqual(16, len(ids))
        for required in (
            "OF_FUND_BENCHMARK_COMPONENT_IDENTIFIER_IDENTIFIER_SCHEME",
            "OF_FUND_BENCHMARK_COMPONENT_IDENTIFIER_IDENTIFIER_VALUE",
            "OF_FUND_BENCHMARK_COMPONENT_IDENTIFIER_NORMALIZED_VALUE",
        ):
            self.assertIn(required, ids)
        self.assertTrue(all(f["entity_code"] == "BENCHMARK_COMPONENT_IDENTIFIER" for f in fields))


if __name__ == "__main__":
    unittest.main()
