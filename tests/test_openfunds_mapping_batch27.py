import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "openfunds" / "mapping" / "v2.13.0" / "MAPPING_REGISTRY.csv"


class OpenfundsMappingBatch27Tests(unittest.TestCase):
    def _rows(self):
        with REGISTRY.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle, delimiter=";"))

    def test_denomination_base_maps_directly_without_price_or_index_inference(self):
        rows = [r for r in self._rows() if r["EXTERNAL_FIELD_ID"] == "OFST023850"]
        self.assertEqual(1, len(rows))
        row = rows[0]
        self.assertEqual("OF_FUND_SHARE_CLASS_TRACKED_INDEX_DENOMINATION_BASE", row["CANONICAL_FIELD_ID"])
        self.assertEqual("SHARE_CLASS_TRACKED_INDEX", row["CANONICAL_ENTITY"])
        self.assertEqual("DIRECT", row["MAPPING_STATUS"])
        self.assertEqual("POSITIVE_DECIMAL_IDENTITY", row["TRANSFORMATION_RULE"])
        self.assertEqual("NONE", row["INFORMATION_LOSS"])
        self.assertEqual("YES", row["IMPORT_SUPPORTED"])
        self.assertEqual("YES", row["EXPORT_SUPPORTED"])
        self.assertIn("FUND_PRICE_DIVIDED_BY_INDEX", row["NOTES"])
        self.assertIn("NO_PRICE_INFERENCE", row["NOTES"])
        self.assertIn("NO_INDEX_LEVEL_INFERENCE", row["NOTES"])

    def test_mapping_ids_remain_unique_and_forward_compatible(self):
        rows = self._rows()
        ids = [r["MAPPING_ID"] for r in rows]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(rows), 93)


if __name__ == "__main__":
    unittest.main()
