import csv
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "openfunds" / "mapping" / "v2.13.0" / "MAPPING_REGISTRY.csv"

EXPECTED = {
    ("MAP-000005", "OFST010410", "OF_FUND_FUND_PROFILE_BASE_CURRENCY_ID", "FUND_PROFILE"),
    ("MAP-000006", "OFST020540", "OF_FUND_SHARE_CLASS_PROFILE_CURRENCY_ID", "SHARE_CLASS_PROFILE"),
}
EXPECTED_RULE = "ISO_4217_TO_REF_CURRENCY_UUID"
SOURCE_SHA = "40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4"


def read_rows():
    with REGISTRY.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


class OpenfundsMappingBatch02ContractTests(unittest.TestCase):
    def test_exact_batch02_currency_mappings_are_validated(self):
        rows = read_rows()
        actual = {
            (row["MAPPING_ID"], row["EXTERNAL_FIELD_ID"], row["CANONICAL_FIELD_ID"], row["CANONICAL_ENTITY"])
            for row in rows
            if row["MAPPING_ID"] in {"MAP-000005", "MAP-000006"}
        }
        self.assertEqual(EXPECTED, actual)

    def test_batch02_mapping_semantics_are_exact(self):
        selected = {row["MAPPING_ID"]: row for row in read_rows() if row["MAPPING_ID"] in {"MAP-000005", "MAP-000006"}}
        self.assertEqual({"MAP-000005", "MAP-000006"}, set(selected))
        for mapping_id, row in selected.items():
            self.assertEqual("2.13.0", row["STANDARD_VERSION"], mapping_id)
            self.assertEqual("TRANSFORMED", row["MAPPING_STATUS"], mapping_id)
            self.assertEqual(EXPECTED_RULE, row["TRANSFORMATION_RULE"], mapping_id)
            self.assertEqual("NONE", row["INFORMATION_LOSS"], mapping_id)
            self.assertEqual("YES", row["IMPORT_SUPPORTED"], mapping_id)
            self.assertEqual("YES", row["EXPORT_SUPPORTED"], mapping_id)
            self.assertEqual("VALIDATED", row["VALIDATION_STATUS"], mapping_id)
            self.assertEqual(SOURCE_SHA, row["SOURCE_SHA256"], mapping_id)
            self.assertEqual(f"official:v2.13.0:{row['EXTERNAL_FIELD_ID']}", row["SOURCE_REFERENCE"], mapping_id)

    def test_batch02_exact_post_state(self):
        rows = read_rows()
        self.assertEqual(6, len(rows))
        self.assertEqual(4, len({row["EXTERNAL_FIELD_ID"] for row in rows}))
        self.assertEqual(6, len({row["CANONICAL_FIELD_ID"] for row in rows}))
        self.assertEqual(6, len({row["MAPPING_ID"] for row in rows}))
        counts = Counter(row["VALIDATION_STATUS"] for row in rows)
        self.assertEqual(6, counts["VALIDATED"])


if __name__ == "__main__":
    unittest.main()
