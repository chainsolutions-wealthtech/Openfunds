import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "openfunds" / "mapping" / "v2.13.0" / "MAPPING_REGISTRY.csv"
SOURCE_SHA = "40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4"

EXPECTED = {
    "MAP-000017": ("OFST062030", "OF_FUND_LISTING_VENUE_MIC", "LISTING", "TRANSFORMED", "TRIM_AND_UPPERCASE_MIC"),
    "MAP-000018": ("OFST062050", "OF_FUND_LISTING_IS_PRIMARY", "LISTING", "TRANSFORMED", "OPENFUNDS_YES_NO_TO_BOOLEAN"),
    "MAP-000019": ("OFST062000", "OF_FUND_LISTING_VALID_FROM", "LISTING", "ONE_TO_MANY", "IDENTITY_DATE"),
    "MAP-000020": ("OFST062000", "OF_FUND_LISTING_VALID_FROM_STATUS", "LISTING", "ONE_TO_MANY", "CONSTANT_KNOWN"),
}


def read_rows():
    with REGISTRY.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


class OpenfundsMappingBatch06ContractTests(unittest.TestCase):
    def test_exact_batch06_rows_exist(self):
        selected = {row["MAPPING_ID"]: row for row in read_rows() if row["MAPPING_ID"] in EXPECTED}
        self.assertEqual(set(EXPECTED), set(selected))
        for mapping_id, (external_id, canonical_id, entity, status, rule) in EXPECTED.items():
            row = selected[mapping_id]
            self.assertEqual(external_id, row["EXTERNAL_FIELD_ID"], mapping_id)
            self.assertEqual(canonical_id, row["CANONICAL_FIELD_ID"], mapping_id)
            self.assertEqual(entity, row["CANONICAL_ENTITY"], mapping_id)
            self.assertEqual(status, row["MAPPING_STATUS"], mapping_id)
            self.assertEqual(rule, row["TRANSFORMATION_RULE"], mapping_id)
            self.assertEqual("NONE", row["INFORMATION_LOSS"], mapping_id)
            self.assertEqual("YES", row["IMPORT_SUPPORTED"], mapping_id)
            self.assertEqual("YES", row["EXPORT_SUPPORTED"], mapping_id)
            self.assertEqual("VALIDATED", row["VALIDATION_STATUS"], mapping_id)
            self.assertEqual(SOURCE_SHA, row["SOURCE_SHA256"], mapping_id)
            self.assertEqual(f"official:v2.13.0:{external_id}", row["SOURCE_REFERENCE"], mapping_id)

    def test_batch06_contract_survives_future_batches(self):
        rows = read_rows()
        mapping_ids = [row["MAPPING_ID"] for row in rows]
        self.assertEqual(len(mapping_ids), len(set(mapping_ids)))
        self.assertTrue(set(EXPECTED).issubset(set(mapping_ids)))

    def test_exchange_place_remains_deferred_in_favour_of_mic(self):
        mapped_ids = {row["EXTERNAL_FIELD_ID"] for row in read_rows()}
        self.assertNotIn("OFST062040", mapped_ids, "Exchange Place is explicitly superseded by MIC")


if __name__ == "__main__":
    unittest.main()
