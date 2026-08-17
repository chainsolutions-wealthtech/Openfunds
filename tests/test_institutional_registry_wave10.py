import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "data" / "reference"

WAVE10_PROMOTED = {
    ("SARB", "CENTRAL_BANK", "AFRIQUE_DU_SUD", "COUNTRY"),
    ("JSE", "STOCK_EXCHANGE", "AFRIQUE_DU_SUD", "COUNTRY"),
    ("CBK", "CENTRAL_BANK", "KENYA", "COUNTRY"),
    ("CMA_KENYA", "FUND_REGULATOR", "KENYA", "COUNTRY"),
    ("KNBS", "STATISTICS_OFFICE", "KENYA", "COUNTRY"),
    ("NATIONAL_TREASURY_KENYA", "TREASURY", "KENYA", "COUNTRY"),
    ("FRA_EGYPT", "FUND_REGULATOR", "EGYPTE", "COUNTRY"),
    ("CAPMAS", "STATISTICS_OFFICE", "EGYPTE", "COUNTRY"),
    ("MOF_EGYPT", "MINISTRY_OF_FINANCE", "EGYPTE", "COUNTRY"),
    ("DMO_NIGERIA", "DEBT_MANAGEMENT_OFFICE", "NIGERIA", "COUNTRY"),
    ("NBS_NIGERIA", "STATISTICS_OFFICE", "NIGERIA", "COUNTRY"),
    ("INS_TUNISIE", "STATISTICS_OFFICE", "TUNISIE", "COUNTRY"),
}


def read_rows(filename: str):
    with (REFERENCE / filename).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


class InstitutionalRegistryWave10ContractTests(unittest.TestCase):
    def test_wave_10_exact_existing_roles_are_validated(self):
        rows = read_rows("ORGANIZATION_SCOPE_ROLES.csv")
        validated = {
            (row["ORGANIZATION_CODE"], row["ROLE_CODE"], row["SCOPE_ENTITY_CODE"], row["SCOPE_ENTITY_TYPE"])
            for row in rows
            if row["VALIDATION_STATUS"] == "VALIDATED"
        }
        self.assertTrue(WAVE10_PROMOTED.issubset(validated), WAVE10_PROMOTED - validated)

    def test_wave_10_does_not_duplicate_or_retarget_rows(self):
        rows = read_rows("ORGANIZATION_SCOPE_ROLES.csv")
        for key in WAVE10_PROMOTED:
            matching = [
                row for row in rows
                if (row["ORGANIZATION_CODE"], row["ROLE_CODE"], row["SCOPE_ENTITY_CODE"], row["SCOPE_ENTITY_TYPE"]) == key
            ]
            self.assertEqual(1, len(matching), key)

    def test_wave_10_source_note_is_exact(self):
        rows = read_rows("ORGANIZATION_SCOPE_ROLES.csv")
        selected = {
            (row["ORGANIZATION_CODE"], row["ROLE_CODE"], row["SCOPE_ENTITY_CODE"], row["SCOPE_ENTITY_TYPE"]): row
            for row in rows
            if (row["ORGANIZATION_CODE"], row["ROLE_CODE"], row["SCOPE_ENTITY_CODE"], row["SCOPE_ENTITY_TYPE"]) in WAVE10_PROMOTED
        }
        self.assertEqual(WAVE10_PROMOTED, set(selected))
        for key, row in selected.items():
            self.assertEqual("OFFICIAL_ROLE_VERIFIED_2026_08_17_WAVE10", row["SOURCE_NOTE"], key)


if __name__ == "__main__":
    unittest.main()
