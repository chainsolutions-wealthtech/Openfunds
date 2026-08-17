import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "data" / "reference"

WAVE11_PROMOTED = {
    ("EGX", "STOCK_EXCHANGE", "EGYPTE", "COUNTRY"),
    ("GSE", "STOCK_EXCHANGE", "GHANA", "COUNTRY"),
    ("NGX", "STOCK_EXCHANGE", "NIGERIA", "COUNTRY"),
}


def read_rows(filename: str):
    with (REFERENCE / filename).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


class InstitutionalRegistryWave11ContractTests(unittest.TestCase):
    def test_wave_11_exact_existing_exchange_roles_are_validated(self):
        rows = read_rows("ORGANIZATION_SCOPE_ROLES.csv")
        validated = {
            (row["ORGANIZATION_CODE"], row["ROLE_CODE"], row["SCOPE_ENTITY_CODE"], row["SCOPE_ENTITY_TYPE"])
            for row in rows
            if row["VALIDATION_STATUS"] == "VALIDATED"
        }
        self.assertTrue(WAVE11_PROMOTED.issubset(validated), WAVE11_PROMOTED - validated)

    def test_wave_11_does_not_duplicate_or_retarget_rows(self):
        rows = read_rows("ORGANIZATION_SCOPE_ROLES.csv")
        for key in WAVE11_PROMOTED:
            matching = [
                row for row in rows
                if (row["ORGANIZATION_CODE"], row["ROLE_CODE"], row["SCOPE_ENTITY_CODE"], row["SCOPE_ENTITY_TYPE"]) == key
            ]
            self.assertEqual(1, len(matching), key)

    def test_wave_11_source_note_is_exact(self):
        rows = read_rows("ORGANIZATION_SCOPE_ROLES.csv")
        selected = {
            (row["ORGANIZATION_CODE"], row["ROLE_CODE"], row["SCOPE_ENTITY_CODE"], row["SCOPE_ENTITY_TYPE"]): row
            for row in rows
            if (row["ORGANIZATION_CODE"], row["ROLE_CODE"], row["SCOPE_ENTITY_CODE"], row["SCOPE_ENTITY_TYPE"]) in WAVE11_PROMOTED
        }
        self.assertEqual(WAVE11_PROMOTED, set(selected))
        for key, row in selected.items():
            self.assertEqual("OFFICIAL_ROLE_VERIFIED_2026_08_17_WAVE11", row["SOURCE_NOTE"], key)


if __name__ == "__main__":
    unittest.main()
