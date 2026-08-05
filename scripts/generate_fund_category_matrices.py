#!/usr/bin/env python3
"""Expand the normalized canonical fund matrices.

Committed CSV files under data/canonical are the compact, reviewable inputs.
This script deterministically expands them into one routing row per
country/category and one reference block per scope/category.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DIR = ROOT / "data" / "canonical"

SCOPE_ROUTING_PATH = CANONICAL_DIR / "FUND_SCOPE_ROUTING_V0_1.csv"
CATEGORY_TEMPLATES_PATH = CANONICAL_DIR / "CATEGORY_TEMPLATE_MATRIX_V0_1.csv"
REFERENCE_OVERRIDES_PATH = CANONICAL_DIR / "SCOPE_REFERENCE_OVERRIDES_V0_1.csv"
ANALYTICS_PATH = CANONICAL_DIR / "ANALYTICS_REFERENCE_REQUIREMENTS_V0_1.csv"

VERSION = "0.1.0"

ROUTING_FILENAME = "FUND_CATEGORY_ROUTING_MATRIX_V0_1.csv"
REFERENCE_FILENAME = "CATEGORY_REFERENCE_MATRIX_V0_1.csv"
ANALYTICS_FILENAME = "ANALYTICS_REFERENCE_REQUIREMENTS_V0_1.csv"
MANIFEST_FILENAME = "MATRIX_MANIFEST_V0_1.json"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


def render_csv(rows: Iterable[dict[str, str]], fieldnames: list[str]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=fieldnames,
        delimiter=";",
        lineterminator="\n",
        extrasaction="ignore",
    )
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def fill(template: str, scope: str) -> str:
    return template.replace("{SCOPE}", scope)


def build_scope_rows(
    scope_routing: list[dict[str, str]],
) -> list[dict[str, str]]:
    local: OrderedDict[str, dict[str, str]] = OrderedDict()
    regions: OrderedDict[str, dict[str, str]] = OrderedDict()

    for route in scope_routing:
        scope_code = route["LOCAL_SCOPE_CODE"]
        local_row = {
            "SCOPE_LEVEL": "LOCAL_MARKET",
            "SCOPE_TYPE": route["LOCAL_SCOPE_TYPE"],
            "SCOPE_CODE": scope_code,
            "PARENT_SCOPE_CODE": route["REGIONAL_SCOPE_CODE"],
            "REFERENCE_CURRENCY_CODE": route["LOCAL_CURRENCY_CODE"],
            "COMMON_EXCHANGE_CODE": route["LOCAL_EXCHANGE_CODE"],
        }
        if scope_code in local:
            existing = local[scope_code]
            for field in (
                "SCOPE_LEVEL",
                "SCOPE_TYPE",
                "SCOPE_CODE",
                "PARENT_SCOPE_CODE",
                "REFERENCE_CURRENCY_CODE",
                "COMMON_EXCHANGE_CODE",
            ):
                if existing[field] != local_row[field]:
                    raise ValueError(
                        f"Inconsistent local scope {scope_code}: "
                        f"{field}={existing[field]!r}/{local_row[field]!r}"
                    )
        else:
            local[scope_code] = local_row

        region_code = route["REGIONAL_SCOPE_CODE"]
        regions.setdefault(
            region_code,
            {
                "SCOPE_LEVEL": "REGIONAL",
                "SCOPE_TYPE": "REGION",
                "SCOPE_CODE": region_code,
                "PARENT_SCOPE_CODE": "AFRICA",
                "REFERENCE_CURRENCY_CODE": "MULTI",
                "COMMON_EXCHANGE_CODE": "",
            },
        )

    return [
        *local.values(),
        *regions.values(),
        {
            "SCOPE_LEVEL": "CONTINENTAL",
            "SCOPE_TYPE": "CONTINENT",
            "SCOPE_CODE": "AFRICA",
            "PARENT_SCOPE_CODE": "",
            "REFERENCE_CURRENCY_CODE": "MULTI",
            "COMMON_EXCHANGE_CODE": "",
        },
    ]


def override_map(
    rows: list[dict[str, str]],
) -> dict[tuple[str, str, str], dict[str, str]]:
    result: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in rows:
        key = (
            row["SCOPE_CODE"],
            row["CATEGORY_SUFFIX"],
            row["FIELD_CODE"],
        )
        if key in result:
            raise ValueError(f"Duplicate override: {key}")
        result[key] = row
    return result


def build_reference_rows(
    scopes: list[dict[str, str]],
    templates: list[dict[str, str]],
    overrides: list[dict[str, str]],
) -> list[dict[str, str]]:
    override_by_key = override_map(overrides)
    result: list[dict[str, str]] = []

    for scope in scopes:
        scope_code = scope["SCOPE_CODE"]
        for template in templates:
            suffix = template["CATEGORY_SUFFIX"]
            provider_override = override_by_key.get(
                (
                    scope_code,
                    suffix,
                    "PRIMARY_PROVIDER_SERIES_CANDIDATE_CODE",
                )
            )
            if provider_override:
                provider_code = provider_override["OVERRIDE_VALUE"]
                provider_status = provider_override["STATUS"]
            elif scope["SCOPE_LEVEL"] == "LOCAL_MARKET":
                provider_code = ""
                provider_status = "TO_RESEARCH"
            else:
                provider_code = ""
                provider_status = "CALCULATED_COMPOSITE_TO_DEFINE"

            category_code = fill(
                template["CATEGORY_CODE_TEMPLATE"],
                scope_code,
            )
            result.append(
                {
                    "REFERENCE_BLOCK_CODE": fill(
                        template["REFERENCE_BLOCK_CODE_TEMPLATE"],
                        scope_code,
                    ),
                    "CATEGORY_CODE": category_code,
                    "CATEGORY_NAME_FR": (
                        f"{template['CATEGORY_NAME_FR']} — {scope_code}"
                    ),
                    "SCOPE_LEVEL": scope["SCOPE_LEVEL"],
                    "SCOPE_TYPE": scope["SCOPE_TYPE"],
                    "SCOPE_CODE": scope_code,
                    "PARENT_SCOPE_CODE": scope["PARENT_SCOPE_CODE"],
                    "REFERENCE_CURRENCY_CODE": scope[
                        "REFERENCE_CURRENCY_CODE"
                    ],
                    "COMMON_EXCHANGE_CODE": scope[
                        "COMMON_EXCHANGE_CODE"
                    ],
                    "ASSET_CLASS_CODE": template[
                        "ASSET_CLASS_CODE"
                    ],
                    "ASSET_SUBCLASS_CODE": template[
                        "ASSET_SUBCLASS_CODE"
                    ],
                    "PEER_GROUP_CODE": fill(
                        template["PEER_GROUP_CODE_TEMPLATE"],
                        scope_code,
                    ),
                    "CATEGORY_MEAN_METHOD_CODE": template[
                        "CATEGORY_MEAN_METHOD_CODE"
                    ],
                    "CATEGORY_MEDIAN_METHOD_CODE": template[
                        "CATEGORY_MEDIAN_METHOD_CODE"
                    ],
                    "CATEGORY_WTI_CODE": fill(
                        template["CATEGORY_WTI_CODE_TEMPLATE"],
                        scope_code,
                    ),
                    "CATEGORY_WTI_METHOD_CODE": template[
                        "CATEGORY_WTI_METHOD_CODE"
                    ],
                    "PRIMARY_BENCHMARK_CODE": fill(
                        template["PRIMARY_BENCHMARK_CODE_TEMPLATE"],
                        scope_code,
                    ),
                    "PRIMARY_PROVIDER_SERIES_CANDIDATE_CODE": (
                        provider_code
                    ),
                    "PRIMARY_PROVIDER_CANDIDATE_STATUS": (
                        provider_status
                    ),
                    "SECONDARY_BENCHMARK_CODE": fill(
                        template[
                            "SECONDARY_BENCHMARK_CODE_TEMPLATE"
                        ],
                        scope_code,
                    ),
                    "WTI_BENCH_CODE": fill(
                        template["WTI_BENCH_CODE_TEMPLATE"],
                        scope_code,
                    ),
                    "WTI_BENCH_METHOD_CODE": template[
                        "WTI_BENCH_METHOD_CODE"
                    ],
                    "WTI_BENCH_STATUS": "METHODOLOGY_TO_VALIDATE",
                    "RISK_FREE_RATE_CODE": fill(
                        template["RISK_FREE_RATE_CODE_TEMPLATE"],
                        scope_code,
                    ),
                    "RISK_FREE_SELECTION_METHOD_CODE": template[
                        "RISK_FREE_SELECTION_METHOD_CODE"
                    ],
                    "RISK_FREE_STATUS": "SERIES_TO_VALIDATE",
                    "MINIMUM_ACCEPTABLE_RETURN_CODE": fill(
                        template[
                            "MINIMUM_ACCEPTABLE_RETURN_CODE_TEMPLATE"
                        ],
                        scope_code,
                    ),
                    "MAR_METHOD_CODE": template["MAR_METHOD_CODE"],
                    "DISPLAY_SERIES_1_CODE": fill(
                        template["DISPLAY_SERIES_1_CODE_TEMPLATE"],
                        scope_code,
                    ),
                    "DISPLAY_SERIES_2_CODE": fill(
                        template["DISPLAY_SERIES_2_CODE_TEMPLATE"],
                        scope_code,
                    ),
                    "DISPLAY_SERIES_3_CODE": fill(
                        template["DISPLAY_SERIES_3_CODE_TEMPLATE"],
                        scope_code,
                    ),
                    "DISPLAY_SERIES_4_OPTIONAL_CODE": fill(
                        template[
                            "DISPLAY_SERIES_4_OPTIONAL_CODE_TEMPLATE"
                        ],
                        scope_code,
                    ),
                    "DEFAULT_REFERENCE_COUNT": template[
                        "DEFAULT_REFERENCE_COUNT"
                    ],
                    "MAX_REFERENCE_COUNT": template[
                        "MAX_REFERENCE_COUNT"
                    ],
                    "RANKING_METHOD_CODE": template[
                        "RANKING_METHOD_CODE"
                    ],
                    "FX_METHOD_CODE": (
                        template["LOCAL_FX_METHOD_CODE"]
                        if scope["SCOPE_LEVEL"] == "LOCAL_MARKET"
                        else template["AGGREGATE_FX_METHOD_CODE"]
                    ),
                    "CANONICAL_STATUS": template[
                        "CANONICAL_STATUS"
                    ],
                    "PRODUCTION_STATUS": template[
                        "PRODUCTION_STATUS"
                    ],
                    "METHODOLOGY_STATUS": template[
                        "METHODOLOGY_STATUS"
                    ],
                    "VALID_FROM": "",
                    "VALID_TO": "",
                    "VERSION": template["VERSION"],
                }
            )
    return result


def build_routing_rows(
    scope_routing: list[dict[str, str]],
    templates: list[dict[str, str]],
) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for route in scope_routing:
        for template in templates:
            suffix = template["CATEGORY_SUFFIX"]
            local_category = fill(
                template["CATEGORY_CODE_TEMPLATE"],
                route["LOCAL_SCOPE_CODE"],
            )
            regional_category = fill(
                template["CATEGORY_CODE_TEMPLATE"],
                route["REGIONAL_SCOPE_CODE"],
            )
            continental_category = fill(
                template["CATEGORY_CODE_TEMPLATE"],
                route["CONTINENT_SCOPE_CODE"],
            )
            result.append(
                {
                    "ROUTING_RULE_CODE": (
                        f"ROUTE_{route['LEGAL_COUNTRY_CODE']}_{suffix}"
                    ),
                    "LEGAL_COUNTRY_ISO3": route[
                        "LEGAL_COUNTRY_ISO3"
                    ],
                    "LEGAL_COUNTRY_CODE": route[
                        "LEGAL_COUNTRY_CODE"
                    ],
                    "LEGAL_COUNTRY_NAME_FR": route[
                        "LEGAL_COUNTRY_NAME_FR"
                    ],
                    "FUND_ASSET_CLASS_CODE": template[
                        "ASSET_CLASS_CODE"
                    ],
                    "FUND_ASSET_SUBCLASS_CODE": template[
                        "ASSET_SUBCLASS_CODE"
                    ],
                    "LOCAL_SCOPE_TYPE": route[
                        "LOCAL_SCOPE_TYPE"
                    ],
                    "LOCAL_SCOPE_CODE": route[
                        "LOCAL_SCOPE_CODE"
                    ],
                    "LOCAL_EXCHANGE_CODE": route[
                        "LOCAL_EXCHANGE_CODE"
                    ],
                    "LOCAL_CURRENCY_CODE": route[
                        "LOCAL_CURRENCY_CODE"
                    ],
                    "LOCAL_CATEGORY_CODE": local_category,
                    "LOCAL_PEER_GROUP_CODE": fill(
                        template["PEER_GROUP_CODE_TEMPLATE"],
                        route["LOCAL_SCOPE_CODE"],
                    ),
                    "LOCAL_REFERENCE_BLOCK_CODE": fill(
                        template[
                            "REFERENCE_BLOCK_CODE_TEMPLATE"
                        ],
                        route["LOCAL_SCOPE_CODE"],
                    ),
                    "REGIONAL_SCOPE_CODE": route[
                        "REGIONAL_SCOPE_CODE"
                    ],
                    "REGIONAL_CATEGORY_CODE": regional_category,
                    "REGIONAL_PEER_GROUP_CODE": fill(
                        template["PEER_GROUP_CODE_TEMPLATE"],
                        route["REGIONAL_SCOPE_CODE"],
                    ),
                    "REGIONAL_REFERENCE_BLOCK_CODE": fill(
                        template[
                            "REFERENCE_BLOCK_CODE_TEMPLATE"
                        ],
                        route["REGIONAL_SCOPE_CODE"],
                    ),
                    "CONTINENT_SCOPE_CODE": route[
                        "CONTINENT_SCOPE_CODE"
                    ],
                    "CONTINENT_CATEGORY_CODE": (
                        continental_category
                    ),
                    "CONTINENT_PEER_GROUP_CODE": fill(
                        template["PEER_GROUP_CODE_TEMPLATE"],
                        route["CONTINENT_SCOPE_CODE"],
                    ),
                    "CONTINENT_REFERENCE_BLOCK_CODE": fill(
                        template[
                            "REFERENCE_BLOCK_CODE_TEMPLATE"
                        ],
                        route["CONTINENT_SCOPE_CODE"],
                    ),
                    "ROUTING_BASIS_CODE": route[
                        "ROUTING_BASIS_CODE"
                    ],
                    "ASSIGNMENT_CONFIDENCE": "DEFAULT_RULE",
                    "CANONICAL_STATUS": "STRUCTURE_PREFILLED",
                    "PRODUCTION_STATUS": "NOT_ACTIVE",
                    "VALID_FROM": "",
                    "VALID_TO": "",
                    "VERSION": VERSION,
                }
            )
    return result


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def build_outputs() -> tuple[dict[str, str], dict[str, object]]:
    scope_routing = read_csv(SCOPE_ROUTING_PATH)
    templates = read_csv(CATEGORY_TEMPLATES_PATH)
    overrides = read_csv(REFERENCE_OVERRIDES_PATH)
    analytics = ANALYTICS_PATH.read_text(encoding="utf-8")

    scopes = build_scope_rows(scope_routing)
    routing_rows = build_routing_rows(scope_routing, templates)
    reference_rows = build_reference_rows(
        scopes,
        templates,
        overrides,
    )

    routing_text = render_csv(
        routing_rows,
        list(routing_rows[0]),
    )
    reference_text = render_csv(
        reference_rows,
        list(reference_rows[0]),
    )

    outputs = {
        ROUTING_FILENAME: routing_text,
        REFERENCE_FILENAME: reference_text,
        ANALYTICS_FILENAME: analytics,
    }
    manifest: dict[str, object] = {
        "schema_version": VERSION,
        "canonical_status": "STRUCTURE_PREFILLED",
        "production_status": "NOT_ACTIVE",
        "rules": {
            "local_scope": (
                "COMMON_STOCK_MARKET_ZONE_ELSE_COUNTRY"
            ),
            "regional_scope": "AFRICA_GEOGRAPHIC_REGION",
            "continental_scope": "AFRICA",
        },
        "counts": {
            "countries": len(scope_routing),
            "local_market_scopes": len(
                {
                    row["LOCAL_SCOPE_CODE"]
                    for row in scope_routing
                }
            ),
            "regions": len(
                {
                    row["REGIONAL_SCOPE_CODE"]
                    for row in scope_routing
                }
            ),
            "continental_scopes": 1,
            "category_templates": len(templates),
            "routing_rules": len(routing_rows),
            "category_reference_blocks": len(reference_rows),
            "analytics_metrics": len(
                read_csv(ANALYTICS_PATH)
            ),
        },
        "outputs": {
            name: {
                "sha256": sha256_text(content),
                "rows": (
                    content.count("\n") - 1
                    if name.endswith(".csv")
                    else None
                ),
            }
            for name, content in outputs.items()
        },
    }
    outputs[MANIFEST_FILENAME] = (
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    return outputs, manifest


def validate(
    outputs: dict[str, str],
    manifest: dict[str, object],
) -> list[str]:
    errors: list[str] = []
    counts = manifest["counts"]

    expected_counts = {
        "countries": 54,
        "local_market_scopes": 42,
        "regions": 5,
        "continental_scopes": 1,
        "category_templates": 9,
        "routing_rules": 486,
        "category_reference_blocks": 432,
        "analytics_metrics": 25,
    }
    for key, expected in expected_counts.items():
        actual = counts[key]
        if actual != expected:
            errors.append(
                f"{key}: expected {expected}, got {actual}"
            )

    routing = list(
        csv.DictReader(
            io.StringIO(outputs[ROUTING_FILENAME]),
            delimiter=";",
        )
    )
    references = list(
        csv.DictReader(
            io.StringIO(outputs[REFERENCE_FILENAME]),
            delimiter=";",
        )
    )
    categories = {
        row["CATEGORY_CODE"] for row in references
    }
    if len(categories) != len(references):
        errors.append("CATEGORY_CODE values are not unique")
    if len(
        {row["REFERENCE_BLOCK_CODE"] for row in references}
    ) != len(references):
        errors.append(
            "REFERENCE_BLOCK_CODE values are not unique"
        )

    for route in routing:
        for field in (
            "LOCAL_CATEGORY_CODE",
            "REGIONAL_CATEGORY_CODE",
            "CONTINENT_CATEGORY_CODE",
        ):
            if route[field] not in categories:
                errors.append(
                    f"{route['ROUTING_RULE_CODE']} targets "
                    f"unknown {field}={route[field]}"
                )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate the matrices without writing files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "build" / "canonical",
        help="Directory receiving expanded CSV and manifest files.",
    )
    args = parser.parse_args()

    outputs, manifest = build_outputs()
    errors = validate(outputs, manifest)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    if args.check:
        print(
            "Canonical fund matrices validated: "
            "486 routing rules, 432 reference blocks."
        )
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, content in outputs.items():
        (args.output_dir / name).write_text(
            content,
            encoding="utf-8",
        )
    print(f"Canonical fund matrices written to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
