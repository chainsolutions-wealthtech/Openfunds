#!/usr/bin/env python3
"""Validate discovery institutional reference registries without promoting runtime status."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "data" / "reference"
CODE_RE = re.compile(r"^[A-Z0-9_]+$")
ALLOWED_STATUS = {"PENDING", "VALIDATED", "REJECTED", "SUPERSEDED"}


def rows(filename: str) -> list[dict[str, str]]:
    path = REFERENCE / filename
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate() -> list[str]:
    errors: list[str] = []
    countries = rows("AFRICA_COUNTRIES.csv")
    zones = rows("MARKET_ZONES.csv")
    organizations = rows("ORGANIZATIONS.csv")
    roles = rows("ORGANIZATION_ROLES.csv")
    scope_roles = rows("ORGANIZATION_SCOPE_ROLES.csv")
    endpoints = rows("SOURCE_ENDPOINTS.csv")

    country_codes = {row["COUNTRY_CODE"] for row in countries}
    zone_codes = {row["ZONE_CODE"] for row in zones}
    organization_codes = [row["ORGANIZATION_CODE"] for row in organizations]
    role_codes = [row["ROLE_CODE"] for row in roles]
    endpoint_codes = [row["ENDPOINT_CODE"] for row in endpoints]

    require(len(countries) == 54, f"expected 54 countries, found {len(countries)}", errors)
    require(len(organization_codes) == len(set(organization_codes)), "duplicate organization code", errors)
    require(len(role_codes) == len(set(role_codes)), "duplicate organization role code", errors)
    require(len(endpoint_codes) == len(set(endpoint_codes)), "duplicate endpoint code", errors)

    for kind, codes in (
        ("organization", organization_codes),
        ("role", role_codes),
        ("endpoint", endpoint_codes),
    ):
        for code in codes:
            require(bool(CODE_RE.fullmatch(code)), f"invalid {kind} technical code: {code}", errors)

    organization_set = set(organization_codes)
    role_set = set(role_codes)

    for row in organizations:
        code = row["ORGANIZATION_CODE"]
        require(row["VALIDATION_STATUS"] in ALLOWED_STATUS, f"invalid organization status: {code}", errors)
        if row["PRIMARY_COUNTRY_CODE"]:
            require(
                row["PRIMARY_COUNTRY_CODE"] in country_codes,
                f"unknown primary country for {code}: {row['PRIMARY_COUNTRY_CODE']}",
                errors,
            )
        if row["PRIMARY_ZONE_CODE"]:
            require(
                row["PRIMARY_ZONE_CODE"] in zone_codes,
                f"unknown primary zone for {code}: {row['PRIMARY_ZONE_CODE']}",
                errors,
            )
        if row["VALIDATION_STATUS"] == "VALIDATED":
            require(bool(row["OFFICIAL_WEBSITE"]), f"validated organization without official website: {code}", errors)

    seen_scope_roles: set[tuple[str, str, str, str]] = set()
    for row in scope_roles:
        key = (
            row["ORGANIZATION_CODE"],
            row["ROLE_CODE"],
            row["SCOPE_ENTITY_CODE"],
            row["SCOPE_ENTITY_TYPE"],
        )
        require(key not in seen_scope_roles, f"duplicate organization scope role: {key}", errors)
        seen_scope_roles.add(key)
        require(row["ORGANIZATION_CODE"] in organization_set, f"unknown organization in scope role: {key}", errors)
        require(row["ROLE_CODE"] in role_set, f"unknown role in scope role: {key}", errors)
        require(row["VALIDATION_STATUS"] in ALLOWED_STATUS, f"invalid scope-role status: {key}", errors)
        if row["SCOPE_ENTITY_TYPE"] == "COUNTRY":
            require(row["SCOPE_ENTITY_CODE"] in country_codes, f"unknown country scope: {key}", errors)
        elif row["SCOPE_ENTITY_TYPE"] in {"MONETARY_ZONE", "MARKET_ZONE"}:
            require(row["SCOPE_ENTITY_CODE"] in zone_codes, f"unknown zone scope: {key}", errors)

    for row in endpoints:
        code = row["ENDPOINT_CODE"]
        require(row["ORGANIZATION_CODE"] in organization_set, f"unknown endpoint organization: {code}", errors)
        require(row["VALIDATION_STATUS"] in ALLOWED_STATUS, f"invalid endpoint status: {code}", errors)
        if row["SCOPE_TYPE"] == "COUNTRY":
            require(row["SCOPE_CODE"] in country_codes, f"unknown endpoint country scope: {code}", errors)
        elif row["SCOPE_TYPE"] == "ZONE":
            require(row["SCOPE_CODE"] in zone_codes, f"unknown endpoint zone scope: {code}", errors)
        if row["VALIDATION_STATUS"] == "VALIDATED":
            require(
                bool(row["OFFICIAL_URL"] or row["DATA_PORTAL_URL"] or row["API_BASE_URL"]),
                f"validated endpoint without canonical URL: {code}",
                errors,
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate institutional registries")
    parser.parse_args()

    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("institutional registry validation: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
