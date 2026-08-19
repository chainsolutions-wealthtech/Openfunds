import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "openfunds" / "mapping" / "v2.13.0" / "MAPPING_REGISTRY.csv"
SOURCE_SHA = "40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4"
EXTERNAL_ID = "OFST020305"
MAPPING_ID = "MAP-000040"
TARGET = "OF_FUND_SHARE_CLASS_PROFILE_NAV_FREQUENCY_DETAIL"


def read_rows():
    with REGISTRY.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


class OpenfundsMappingBatch14ContractTests(unittest.TestCase):
    def test_nav_frequency_detail_maps_to_source_preserving_detail_field(self):
        selected = [row for row in read_rows() if row["MAPPING_ID"] == MAPPING_ID]
        self.assertEqual(1, len(selected))
        row = selected[0]
        self.assertEqual(EXTERNAL_ID, row["EXTERNAL_FIELD_ID"])
        self.assertEqual(TARGET, row["CANONICAL_FIELD_ID"])
        self.assertEqual("SHARE_CLASS_PROFILE", row["CANONICAL_ENTITY"])
        self.assertEqual("DIRECT", row["MAPPING_STATUS"])
        self.assertEqual("TRIM_OUTER_WHITESPACE_PRESERVE_SOURCE_TEXT", row["TRANSFORMATION_RULE"])
        self.assertEqual("NONE", row["INFORMATION_LOSS"])
        self.assertEqual("YES", row["IMPORT_SUPPORTED"])
        self.assertEqual("YES", row["EXPORT_SUPPORTED"])
        self.assertEqual("VALIDATED", row["VALIDATION_STATUS"])
        self.assertEqual(SOURCE_SHA, row["SOURCE_SHA256"])
        self.assertEqual(f"official:v2.13.0:{EXTERNAL_ID}", row["SOURCE_REFERENCE"])

    def test_detail_does_not_replace_nav_frequency(self):
        rows = [row for row in read_rows() if row["EXTERNAL_FIELD_ID"] == EXTERNAL_ID]
        self.assertEqual({TARGET}, {row["CANONICAL_FIELD_ID"] for row in rows})

    def test_registry_remains_unique_and_forward_compatible(self):
        rows = read_rows()
        self.assertGreaterEqual(len(rows), 40)
        self.assertEqual(len(rows), len({row["MAPPING_ID"] for row in rows}))


if __name__ == "__main__":
    unittest.main()
