from __future__ import annotations

import csv
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "openfunds" / "mapping" / "v2.13.0" / "MAPPING_REGISTRY.csv"


class OpenfundsMappingBatch17Tests(unittest.TestCase):
    def rows(self):
        with REGISTRY.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle, delimiter=";"))

    def test_share_class_lifecycle_maps_to_precise_lifecycle_phase_only(self):
        rows = [r for r in self.rows() if r["EXTERNAL_FIELD_ID"] == "OFST020545"]
        self.assertEqual(1, len(rows))
        row = rows[0]
        self.assertEqual("OF_FUND_FUND_ENTITY_STATE_LIFECYCLE_PHASE", row["CANONICAL_FIELD_ID"])
        self.assertEqual("FUND_ENTITY_STATE", row["CANONICAL_ENTITY"])
        self.assertEqual("TRANSFORMED", row["MAPPING_STATUS"])
        self.assertEqual("OPENFUNDS_LIFECYCLE_PHASE_TO_CANONICAL_ENUM", row["TRANSFORMATION_RULE"])
        self.assertEqual("NONE", row["INFORMATION_LOSS"])
        self.assertEqual("YES", row["IMPORT_SUPPORTED"])
        self.assertEqual("YES", row["EXPORT_SUPPORTED"])
        self.assertNotEqual("OF_FUND_FUND_ENTITY_STATE_LIFECYCLE_STATUS", row["CANONICAL_FIELD_ID"])


if __name__ == "__main__":
    unittest.main()
