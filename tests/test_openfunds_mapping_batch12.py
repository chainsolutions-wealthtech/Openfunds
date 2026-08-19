import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "openfunds" / "mapping" / "v2.13.0" / "MAPPING_REGISTRY.csv"
SOURCE_SHA = "40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4"
EXTERNAL_ID = "OFST020300"
MAPPING_ID = "MAP-000038"
TARGET = "OF_FUND_SHARE_CLASS_PROFILE_NAV_FREQUENCY"


def read_rows():
    with REGISTRY.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


class OpenfundsMappingBatch12ContractTests(unittest.TestCase):
    def test_valuation_frequency_maps_to_existing_nav_frequency(self):
        selected = [row for row in read_rows() if row["MAPPING_ID"] == MAPPING_ID]
        self.assertEqual(1, len(selected))
        row = selected[0]
        self.assertEqual(EXTERNAL_ID, row["EXTERNAL_FIELD_ID"])
        self.assertEqual(TARGET, row["CANONICAL_FIELD_ID"])
        self.assertEqual("SHARE_CLASS_PROFILE", row["CANONICAL_ENTITY"])
        self.assertEqual("TRANSFORMED", row["MAPPING_STATUS"])
        self.assertEqual("OPENFUNDS_FREQUENCY_TO_CANONICAL_CODE", row["TRANSFORMATION_RULE"])
        self.assertEqual("NONE", row["INFORMATION_LOSS"])
        self.assertEqual("YES", row["IMPORT_SUPPORTED"])
        self.assertEqual("YES", row["EXPORT_SUPPORTED"])
        self.assertEqual("VALIDATED", row["VALIDATION_STATUS"])
        self.assertEqual(SOURCE_SHA, row["SOURCE_SHA256"])
        self.assertEqual(f"official:v2.13.0:{EXTERNAL_ID}", row["SOURCE_REFERENCE"])
        self.assertIn("DAILY", row["NOTES"])
        self.assertIn("AT_LEAST_ANNUALLY", row["NOTES"])
        self.assertIn("REVERSIBLE", row["NOTES"])

    def test_valuation_frequency_uses_no_parallel_frequency_field(self):
        rows = [row for row in read_rows() if row["EXTERNAL_FIELD_ID"] == EXTERNAL_ID]
        self.assertEqual({TARGET}, {row["CANONICAL_FIELD_ID"] for row in rows})

    def test_batch12_is_forward_compatible(self):
        rows = read_rows()
        self.assertGreaterEqual(len(rows), 38)
        self.assertEqual(len(rows), len({row["MAPPING_ID"] for row in rows}))


if __name__ == "__main__":
    unittest.main()
