import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "data" / "reference"

WAVE08_ORGANIZATIONS = {
    "INSBU", "ICASEES", "INS_CAMEROUN", "INS_RDC", "INS_CONGO", "INSEED_COMORES",
    "INSTAD_DJIBOUTI", "DGS_GABON", "INEGE", "BSC_LIBYA", "INSTAT_MADAGASCAR",
    "ANSADE", "CBOS", "SNBS", "NBS_SOUTH_SUDAN", "INE_STP", "INSEED_TCHAD",
}

WAVE08_SCOPE_ROLES = {
    ("INSBU", "STATISTICS_OFFICE", "BURUNDI", "COUNTRY"),
    ("ICASEES", "STATISTICS_OFFICE", "REPUBLIQUE_CENTRAFRICAINE", "COUNTRY"),
    ("INS_CAMEROUN", "STATISTICS_OFFICE", "CAMEROUN", "COUNTRY"),
    ("INS_RDC", "STATISTICS_OFFICE", "REPUBLIQUE_DEMOCRATIQUE_DU_CONGO", "COUNTRY"),
    ("INS_CONGO", "STATISTICS_OFFICE", "REPUBLIQUE_DU_CONGO", "COUNTRY"),
    ("INSEED_COMORES", "STATISTICS_OFFICE", "COMORES", "COUNTRY"),
    ("INSTAD_DJIBOUTI", "STATISTICS_OFFICE", "DJIBOUTI", "COUNTRY"),
    ("DGS_GABON", "STATISTICS_OFFICE", "GABON", "COUNTRY"),
    ("INEGE", "STATISTICS_OFFICE", "GUINEE_EQUATORIALE", "COUNTRY"),
    ("BSC_LIBYA", "STATISTICS_OFFICE", "LIBYE", "COUNTRY"),
    ("INSTAT_MADAGASCAR", "STATISTICS_OFFICE", "MADAGASCAR", "COUNTRY"),
    ("ANSADE", "STATISTICS_OFFICE", "MAURITANIE", "COUNTRY"),
    ("CBOS", "CENTRAL_BANK", "SOUDAN", "COUNTRY"),
    ("SNBS", "STATISTICS_OFFICE", "SOMALIE", "COUNTRY"),
    ("NBS_SOUTH_SUDAN", "STATISTICS_OFFICE", "SOUDAN_DU_SUD", "COUNTRY"),
    ("INE_STP", "STATISTICS_OFFICE", "SAO_TOME_ET_PRINCIPE", "COUNTRY"),
    ("INSEED_TCHAD", "STATISTICS_OFFICE", "TCHAD", "COUNTRY"),
}


def read_rows(filename: str):
    with (REFERENCE / filename).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


class InstitutionalRegistryWave08ContractTests(unittest.TestCase):
    def test_wave_08_organization_allowlist_is_integrated(self):
        actual = {row["ORGANIZATION_CODE"] for row in read_rows("ORGANIZATIONS.csv")}
        self.assertTrue(WAVE08_ORGANIZATIONS.issubset(actual), WAVE08_ORGANIZATIONS - actual)

    def test_wave_08_scope_roles_are_integrated_and_validated(self):
        actual = {
            (row["ORGANIZATION_CODE"], row["ROLE_CODE"], row["SCOPE_ENTITY_CODE"], row["SCOPE_ENTITY_TYPE"])
            for row in read_rows("ORGANIZATION_SCOPE_ROLES.csv")
            if row["VALIDATION_STATUS"] == "VALIDATED"
        }
        self.assertTrue(WAVE08_SCOPE_ROLES.issubset(actual), WAVE08_SCOPE_ROLES - actual)

    def test_eritrea_remains_uncovered_until_primary_official_source_is_verified(self):
        organizations = read_rows("ORGANIZATIONS.csv")
        covered = {row["PRIMARY_COUNTRY_CODE"] for row in organizations if row["PRIMARY_COUNTRY_CODE"]}
        self.assertNotIn("ERYTHREE", covered)


if __name__ == "__main__":
    unittest.main()
