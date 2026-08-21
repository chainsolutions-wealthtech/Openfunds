import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "openfunds" / "mapping" / "v2.13.0" / "MAPPING_REGISTRY.csv"

EXPECTED = {
    "OFST023800": {
        "OF_FUND_SHARE_CLASS_TRACKED_INDEX_INDEX_NAME": ("DIRECT", "TRIM_OUTER_WHITESPACE_PRESERVE_SOURCE_TEXT"),
    },
    "OFST023805": {
        "OF_FUND_SHARE_CLASS_TRACKED_INDEX_INDEX_CURRENCY_ID": ("TRANSFORMED", "ISO4217_TO_REF_CURRENCY_UUID_IF_PRESENT"),
        "OF_FUND_SHARE_CLASS_TRACKED_INDEX_INDEX_CURRENCY_MODE": ("TRANSFORMED", "OPENFUNDS_INDEX_CURRENCY_TO_CANONICAL_MODE"),
    },
    "OFST023810": {
        "OF_FUND_SHARE_CLASS_TRACKED_INDEX_INDEX_TYPE": ("TRANSFORMED", "OPENFUNDS_INDEX_TYPE_TO_CANONICAL_ENUM"),
    },
}


class OpenfundsMappingBatch25Tests(unittest.TestCase):
    def _rows(self):
        with REGISTRY.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle, delimiter=";"))

    def test_tracked_index_fields_map_without_currency_inference(self):
        rows = self._rows()
        matches = [r for r in rows if r["EXTERNAL_FIELD_ID"] in EXPECTED]
        self.assertEqual(4, len(matches))
        for external_id, targets in EXPECTED.items():
            ext_rows = [r for r in matches if r["EXTERNAL_FIELD_ID"] == external_id]
            self.assertEqual(set(targets), {r["CANONICAL_FIELD_ID"] for r in ext_rows})
            for row in ext_rows:
                status, rule = targets[row["CANONICAL_FIELD_ID"]]
                self.assertEqual("SHARE_CLASS_TRACKED_INDEX", row["CANONICAL_ENTITY"])
                self.assertEqual(status, row["MAPPING_STATUS"])
                self.assertEqual(rule, row["TRANSFORMATION_RULE"])
                self.assertEqual("YES", row["IMPORT_SUPPORTED"])
                self.assertEqual("YES", row["EXPORT_SUPPORTED"])
                self.assertEqual("NONE", row["INFORMATION_LOSS"])

    def test_blank_index_currency_means_local_currency_without_inference(self):
        rows = [r for r in self._rows() if r["EXTERNAL_FIELD_ID"] == "OFST023805"]
        notes = " ".join(r["NOTES"] for r in rows)
        self.assertIn("BLANK_SOURCE_VALUE_TO_LOCAL_CURRENCY_MODE", notes)
        self.assertIn("NO_SHARE_CLASS_CURRENCY_INFERENCE", notes)
        self.assertIn("NONEMPTY_ISO4217_TO_EXPLICIT_MODE", notes)

    def test_index_type_vocabulary_is_reversible(self):
        row = next(r for r in self._rows() if r["EXTERNAL_FIELD_ID"] == "OFST023810")
        notes = row["NOTES"]
        for token in (
            "price=PRICE",
            "performance=PERFORMANCE",
            "performance net dividends=PERFORMANCE_NET_DIVIDENDS",
            "performance gross dividends=PERFORMANCE_GROSS_DIVIDENDS",
        ):
            self.assertIn(token, notes)

    def test_mapping_ids_remain_unique_and_forward_compatible(self):
        rows = self._rows()
        ids = [r["MAPPING_ID"] for r in rows]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(rows), 86)


if __name__ == "__main__":
    unittest.main()
