import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "openfunds" / "mapping" / "v2.13.0" / "MAPPING_REGISTRY.csv"
SOURCE_SHA = "40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4"
EXPECTED = {
    "MAP-000041": ("OFST010250", "OF_FUND_FUND_PROFILE_VALUATION_POINT_TIME", "FUND_PROFILE", "TIME_HH_MM_IDENTITY"),
    "MAP-000042": ("OFST010251", "OF_FUND_FUND_PROFILE_VALUATION_TIMEZONE_LABEL", "FUND_PROFILE", "TRIM_SOURCE_TIMEZONE_LABEL_NO_IANA_INFERENCE"),
    "MAP-000043": ("OFST010252", "OF_FUND_FUND_PROFILE_VALUATION_TIMEZONE_IANA", "FUND_PROFILE", "IANA_TZDB_IDENTITY"),
    "MAP-000044": ("OFST020320", "OF_FUND_SHARE_CLASS_PROFILE_NAV_PUBLICATION_TIME", "SHARE_CLASS_PROFILE", "TIME_HH_MM_IDENTITY"),
}


def read_rows():
    with REGISTRY.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


class OpenfundsMappingBatch15ContractTests(unittest.TestCase):
    def test_valuation_time_semantics_are_mapped_as_one_governed_group(self):
        selected = {row["MAPPING_ID"]: row for row in read_rows() if row["MAPPING_ID"] in EXPECTED}
        self.assertEqual(set(EXPECTED), set(selected))
        for mapping_id, (external_id, target, entity, rule) in EXPECTED.items():
            row = selected[mapping_id]
            self.assertEqual(external_id, row["EXTERNAL_FIELD_ID"])
            self.assertEqual(target, row["CANONICAL_FIELD_ID"])
            self.assertEqual(entity, row["CANONICAL_ENTITY"])
            self.assertEqual(rule, row["TRANSFORMATION_RULE"])
            self.assertEqual("NONE", row["INFORMATION_LOSS"])
            self.assertEqual("YES", row["IMPORT_SUPPORTED"])
            self.assertEqual("YES", row["EXPORT_SUPPORTED"])
            self.assertEqual("VALIDATED", row["VALIDATION_STATUS"])
            self.assertEqual(SOURCE_SHA, row["SOURCE_SHA256"])
            self.assertEqual(f"official:v2.13.0:{external_id}", row["SOURCE_REFERENCE"])

    def test_abbreviated_timezone_never_infers_iana_timezone(self):
        row = next(row for row in read_rows() if row["MAPPING_ID"] == "MAP-000042")
        self.assertIn("NO_IANA_INFERENCE", row["TRANSFORMATION_RULE"])
        self.assertIn("NOT_AUTOMATION_SAFE", row["NOTES"])

    def test_nav_publication_time_declares_inherited_fund_timezone_context(self):
        row = next(row for row in read_rows() if row["MAPPING_ID"] == "MAP-000044")
        self.assertIn("INHERITS_FUND_VALUATION_TIMEZONE", row["NOTES"])

    def test_registry_remains_unique_and_forward_compatible(self):
        rows = read_rows()
        self.assertGreaterEqual(len(rows), 44)
        self.assertEqual(len(rows), len({row["MAPPING_ID"] for row in rows}))


if __name__ == "__main__":
    unittest.main()
