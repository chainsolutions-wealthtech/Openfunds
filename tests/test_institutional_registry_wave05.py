import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "data" / "reference"

WAVE05_ORGANIZATIONS = {
    "CBL",
    "BOS_LESOTHO",
    "CBE_ESWATINI",
    "FSRA_ESWATINI",
    "ESE",
    "CSO_ESWATINI",
}

WAVE05_SCOPE_ROLES = {
    ("CBL", "CENTRAL_BANK", "LESOTHO", "COUNTRY"),
    ("CBL", "CAPITAL_MARKET_REGULATOR", "LESOTHO", "COUNTRY"),
    ("CBL", "FUND_REGULATOR", "LESOTHO", "COUNTRY"),
    ("CBL", "INSURANCE_PENSION_REGULATOR", "LESOTHO", "COUNTRY"),
    ("BOS_LESOTHO", "STATISTICS_OFFICE", "LESOTHO", "COUNTRY"),
    ("CBE_ESWATINI", "CENTRAL_BANK", "ESWATINI", "COUNTRY"),
    ("FSRA_ESWATINI", "CAPITAL_MARKET_REGULATOR", "ESWATINI", "COUNTRY"),
    ("FSRA_ESWATINI", "FUND_REGULATOR", "ESWATINI", "COUNTRY"),
    ("FSRA_ESWATINI", "INSURANCE_PENSION_REGULATOR", "ESWATINI", "COUNTRY"),
    ("ESE", "STOCK_EXCHANGE", "ESWATINI", "COUNTRY"),
    ("CSO_ESWATINI", "STATISTICS_OFFICE", "ESWATINI", "COUNTRY"),
}


def read_rows(filename: str):
    with (REFERENCE / filename).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


class InstitutionalRegistryWave05ContractTests(unittest.TestCase):
    def test_wave_05_organization_allowlist_is_integrated(self):
        actual = {row["ORGANIZATION_CODE"] for row in read_rows("ORGANIZATIONS.csv")}
        self.assertTrue(WAVE05_ORGANIZATIONS.issubset(actual), WAVE05_ORGANIZATIONS - actual)

    def test_wave_05_scope_roles_are_integrated_and_validated(self):
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
        self.assertTrue(WAVE05_SCOPE_ROLES.issubset(actual), WAVE05_SCOPE_ROLES - actual)


if __name__ == "__main__":
    unittest.main()
