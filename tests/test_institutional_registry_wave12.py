import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "data" / "reference"

WAVE12_PROMOTED = {
    ("GSE", "INDEX_PROVIDER", "GHANA", "COUNTRY"),
    ("CASABLANCA_BOURSE", "INDEX_PROVIDER", "MAROC", "COUNTRY"),
    ("BRVM", "INDEX_PROVIDER", "UEMOA", "MONETARY_ZONE"),
    ("BVMAC", "INDEX_PROVIDER", "CEMAC", "MONETARY_ZONE"),
}


def read_rows(filename: str):
    with (REFERENCE / filename).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


class InstitutionalRegistryWave12ContractTests(unittest.TestCase):
    def test_wave_12_exact_existing_index_provider_roles_are_validated(self):
        rows = read_rows("ORGANIZATION_SCOPE_ROLES.csv")
        validated = {
            (row["ORGANIZATION_CODE"], row["ROLE_CODE"], row["SCOPE_ENTITY_CODE"], row["SCOPE_ENTITY_TYPE"])
            for row in rows
            if row["VALIDATION_STATUS"] == "VALIDATED"
        }
        self.assertTrue(WAVE12_PROMOTED.issubset(validated), WAVE12_PROMOTED - validated)

    def test_wave_12_does_not_duplicate_or_retarget_rows(self):
        rows = read_rows("ORGANIZATION_SCOPE_ROLES.csv")
        for key in WAVE12_PROMOTED:
            matching = [
                row for row in rows
                if (row["ORGANIZATION_CODE"], row["ROLE_CODE"], row["SCOPE_ENTITY_CODE"], row["SCOPE_ENTITY_TYPE"]) == key
            ]
            self.assertEqual(1, len(matching), key)

    def test_wave_12_source_note_is_exact(self):
        rows = read_rows("ORGANIZATION_SCOPE_ROLES.csv")
        selected = {
            (row["ORGANIZATION_CODE"], row["ROLE_CODE"], row["SCOPE_ENTITY_CODE"], row["SCOPE_ENTITY_TYPE"]): row
            for row in rows
            if (row["ORGANIZATION_CODE"], row["ROLE_CODE"], row["SCOPE_ENTITY_CODE"], row["SCOPE_ENTITY_TYPE"]) in WAVE12_PROMOTED
        }
        self.assertEqual(WAVE12_PROMOTED, set(selected))
        for key, row in selected.items():
            self.assertEqual("OFFICIAL_INDEX_PROVIDER_VERIFIED_2026_08_17_WAVE12", row["SOURCE_NOTE"], key)


if __name__ == "__main__":
    unittest.main()
