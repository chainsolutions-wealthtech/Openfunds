import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "openfunds" / "mapping" / "v2.13.0" / "MAPPING_REGISTRY.csv"
SOURCE_SHA = "40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4"

EXPECTED = {
    "MAP-000014": ("OF_FUND_LISTING_IDENTIFIER_IDENTIFIER_VALUE", "IDENTITY"),
    "MAP-000015": ("OF_FUND_LISTING_IDENTIFIER_IDENTIFIER_SCHEME", "CONSTANT_SEDOL"),
    "MAP-000016": ("OF_FUND_LISTING_IDENTIFIER_NORMALIZED_VALUE", "TRIM_AND_UPPERCASE_SEDOL"),
}


def read_rows():
    with REGISTRY.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


class OpenfundsMappingBatch05ContractTests(unittest.TestCase):
    def test_exact_sedol_listing_mappings_exist(self):
        selected = {row["MAPPING_ID"]: row for row in read_rows() if row["MAPPING_ID"] in EXPECTED}
        self.assertEqual(set(EXPECTED), set(selected))
        for mapping_id, (canonical_id, rule) in EXPECTED.items():
            row = selected[mapping_id]
            self.assertEqual("OFST020040", row["EXTERNAL_FIELD_ID"], mapping_id)
            self.assertEqual(canonical_id, row["CANONICAL_FIELD_ID"], mapping_id)
            self.assertEqual("LISTING_IDENTIFIER", row["CANONICAL_ENTITY"], mapping_id)
            self.assertEqual("ONE_TO_MANY", row["MAPPING_STATUS"], mapping_id)
            self.assertEqual(rule, row["TRANSFORMATION_RULE"], mapping_id)
            self.assertEqual("NONE", row["INFORMATION_LOSS"], mapping_id)
            self.assertEqual("NO", row["IMPORT_SUPPORTED"], mapping_id)
            self.assertEqual("NO", row["EXPORT_SUPPORTED"], mapping_id)
            self.assertEqual("VALIDATED", row["VALIDATION_STATUS"], mapping_id)
            self.assertEqual(SOURCE_SHA, row["SOURCE_SHA256"], mapping_id)
            self.assertEqual("official:v2.13.0:OFST020040", row["SOURCE_REFERENCE"], mapping_id)
            self.assertIn("LICENSE_GATE_REQUIRED", row["NOTES"], mapping_id)

    def test_batch05_closure_is_forward_compatible(self):
        rows = read_rows()
        selected = [row for row in rows if row["MAPPING_ID"] in EXPECTED]
        self.assertEqual(3, len(selected))
        self.assertEqual(set(EXPECTED), {row["MAPPING_ID"] for row in selected})
        self.assertEqual({"OFST020040"}, {row["EXTERNAL_FIELD_ID"] for row in selected})
        self.assertEqual(3, len({row["CANONICAL_FIELD_ID"] for row in selected}))

    def test_sedol_is_not_activated_without_licence_gate(self):
        rows = [row for row in read_rows() if row["EXTERNAL_FIELD_ID"] == "OFST020040"]
        self.assertEqual(3, len(rows))
        self.assertTrue(all(row["IMPORT_SUPPORTED"] == "NO" for row in rows))
        self.assertTrue(all(row["EXPORT_SUPPORTED"] == "NO" for row in rows))


if __name__ == "__main__":
    unittest.main()
