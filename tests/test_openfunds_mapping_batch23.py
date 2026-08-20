import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "openfunds" / "mapping" / "v2.13.0" / "MAPPING_REGISTRY.csv"
EXPECTED = {
    "OF_FUND_SHARE_CLASS_BENCHMARK_COMPONENT_COMPONENT_ORDER": "PIPE_POSITION_TO_ONE_BASED_COMPONENT_ORDER",
    "OF_FUND_SHARE_CLASS_BENCHMARK_COMPONENT_COMPONENT_NAME": "PARSE_BENCHMARK_COMPONENT_NAME_PRESERVE_TEXT",
    "OF_FUND_SHARE_CLASS_BENCHMARK_COMPONENT_COMPONENT_WEIGHT": "PARSE_OPTIONAL_BRACKETED_COMPONENT_WEIGHT",
}


class OpenfundsMappingBatch23Tests(unittest.TestCase):
    def _rows(self):
        with REGISTRY.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle, delimiter=";"))

    def test_benchmark_is_normalized_to_ordered_component_rows(self):
        matches = [r for r in self._rows() if r["EXTERNAL_FIELD_ID"] == "OFST023200"]
        self.assertEqual(3, len(matches))
        self.assertEqual(set(EXPECTED), {r["CANONICAL_FIELD_ID"] for r in matches})
        for row in matches:
            self.assertEqual("SHARE_CLASS_BENCHMARK_COMPONENT", row["CANONICAL_ENTITY"])
            self.assertEqual("ONE_TO_MANY", row["MAPPING_STATUS"])
            self.assertEqual(EXPECTED[row["CANONICAL_FIELD_ID"]], row["TRANSFORMATION_RULE"])
            self.assertEqual("NONE", row["INFORMATION_LOSS"])
            self.assertIn("NO_PIPE_STRING_STORAGE", row["NOTES"])

    def test_no_vendor_ticker_is_included_in_batch_23(self):
        self.assertFalse(any(r["EXTERNAL_FIELD_ID"] == "OFST023205" for r in self._rows()))

    def test_mapping_ids_remain_unique(self):
        rows = self._rows()
        ids = [r["MAPPING_ID"] for r in rows]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(rows), 79)


if __name__ == "__main__":
    unittest.main()
