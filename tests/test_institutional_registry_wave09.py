import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "data" / "reference"

WAVE09_PROMOTED = {
    ("BCEAO", "CENTRAL_BANK", "UEMOA", "MONETARY_ZONE"),
    ("BEAC", "CENTRAL_BANK", "CEMAC", "MONETARY_ZONE"),
    ("BRVM", "COMMON_STOCK_EXCHANGE", "UEMOA", "MONETARY_ZONE"),
    ("BVMAC", "COMMON_STOCK_EXCHANGE", "CEMAC", "MONETARY_ZONE"),
}


def read_rows(filename: str):
    with (REFERENCE / filename).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


class InstitutionalRegistryWave09ContractTests(unittest.TestCase):
    def test_wave_09_exact_zone_roles_are_validated(self):
        rows = read_rows("ORGANIZATION_SCOPE_ROLES.csv")
        validated = {
            (row["ORGANIZATION_CODE"], row["ROLE_CODE"], row["SCOPE_ENTITY_CODE"], row["SCOPE_ENTITY_TYPE"])
            for row in rows
            if row["VALIDATION_STATUS"] == "VALIDATED"
        }
        self.assertTrue(WAVE09_PROMOTED.issubset(validated), WAVE09_PROMOTED - validated)

    def test_wave_09_does_not_duplicate_exact_zone_roles(self):
        rows = read_rows("ORGANIZATION_SCOPE_ROLES.csv")
        for key in WAVE09_PROMOTED:
            matching = [
                row for row in rows
                if (row["ORGANIZATION_CODE"], row["ROLE_CODE"], row["SCOPE_ENTITY_CODE"], row["SCOPE_ENTITY_TYPE"]) == key
            ]
            self.assertEqual(1, len(matching), key)


if __name__ == "__main__":
    unittest.main()
