import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "openfunds" / "mapping" / "v2.13.0" / "MAPPING_REGISTRY.csv"
SOURCE_SHA = "40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4"
EXPECTED = {
    "MAP-000045": ("OFST020530", "OF_FUND_SHARE_CLASS_PROFILE_IS_MULTICURRENCY", "SHARE_CLASS_PROFILE", "OPENFUNDS_YES_NO_TO_BOOLEAN"),
    "MAP-000046": ("OFST020535", "OF_FUND_SHARE_CLASS_DEALING_CURRENCY_CURRENCY_ID", "SHARE_CLASS_DEALING_CURRENCY", "PIPE_SEPARATED_ISO4217_TO_REF_CURRENCY_UUID_ROWS"),
}


def read_rows():
    with REGISTRY.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


class OpenfundsMappingBatch16ContractTests(unittest.TestCase):
    def test_multicurrency_fields_map_to_flag_and_additional_currency_rows(self):
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

    def test_additional_currencies_never_overwrite_reference_currency(self):
        rows = [row for row in read_rows() if row["EXTERNAL_FIELD_ID"] == "OFST020535"]
        targets = {row["CANONICAL_FIELD_ID"] for row in rows}
        self.assertEqual({"OF_FUND_SHARE_CLASS_DEALING_CURRENCY_CURRENCY_ID"}, targets)
        self.assertNotIn("OF_FUND_SHARE_CLASS_PROFILE_CURRENCY_ID", targets)

    def test_registry_remains_unique_and_forward_compatible(self):
        rows = read_rows()
        self.assertGreaterEqual(len(rows), 46)
        self.assertEqual(len(rows), len({row["MAPPING_ID"] for row in rows}))


if __name__ == "__main__":
    unittest.main()
