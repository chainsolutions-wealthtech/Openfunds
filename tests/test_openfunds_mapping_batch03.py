import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "openfunds" / "mapping" / "v2.13.0" / "MAPPING_REGISTRY.csv"
SOURCE_SHA = "40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4"

EXPECTED = {
    "MAP-000007": ("OFST020010", "OF_FUND_FUND_ENTITY_IDENTIFIER_IDENTIFIER_VALUE", "INTEGER_TO_DECIMAL_STRING"),
    "MAP-000008": ("OFST020010", "OF_FUND_FUND_ENTITY_IDENTIFIER_IDENTIFIER_SCHEME", "CONSTANT_VALOR"),
    "MAP-000009": ("OFST020010", "OF_FUND_FUND_ENTITY_IDENTIFIER_NORMALIZED_VALUE", "INTEGER_TO_DECIMAL_STRING"),
    "MAP-000010": ("OFST020015", "OF_FUND_FUND_ENTITY_IDENTIFIER_IDENTIFIER_VALUE", "IDENTITY"),
    "MAP-000011": ("OFST020015", "OF_FUND_FUND_ENTITY_IDENTIFIER_IDENTIFIER_SCHEME", "CONSTANT_WKN"),
    "MAP-000012": ("OFST020015", "OF_FUND_FUND_ENTITY_IDENTIFIER_NORMALIZED_VALUE", "TRIM_AND_UPPERCASE_WKN"),
}


def read_rows():
    with REGISTRY.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


class OpenfundsMappingBatch03ContractTests(unittest.TestCase):
    def test_exact_batch03_rows_exist(self):
        selected = {row["MAPPING_ID"]: row for row in read_rows() if row["MAPPING_ID"] in EXPECTED}
        self.assertEqual(set(EXPECTED), set(selected))
        for mapping_id, (external_id, canonical_id, rule) in EXPECTED.items():
            row = selected[mapping_id]
            self.assertEqual(external_id, row["EXTERNAL_FIELD_ID"], mapping_id)
            self.assertEqual(canonical_id, row["CANONICAL_FIELD_ID"], mapping_id)
            self.assertEqual("FUND_ENTITY_IDENTIFIER", row["CANONICAL_ENTITY"], mapping_id)
            self.assertEqual("ONE_TO_MANY", row["MAPPING_STATUS"], mapping_id)
            self.assertEqual(rule, row["TRANSFORMATION_RULE"], mapping_id)
            self.assertEqual("NONE", row["INFORMATION_LOSS"], mapping_id)
            self.assertEqual("YES", row["IMPORT_SUPPORTED"], mapping_id)
            self.assertEqual("YES", row["EXPORT_SUPPORTED"], mapping_id)
            self.assertEqual("VALIDATED", row["VALIDATION_STATUS"], mapping_id)
            self.assertEqual(SOURCE_SHA, row["SOURCE_SHA256"], mapping_id)
            self.assertEqual(f"official:v2.13.0:{external_id}", row["SOURCE_REFERENCE"], mapping_id)

    def test_sedol_listing_field_is_not_forced_into_fund_entity_identifier(self):
        rows = read_rows()
        self.assertFalse(any(row["EXTERNAL_FIELD_ID"] == "OFST020040" for row in rows))

    def test_batch03_exact_cumulative_post_state(self):
        rows = read_rows()
        self.assertEqual(12, len(rows))
        self.assertEqual(6, len({row["EXTERNAL_FIELD_ID"] for row in rows}))
        self.assertEqual(6, len({row["CANONICAL_FIELD_ID"] for row in rows}))
        self.assertEqual(12, len({row["MAPPING_ID"] for row in rows}))


if __name__ == "__main__":
    unittest.main()
