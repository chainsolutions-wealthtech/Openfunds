"""Strict mirror-first tooling for the D00-D17 country indicator catalogue.

The legacy Markdown files are frozen bootstrap/fidelity inputs. Absent source
semantics remain null with explicit status. The JSON package under
``data/indicator_catalog/v1`` is the governed authoring authority and may add
separate, provenance-bearing governance semantics without rewriting source
assertions.
"""
from __future__ import annotations

import csv
import hashlib
import io
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
    "D00": 15, "D01": 20, "D02": 16, "D03": 24, "D04": 14, "D05": 26,
    "D06": 24, "D07": 23, "D08": 28, "D09": 29, "D10": 45, "D11": 24,
    "D12": 48, "D13": 12, "D14": 9, "D15": 16, "D16": 17, "D17": 30,
}

AUTHORING_FILES = ("00_metadata.json",) + tuple(f"{d}.json" for d in EXPECTED_DOMAIN_COUNTS)
DOMAIN_HEADING_RE = re.compile(r"^#{1,6}\s+(D\d{2})\s+[—-]\s+(.+?)\s*$")
INDICATOR_CODE_RE = re.compile(r"^D\d{2}\.[A-Z0-9_]+$")
ALLOWED_CANONICAL_NATURES = ("RAW", "METADATA", "EVENT", "CALCULATED")
CLASSIFICATION_DECISION_ID = "OF-DATA-003-A"
CLASSIFICATION_POLICY_VERSION = "1.0.0"
NULL_EXPORT_TOKEN = "<NULL>"

EXPLICIT_EVENT_CODES = frozenset({
    "D07.MPC_MEETING_DATE", "D07.MPC_DECISION", "D12.FUND_EVENT",
    "D16.DEFAULT_EVENT", "D16.ELECTION", "D16.GOVERNMENT_CHANGE", "D16.IMF_REVIEW",
})

EXPLICIT_METADATA_CODES = frozenset({
    "D10.SECURITY_ISIN", "D10.SECURITY_LOCAL_CODE", "D10.SECURITY_TYPE",
    "D10.SECURITY_CURRENCY", "D10.SECURITY_ISSUER", "D10.ISSUE_DATE",
    "D10.SETTLEMENT_DATE", "D10.MATURITY_DATE", "D10.ORIGINAL_TENOR",
    "D10.NOMINAL", "D10.COUPON_RATE", "D10.COUPON_TYPE", "D10.COUPON_FREQUENCY",
    "D10.DAY_COUNT", "D10.CURVE_METHOD",
    "D11.EXCHANGE", "D11.TICKER", "D11.EQUITY_ISIN", "D11.COMPANY", "D11.SECTOR",
    "D12.FUND_CANONICAL_ID", "D12.PUBLISHED_NAME", "D12.CANONICAL_NAME",
    "D12.FUND_ALIAS", "D12.LEGAL_FORM", "D12.FUND_STATUS", "D12.APPROVAL_DATE",
    "D12.LAUNCH_DATE", "D12.CLOSURE_DATE", "D12.MANAGEMENT_COMPANY", "D12.DEPOSITARY",
    "D12.ADMINISTRATOR", "D12.AUDITOR", "D12.DISTRIBUTOR", "D12.LOCAL_CATEGORY",
    "D12.ASSET_CLASS", "D12.GEOGRAPHY", "D12.FUND_CURRENCY", "D12.SHARE_CLASS_ID",
    "D12.SHARE_CLASS_ISIN", "D12.DISTRIBUTION_POLICY", "D12.DECLARED_BENCHMARK",
    "D12.INVESTMENT_OBJECTIVE", "D12.ALLOCATION_LIMITS", "D12.PROSPECTUS",
    "D12.FACTSHEET", "D12.FINANCIAL_STATEMENTS",
    "D16.RATING_AGENCY", "D16.FOREIGN_INVESTOR_RULES", "D16.FUND_REGULATION",
})

CSV_COLUMNS = (
    "indicator_code", "domain_code", "label_fr", "label_en", "definition_fr", "definition_en",
    "source_nature", "canonical_nature", "canonical_nature_status", "frequency_source",
    "unit_source", "currency_rule", "granularity", "preferred_source_text", "utility",
    "benchmark_or_index", "priority", "target_history", "mandatory", "definition_status",
    "source_mapping_status", "collection_spec_status", "collection_test_status", "history_status",
    "calculation_status", "source_file", "source_sha256", "source_row_key",
    "classification_decision_id", "classification_rule", "schema_version",
)

SQL_DATA_COLUMNS = (
    "indicator_code", "domain_code", "label_fr", "label_en", "definition_fr", "definition_en",
    "source_nature", "canonical_nature", "canonical_nature_status", "frequency_source",
    "unit_source", "currency_rule", "granularity", "preferred_source_text", "utility",
    "benchmark_or_index", "priority", "target_history", "mandatory", "definition_status",
    "source_mapping_status", "collection_spec_status", "collection_test_status", "history_status",
    "calculation_status", "source_file", "source_sha256", "source_row_key",
    "classification_decision_id", "classification_rule", "schema_version", "catalog_version",
)


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


def _build_item(row: dict[str, str], *, domain_code: str, source_file: str, source_sha256: str) -> dict[str, Any]:
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
    mandatory = _parse_yes_no(row.get("Mandatory"))
    return {
        "indicator_code": code, "domain_code": domain_code,
        "label_fr": label_fr, "label_fr_status": "SOURCE_AUTHORED",
        "label_en": None, "label_en_status": "NOT_AUTHORED",
        "definition_fr": definition_fr, "definition_fr_status": _authored_status(definition_fr),
        "definition_en": None, "definition_en_status": "NOT_AUTHORED",
        "source_nature": source_nature, "source_nature_status": _authored_status(source_nature),
        "canonical_nature": None, "canonical_nature_status": "NOT_AUTHORED",
        "frequency_source": _nullable_text(row.get("Frequency")),
        "unit_source": _nullable_text(row.get("Unit")),
        "currency_rule": None, "currency_rule_status": "NOT_AUTHORED",
        "granularity": None, "granularity_status": "NOT_AUTHORED",
        "preferred_source_text": _nullable_text(row.get("Preferred source")),
        "utility": _nullable_text(row.get("Utility")),
        "benchmark_or_index": _nullable_text(row.get("Benchmark / index")),
        "priority": _nullable_text(row.get("Priority")),
        "target_history": _nullable_text(row.get("History")),
        "mandatory": mandatory, "mandatory_status": _authored_status(mandatory),
        "calculation_method_id": None, "calculation_method_status": "NOT_AUTHORED",
        "definition_status": _authored_status(definition_fr),
        "source_mapping_status": "NOT_ASSERTED_BY_DEFINITION_CATALOGUE",
        "collection_spec_status": "NOT_ASSERTED_BY_DEFINITION_CATALOGUE",
        "collection_test_status": "NOT_ASSERTED_BY_DEFINITION_CATALOGUE",
        "history_status": "NOT_ASSERTED_BY_DEFINITION_CATALOGUE",
        "calculation_status": "NOT_ASSERTED_BY_DEFINITION_CATALOGUE",
        "source_file": source_file, "source_sha256": source_sha256, "source_row_key": code,
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
            if stripped == "": current_headers = None
            continue
        cells = _split_markdown_row(stripped)
        if _is_separator_row(cells): continue
        if cells and cells[0] == "Code":
            current_headers = cells
            continue
        if not cells or not INDICATOR_CODE_RE.fullmatch(cells[0]): continue
        if current_domain is None or current_headers is None:
            raise ValueError(f"indicator row found outside governed table in {relative_path}: {cells[0]}")
        if len(cells) != len(current_headers):
            raise ValueError(f"{cells[0]}: expected {len(current_headers)} cells, got {len(cells)}")
        items.append(_build_item(dict(zip(current_headers, cells)), domain_code=current_domain,
                                 source_file=relative_path, source_sha256=digest))
    return items, domain_names


def validate_catalog(catalog: dict[str, Any]) -> None:
    indicators, domains = catalog.get("indicators"), catalog.get("domains")
    if not isinstance(indicators, list) or not isinstance(domains, list):
        raise ValueError("catalog must contain domain and indicator lists")
    actual_counts = dict(sorted(Counter(i["domain_code"] for i in indicators).items()))
    if actual_counts != EXPECTED_DOMAIN_COUNTS:
        raise ValueError(f"domain count drift: actual={actual_counts} expected={EXPECTED_DOMAIN_COUNTS}")
    if len(indicators) != 420 or len(domains) != 18:
        raise ValueError(f"expected 18 domains / 420 indicators, got {len(domains)} / {len(indicators)}")
    codes = [i["indicator_code"] for i in indicators]
    duplicates = sorted(c for c, n in Counter(codes).items() if n > 1)
    if duplicates: raise ValueError(f"duplicate indicator codes: {duplicates}")
    for item in indicators:
        code = item["indicator_code"]
        if not INDICATOR_CODE_RE.fullmatch(code): raise ValueError(f"invalid canonical code: {code}")
        if item["history_status"] != "NOT_ASSERTED_BY_DEFINITION_CATALOGUE":
            raise ValueError(f"{code}: definition catalogue cannot assert loaded history")
        if not re.fullmatch(r"[0-9a-f]{64}", item["source_sha256"]): raise ValueError(f"{code}: invalid source hash")
        if item["source_row_key"] != code: raise ValueError(f"{code}: source row key drift")


def parse_legacy_catalog(root: Path) -> dict[str, Any]:
    all_items: list[dict[str, Any]] = []
    names: dict[str, str] = {}
    source_hashes: dict[str, str] = {}
    for relative_path in LEGACY_FILES:
        items, file_names = _parse_file(root, relative_path)
        all_items.extend(items); names.update(file_names)
        source_hashes[relative_path] = sha256_bytes((root / relative_path).read_bytes())
    domains = [{"domain_code": c, "name_fr": names.get(c), "expected_indicator_count": EXPECTED_DOMAIN_COUNTS[c]}
               for c in sorted(EXPECTED_DOMAIN_COUNTS)]
    catalog = {
        "catalog_id": "AFRICAFUNDS_COUNTRY_INDICATOR_CATALOG", "catalog_version": "1.0.0-bootstrap",
        "status": "BOOTSTRAP_MIRROR_ONLY", "authoring_authority": "LEGACY_MARKDOWN_FOR_BOOTSTRAP_ONLY",
        "policy": {"strategy": "MIRROR_FIRST", "missing_value": "NULL_WITH_EXPLICIT_STATUS",
                   "loaded_history_claims": "FORBIDDEN_FROM_DEFINITION_CATALOGUE",
                   "canonical_nature": "SEPARATE_GOVERNED_CLASSIFICATION"},
        "legacy_sources": [{"path": p, "sha256": source_hashes[p]} for p in LEGACY_FILES],
        "domains": domains, "indicators": sorted(all_items, key=lambda i: i["indicator_code"]),
    }
    validate_catalog(catalog); return catalog


def build_authoring_package_files(root: Path) -> dict[str, str]:
    legacy = parse_legacy_catalog(root)
    metadata = {
        "catalog_id": legacy["catalog_id"], "catalog_version": "1.0.0",
        "status": "AUTHORING_MIRROR_INITIALIZED", "authoring_authority": "MACHINE_READABLE_JSON_PACKAGE",
        "authoritative_path": "data/indicator_catalog/v1/", "policy": legacy["policy"],
        "legacy_sources": legacy["legacy_sources"], "domain_files": [f"{c}.json" for c in EXPECTED_DOMAIN_COUNTS],
        "domain_count": 18, "indicator_count": 420,
    }
    files = {"00_metadata.json": canonical_json(metadata)}
    by_domain = {c: [] for c in EXPECTED_DOMAIN_COUNTS}
    for item in legacy["indicators"]: by_domain[item["domain_code"]].append(item)
    domain_by_code = {d["domain_code"]: d for d in legacy["domains"]}
    for code in EXPECTED_DOMAIN_COUNTS:
        files[f"{code}.json"] = canonical_json({"domain": domain_by_code[code], "indicators": by_domain[code]})
    return files


def load_authoring_package(path: Path) -> dict[str, Any]:
    actual_files = {p.name for p in path.glob("*.json")}
    if actual_files != set(AUTHORING_FILES):
        raise ValueError(f"authoring package file drift: actual={sorted(actual_files)} expected={sorted(AUTHORING_FILES)}")
    metadata = json.loads((path / "00_metadata.json").read_text(encoding="utf-8"))
    if metadata.get("authoring_authority") != "MACHINE_READABLE_JSON_PACKAGE": raise ValueError("invalid authoring authority")
    if metadata.get("policy", {}).get("strategy") != "MIRROR_FIRST": raise ValueError("authoring package must preserve MIRROR_FIRST")
    domains, indicators = [], []
    for code in EXPECTED_DOMAIN_COUNTS:
        payload = json.loads((path / f"{code}.json").read_text(encoding="utf-8"))
        domain, rows = payload.get("domain"), payload.get("indicators")
        if not isinstance(domain, dict) or not isinstance(rows, list): raise ValueError(f"{code}.json invalid")
        if domain.get("domain_code") != code: raise ValueError(f"{code}.json domain code drift")
        domains.append(domain); indicators.extend(rows)
    catalog = {**metadata, "domains": domains, "indicators": sorted(indicators, key=lambda i: i["indicator_code"])}
    validate_catalog(catalog)
    if metadata.get("domain_count") != len(domains) or metadata.get("indicator_count") != len(indicators):
        raise ValueError("metadata counts do not match package contents")
    return catalog


def classify_canonical_nature(indicator_code: str) -> tuple[str, str]:
    domain = indicator_code.split(".", 1)[0]
    if domain in {"D00", "D01"}: return "METADATA", "DOMAIN_METADATA"
    if indicator_code in EXPLICIT_METADATA_CODES: return "METADATA", "EXPLICIT_METADATA_CODE"
    if indicator_code in EXPLICIT_EVENT_CODES: return "EVENT", "EXPLICIT_EVENT_CODE"
    if domain == "D17": return "CALCULATED", "DOMAIN_CALCULATED"
    return "RAW", "DEFAULT_OBSERVED_RAW"


def _classified_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    result = dict(metadata)
    result["status"] = "AUTHORING_GOVERNED_CLASSIFIED"
    result["classification_policy"] = {
        "decision_id": CLASSIFICATION_DECISION_ID, "policy_version": CLASSIFICATION_POLICY_VERSION,
        "allowed_values": list(ALLOWED_CANONICAL_NATURES), "source_semantics": "SEPARATE_FROM_SOURCE_NATURE",
        "rule_precedence": ["DOMAIN_METADATA", "EXPLICIT_METADATA_CODE", "EXPLICIT_EVENT_CODE",
                            "DOMAIN_CALCULATED", "DEFAULT_OBSERVED_RAW"],
        "statement": "Governance classification only; it does not replace source_nature or assert provider authorship.",
    }
    return result


def apply_governed_classification(path: Path) -> dict[str, Any]:
    package = load_authoring_package(path)
    available = {i["indicator_code"] for i in package["indicators"]}
    unknown = sorted((EXPLICIT_EVENT_CODES | EXPLICIT_METADATA_CODES) - available)
    if unknown: raise ValueError(f"classification policy references unknown codes: {unknown}")
    metadata = _classified_metadata({k: v for k, v in package.items() if k not in {"domains", "indicators"}})
    (path / "00_metadata.json").write_text(canonical_json(metadata), encoding="utf-8")
    by_domain = {c: [] for c in EXPECTED_DOMAIN_COUNTS}
    for source_item in package["indicators"]:
        item = dict(source_item); nature, rule = classify_canonical_nature(item["indicator_code"])
        item["canonical_nature"] = nature; item["canonical_nature_status"] = "GOVERNED_CLASSIFICATION"
        item["canonical_nature_provenance"] = {"decision_id": CLASSIFICATION_DECISION_ID,
                                                "policy_version": CLASSIFICATION_POLICY_VERSION, "rule": rule}
        item["schema_version"] = "1.0.0"; by_domain[item["domain_code"]].append(item)
    domain_by_code = {d["domain_code"]: d for d in package["domains"]}
    for code in EXPECTED_DOMAIN_COUNTS:
        (path / f"{code}.json").write_text(canonical_json({"domain": domain_by_code[code],
            "indicators": sorted(by_domain[code], key=lambda i: i["indicator_code"])}), encoding="utf-8")
    classified = load_authoring_package(path)
    for item in classified["indicators"]:
        if item.get("canonical_nature") not in ALLOWED_CANONICAL_NATURES: raise ValueError(f"{item['indicator_code']}: nature missing")
        if item.get("canonical_nature_status") != "GOVERNED_CLASSIFICATION": raise ValueError(f"{item['indicator_code']}: status drift")
    return classified


def _export_value(value: Any) -> str:
    if value is None: return NULL_EXPORT_TOKEN
    if value is True: return "TRUE"
    if value is False: return "FALSE"
    return str(value).replace("\r\n", " ").replace("\n", " ")


def _classification_fields(item: dict[str, Any]) -> tuple[str, str]:
    provenance = item.get("canonical_nature_provenance") or {}
    return str(provenance.get("decision_id") or ""), str(provenance.get("rule") or "")


def _render_expanded_json(catalog: dict[str, Any]) -> str:
    payload = {k: v for k, v in catalog.items() if k not in {"domains", "indicators"}}
    payload["domains"] = catalog["domains"]
    payload["indicators"] = catalog["indicators"]
    return canonical_json(payload)


def _render_csv(catalog: dict[str, Any]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, delimiter=";", lineterminator="\n")
    writer.writerow(CSV_COLUMNS)
    for item in catalog["indicators"]:
        decision_id, rule = _classification_fields(item)
        row = dict(item); row["classification_decision_id"] = decision_id; row["classification_rule"] = rule
        writer.writerow([_export_value(row.get(column)) for column in CSV_COLUMNS])
    return stream.getvalue()


def _md(value: Any) -> str:
    return _export_value(value).replace("|", "\\|")


def _render_markdown(catalog: dict[str, Any]) -> str:
    lines = [
        "# Country Indicator Catalogue — v1", "",
        "Authoring authority: `data/indicator_catalog/v1/`.",
        "Policy: `MIRROR_FIRST`; absent source semantics remain `<NULL>` / `NOT_AUTHORED`.",
        "`target_history` is a coverage requirement, never evidence that history is loaded.",
        "All `history_status` values remain `NOT_ASSERTED_BY_DEFINITION_CATALOGUE` in this catalogue.", "",
    ]
    by_domain = {c: [] for c in EXPECTED_DOMAIN_COUNTS}
    for item in catalog["indicators"]: by_domain[item["domain_code"]].append(item)
    domain_by_code = {d["domain_code"]: d for d in catalog["domains"]}
    for code in EXPECTED_DOMAIN_COUNTS:
        domain = domain_by_code[code]
        lines.extend([
            f"## {code} — {domain['name_fr']}", "",
            "| Code | Libellé source | Nature source | Nature canonique | Fréquence | Unité | Source préférée | Priorité | Historique cible | Statut définition | Statut historique |",
            "|---|---|---|---|---|---|---|---|---|---|---|",
        ])
        for item in by_domain[code]:
            lines.append("| " + " | ".join(_md(v) for v in (
                item["indicator_code"], item["label_fr"], item.get("source_nature"), item["canonical_nature"],
                item.get("frequency_source"), item.get("unit_source"), item.get("preferred_source_text"),
                item.get("priority"), item.get("target_history"), item["definition_status"], item["history_status"],
            )) + " |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _sql_literal(value: Any) -> str:
    if value is None: return "NULL"
    if value is True: return "TRUE"
    if value is False: return "FALSE"
    return "'" + str(value).replace("'", "''") + "'"


def _sql_row(item: dict[str, Any], catalog_version: str) -> str:
    decision_id, rule = _classification_fields(item)
    row = dict(item); row["classification_decision_id"] = decision_id; row["classification_rule"] = rule
    row["catalog_version"] = catalog_version
    return "(" + ", ".join(_sql_literal(row.get(c)) for c in SQL_DATA_COLUMNS) + ")"


def _render_sql(catalog: dict[str, Any]) -> str:
    catalog_version = str(catalog["catalog_version"])
    domain_values = ",\n  ".join(
        "(" + ", ".join((_sql_literal(d["domain_code"]), _sql_literal(d["name_fr"]),
                           str(d["expected_indicator_count"]), _sql_literal(catalog_version))) + ")"
        for d in catalog["domains"]
    )
    indicator_values = ",\n  ".join(_sql_row(i, catalog_version) for i in catalog["indicators"])
    compare_cols = [c for c in SQL_DATA_COLUMNS if c != "indicator_code"]
    lhs = ", ".join(f"a.{c}" for c in compare_cols)
    rhs = ", ".join(f"e.{c}" for c in compare_cols)
    cols = ", ".join(SQL_DATA_COLUMNS)
    return f"""-- GENERATED FILE. DO NOT HAND-EDIT.
-- Source: data/indicator_catalog/v1/ (OF-DATA-003 Option A)
-- Scope: catalogue definitions only; no country observations, histories or provider-series data.

CREATE SCHEMA IF NOT EXISTS ref;

CREATE TABLE IF NOT EXISTS ref.indicator_domain (
  domain_code text PRIMARY KEY CHECK (domain_code ~ '^D[0-9]{{2}}$'),
  name_fr text NOT NULL,
  expected_indicator_count integer NOT NULL CHECK (expected_indicator_count > 0),
  catalog_version text NOT NULL
);

CREATE TABLE IF NOT EXISTS ref.indicator_definition (
  indicator_code text PRIMARY KEY CHECK (indicator_code ~ '^D[0-9]{{2}}\\.[A-Z0-9_]+$'),
  domain_code text NOT NULL REFERENCES ref.indicator_domain(domain_code),
  label_fr text NOT NULL,
  label_en text,
  definition_fr text,
  definition_en text,
  source_nature text,
  canonical_nature text NOT NULL CHECK (canonical_nature IN ('RAW','METADATA','EVENT','CALCULATED')),
  canonical_nature_status text NOT NULL,
  frequency_source text,
  unit_source text,
  currency_rule text,
  granularity text,
  preferred_source_text text,
  utility text,
  benchmark_or_index text,
  priority text,
  target_history text,
  mandatory boolean,
  definition_status text NOT NULL,
  source_mapping_status text NOT NULL,
  collection_spec_status text NOT NULL,
  collection_test_status text NOT NULL,
  history_status text NOT NULL,
  calculation_status text NOT NULL,
  source_file text NOT NULL,
  source_sha256 char(64) NOT NULL CHECK (source_sha256 ~ '^[0-9a-f]{{64}}$'),
  source_row_key text NOT NULL,
  classification_decision_id text NOT NULL,
  classification_rule text NOT NULL,
  schema_version text NOT NULL,
  catalog_version text NOT NULL
);

CREATE TEMP TABLE tmp_indicator_domain_v1 (
  domain_code text PRIMARY KEY,
  name_fr text NOT NULL,
  expected_indicator_count integer NOT NULL,
  catalog_version text NOT NULL
) ON COMMIT DROP;

INSERT INTO tmp_indicator_domain_v1 (domain_code, name_fr, expected_indicator_count, catalog_version) VALUES
  {domain_values};

INSERT INTO ref.indicator_domain (domain_code, name_fr, expected_indicator_count, catalog_version)
SELECT domain_code, name_fr, expected_indicator_count, catalog_version FROM tmp_indicator_domain_v1
ON CONFLICT (domain_code) DO NOTHING;

DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM tmp_indicator_domain_v1 e
    JOIN ref.indicator_domain a USING (domain_code)
    WHERE ROW(a.name_fr, a.expected_indicator_count, a.catalog_version)
      IS DISTINCT FROM ROW(e.name_fr, e.expected_indicator_count, e.catalog_version)
  ) THEN
    RAISE EXCEPTION 'OF-DATA-003 domain semantic collision';
  END IF;
END $$;

CREATE TEMP TABLE tmp_indicator_definition_v1 (LIKE ref.indicator_definition INCLUDING DEFAULTS) ON COMMIT DROP;

INSERT INTO tmp_indicator_definition_v1 ({cols}) VALUES
  {indicator_values};

INSERT INTO ref.indicator_definition ({cols})
SELECT {cols} FROM tmp_indicator_definition_v1
ON CONFLICT (indicator_code) DO NOTHING;

DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM tmp_indicator_definition_v1 e
    JOIN ref.indicator_definition a USING (indicator_code)
    WHERE ROW({lhs}) IS DISTINCT FROM ROW({rhs})
  ) THEN
    RAISE EXCEPTION 'OF-DATA-003 indicator semantic collision';
  END IF;
  IF (SELECT count(*) FROM tmp_indicator_definition_v1) <> 420 THEN
    RAISE EXCEPTION 'OF-DATA-003 expected 420 indicator definitions';
  END IF;
END $$;
"""


def build_derived_outputs(catalog: dict[str, Any]) -> dict[str, str]:
    validate_catalog(catalog)
    if catalog.get("classification_policy", {}).get("decision_id") != CLASSIFICATION_DECISION_ID:
        raise ValueError("governed classification policy must be applied before rendering")
    return {"json": _render_expanded_json(catalog), "csv": _render_csv(catalog),
            "markdown": _render_markdown(catalog), "sql": _render_sql(catalog)}


def build_output_manifest(catalog: dict[str, Any], outputs: dict[str, str]) -> dict[str, Any]:
    counts = Counter(i["canonical_nature"] for i in catalog["indicators"])
    paths = {
        "json": "build/indicator_catalog/COUNTRY_INDICATOR_CATALOG_V1.json",
        "csv": "build/indicator_catalog/COUNTRY_INDICATOR_CATALOG_V1.csv",
        "markdown": "build/indicator_catalog/COUNTRY_INDICATOR_CATALOG_V1.md",
        "sql": "build/indicator_catalog/COUNTRY_INDICATOR_CATALOG_V1.sql",
    }
    return {
        "catalog_id": catalog["catalog_id"], "catalog_version": catalog["catalog_version"],
        "authoring_authority": catalog["authoring_authority"],
        "classification_decision_id": CLASSIFICATION_DECISION_ID,
        "domain_count": len(catalog["domains"]), "indicator_count": len(catalog["indicators"]),
        "canonical_nature_counts": {k: counts.get(k, 0) for k in ALLOWED_CANONICAL_NATURES},
        "legacy_sources": catalog["legacy_sources"],
        "outputs": {k: {"path": paths[k], "sha256": sha256_bytes(v.encode("utf-8")),
                         "bytes": len(v.encode("utf-8"))} for k, v in outputs.items()},
        "frozen_sql_path": "schemas/reference/016_country_indicator_catalog.sql",
        "policy": {"generated": True, "hand_edit": "FORBIDDEN", "null_export_token": NULL_EXPORT_TOKEN},
    }
