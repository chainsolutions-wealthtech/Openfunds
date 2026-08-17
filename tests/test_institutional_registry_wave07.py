import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "data" / "reference"

WAVE07_ORGANIZATIONS = {
    "INSTAD_BENIN", "INSD_BURKINA", "ANSTAT_CIV", "INE_GUINEE_BISSAU",
    "INSTAT_MALI", "INS_NIGER", "ANSD_SENEGAL", "INSEED_TOGO",
}

WAVE07_SCOPE_ROLES = {
    ("INSTAD_BENIN", "STATISTICS_OFFICE", "BENIN", "COUNTRY"),
    ("INSD_BURKINA", "STATISTICS_OFFICE", "BURKINA_FASO", "COUNTRY"),
    ("ANSTAT_CIV", "STATISTICS_OFFICE", "COTE_DIVOIRE", "COUNTRY"),
    ("INE_GUINEE_BISSAU", "STATISTICS_OFFICE", "GUINEE_BISSAU", "COUNTRY"),
    ("INSTAT_MALI", "STATISTICS_OFFICE", "MALI", "COUNTRY"),
    ("INS_NIGER", "STATISTICS_OFFICE", "NIGER", "COUNTRY"),
    ("ANSD_SENEGAL", "STATISTICS_OFFICE", "SENEGAL", "COUNTRY"),
    ("INSEED_TOGO", "STATISTICS_OFFICE", "TOGO", "COUNTRY"),
}

def read_rows(filename: str):
    with (REFERENCE / filename).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))

class InstitutionalRegistryWave07ContractTests(unittest.TestCase):
    def test_wave_07_organization_allowlist_is_integrated(self):
        actual = {row["ORGANIZATION_CODE"] for row in read_rows("ORGANIZATIONS.csv")}
        self.assertTrue(WAVE07_ORGANIZATIONS.issubset(actual), WAVE07_ORGANIZATIONS - actual)

    def test_wave_07_scope_roles_are_integrated_and_validated(self):
        actual = {
            (row["ORGANIZATION_CODE"], row["ROLE_CODE"], row["SCOPE_ENTITY_CODE"], row["SCOPE_ENTITY_TYPE"])
            for row in read_rows("ORGANIZATION_SCOPE_ROLES.csv")
            if row["VALIDATION_STATUS"] == "VALIDATED"
        }
        self.assertTrue(WAVE07_SCOPE_ROLES.issubset(actual), WAVE07_SCOPE_ROLES - actual)

if __name__ == "__main__":
    unittest.main()
