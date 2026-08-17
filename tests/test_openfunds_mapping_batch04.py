import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "openfunds" / "mapping" / "v2.13.0" / "MAPPING_REGISTRY.csv"
SOURCE_SHA = "40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4"


class OpenfundsMappingBatch04ContractTests(unittest.TestCase):
    def test_distribution_policy_mapping_is_exact(self):
        with REGISTRY.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter=";"))
        selected = [row for row in rows if row["MAPPING_ID"] == "MAP-000013"]
        self.assertEqual(1, len(selected))
        row = selected[0]
        self.assertEqual("OFST020400", row["EXTERNAL_FIELD_ID"])
        self.assertEqual("OF_FUND_SHARE_CLASS_PROFILE_DISTRIBUTION_POLICY", row["CANONICAL_FIELD_ID"])
        self.assertEqual("SHARE_CLASS_PROFILE", row["CANONICAL_ENTITY"])
        self.assertEqual("TRANSFORMED", row["MAPPING_STATUS"])
        self.assertEqual("OPENFUNDS_DISTRIBUTION_POLICY_TO_CANONICAL_ENUM", row["TRANSFORMATION_RULE"])
        self.assertEqual("NONE", row["INFORMATION_LOSS"])
        self.assertEqual("YES", row["IMPORT_SUPPORTED"])
        self.assertEqual("YES", row["EXPORT_SUPPORTED"])
        self.assertEqual("VALIDATED", row["VALIDATION_STATUS"])
        self.assertEqual(SOURCE_SHA, row["SOURCE_SHA256"])
        self.assertEqual("official:v2.13.0:OFST020400", row["SOURCE_REFERENCE"])

    def test_batch04_exact_cumulative_post_state(self):
        with REGISTRY.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter=";"))
        self.assertEqual(13, len(rows))
        self.assertEqual(7, len({row["EXTERNAL_FIELD_ID"] for row in rows}))
        self.assertEqual(7, len({row["CANONICAL_FIELD_ID"] for row in rows}))


if __name__ == "__main__":
    unittest.main()
