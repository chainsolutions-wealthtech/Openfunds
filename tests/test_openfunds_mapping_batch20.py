from __future__ import annotations

import csv
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "openfunds" / "mapping" / "v2.13.0" / "MAPPING_REGISTRY.csv"


class OpenfundsMappingBatch20Tests(unittest.TestCase):
    def rows(self):
        with REGISTRY.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle, delimiter=";"))

    def test_is_etf_maps_to_share_class_boolean_only(self):
        rows = [r for r in self.rows() if r["EXTERNAL_FIELD_ID"] == "OFST010580"]
        self.assertEqual(1, len(rows))
        row = rows[0]
        self.assertEqual("OF_FUND_SHARE_CLASS_PROFILE_IS_ETF", row["CANONICAL_FIELD_ID"])
        self.assertEqual("SHARE_CLASS_PROFILE", row["CANONICAL_ENTITY"])
        self.assertEqual("TRANSFORMED", row["MAPPING_STATUS"])
        self.assertEqual("OPENFUNDS_YES_NO_TO_BOOLEAN", row["TRANSFORMATION_RULE"])
        self.assertEqual("NONE", row["INFORMATION_LOSS"])
        self.assertEqual("YES", row["IMPORT_SUPPORTED"])
        self.assertEqual("YES", row["EXPORT_SUPPORTED"])


if __name__ == "__main__":
    unittest.main()
