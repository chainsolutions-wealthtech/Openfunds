import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "data" / "reference"

WAVE13_PROMOTED = {
    ("BCEAO", "FX_REFERENCE_RATE_PROVIDER", "UEMOA", "MONETARY_ZONE"),
    ("BEAC", "FX_REFERENCE_RATE_PROVIDER", "CEMAC", "MONETARY_ZONE"),
    ("SARB", "FX_REFERENCE_RATE_PROVIDER", "AFRIQUE_DU_SUD", "COUNTRY"),
    ("BAM", "FX_REFERENCE_RATE_PROVIDER", "MAROC", "COUNTRY"),
    ("BOG", "FX_REFERENCE_RATE_PROVIDER", "GHANA", "COUNTRY"),
    ("CBN", "FX_REFERENCE_RATE_PROVIDER", "NIGERIA", "COUNTRY"),
    ("BCT", "FX_REFERENCE_RATE_PROVIDER", "TUNISIE", "COUNTRY"),
    ("CBE", "FX_REFERENCE_RATE_PROVIDER", "EGYPTE", "COUNTRY"),
    ("CBK", "FX_REFERENCE_RATE_PROVIDER", "KENYA", "COUNTRY"),
}

EXPECTED_NOTE = "OFFICIAL_FX_REFERENCE_PUBLICATION_VERIFIED_2026_08_17_WAVE13"


def read_rows(filename: str):
    with (REFERENCE / filename).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


class InstitutionalRegistryWave13ContractTests(unittest.TestCase):
    def test_wave_13_exact_existing_fx_provider_roles_are_validated(self):
        rows = read_rows("ORGANIZATION_SCOPE_ROLES.csv")
        validated = {
            (row["ORGANIZATION_CODE"], row["ROLE_CODE"], row["SCOPE_ENTITY_CODE"], row["SCOPE_ENTITY_TYPE"])
            for row in rows
            if row["VALIDATION_STATUS"] == "VALIDATED"
        }
        self.assertTrue(WAVE13_PROMOTED.issubset(validated), WAVE13_PROMOTED - validated)

    def test_wave_13_does_not_duplicate_or_retarget_rows(self):
        rows = read_rows("ORGANIZATION_SCOPE_ROLES.csv")
        for key in WAVE13_PROMOTED:
            matching = [
                row for row in rows
                if (row["ORGANIZATION_CODE"], row["ROLE_CODE"], row["SCOPE_ENTITY_CODE"], row["SCOPE_ENTITY_TYPE"]) == key
            ]
            self.assertEqual(1, len(matching), key)

    def test_wave_13_source_note_is_exact(self):
        rows = read_rows("ORGANIZATION_SCOPE_ROLES.csv")
        selected = {
            (row["ORGANIZATION_CODE"], row["ROLE_CODE"], row["SCOPE_ENTITY_CODE"], row["SCOPE_ENTITY_TYPE"]): row
            for row in rows
            if (row["ORGANIZATION_CODE"], row["ROLE_CODE"], row["SCOPE_ENTITY_CODE"], row["SCOPE_ENTITY_TYPE"]) in WAVE13_PROMOTED
        }
        self.assertEqual(WAVE13_PROMOTED, set(selected))
        for key, row in selected.items():
            self.assertEqual(EXPECTED_NOTE, row["SOURCE_NOTE"], key)

    def test_wave_13_exact_post_state(self):
        rows = read_rows("ORGANIZATION_SCOPE_ROLES.csv")
        self.assertEqual(199, len(rows))
        counts = {status: sum(row["VALIDATION_STATUS"] == status for row in rows) for status in {"VALIDATED", "PENDING"}}
        self.assertEqual(187, counts["VALIDATED"])
        self.assertEqual(12, counts["PENDING"])
        pending_fx = [row for row in rows if row["ROLE_CODE"] == "FX_REFERENCE_RATE_PROVIDER" and row["VALIDATION_STATUS"] == "PENDING"]
        self.assertEqual([], pending_fx)


if __name__ == "__main__":
    unittest.main()
