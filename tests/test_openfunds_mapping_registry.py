import csv
import io
import subprocess
import sys
import unittest
from pathlib import Path

EXPECTED_HEADER = [
    "MAPPING_ID",
    "STANDARD_VERSION",
    "EXTERNAL_FIELD_ID",
    "CANONICAL_FIELD_ID",
    "CANONICAL_ENTITY",
    "MAPPING_STATUS",
    "TRANSFORMATION_RULE",
    "INFORMATION_LOSS",
    "IMPORT_SUPPORTED",
    "EXPORT_SUPPORTED",
    "VALIDATION_STATUS",
    "SOURCE_SHA256",
    "SOURCE_REFERENCE",
    "NOTES",
]


def fixture_row(mapping_id="MAP-000001"):
    return {
        "MAPPING_ID": mapping_id,
        "STANDARD_VERSION": "2.13.0",
        "EXTERNAL_FIELD_ID": "OFST001000",
        "CANONICAL_FIELD_ID": "OF_FUND_ENTITY_CANONICAL_CODE",
        "CANONICAL_ENTITY": "FUND_ENTITY",
        "MAPPING_STATUS": "DIRECT",
        "TRANSFORMATION_RULE": "IDENTITY",
        "INFORMATION_LOSS": "NONE",
        "IMPORT_SUPPORTED": "YES",
        "EXPORT_SUPPORTED": "YES",
        "VALIDATION_STATUS": "PROPOSED",
        "SOURCE_SHA256": "40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4",
        "SOURCE_REFERENCE": "official:v2.13.0:OFST001000",
        "NOTES": "fixture",
    }


class OpenfundsMappingRegistryContractTests(unittest.TestCase):
    def setUp(self):
        from scripts.validate_openfunds_mapping_registry import validate_rows
        self.validate_rows = validate_rows

    def make_rows(self, text):
        return list(csv.DictReader(io.StringIO(text), delimiter=";"))

    def test_cli_entrypoint_can_execute_from_repository_root(self):
        completed = subprocess.run(
            [sys.executable, "scripts/validate_openfunds_mapping_registry.py", "--help"],
            cwd=Path(__file__).resolve().parents[1],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertIn("Validate the governed Openfunds mapping registry", completed.stdout)

    def test_empty_reviewed_registry_is_valid(self):
        self.assertEqual([], self.validate_rows([], {"OFST001000"}, {"OF_FUND_ENTITY_CANONICAL_CODE"}))

    def test_valid_direct_mapping_passes(self):
        self.assertEqual([], self.validate_rows([fixture_row()], {"OFST001000"}, {"OF_FUND_ENTITY_CANONICAL_CODE"}))

    def test_unknown_external_id_is_rejected(self):
        row = fixture_row()
        row["EXTERNAL_FIELD_ID"] = "OFZZ999999"
        row["MAPPING_STATUS"] = "TO_CONFIRM"
        row["TRANSFORMATION_RULE"] = "NONE"
        row["INFORMATION_LOSS"] = "UNKNOWN"
        row["IMPORT_SUPPORTED"] = "NO"
        row["EXPORT_SUPPORTED"] = "NO"
        row["SOURCE_REFERENCE"] = "official:v2.13.0:OFZZ999999"
        errors = self.validate_rows([row], {"OFST001000"}, {"OF_FUND_ENTITY_CANONICAL_CODE"})
        self.assertTrue(any("unknown external OF-ID" in error for error in errors), errors)

    def test_unknown_canonical_field_is_rejected(self):
        row = fixture_row()
        row["CANONICAL_FIELD_ID"] = "OF_FUND_FAKE_UNKNOWN"
        row["MAPPING_STATUS"] = "TO_CONFIRM"
        row["TRANSFORMATION_RULE"] = "NONE"
        row["INFORMATION_LOSS"] = "UNKNOWN"
        row["IMPORT_SUPPORTED"] = "NO"
        row["EXPORT_SUPPORTED"] = "NO"
        errors = self.validate_rows([row], {"OFST001000"}, {"OF_FUND_ENTITY_CANONICAL_CODE"})
        self.assertTrue(any("unknown canonical FIELD_ID" in error for error in errors), errors)

    def test_parameterized_xx_id_is_preserved(self):
        row = fixture_row()
        row["EXTERNAL_FIELD_ID"] = "OFST6010XX"
        row["MAPPING_STATUS"] = "TO_CONFIRM"
        row["TRANSFORMATION_RULE"] = "PARAMETERIZED_COUNTRY_TEMPLATE_PRESERVED"
        row["IMPORT_SUPPORTED"] = "NO"
        row["EXPORT_SUPPORTED"] = "NO"
        row["SOURCE_REFERENCE"] = "official:v2.13.0:OFST6010XX"
        self.assertEqual([], self.validate_rows([row], {"OFST6010XX"}, {"OF_FUND_ENTITY_CANONICAL_CODE"}))

    def test_duplicate_mapping_id_is_rejected(self):
        errors = self.validate_rows(
            [fixture_row(), fixture_row()],
            {"OFST001000"},
            {"OF_FUND_ENTITY_CANONICAL_CODE"},
        )
        self.assertTrue(any("duplicate MAPPING_ID" in error for error in errors), errors)

    def test_duplicate_external_to_canonical_pair_is_rejected_even_with_distinct_mapping_ids(self):
        errors = self.validate_rows(
            [fixture_row("MAP-000001"), fixture_row("MAP-000002")],
            {"OFST001000"},
            {"OF_FUND_ENTITY_CANONICAL_CODE"},
        )
        self.assertTrue(any("duplicate external/canonical mapping pair" in error for error in errors), errors)

    def test_canonical_entity_must_match_governed_field_entity(self):
        row = fixture_row()
        row["CANONICAL_ENTITY"] = "FUND_PROFILE"
        errors = self.validate_rows(
            [row],
            {"OFST001000"},
            {"OF_FUND_ENTITY_CANONICAL_CODE"},
            {"OF_FUND_ENTITY_CANONICAL_CODE": "FUND_ENTITY"},
        )
        self.assertTrue(any("CANONICAL_ENTITY mismatch" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
