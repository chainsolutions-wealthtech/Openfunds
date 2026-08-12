import csv
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "data" / "reference"
CODE_RE = re.compile(r"^[A-Z0-9_]+$")
ALLOWED_STATUS = {"PENDING", "VALIDATED", "REJECTED", "SUPERSEDED"}

WAVE01_ORGANIZATIONS = {
    "BOB",
    "NBFIRA",
    "BSE",
    "STATISTICS_BOTSWANA",
    "BON",
    "NAMFISA",
    "NSX",
    "NSA_NAMIBIA",
    "NBE",
    "ECMA",
    "ESX",
    "ESS_ETHIOPIA",
    "AMF_UMOA",
    "UMOA_TITRES",
    "COSUMAF",
}

WAVE01_SCOPE_ROLES = {
    ("BOB", "CENTRAL_BANK", "BOTSWANA", "COUNTRY"),
    ("NBFIRA", "CAPITAL_MARKET_REGULATOR", "BOTSWANA", "COUNTRY"),
    ("NBFIRA", "FUND_REGULATOR", "BOTSWANA", "COUNTRY"),
    ("NBFIRA", "INSURANCE_PENSION_REGULATOR", "BOTSWANA", "COUNTRY"),
    ("BSE", "STOCK_EXCHANGE", "BOTSWANA", "COUNTRY"),
    ("STATISTICS_BOTSWANA", "STATISTICS_OFFICE", "BOTSWANA", "COUNTRY"),
    ("BON", "CENTRAL_BANK", "NAMIBIE", "COUNTRY"),
    ("NAMFISA", "CAPITAL_MARKET_REGULATOR", "NAMIBIE", "COUNTRY"),
    ("NAMFISA", "FUND_REGULATOR", "NAMIBIE", "COUNTRY"),
    ("NAMFISA", "INSURANCE_PENSION_REGULATOR", "NAMIBIE", "COUNTRY"),
    ("NSX", "STOCK_EXCHANGE", "NAMIBIE", "COUNTRY"),
    ("NSA_NAMIBIA", "STATISTICS_OFFICE", "NAMIBIE", "COUNTRY"),
    ("NBE", "CENTRAL_BANK", "ETHIOPIE", "COUNTRY"),
    ("ECMA", "CAPITAL_MARKET_REGULATOR", "ETHIOPIE", "COUNTRY"),
    ("ECMA", "FUND_REGULATOR", "ETHIOPIE", "COUNTRY"),
    ("ESX", "STOCK_EXCHANGE", "ETHIOPIE", "COUNTRY"),
    ("ESS_ETHIOPIA", "STATISTICS_OFFICE", "ETHIOPIE", "COUNTRY"),
    ("AMF_UMOA", "CAPITAL_MARKET_REGULATOR", "UEMOA", "MONETARY_ZONE"),
    ("AMF_UMOA", "FUND_REGULATOR", "UEMOA", "MONETARY_ZONE"),
    ("UMOA_TITRES", "GOVERNMENT_SECURITIES_AGENCY", "UEMOA", "MONETARY_ZONE"),
    ("COSUMAF", "CAPITAL_MARKET_REGULATOR", "CEMAC", "MONETARY_ZONE"),
    ("COSUMAF", "FUND_REGULATOR", "CEMAC", "MONETARY_ZONE"),
}


def read_rows(filename: str):
    with (REFERENCE / filename).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


class InstitutionalRegistryContractTests(unittest.TestCase):
    def test_validator_cli_accepts_registry(self):
        result = subprocess.run(
            [sys.executable, "scripts/validate_institutional_registry.py", "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_existing_registry_invariants(self):
        countries = read_rows("AFRICA_COUNTRIES.csv")
        organizations = read_rows("ORGANIZATIONS.csv")
        roles = read_rows("ORGANIZATION_ROLES.csv")
        scope_roles = read_rows("ORGANIZATION_SCOPE_ROLES.csv")
        endpoints = read_rows("SOURCE_ENDPOINTS.csv")

        country_codes = {row["COUNTRY_CODE"] for row in countries}
        organization_codes = [row["ORGANIZATION_CODE"] for row in organizations]
        role_codes = {row["ROLE_CODE"] for row in roles}

        self.assertEqual(len(countries), 54)
        self.assertEqual(len(organization_codes), len(set(organization_codes)))
        self.assertTrue(all(CODE_RE.fullmatch(code) for code in organization_codes))
        self.assertTrue(all(CODE_RE.fullmatch(code) for code in role_codes))

        for row in organizations:
            self.assertIn(row["VALIDATION_STATUS"], ALLOWED_STATUS)
            if row["PRIMARY_COUNTRY_CODE"]:
                self.assertIn(row["PRIMARY_COUNTRY_CODE"], country_codes)
            if row["VALIDATION_STATUS"] == "VALIDATED":
                self.assertTrue(row["OFFICIAL_WEBSITE"], row["ORGANIZATION_CODE"])

        for row in scope_roles:
            self.assertIn(row["ORGANIZATION_CODE"], set(organization_codes))
            self.assertIn(row["ROLE_CODE"], role_codes)
            self.assertIn(row["VALIDATION_STATUS"], ALLOWED_STATUS)
            if row["SCOPE_ENTITY_TYPE"] == "COUNTRY":
                self.assertIn(row["SCOPE_ENTITY_CODE"], country_codes)

        endpoint_codes = [row["ENDPOINT_CODE"] for row in endpoints]
        self.assertEqual(len(endpoint_codes), len(set(endpoint_codes)))
        self.assertTrue(all(CODE_RE.fullmatch(code) for code in endpoint_codes))
        for row in endpoints:
            self.assertIn(row["ORGANIZATION_CODE"], set(organization_codes))
            self.assertIn(row["VALIDATION_STATUS"], ALLOWED_STATUS)
            if row["VALIDATION_STATUS"] == "VALIDATED":
                self.assertTrue(
                    row["OFFICIAL_URL"] or row["DATA_PORTAL_URL"] or row["API_BASE_URL"],
                    row["ENDPOINT_CODE"],
                )

    def test_wave_01_organization_allowlist_is_integrated(self):
        actual = {row["ORGANIZATION_CODE"] for row in read_rows("ORGANIZATIONS.csv")}
        self.assertTrue(WAVE01_ORGANIZATIONS.issubset(actual), WAVE01_ORGANIZATIONS - actual)

    def test_wave_01_scope_roles_are_integrated_and_validated(self):
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
        self.assertTrue(WAVE01_SCOPE_ROLES.issubset(actual), WAVE01_SCOPE_ROLES - actual)


if __name__ == "__main__":
    unittest.main()
