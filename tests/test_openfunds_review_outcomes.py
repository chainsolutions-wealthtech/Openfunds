import csv
import io
import subprocess
import sys
import unittest
from pathlib import Path

SOURCE_SHA256 = "40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4"
EXPECTED_HEADER = [
    "STANDARD_VERSION",
    "EXTERNAL_FIELD_ID",
    "OUTCOME",
    "REASON_CODE",
    "SOURCE_SHA256",
    "SOURCE_REFERENCE",
    "NOTES",
]


def fixture_row(external_id="OFST001000", outcome="DEFERRED_NOT_REQUIRED_FOR_PRODUCT"):
    return {
        "STANDARD_VERSION": "2.13.0",
        "EXTERNAL_FIELD_ID": external_id,
        "OUTCOME": outcome,
        "REASON_CODE": "OUTSIDE_CURRENT_PRODUCT_SCOPE",
        "SOURCE_SHA256": SOURCE_SHA256,
        "SOURCE_REFERENCE": f"official:v2.13.0:{external_id}",
        "NOTES": "reviewed fixture",
    }


class OpenfundsReviewOutcomesTests(unittest.TestCase):
    def setUp(self):
        from scripts.validate_openfunds_review_outcomes import (
            compute_merged_coverage,
            validate_outcome_rows,
        )
        self.compute_merged_coverage = compute_merged_coverage
        self.validate_outcome_rows = validate_outcome_rows

    def test_cli_entrypoint_can_execute_from_repository_root(self):
        completed = subprocess.run(
            [sys.executable, "scripts/validate_openfunds_review_outcomes.py", "--help"],
            cwd=Path(__file__).resolve().parents[1],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertIn("Validate Openfunds review outcomes", completed.stdout)

    def test_empty_sparse_outcome_registry_is_valid(self):
        self.assertEqual([], self.validate_outcome_rows([], {"OFST001000"}, set()))

    def test_valid_deferred_outcome_passes(self):
        self.assertEqual(
            [],
            self.validate_outcome_rows([fixture_row()], {"OFST001000"}, set()),
        )

    def test_duplicate_external_id_is_rejected(self):
        errors = self.validate_outcome_rows(
            [fixture_row(), fixture_row()],
            {"OFST001000"},
            set(),
        )
        self.assertTrue(any("duplicate EXTERNAL_FIELD_ID" in error for error in errors), errors)

    def test_unknown_external_id_is_rejected(self):
        row = fixture_row("OFZZ999999")
        errors = self.validate_outcome_rows([row], {"OFST001000"}, set())
        self.assertTrue(any("unknown external OF-ID" in error for error in errors), errors)

    def test_invalid_outcome_is_rejected(self):
        row = fixture_row()
        row["OUTCOME"] = "IGNORED"
        errors = self.validate_outcome_rows([row], {"OFST001000"}, set())
        self.assertTrue(any("invalid OUTCOME" in error for error in errors), errors)

    def test_reason_code_is_required_for_sparse_outcome(self):
        row = fixture_row()
        row["REASON_CODE"] = ""
        errors = self.validate_outcome_rows([row], {"OFST001000"}, set())
        self.assertTrue(any("REASON_CODE is required" in error for error in errors), errors)

    def test_source_sha_mismatch_is_rejected(self):
        row = fixture_row()
        row["SOURCE_SHA256"] = "0" * 64
        errors = self.validate_outcome_rows([row], {"OFST001000"}, set())
        self.assertTrue(any("unexpected SOURCE_SHA256" in error for error in errors), errors)

    def test_source_reference_must_identify_exact_of_id(self):
        row = fixture_row()
        row["SOURCE_REFERENCE"] = "official:v2.13.0:OFST999999"
        errors = self.validate_outcome_rows([row], {"OFST001000"}, set())
        self.assertTrue(any("SOURCE_REFERENCE" in error for error in errors), errors)

    def test_sparse_outcome_must_not_duplicate_a_mapped_external_id(self):
        row = fixture_row()
        errors = self.validate_outcome_rows(
            [row],
            {"OFST001000"},
            {"OFST001000"},
        )
        self.assertTrue(any("already mapped" in error for error in errors), errors)

    def test_mapped_categories_are_derived_not_stored_in_sparse_registry(self):
        for outcome in ("MAPPED_CANONICAL", "MAPPED_DERIVED"):
            row = fixture_row(outcome=outcome)
            errors = self.validate_outcome_rows([row], {"OFST001000"}, set())
            self.assertTrue(any("derived from MAPPING_REGISTRY" in error for error in errors), errors)

    def test_parameterized_xx_template_is_preserved(self):
        row = fixture_row("OFST6010XX", "TO_CONFIRM")
        row["REASON_CODE"] = "PARAMETERIZED_TEMPLATE_REQUIRES_GOVERNED_EXPANSION_RULE"
        self.assertEqual(
            [],
            self.validate_outcome_rows([row], {"OFST6010XX"}, set()),
        )

    def test_merged_coverage_partitions_official_inventory(self):
        official = {"OFST001000", "OFST001001", "OFST001002", "OFST001003", "OFST001004"}
        mapped = {"OFST001000"}
        rows = [
            fixture_row("OFST001001", "DEFERRED_NOT_REQUIRED_FOR_PRODUCT"),
            fixture_row("OFST001002", "NO_CANONICAL_EQUIVALENT"),
            fixture_row("OFST001003", "GATED_VENDOR_OR_LICENSE"),
        ]
        rows[1]["REASON_CODE"] = "NO_PRODUCT_CANONICAL_CONCEPT"
        rows[2]["REASON_CODE"] = "EXPLICIT_USAGE_CLEARANCE_REQUIRED"
        coverage = self.compute_merged_coverage(official, mapped, rows)
        self.assertEqual(5, coverage["total_official_ids"])
        self.assertEqual(1, coverage["mapped_external_ids"])
        self.assertEqual(2, coverage["reviewed_nonmapped_external_ids"])
        self.assertEqual(1, coverage["vendor_gated_external_ids"])
        self.assertEqual(0, coverage["to_confirm_external_ids"])
        self.assertEqual(1, coverage["unreviewed_external_ids"])
        self.assertEqual(5, sum(
            coverage[key]
            for key in (
                "mapped_external_ids",
                "reviewed_nonmapped_external_ids",
                "vendor_gated_external_ids",
                "to_confirm_external_ids",
                "unreviewed_external_ids",
            )
        ))


if __name__ == "__main__":
    unittest.main()
