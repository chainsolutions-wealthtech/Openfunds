import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "openfunds" / "mapping" / "v2.13.0" / "MAPPING_REGISTRY.csv"

EXPECTED = {
    "OFST023820": {
        "OF_FUND_TRACKED_INDEX_IDENTIFIER_IDENTIFIER_VALUE": "IDENTITY",
        "OF_FUND_TRACKED_INDEX_IDENTIFIER_IDENTIFIER_SCHEME": "CONSTANT_BLOOMBERG",
        "OF_FUND_TRACKED_INDEX_IDENTIFIER_NORMALIZED_VALUE": "TRIM_ONLY_BLOOMBERG",
    },
    "OFST023830": {
        "OF_FUND_TRACKED_INDEX_IDENTIFIER_IDENTIFIER_VALUE": "IDENTITY",
        "OF_FUND_TRACKED_INDEX_IDENTIFIER_IDENTIFIER_SCHEME": "CONSTANT_RIC",
        "OF_FUND_TRACKED_INDEX_IDENTIFIER_NORMALIZED_VALUE": "TRIM_ONLY_RIC_CASE_PRESERVING",
    },
}


class OpenfundsMappingBatch26Tests(unittest.TestCase):
    def _rows(self):
        with REGISTRY.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle, delimiter=";"))

    def test_tracked_index_vendor_identifiers_are_separate_and_usage_gated(self):
        rows = self._rows()
        matches = [r for r in rows if r["EXTERNAL_FIELD_ID"] in EXPECTED]
        self.assertEqual(6, len(matches))
        for external_id, targets in EXPECTED.items():
            ext_rows = [r for r in matches if r["EXTERNAL_FIELD_ID"] == external_id]
            self.assertEqual(set(targets), {r["CANONICAL_FIELD_ID"] for r in ext_rows})
            for row in ext_rows:
                self.assertEqual("TRACKED_INDEX_IDENTIFIER", row["CANONICAL_ENTITY"])
                self.assertEqual("ONE_TO_MANY", row["MAPPING_STATUS"])
                self.assertEqual(targets[row["CANONICAL_FIELD_ID"]], row["TRANSFORMATION_RULE"])
                self.assertEqual("NO", row["IMPORT_SUPPORTED"])
                self.assertEqual("NO", row["EXPORT_SUPPORTED"])
                self.assertEqual("NONE", row["INFORMATION_LOSS"])
                self.assertIn("PROPRIETARY_IDENTIFIER_USAGE_REVIEW_REQUIRED", row["NOTES"])
                self.assertIn("TRACKED_INDEX_SUBJECT_REQUIRED", row["NOTES"])

    def test_ric_mapping_explicitly_preserves_case(self):
        rows = [r for r in self._rows() if r["EXTERNAL_FIELD_ID"] == "OFST023830"]
        notes = " ".join(r["NOTES"] for r in rows)
        self.assertIn("CASE_SENSITIVE_SOURCE_PRESERVED", notes)
        self.assertNotIn("UPPERCASE_RIC", notes)

    def test_project_gate_is_not_misattributed_to_openfunds(self):
        rows = [r for r in self._rows() if r["EXTERNAL_FIELD_ID"] in EXPECTED]
        for row in rows:
            self.assertNotIn("OPENFUNDS_LICENSE_WARNING", row["NOTES"])

    def test_mapping_ids_remain_unique_and_forward_compatible(self):
        rows = self._rows()
        ids = [r["MAPPING_ID"] for r in rows]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(rows), 92)


if __name__ == "__main__":
    unittest.main()
