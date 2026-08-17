import csv
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "data" / "reference"

WAVE14_PROMOTED = {
    ("JSE", "INDEX_PROVIDER", "AFRIQUE_DU_SUD", "COUNTRY"),
    ("BVMT", "INDEX_PROVIDER", "TUNISIE", "COUNTRY"),
}
RETAINED_PENDING = {
    ("EGX", "INDEX_PROVIDER", "EGYPTE", "COUNTRY"),
    ("NSE", "INDEX_PROVIDER", "KENYA", "COUNTRY"),
    ("NGX", "INDEX_PROVIDER", "NIGERIA", "COUNTRY"),
}
EXPECTED_NOTE = "OFFICIAL_INDEX_PROVIDER_VERIFIED_2026_08_17_WAVE14"


def read_rows():
    with (REFERENCE / "ORGANIZATION_SCOPE_ROLES.csv").open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


def key(row):
    return (row["ORGANIZATION_CODE"], row["ROLE_CODE"], row["SCOPE_ENTITY_CODE"], row["SCOPE_ENTITY_TYPE"])


class InstitutionalRegistryWave14ContractTests(unittest.TestCase):
    def test_wave14_exact_two_index_provider_roles_are_validated(self):
        rows = read_rows()
        validated = {key(row) for row in rows if row["VALIDATION_STATUS"] == "VALIDATED"}
        self.assertTrue(WAVE14_PROMOTED.issubset(validated), WAVE14_PROMOTED - validated)

    def test_wave14_does_not_duplicate_or_retarget_rows(self):
        rows = read_rows()
        for expected in WAVE14_PROMOTED | RETAINED_PENDING:
            self.assertEqual(1, sum(key(row) == expected for row in rows), expected)

    def test_wave14_source_note_is_exact(self):
        selected = {key(row): row for row in read_rows() if key(row) in WAVE14_PROMOTED}
        self.assertEqual(WAVE14_PROMOTED, set(selected))
        for expected, row in selected.items():
            self.assertEqual(EXPECTED_NOTE, row["SOURCE_NOTE"], expected)

    def test_wave14_retains_three_ambiguous_index_providers_pending(self):
        rows = read_rows()
        pending = {key(row) for row in rows if row["VALIDATION_STATUS"] == "PENDING"}
        self.assertTrue(RETAINED_PENDING.issubset(pending), RETAINED_PENDING - pending)
        self.assertEqual(3, sum(row["ROLE_CODE"] == "INDEX_PROVIDER" and row["VALIDATION_STATUS"] == "PENDING" for row in rows))

    def test_wave14_exact_post_state(self):
        rows = read_rows()
        counts = Counter(row["VALIDATION_STATUS"] for row in rows)
        self.assertEqual(199, len(rows))
        self.assertEqual(189, counts["VALIDATED"])
        self.assertEqual(10, counts["PENDING"])


if __name__ == "__main__":
    unittest.main()
