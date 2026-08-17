#!/usr/bin/env python3
"""Read-only institutional role-coverage audit for OF-SOURCE-002."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "data" / "reference"

ROLE_GROUPS = {
    "MONETARY_AUTHORITY": {"CENTRAL_BANK", "MONETARY_AUTHORITY"},
    "STATISTICS": {"STATISTICS_OFFICE"},
    "CAPITAL_MARKET_REGULATION": {"CAPITAL_MARKET_REGULATOR"},
    "FUND_REGULATION": {"FUND_REGULATOR"},
    "INSURANCE_PENSION_REGULATION": {"INSURANCE_PENSION_REGULATOR"},
    "EXCHANGE": {"STOCK_EXCHANGE", "COMMON_STOCK_EXCHANGE"},
    "FISCAL_DEBT": {
        "MINISTRY_OF_FINANCE",
        "TREASURY",
        "DEBT_MANAGEMENT_OFFICE",
        "GOVERNMENT_SECURITIES_AGENCY",
    },
}


def rows(name: str):
    with (REF / name).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


def main() -> int:
    countries = [r["COUNTRY_CODE"] for r in rows("AFRICA_COUNTRIES.csv")]
    relationships = rows("COUNTRY_RELATIONSHIPS.csv")
    role_rows = rows("ORGANIZATION_SCOPE_ROLES.csv")

    roles_by_scope: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in role_rows:
        if row["VALIDATION_STATUS"] != "VALIDATED":
            continue
        roles_by_scope[(row["SCOPE_ENTITY_TYPE"], row["SCOPE_ENTITY_CODE"])].add(row["ROLE_CODE"])

    related_scopes: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for row in relationships:
        country = row["SOURCE_ENTITY_CODE"]
        if country not in countries:
            continue
        relationship = row["RELATIONSHIP_TYPE"]
        target = row["TARGET_ENTITY_CODE"]
        if relationship in {"USES_MARKET_SCOPE", "BELONGS_TO_MONETARY_ZONE"} and target != country:
            related_scopes[country].add(("ZONE", target))

    report = []
    missing_totals = defaultdict(int)
    complete = 0

    for country in countries:
        effective_roles = set(roles_by_scope.get(("COUNTRY", country), set()))
        inherited = {}
        for scope in sorted(related_scopes.get(country, set())):
            inherited_roles = roles_by_scope.get(scope, set())
            if inherited_roles:
                inherited[f"{scope[0]}:{scope[1]}"] = sorted(inherited_roles)
                effective_roles.update(inherited_roles)

        group_status = {}
        missing = []
        for group, accepted_roles in ROLE_GROUPS.items():
            matches = sorted(effective_roles & accepted_roles)
            group_status[group] = matches
            if not matches:
                missing.append(group)
                missing_totals[group] += 1

        if not missing:
            complete += 1

        report.append(
            {
                "country": country,
                "country_roles": sorted(roles_by_scope.get(("COUNTRY", country), set())),
                "inherited_zone_roles": inherited,
                "effective_role_groups": group_status,
                "missing_role_groups": missing,
            }
        )

    payload = {
        "countries": len(countries),
        "countries_complete_for_required_groups": complete,
        "required_role_groups": list(ROLE_GROUPS),
        "missing_group_counts": dict(sorted(missing_totals.items())),
        "countries_detail": report,
    }

    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
