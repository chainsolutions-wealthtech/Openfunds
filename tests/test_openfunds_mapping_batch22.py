import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "openfunds" / "mapping" / "v2.13.0" / "MAPPING_REGISTRY.csv"


class OpenfundsMappingBatch22Tests(unittest.TestCase):
    def _rows(self):
        with REGISTRY.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle, delimiter=";"))

    def test_first_level_maps_to_fund_profile_enum(self):
        matches = [r for r in self._rows() if r["EXTERNAL_FIELD_ID"] == "OFST010900"]
        self.assertEqual(1, len(matches))
        row = matches[0]
        self.assertEqual("OF_FUND_FUND_PROFILE_REPLICATION_METHODOLOGY_FIRST_LEVEL", row["CANONICAL_FIELD_ID"])
        self.assertEqual("FUND_PROFILE", row["CANONICAL_ENTITY"])
        self.assertEqual("OPENFUNDS_REPLICATION_FIRST_LEVEL_TO_CANONICAL_ENUM", row["TRANSFORMATION_RULE"])
        self.assertEqual("NONE", row["INFORMATION_LOSS"])

    def test_second_level_splits_pipe_values_into_relation_rows(self):
        matches = [r for r in self._rows() if r["EXTERNAL_FIELD_ID"] == "OFST010901"]
        self.assertEqual(1, len(matches))
        row = matches[0]
        self.assertEqual("OF_FUND_REPLICATION_METHODOLOGY_DETAIL_DETAIL_CODE", row["CANONICAL_FIELD_ID"])
        self.assertEqual("REPLICATION_METHODOLOGY_DETAIL", row["CANONICAL_ENTITY"])
        self.assertEqual("ONE_TO_MANY", row["MAPPING_STATUS"])
        self.assertEqual("PIPE_SEPARATED_REPLICATION_DETAILS_TO_CANONICAL_ROWS", row["TRANSFORMATION_RULE"])
        self.assertIn("OFST010900_CONTEXT_REQUIRED", row["NOTES"])
        self.assertIn("NO_PIPE_STRING_STORAGE", row["NOTES"])

    def test_mapping_ids_remain_unique(self):
        rows = self._rows()
        ids = [r["MAPPING_ID"] for r in rows]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(rows), 76)


if __name__ == "__main__":
    unittest.main()
