"""Strict mirror-first tooling for the D00-D17 country indicator catalogue.

The legacy Markdown files are accepted only as frozen bootstrap/fidelity inputs.
Absent semantics remain null with explicit status. Once materialized, the JSON
package under data/indicator_catalog/v1 is the governed authoring authority.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

LEGACY_FILES = (
    "docs/04_DATA_GOVERNANCE/indicator_catalog/D00_gouvernance_et_traçabilite.md",
    "docs/04_DATA_GOVERNANCE/indicator_catalog/Indicators_D01_D03_Identity_Demography_Economy.md",
    "docs/04_DATA_GOVERNANCE/indicator_catalog/Indicators_D04_D06_Prices_Fiscal_Debt.md",
    "docs/04_DATA_GOVERNANCE/indicator_catalog/Indicators_D07_D09_Monetary_Banking_External.md",
    "docs/04_DATA_GOVERNANCE/indicator_catalog/Indicators_D10_D11_Government_Securities_Equities.md",
    "docs/04_DATA_GOVERNANCE/indicator_catalog/Indicators_D12_D14_Funds_Institutionals_Real_Estate.md",
    "docs/04_DATA_GOVERNANCE/indicator_catalog/Indicators_D15_D17_Sectors_Risk_Analytics.md",
)

EXPECTED_DOMAIN_COUNTS = {
    "D00": 15,
    "D01": 20,
    "D02": 16,
    "D03": 24,
    "D04": 14,
    "D05": 26,
    "D06": 24,
    "D07": 23,
    "D08": 28,
    "D09": 29,
    "D10": 45,
    "D11": 24,
    "D12": 48,
    "D13": 12,
    "D14": 9,
    "D15": 16,
    "D16": 17,
    "D17": 30,
}

AUTHORING_FILES = ("00_metadata.json",) + tuple(
    f"{domain}.json" for domain in EXPECTED_DOMAIN_COUNTS
)
DOMAIN_HEADING_RE = re.compile(r"^#{1,6}\s+(D\d{2})\s+[—-]\s+(.+?)\s*$")
INDICATOR_CODE_RE = re.compile(r"^D\d{2}\.[A-Z0-9_]+$")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False) + "\n"


def _split_markdown_row(line: str) -> list[str]:
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        raise ValueError(f"not a Markdown table row: {line!r}")
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def _is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def _nullable_text(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _authored_status(value: Any) -> str:
    return "SOURCE_AUTHORED" if value is not None else "NOT_AUTHORED"


def _parse_yes_no(value: str | None) -> bool | None:
    normalized = _nullable_text(value)
    if normalized is None:
        return None
    lowered = normalized.casefold()
    if lowered in {"oui", "yes", "true"}:
        return True
    if lowered in {"non", "no", "false"}:
        return False
    raise ValueError(f"unsupported mandatory value: {value!r}")


def _build_item(
    row: dict[str, str],
    *,
    domain_code: str,
    source_file: str,
    source_sha256: str,
) -> dict[str, Any]:
    code = _nullable_text(row.get("Code"))
    if code is None or not INDICATOR_CODE_RE.fullmatch(code):
        raise ValueError(f"invalid indicator code in {source_file}: {code!r}")
    if not code.startswith(domain_code + "."):
        raise ValueError(f"indicator {code} does not belong to {domain_code}")

    label_fr = _nullable_text(row.get("Indicator"))
    if label_fr is None:
        raise ValueError(f"{code}: source label is required")

    definition_fr = _nullable_text(row.get("Definition"))
    source_nature = _nullable_text(row.get("Nature"))
    benchmark = _nullable_text(row.get("Benchmark / index"))
    mandatory = _parse_yes_no(row.get("Mandatory"))

    return {
        "indicator_code": code,
        "domain_code": domain_code,
        "label_fr": label_fr,
        "label_fr_status": "SOURCE_AUTHORED",
        "label_en": None,
        "label_en_status": "NOT_AUTHORED",
        "definition_fr": definition_fr,
        "definition_fr_status": _authored_status(definition_fr),
        "definition_en": None,
        "definition_en_status": "NOT_AUTHORED",
        "source_nature": source_nature,
        "source_nature_status": _authored_status(source_nature),
        "canonical_nature": None,
        "canonical_nature_status": "NOT_AUTHORED",
        "frequency_source": _nullable_text(row.get("Frequency")),
        "unit_source": _nullable_text(row.get("Unit")),
        "currency_rule": None,
        "currency_rule_status": "NOT_AUTHORED",
        "granularity": None,
        "granularity_status": "NOT_AUTHORED",
        "preferred_source_text": _nullable_text(row.get("Preferred source")),
        "utility": _nullable_text(row.get("Utility")),
        "benchmark_or_index": benchmark,
        "priority": _nullable_text(row.get("Priority")),
        "target_history": _nullable_text(row.get("History")),
        "mandatory": mandatory,
        "mandatory_status": _authored_status(mandatory),
        "calculation_method_id": None,
        "calculation_method_status": "NOT_AUTHORED",
        "definition_status": _authored_status(definition_fr),
        "source_mapping_status": "NOT_ASSERTED_BY_DEFINITION_CATALOGUE",
        "collection_spec_status": "NOT_ASSERTED_BY_DEFINITION_CATALOGUE",
        "collection_test_status": "NOT_ASSERTED_BY_DEFINITION_CATALOGUE",
        "history_status": "NOT_ASSERTED_BY_DEFINITION_CATALOGUE",
        "calculation_status": "NOT_ASSERTED_BY_DEFINITION_CATALOGUE",
        "source_file": source_file,
        "source_sha256": source_sha256,
        "source_row_key": code,
        "schema_version": "1.0.0-bootstrap",
    }


def _parse_file(root: Path, relative_path: str) -> tuple[list[dict[str, Any]], dict[str, str]]:
    path = root / relative_path
    if not path.is_file():
        raise ValueError(f"legacy catalogue source missing: {relative_path}")
    payload = path.read_bytes()
    text = payload.decode("utf-8")
    digest = sha256_bytes(payload)

    current_domain: str | None = None
    domain_names: dict[str, str] = {}
    current_headers: list[str] | None = None
    items: list[dict[str, Any]] = []

    for line in text.splitlines():
        heading = DOMAIN_HEADING_RE.match(line.strip())
        if heading:
            current_domain = heading.group(1)
            domain_names[current_domain] = heading.group(2).strip()
            current_headers = None
            continue

        stripped = line.strip()
        if not stripped.startswith("|"):
            if stripped == "":
                current_headers = None
            continue

        cells = _split_markdown_row(stripped)
        if _is_separator_row(cells):
            continue
        if cells and cells[0] == "Code":
            current_headers = cells
            continue
        if not cells or not INDICATOR_CODE_RE.fullmatch(cells[0]):
            continue
        if current_domain is None or current_headers is None:
            raise ValueError(f"indicator row found outside governed table in {relative_path}: {cells[0]}")
        if len(cells) != len(current_headers):
            raise ValueError(
                f"{cells[0]}: expected {len(current_headers)} cells, got {len(cells)}"
            )
        row = dict(zip(current_headers, cells))
        items.append(
            _build_item(
                row,
                domain_code=current_domain,
                source_file=relative_path,
                source_sha256=digest,
            )
        )

    return items, domain_names


def validate_catalog(catalog: dict[str, Any]) -> None:
    indicators = catalog.get("indicators")
    domains = catalog.get("domains")
    if not isinstance(indicators, list) or not isinstance(domains, list):
        raise ValueError("catalog must contain domain and indicator lists")

    counts = Counter(item["domain_code"] for item in indicators)
    actual_counts = dict(sorted(counts.items()))
    if actual_counts != EXPECTED_DOMAIN_COUNTS:
        raise ValueError(
            f"domain count drift: actual={actual_counts} expected={EXPECTED_DOMAIN_COUNTS}"
        )
    if len(indicators) != 420:
        raise ValueError(f"expected 420 indicators, got {len(indicators)}")
    if len(domains) != 18:
        raise ValueError(f"expected 18 domains, got {len(domains)}")

    codes = [item["indicator_code"] for item in indicators]
    duplicates = sorted(code for code, count in Counter(codes).items() if count > 1)
    if duplicates:
        raise ValueError(f"duplicate indicator codes: {duplicates}")

    for item in indicators:
        code = item["indicator_code"]
        if not INDICATOR_CODE_RE.fullmatch(code):
            raise ValueError(f"invalid canonical code: {code}")
        if item["history_status"] != "NOT_ASSERTED_BY_DEFINITION_CATALOGUE":
            raise ValueError(f"{code}: definition catalogue cannot assert loaded history")
        if not re.fullmatch(r"[0-9a-f]{64}", item["source_sha256"]):
            raise ValueError(f"{code}: invalid source hash")
        if item["source_row_key"] != code:
            raise ValueError(f"{code}: source row key drift")


def parse_legacy_catalog(root: Path) -> dict[str, Any]:
    all_items: list[dict[str, Any]] = []
    names: dict[str, str] = {}
    source_hashes: dict[str, str] = {}

    for relative_path in LEGACY_FILES:
        items, file_names = _parse_file(root, relative_path)
        all_items.extend(items)
        names.update(file_names)
        source_hashes[relative_path] = sha256_bytes((root / relative_path).read_bytes())

    domains = [
        {
            "domain_code": code,
            "name_fr": names.get(code),
            "expected_indicator_count": EXPECTED_DOMAIN_COUNTS[code],
        }
        for code in sorted(EXPECTED_DOMAIN_COUNTS)
    ]
    catalog = {
        "catalog_id": "AFRICAFUNDS_COUNTRY_INDICATOR_CATALOG",
        "catalog_version": "1.0.0-bootstrap",
        "status": "BOOTSTRAP_MIRROR_ONLY",
        "authoring_authority": "LEGACY_MARKDOWN_FOR_BOOTSTRAP_ONLY",
        "policy": {
            "strategy": "MIRROR_FIRST",
            "missing_value": "NULL_WITH_EXPLICIT_STATUS",
            "loaded_history_claims": "FORBIDDEN_FROM_DEFINITION_CATALOGUE",
            "canonical_nature": "SEPARATE_GOVERNED_CLASSIFICATION",
        },
        "legacy_sources": [
            {"path": path, "sha256": source_hashes[path]} for path in LEGACY_FILES
        ],
        "domains": domains,
        "indicators": sorted(all_items, key=lambda item: item["indicator_code"]),
    }
    validate_catalog(catalog)
    return catalog


def build_authoring_package_files(root: Path) -> dict[str, str]:
    """Render the initial governed JSON package exactly from the pinned legacy mirror."""
    legacy = parse_legacy_catalog(root)
    metadata = {
        "catalog_id": legacy["catalog_id"],
        "catalog_version": "1.0.0",
        "status": "AUTHORING_MIRROR_INITIALIZED",
        "authoring_authority": "MACHINE_READABLE_JSON_PACKAGE",
        "authoritative_path": "data/indicator_catalog/v1/",
        "policy": legacy["policy"],
        "legacy_sources": legacy["legacy_sources"],
        "domain_files": [f"{code}.json" for code in EXPECTED_DOMAIN_COUNTS],
        "domain_count": 18,
        "indicator_count": 420,
    }
    files = {"00_metadata.json": canonical_json(metadata)}
    by_domain = {code: [] for code in EXPECTED_DOMAIN_COUNTS}
    for item in legacy["indicators"]:
        by_domain[item["domain_code"]].append(item)
    domain_by_code = {item["domain_code"]: item for item in legacy["domains"]}
    for code in EXPECTED_DOMAIN_COUNTS:
        files[f"{code}.json"] = canonical_json(
            {
                "domain": domain_by_code[code],
                "indicators": by_domain[code],
            }
        )
    return files


def load_authoring_package(path: Path) -> dict[str, Any]:
    actual_files = {item.name for item in path.glob("*.json")}
    expected_files = set(AUTHORING_FILES)
    if actual_files != expected_files:
        raise ValueError(
            f"authoring package file drift: actual={sorted(actual_files)} expected={sorted(expected_files)}"
        )
    metadata = json.loads((path / "00_metadata.json").read_text(encoding="utf-8"))
    if metadata.get("authoring_authority") != "MACHINE_READABLE_JSON_PACKAGE":
        raise ValueError("authoring authority must be MACHINE_READABLE_JSON_PACKAGE")
    if metadata.get("policy", {}).get("strategy") != "MIRROR_FIRST":
        raise ValueError("authoring package must preserve MIRROR_FIRST policy")

    domains: list[dict[str, Any]] = []
    indicators: list[dict[str, Any]] = []
    for code in EXPECTED_DOMAIN_COUNTS:
        payload = json.loads((path / f"{code}.json").read_text(encoding="utf-8"))
        domain = payload.get("domain")
        rows = payload.get("indicators")
        if not isinstance(domain, dict) or not isinstance(rows, list):
            raise ValueError(f"{code}.json must contain domain and indicators")
        if domain.get("domain_code") != code:
            raise ValueError(f"{code}.json domain code drift")
        domains.append(domain)
        indicators.extend(rows)

    catalog = {
        **metadata,
        "domains": domains,
        "indicators": sorted(indicators, key=lambda item: item["indicator_code"]),
    }
    validate_catalog(catalog)
    if metadata.get("domain_count") != len(domains) or metadata.get("indicator_count") != len(indicators):
        raise ValueError("metadata counts do not match package contents")
    return catalog
