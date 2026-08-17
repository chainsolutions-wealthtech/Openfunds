import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "data" / "reference"

WAVE06_ORGANIZATIONS = {
    "CBL_LIBERIA",
    "LISGIS",
    "CBG",
    "GBOS_GAMBIA",
    "BSL",
    "STATS_SL",
    "BCRG",
    "INS_GUINEE",
}

WAVE06_SCOPE_ROLES = {
    ("CBL_LIBERIA", "CENTRAL_BANK", "LIBERIA", "COUNTRY"),
    ("LISGIS", "STATISTICS_OFFICE", "LIBERIA", "COUNTRY"),
    ("CBG", "CENTRAL_BANK", "GAMBIE", "COUNTRY"),
    ("GBOS_GAMBIA", "STATISTICS_OFFICE", "GAMBIE", "COUNTRY"),
    ("BSL", "CENTRAL_BANK", "SIERRA_LEONE", "COUNTRY"),
    ("STATS_SL", "STATISTICS_OFFICE", "SIERRA_LEONE", "COUNTRY"),
    ("BCRG", "CENTRAL_BANK", "GUINEE", "COUNTRY"),
    ("INS_GUINEE", "STATISTICS_OFFICE", "GUINEE", "COUNTRY"),
}


def read_rows(filename: str):
    with (REFERENCE / filename).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


class InstitutionalRegistryWave06ContractTests(unittest.TestCase):
    def test_wave_06_organization_allowlist_is_integrated(self):
        actual = {row["ORGANIZATION_CODE"] for row in read_rows("ORGANIZATIONS.csv")}
        self.assertTrue(WAVE06_ORGANIZATIONS.issubset(actual), WAVE06_ORGANIZATIONS - actual)

    def test_wave_06_scope_roles_are_integrated_and_validated(self):
        actual = {
            (
                row["ORGANIZATION_CODE"],
                row["ROLE_CODE"],
                row["SCOPE_ENTITY_CODE"],
                row["SCOPE_ENTITY_TYPE"],
            )
            for row in read_rows("ORGANIZATION_SCOPE_ROLES.csv")
            if row["VALIDATION_STATUS"] == "VALIDATED"
        }
        self.assertTrue(WAVE06_SCOPE_ROLES.issubset(actual), WAVE06_SCOPE_ROLES - actual)


if __name__ == "__main__":
    unittest.main()
