from __future__ import annotations

import csv
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "openfunds" / "mapping" / "v2.13.0" / "MAPPING_REGISTRY.csv"

EVENT_TYPE_BY_OFID = {
    "OFST020558": "SUBSCRIPTION_PERIOD_START",
    "OFST020559": "SUBSCRIPTION_PERIOD_END",
    "OFST020560": "LAUNCH",
    "OFST020562": "DORMANCY_START",
    "OFST020563": "DORMANCY_END",
    "OFST020564": "LIQUIDATION_START",
    "OFST020566": "TERMINATION",
}
TARGETS = {
    "OF_FUND_FUND_ENTITY_EVENT_EFFECTIVE_DATE",
    "OF_FUND_FUND_ENTITY_EVENT_EFFECTIVE_DATE_STATUS",
    "OF_FUND_FUND_ENTITY_EVENT_EVENT_TYPE",
}


class OpenfundsMappingBatch18Tests(unittest.TestCase):
    def rows(self):
        with REGISTRY.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle, delimiter=";"))

    def test_lifecycle_dates_map_to_versionable_events(self):
        rows = self.rows()
        for ofid, event_type in EVENT_TYPE_BY_OFID.items():
            scoped = [r for r in rows if r["EXTERNAL_FIELD_ID"] == ofid]
            self.assertEqual(3, len(scoped), ofid)
            self.assertEqual(TARGETS, {r["CANONICAL_FIELD_ID"] for r in scoped})
            self.assertTrue(all(r["CANONICAL_ENTITY"] == "FUND_ENTITY_EVENT" for r in scoped))
            type_row = next(r for r in scoped if r["CANONICAL_FIELD_ID"].endswith("_EVENT_TYPE"))
            self.assertEqual(f"CONSTANT_{event_type}", type_row["TRANSFORMATION_RULE"])
            date_row = next(r for r in scoped if r["CANONICAL_FIELD_ID"].endswith("_EFFECTIVE_DATE"))
            self.assertEqual("IDENTITY_DATE", date_row["TRANSFORMATION_RULE"])
            status_row = next(r for r in scoped if r["CANONICAL_FIELD_ID"].endswith("_EFFECTIVE_DATE_STATUS"))
            self.assertEqual("CONSTANT_KNOWN", status_row["TRANSFORMATION_RULE"])
            self.assertTrue(all(r["INFORMATION_LOSS"] == "NONE" for r in scoped))

    def test_lifecycle_dates_are_not_collapsed_to_single_entity_state_bounds(self):
        forbidden = {
            "OF_FUND_FUND_ENTITY_STATE_EFFECTIVE_FROM",
            "OF_FUND_FUND_ENTITY_STATE_EFFECTIVE_TO",
        }
        scoped = [r for r in self.rows() if r["EXTERNAL_FIELD_ID"] in EVENT_TYPE_BY_OFID]
        self.assertTrue(forbidden.isdisjoint({r["CANONICAL_FIELD_ID"] for r in scoped}))


if __name__ == "__main__":
    unittest.main()
