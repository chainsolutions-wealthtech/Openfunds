#!/usr/bin/env python3
"""Generate the governed PostgreSQL migration for canonical fund taxonomy V0.1."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_DIR = ROOT / "data" / "canonical"
DEFAULT_OUTPUT = ROOT / "schemas" / "taxonomy" / "017_canonical_fund_taxonomy_v0_1.sql"

FILES = {
    "asset_classes": "ASSET_CLASSES_V0_1.csv",
    "asset_subclasses": "ASSET_SUBCLASSES_V0_1.csv",
    "fund_scope_routing": "FUND_SCOPE_ROUTING_V0_1.csv",
    "category_templates": "CATEGORY_TEMPLATE_MATRIX_V0_1.csv",
    "scope_reference_overrides": "SCOPE_REFERENCE_OVERRIDES_V0_1.csv",
    "analytics_reference_requirements": "ANALYTICS_REFERENCE_REQUIREMENTS_V0_1.csv",
}
MANIFEST = "MATRIX_MANIFEST_V0_1.json"

EXPECTED_HEADERS = {
    "asset_classes": (
        "ASSET_CLASS_CODE", "NAME_FR", "REQUIRES_SUBCLASS", "SUBCLASS_DIMENSION", "IS_ACTIVE", "VERSION"
    ),
    "asset_subclasses": (
        "ASSET_CLASS_CODE", "ASSET_SUBCLASS_CODE", "NAME_FR", "SUBCLASS_DIMENSION", "SORT_ORDER", "IS_ACTIVE", "VERSION"
    ),
    "fund_scope_routing": (
        "LEGAL_COUNTRY_ISO3", "LEGAL_COUNTRY_CODE", "LEGAL_COUNTRY_NAME_FR", "LOCAL_SCOPE_TYPE", "LOCAL_SCOPE_CODE",
        "LOCAL_EXCHANGE_CODE", "LOCAL_CURRENCY_CODE", "REGIONAL_SCOPE_CODE", "CONTINENT_SCOPE_CODE", "ROUTING_BASIS_CODE",
        "STATUS", "VERSION"
    ),
    "category_templates": (
        "CATEGORY_TEMPLATE_CODE", "ASSET_CLASS_CODE", "ASSET_SUBCLASS_CODE", "CATEGORY_NAME_FR", "CATEGORY_SUFFIX",
        "CATEGORY_CODE_TEMPLATE", "REFERENCE_BLOCK_CODE_TEMPLATE", "PEER_GROUP_CODE_TEMPLATE", "CATEGORY_WTI_CODE_TEMPLATE",
        "CATEGORY_WTI_METHOD_CODE", "CATEGORY_MEAN_METHOD_CODE", "CATEGORY_MEDIAN_METHOD_CODE", "PRIMARY_BENCHMARK_CODE_TEMPLATE",
        "SECONDARY_BENCHMARK_CODE_TEMPLATE", "WTI_BENCH_CODE_TEMPLATE", "WTI_BENCH_METHOD_CODE", "RISK_FREE_RATE_CODE_TEMPLATE",
        "RISK_FREE_SELECTION_METHOD_CODE", "MINIMUM_ACCEPTABLE_RETURN_CODE_TEMPLATE", "MAR_METHOD_CODE",
        "DISPLAY_SERIES_1_CODE_TEMPLATE", "DISPLAY_SERIES_2_CODE_TEMPLATE", "DISPLAY_SERIES_3_CODE_TEMPLATE",
        "DISPLAY_SERIES_4_OPTIONAL_CODE_TEMPLATE", "DEFAULT_REFERENCE_COUNT", "MAX_REFERENCE_COUNT", "RANKING_METHOD_CODE",
        "LOCAL_FX_METHOD_CODE", "AGGREGATE_FX_METHOD_CODE", "CANONICAL_STATUS", "PRODUCTION_STATUS", "METHODOLOGY_STATUS", "VERSION"
    ),
    "scope_reference_overrides": (
        "SCOPE_CODE", "CATEGORY_SUFFIX", "FIELD_CODE", "OVERRIDE_VALUE", "STATUS", "NOTES", "VERSION"
    ),
    "analytics_reference_requirements": (
        "METRIC_CODE", "METRIC_NAME_FR", "FUND_SERIES_REQUIRED", "PEER_GROUP_REQUIRED", "CATEGORY_WTI_REQUIRED",
        "PRIMARY_BENCHMARK_REQUIRED", "SECONDARY_BENCHMARK_REQUIRED", "RISK_FREE_RATE_REQUIRED", "MAR_REQUIRED",
        "COMPARISON_FAMILY", "METHODOLOGY_CODE", "STATUS", "NOTES"
    ),
}

KEY_FIELDS = {
    "asset_classes": ("ASSET_CLASS_CODE",),
    "asset_subclasses": ("ASSET_CLASS_CODE", "ASSET_SUBCLASS_CODE"),
    "fund_scope_routing": ("LEGAL_COUNTRY_ISO3",),
    "category_templates": ("CATEGORY_TEMPLATE_CODE",),
    "scope_reference_overrides": ("SCOPE_CODE", "CATEGORY_SUFFIX", "FIELD_CODE"),
    "analytics_reference_requirements": ("METRIC_CODE",),
}


def sql_literal(value: str | None) -> str:
    if value is None or value == "":
        return "NULL"
    return "'" + value.replace("'", "''") + "'"


def sql_bool(value: str) -> str:
    if value == "True":
        return "true"
    if value == "False":
        return "false"
    raise ValueError(f"invalid boolean value: {value}")


def sql_int(value: str) -> str:
    try:
        return str(int(value))
    except ValueError as exc:
        raise ValueError(f"invalid integer value: {value}") from exc


def _load_csv(path: Path, expected_header: tuple[str, ...], keys: tuple[str, ...]) -> list[dict[str, str]]:
    raw = path.read_text(encoding="utf-8")
    if "\r" in raw:
        raise ValueError(f"CR characters are forbidden: {path}")
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=";")
        if tuple(reader.fieldnames or ()) != expected_header:
            raise ValueError(f"unexpected header: {path.name}")
        rows = list(reader)
    seen: set[tuple[str, ...]] = set()
    for row in rows:
        if None in row:
            raise ValueError(f"malformed row: {path.name}")
        key = tuple(row[field] for field in keys)
        if any(not part for part in key):
            raise ValueError(f"empty canonical key in {path.name}: {key}")
        if key in seen:
            raise ValueError(f"duplicate canonical key in {path.name}: {key}")
        seen.add(key)
    return rows


def load_sources(root: Path = DEFAULT_SOURCE_DIR) -> dict[str, Any]:
    loaded: dict[str, Any] = {}
    for key, filename in FILES.items():
        loaded[key] = _load_csv(root / filename, EXPECTED_HEADERS[key], KEY_FIELDS[key])
    manifest_path = root / MANIFEST
    manifest_raw = manifest_path.read_bytes()
    manifest = json.loads(manifest_raw.decode("utf-8"))
    if manifest.get("schema_version") != "0.1.0":
        raise ValueError("unexpected taxonomy schema version")
    if manifest.get("canonical_status") != "STRUCTURE_PREFILLED":
        raise ValueError("unexpected canonical taxonomy status")
    if manifest.get("production_status") != "NOT_ACTIVE":
        raise ValueError("unexpected taxonomy production status")
    loaded["manifest"] = manifest
    loaded["manifest_sha256"] = hashlib.sha256(manifest_raw).hexdigest()
    return loaded


def _upsert(table: str, columns: list[str], values: list[str], conflict: list[str]) -> str:
    assignments = [f"{column}=excluded.{column}" for column in columns if column not in conflict]
    return (
        f"insert into {table} ({','.join(columns)}) values ({','.join(values)}) "
        f"on conflict ({','.join(conflict)}) do update set {','.join(assignments)};"
    )


def build_sql(sources: dict[str, Any]) -> str:
    manifest = sources["manifest"]
    lines = [
        "-- GENERATED FILE: DO NOT EDIT.",
        "-- Authoring inputs: data/canonical/*_V0_1.csv + MATRIX_MANIFEST_V0_1.json",
        "-- PostgreSQL is runtime source of truth after governed application.",
        "-- This migration preserves STRUCTURE_PREFILLED / NOT_ACTIVE status.",
        "",
        "create schema if not exists taxonomy;",
        "",
        "create table if not exists taxonomy.asset_class (",
        "  asset_class_code text primary key,",
        "  name_fr text not null,",
        "  requires_subclass boolean not null,",
        "  subclass_dimension text,",
        "  is_active boolean not null,",
        "  version text not null",
        ");",
        "",
        "create table if not exists taxonomy.asset_subclass (",
        "  asset_class_code text not null references taxonomy.asset_class(asset_class_code),",
        "  asset_subclass_code text not null,",
        "  name_fr text not null,",
        "  subclass_dimension text not null,",
        "  sort_order integer not null,",
        "  is_active boolean not null,",
        "  version text not null,",
        "  primary key (asset_class_code, asset_subclass_code)",
        ");",
        "",
        "create table if not exists taxonomy.fund_scope_routing (",
        "  legal_country_iso3 text primary key,",
        "  legal_country_code text not null unique,",
        "  legal_country_name_fr text not null,",
        "  local_scope_type text not null,",
        "  local_scope_code text not null,",
        "  local_exchange_code text,",
        "  local_currency_code text not null,",
        "  regional_scope_code text not null,",
        "  continent_scope_code text not null,",
        "  routing_basis_code text not null,",
        "  status text not null,",
        "  version text not null",
        ");",
        "",
        "create table if not exists taxonomy.category_template (",
        "  category_template_code text primary key,",
        "  asset_class_code text not null references taxonomy.asset_class(asset_class_code),",
        "  asset_subclass_code text,",
        "  category_name_fr text not null,",
        "  category_suffix text not null,",
        "  category_code_template text not null,",
        "  reference_block_code_template text not null,",
        "  peer_group_code_template text not null,",
        "  category_wti_code_template text not null,",
        "  category_wti_method_code text not null,",
        "  category_mean_method_code text not null,",
        "  category_median_method_code text not null,",
        "  primary_benchmark_code_template text not null,",
        "  secondary_benchmark_code_template text not null,",
        "  wti_bench_code_template text not null,",
        "  wti_bench_method_code text not null,",
        "  risk_free_rate_code_template text not null,",
        "  risk_free_selection_method_code text not null,",
        "  minimum_acceptable_return_code_template text not null,",
        "  mar_method_code text not null,",
        "  display_series_1_code_template text not null,",
        "  display_series_2_code_template text not null,",
        "  display_series_3_code_template text not null,",
        "  display_series_4_optional_code_template text,",
        "  default_reference_count integer not null,",
        "  max_reference_count integer not null,",
        "  ranking_method_code text not null,",
        "  local_fx_method_code text not null,",
        "  aggregate_fx_method_code text not null,",
        "  canonical_status text not null,",
        "  production_status text not null,",
        "  methodology_status text not null,",
        "  version text not null",
        ");",
        "",
        "create table if not exists taxonomy.scope_reference_override (",
        "  scope_code text not null,",
        "  category_suffix text not null,",
        "  field_code text not null,",
        "  override_value text,",
        "  status text not null,",
        "  notes text,",
        "  version text not null,",
        "  primary key (scope_code, category_suffix, field_code)",
        ");",
        "",
        "create table if not exists taxonomy.analytics_reference_requirement (",
        "  metric_code text primary key,",
        "  metric_name_fr text not null,",
        "  fund_series_required boolean not null,",
        "  peer_group_required boolean not null,",
        "  category_wti_required boolean not null,",
        "  primary_benchmark_required boolean not null,",
        "  secondary_benchmark_required boolean not null,",
        "  risk_free_rate_required boolean not null,",
        "  mar_required boolean not null,",
        "  comparison_family text not null,",
        "  methodology_code text not null,",
        "  status text not null,",
        "  notes text",
        ");",
        "",
        "create table if not exists taxonomy.taxonomy_release (",
        "  schema_version text primary key,",
        "  canonical_status text not null,",
        "  production_status text not null,",
        "  source_manifest_sha256 char(64) not null,",
        "  source_manifest_path text not null",
        ");",
        "",
    ]

    for row in sources["asset_classes"]:
        lines.append(_upsert(
            "taxonomy.asset_class",
            ["asset_class_code", "name_fr", "requires_subclass", "subclass_dimension", "is_active", "version"],
            [sql_literal(row["ASSET_CLASS_CODE"]), sql_literal(row["NAME_FR"]), sql_bool(row["REQUIRES_SUBCLASS"]),
             sql_literal(row["SUBCLASS_DIMENSION"]), sql_bool(row["IS_ACTIVE"]), sql_literal(row["VERSION"])],
            ["asset_class_code"],
        ))

    lines.append("")
    for row in sources["asset_subclasses"]:
        lines.append(_upsert(
            "taxonomy.asset_subclass",
            ["asset_class_code", "asset_subclass_code", "name_fr", "subclass_dimension", "sort_order", "is_active", "version"],
            [sql_literal(row["ASSET_CLASS_CODE"]), sql_literal(row["ASSET_SUBCLASS_CODE"]), sql_literal(row["NAME_FR"]),
             sql_literal(row["SUBCLASS_DIMENSION"]), sql_int(row["SORT_ORDER"]), sql_bool(row["IS_ACTIVE"]), sql_literal(row["VERSION"])],
            ["asset_class_code", "asset_subclass_code"],
        ))

    lines.append("")
    routing_columns = [
        "legal_country_iso3", "legal_country_code", "legal_country_name_fr", "local_scope_type", "local_scope_code",
        "local_exchange_code", "local_currency_code", "regional_scope_code", "continent_scope_code", "routing_basis_code", "status", "version"
    ]
    routing_source = [
        "LEGAL_COUNTRY_ISO3", "LEGAL_COUNTRY_CODE", "LEGAL_COUNTRY_NAME_FR", "LOCAL_SCOPE_TYPE", "LOCAL_SCOPE_CODE",
        "LOCAL_EXCHANGE_CODE", "LOCAL_CURRENCY_CODE", "REGIONAL_SCOPE_CODE", "CONTINENT_SCOPE_CODE", "ROUTING_BASIS_CODE", "STATUS", "VERSION"
    ]
    for row in sources["fund_scope_routing"]:
        lines.append(_upsert(
            "taxonomy.fund_scope_routing", routing_columns,
            [sql_literal(row[field]) for field in routing_source], ["legal_country_iso3"]
        ))

    lines.append("")
    template_columns = [field.lower() for field in EXPECTED_HEADERS["category_templates"]]
    int_fields = {"DEFAULT_REFERENCE_COUNT", "MAX_REFERENCE_COUNT"}
    for row in sources["category_templates"]:
        values = [sql_int(row[field]) if field in int_fields else sql_literal(row[field]) for field in EXPECTED_HEADERS["category_templates"]]
        lines.append(_upsert("taxonomy.category_template", template_columns, values, ["category_template_code"]))

    lines.append("")
    override_columns = ["scope_code", "category_suffix", "field_code", "override_value", "status", "notes", "version"]
    for row in sources["scope_reference_overrides"]:
        lines.append(_upsert(
            "taxonomy.scope_reference_override", override_columns,
            [sql_literal(row[field]) for field in EXPECTED_HEADERS["scope_reference_overrides"]],
            ["scope_code", "category_suffix", "field_code"],
        ))

    lines.append("")
    analytics_columns = [field.lower() for field in EXPECTED_HEADERS["analytics_reference_requirements"]]
    analytics_bool_fields = {
        "FUND_SERIES_REQUIRED", "PEER_GROUP_REQUIRED", "CATEGORY_WTI_REQUIRED", "PRIMARY_BENCHMARK_REQUIRED",
        "SECONDARY_BENCHMARK_REQUIRED", "RISK_FREE_RATE_REQUIRED", "MAR_REQUIRED"
    }
    for row in sources["analytics_reference_requirements"]:
        values = [sql_bool(row[field]) if field in analytics_bool_fields else sql_literal(row[field])
                  for field in EXPECTED_HEADERS["analytics_reference_requirements"]]
        lines.append(_upsert("taxonomy.analytics_reference_requirement", analytics_columns, values, ["metric_code"]))

    lines += [
        "",
        _upsert(
            "taxonomy.taxonomy_release",
            ["schema_version", "canonical_status", "production_status", "source_manifest_sha256", "source_manifest_path"],
            [sql_literal(manifest["schema_version"]), sql_literal(manifest["canonical_status"]),
             sql_literal(manifest["production_status"]), sql_literal(sources["manifest_sha256"]),
             sql_literal("data/canonical/MATRIX_MANIFEST_V0_1.json")],
            ["schema_version"],
        ),
        "",
    ]
    return "\n".join(lines)


def check_output(path: Path, expected: str) -> None:
    if not path.is_file():
        raise ValueError(f"generated migration is missing: {path}")
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise ValueError("committed SQL does not match deterministic generation")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    expected = build_sql(load_sources(args.source_dir))
    if args.check:
        check_output(args.output, expected)
        print(f"OK: deterministic taxonomy migration matches {args.output}")
        return 0
    if args.output.exists():
        raise SystemExit(f"refusing to overwrite existing migration: {args.output}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(expected, encoding="utf-8", newline="\n")
    print(f"CREATED: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
