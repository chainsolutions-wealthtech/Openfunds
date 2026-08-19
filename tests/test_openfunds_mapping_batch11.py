import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "openfunds" / "mapping" / "v2.13.0" / "MAPPING_REGISTRY.csv"
SOURCE_SHA = "40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4"
EXTERNAL_ID = "OFST062020"
MAPPING_ID = "MAP-000037"
TARGET = "OF_FUND_LISTING_INCEPTION_PRICE"


def read_rows():
    with REGISTRY.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


class OpenfundsMappingBatch11ContractTests(unittest.TestCase):
    def test_inception_price_maps_to_listing_inception_price(self):
        selected = [row for row in read_rows() if row["MAPPING_ID"] == MAPPING_ID]
        self.assertEqual(1, len(selected))
        row = selected[0]
        self.assertEqual(EXTERNAL_ID, row["EXTERNAL_FIELD_ID"])
        self.assertEqual(TARGET, row["CANONICAL_FIELD_ID"])
        self.assertEqual("LISTING", row["CANONICAL_ENTITY"])
        self.assertEqual("DIRECT", row["MAPPING_STATUS"])
        self.assertEqual("DECIMAL_IDENTITY", row["TRANSFORMATION_RULE"])
        self.assertEqual("NONE", row["INFORMATION_LOSS"])
        self.assertEqual("YES", row["IMPORT_SUPPORTED"])
        self.assertEqual("YES", row["EXPORT_SUPPORTED"])
        self.assertEqual("VALIDATED", row["VALIDATION_STATUS"])
        self.assertEqual(SOURCE_SHA, row["SOURCE_SHA256"])
        self.assertEqual(f"official:v2.13.0:{EXTERNAL_ID}", row["SOURCE_REFERENCE"])
        self.assertIn("NO_CURRENCY_INFERENCE", row["NOTES"])
        self.assertIn("NO_QUOTE_FACTOR_INFERENCE", row["NOTES"])

    def test_inception_price_does_not_map_to_currency_or_quote_factor(self):
        rows = [row for row in read_rows() if row["EXTERNAL_FIELD_ID"] == EXTERNAL_ID]
        targets = {row["CANONICAL_FIELD_ID"] for row in rows}
        self.assertEqual({TARGET}, targets)

    def test_batch11_is_forward_compatible(self):
        rows = read_rows()
        self.assertGreaterEqual(len(rows), 37)
        self.assertEqual(len(rows), len({row["MAPPING_ID"] for row in rows}))


if __name__ == "__main__":
    unittest.main()
