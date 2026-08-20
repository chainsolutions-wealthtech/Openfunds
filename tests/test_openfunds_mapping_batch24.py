import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "openfunds" / "mapping" / "v2.13.0" / "MAPPING_REGISTRY.csv"
EXPECTED = {
    "OF_FUND_BENCHMARK_COMPONENT_IDENTIFIER_IDENTIFIER_VALUE": "PIPE_ALIGNED_BLOOMBERG_TICKER_IDENTITY",
    "OF_FUND_BENCHMARK_COMPONENT_IDENTIFIER_IDENTIFIER_SCHEME": "CONSTANT_BLOOMBERG",
    "OF_FUND_BENCHMARK_COMPONENT_IDENTIFIER_NORMALIZED_VALUE": "PIPE_ALIGNED_TRIM_ONLY_BLOOMBERG",
}


class OpenfundsMappingBatch24Tests(unittest.TestCase):
    def _rows(self):
        with REGISTRY.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle, delimiter=";"))

    def test_benchmark_bloomberg_tickers_align_to_component_order(self):
        matches = [r for r in self._rows() if r["EXTERNAL_FIELD_ID"] == "OFST023205"]
        self.assertEqual(3, len(matches))
        self.assertEqual(set(EXPECTED), {r["CANONICAL_FIELD_ID"] for r in matches})
        for row in matches:
            self.assertEqual("BENCHMARK_COMPONENT_IDENTIFIER", row["CANONICAL_ENTITY"])
            self.assertEqual("ONE_TO_MANY", row["MAPPING_STATUS"])
            self.assertEqual(EXPECTED[row["CANONICAL_FIELD_ID"]], row["TRANSFORMATION_RULE"])
            self.assertEqual("NO", row["IMPORT_SUPPORTED"])
            self.assertEqual("NO", row["EXPORT_SUPPORTED"])
            self.assertIn("BENCHMARK_COMPONENT_ORDER_ALIGNMENT_REQUIRED", row["NOTES"])
            self.assertIn("PROPRIETARY_IDENTIFIER_USAGE_REVIEW_REQUIRED", row["NOTES"])

    def test_project_gate_is_not_misattributed_to_openfunds(self):
        matches = [r for r in self._rows() if r["EXTERNAL_FIELD_ID"] == "OFST023205"]
        for row in matches:
            self.assertNotIn("OPENFUNDS_LICENSE_WARNING", row["NOTES"])

    def test_mapping_ids_remain_unique(self):
        rows = self._rows()
        ids = [r["MAPPING_ID"] for r in rows]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(rows), 82)


if __name__ == "__main__":
    unittest.main()
