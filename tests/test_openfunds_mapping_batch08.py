import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "openfunds" / "mapping" / "v2.13.0" / "MAPPING_REGISTRY.csv"
SOURCE_SHA = "40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4"
EXTERNAL_ID = "OFST062045"
MAPPING_ID = "MAP-000022"
TARGET = "OF_FUND_LISTING_LISTING_STATUS"


def read_rows():
    with REGISTRY.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


class OpenfundsMappingBatch08ContractTests(unittest.TestCase):
    def test_listing_status_maps_to_dedicated_business_status(self):
        selected = [row for row in read_rows() if row["MAPPING_ID"] == MAPPING_ID]
        self.assertEqual(1, len(selected))
        row = selected[0]
        self.assertEqual(EXTERNAL_ID, row["EXTERNAL_FIELD_ID"])
        self.assertEqual(TARGET, row["CANONICAL_FIELD_ID"])
        self.assertEqual("LISTING", row["CANONICAL_ENTITY"])
        self.assertEqual("TRANSFORMED", row["MAPPING_STATUS"])
        self.assertEqual("OPENFUNDS_LISTING_STATUS_TO_CANONICAL_ENUM", row["TRANSFORMATION_RULE"])
        self.assertEqual("NONE", row["INFORMATION_LOSS"])
        self.assertEqual("YES", row["IMPORT_SUPPORTED"])
        self.assertEqual("YES", row["EXPORT_SUPPORTED"])
        self.assertEqual("VALIDATED", row["VALIDATION_STATUS"])
        self.assertEqual(SOURCE_SHA, row["SOURCE_SHA256"])
        self.assertEqual(f"official:v2.13.0:{EXTERNAL_ID}", row["SOURCE_REFERENCE"])
        self.assertIn("EXPLICIT_SOURCE_VALUE_ONLY", row["NOTES"])
        self.assertIn("NO_DEFAULT_ACTIVE_ON_ABSENCE", row["NOTES"])

    def test_listing_status_never_maps_to_bitemporal_is_current(self):
        rows = [row for row in read_rows() if row["EXTERNAL_FIELD_ID"] == EXTERNAL_ID]
        targets = {row["CANONICAL_FIELD_ID"] for row in rows}
        self.assertEqual({TARGET}, targets)
        self.assertNotIn("OF_FUND_LISTING_IS_CURRENT", targets)

    def test_batch08_contract_survives_future_batches(self):
        rows = read_rows()
        mapping_ids = [row["MAPPING_ID"] for row in rows]
        self.assertEqual(len(mapping_ids), len(set(mapping_ids)))
        self.assertIn(MAPPING_ID, set(mapping_ids))


if __name__ == "__main__":
    unittest.main()
