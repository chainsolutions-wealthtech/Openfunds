import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "data" / "reference"

WAVE15_PROMOTED = {
    ("UEMOA", "MONETARY_UNION", "UEMOA", "MONETARY_ZONE"),
    ("UEMOA", "SUPRANATIONAL_AUTHORITY", "UEMOA", "MONETARY_ZONE"),
    ("CEMAC", "MONETARY_UNION", "CEMAC", "MONETARY_ZONE"),
    ("CEMAC", "SUPRANATIONAL_AUTHORITY", "CEMAC", "MONETARY_ZONE"),
    ("BCEAO", "INTERBANK_MARKET_OPERATOR", "UEMOA", "MONETARY_ZONE"),
    ("BEAC", "INTERBANK_MARKET_OPERATOR", "CEMAC", "MONETARY_ZONE"),
}
RETAINED_PENDING = {
    ("CMA", "MONETARY_UNION", "CMA", "MONETARY_ZONE"),
    ("EGX", "INDEX_PROVIDER", "EGYPTE", "COUNTRY"),
    ("NSE", "INDEX_PROVIDER", "KENYA", "COUNTRY"),
    ("NGX", "INDEX_PROVIDER", "NIGERIA", "COUNTRY"),
}
EXPECTED_NOTE = "OFFICIAL_ZONE_SEMANTICS_VERIFIED_2026_08_17_WAVE15"


def read_rows():
    with (REFERENCE / "ORGANIZATION_SCOPE_ROLES.csv").open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


def key(row):
    return (row["ORGANIZATION_CODE"], row["ROLE_CODE"], row["SCOPE_ENTITY_CODE"], row["SCOPE_ENTITY_TYPE"])


class InstitutionalRegistryWave15ContractTests(unittest.TestCase):
    def test_wave15_exact_zone_roles_are_validated(self):
        validated = {key(row) for row in read_rows() if row["VALIDATION_STATUS"] == "VALIDATED"}
        self.assertTrue(WAVE15_PROMOTED.issubset(validated), WAVE15_PROMOTED - validated)

    def test_wave15_does_not_duplicate_or_retarget_rows(self):
        rows = read_rows()
        for expected in WAVE15_PROMOTED | RETAINED_PENDING:
            self.assertEqual(1, sum(key(row) == expected for row in rows), expected)

    def test_wave15_source_note_is_exact(self):
        selected = {key(row): row for row in read_rows() if key(row) in WAVE15_PROMOTED}
        self.assertEqual(WAVE15_PROMOTED, set(selected))
        for expected, row in selected.items():
            self.assertEqual(EXPECTED_NOTE, row["SOURCE_NOTE"], expected)

    def test_wave15_retains_only_explicit_semantic_blockers_from_existing_pending_set(self):
        pending = {key(row) for row in read_rows() if row["VALIDATION_STATUS"] == "PENDING"}
        self.assertTrue(RETAINED_PENDING.issubset(pending), RETAINED_PENDING - pending)
        self.assertNotIn(("BCEAO", "INTERBANK_MARKET_OPERATOR", "UEMOA", "MONETARY_ZONE"), pending)
        self.assertNotIn(("BEAC", "INTERBANK_MARKET_OPERATOR", "CEMAC", "MONETARY_ZONE"), pending)


if __name__ == "__main__":
    unittest.main()
