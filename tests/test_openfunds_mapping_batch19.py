from __future__ import annotations

import csv
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "openfunds" / "mapping" / "v2.13.0" / "MAPPING_REGISTRY.csv"


class OpenfundsMappingBatch19Tests(unittest.TestCase):
    def rows(self):
        with REGISTRY.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle, delimiter=";"))

    def test_investment_status_enum_maps_without_lifecycle_collapse(self):
        rows = [r for r in self.rows() if r["EXTERNAL_FIELD_ID"] == "OFST023100"]
        self.assertEqual(1, len(rows))
        row = rows[0]
        self.assertEqual("OF_FUND_SHARE_CLASS_PROFILE_INVESTMENT_STATUS", row["CANONICAL_FIELD_ID"])
        self.assertEqual("OPENFUNDS_INVESTMENT_STATUS_TO_CANONICAL_ENUM", row["TRANSFORMATION_RULE"])
        self.assertEqual("NONE", row["INFORMATION_LOSS"])

    def test_description_is_source_preserving(self):
        rows = [r for r in self.rows() if r["EXTERNAL_FIELD_ID"] == "OFST023105"]
        self.assertEqual(1, len(rows))
        self.assertEqual("OF_FUND_SHARE_CLASS_PROFILE_INVESTMENT_STATUS_DESCRIPTION", rows[0]["CANONICAL_FIELD_ID"])
        self.assertEqual("TRIM_OUTER_WHITESPACE_PRESERVE_SOURCE_TEXT", rows[0]["TRANSFORMATION_RULE"])

    def test_reference_date_sets_date_and_known_status(self):
        rows = [r for r in self.rows() if r["EXTERNAL_FIELD_ID"] == "OFST023110"]
        self.assertEqual(2, len(rows))
        self.assertEqual(
            {
                "OF_FUND_SHARE_CLASS_PROFILE_INVESTMENT_STATUS_DATE",
                "OF_FUND_SHARE_CLASS_PROFILE_INVESTMENT_STATUS_DATE_STATUS",
            },
            {r["CANONICAL_FIELD_ID"] for r in rows},
        )
        date_row = next(r for r in rows if r["CANONICAL_FIELD_ID"].endswith("_DATE"))
        status_row = next(r for r in rows if r["CANONICAL_FIELD_ID"].endswith("_DATE_STATUS"))
        self.assertEqual("IDENTITY_DATE", date_row["TRANSFORMATION_RULE"])
        self.assertEqual("CONSTANT_KNOWN", status_row["TRANSFORMATION_RULE"])


if __name__ == "__main__":
    unittest.main()
