import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "openfunds" / "mapping" / "v2.13.0" / "MAPPING_REGISTRY.csv"


class OpenfundsMappingBatch21Tests(unittest.TestCase):
    def test_ofst010720_maps_only_to_fund_passive_flag(self):
        with REGISTRY.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter=";"))
        matches = [r for r in rows if r["EXTERNAL_FIELD_ID"] == "OFST010720"]
        self.assertEqual(1, len(matches))
        row = matches[0]
        self.assertEqual("OF_FUND_FUND_PROFILE_IS_PASSIVE", row["CANONICAL_FIELD_ID"])
        self.assertEqual("FUND_PROFILE", row["CANONICAL_ENTITY"])
        self.assertEqual("TRANSFORMED", row["MAPPING_STATUS"])
        self.assertEqual("OPENFUNDS_YES_NO_TO_BOOLEAN", row["TRANSFORMATION_RULE"])
        self.assertEqual("NONE", row["INFORMATION_LOSS"])
        self.assertEqual("YES", row["IMPORT_SUPPORTED"])
        self.assertEqual("YES", row["EXPORT_SUPPORTED"])
        self.assertNotIn("SHARE_CLASS", row["CANONICAL_ENTITY"])

    def test_mapping_ids_remain_unique(self):
        with REGISTRY.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter=";"))
        ids = [r["MAPPING_ID"] for r in rows]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(rows), 74)


if __name__ == "__main__":
    unittest.main()
