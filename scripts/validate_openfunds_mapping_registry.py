#!/usr/bin/env python3
"""Validate reviewed Openfunds v2.13.0 mappings against governed canonical inventories."""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Iterable

try:
    from scripts.canonical_field_dictionary import expand, load_package
    from scripts.parse_openfunds_v2_13_0 import extract_layout_text, parse_records_from_layout_text, verify_source_sha256
except ModuleNotFoundError as exc:
    if exc.name != "scripts":
        raise
    from canonical_field_dictionary import expand, load_package
    from parse_openfunds_v2_13_0 import extract_layout_text, parse_records_from_layout_text, verify_source_sha256

STANDARD_VERSION = "2.13.0"
SOURCE_SHA256 = "40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4"
EXPECTED_HEADER = [
    "MAPPING_ID", "STANDARD_VERSION", "EXTERNAL_FIELD_ID", "CANONICAL_FIELD_ID",
    "CANONICAL_ENTITY", "MAPPING_STATUS", "TRANSFORMATION_RULE", "INFORMATION_LOSS",
    "IMPORT_SUPPORTED", "EXPORT_SUPPORTED", "VALIDATION_STATUS", "SOURCE_SHA256",
    "SOURCE_REFERENCE", "NOTES",
]
ALLOWED_MAPPING_STATUSES = {"DIRECT", "TRANSFORMED", "ONE_TO_MANY", "MANY_TO_ONE", "TO_CONFIRM"}
ALLOWED_VALIDATION_STATUSES = {"PROPOSED", "VALIDATED"}
ALLOWED_YES_NO = {"YES", "NO"}
ALLOWED_INFORMATION_LOSS = {"NONE", "PARTIAL", "YES", "UNKNOWN"}
MAPPING_ID_RE = re.compile(r"^MAP-\d{6}$")


def load_canonical_inventory(core_package: Path, extension_packages: Iterable[Path] = ()):
    """Union the immutable 143-field core with additive canonical extensions."""
    core_fields = expand(load_package(core_package))
    ids: set[str] = set()
    entities: dict[str, str] = {}
    for field in core_fields:
        field_id = str(field["FIELD_ID"])
        if field_id in ids:
            raise ValueError(f"duplicate canonical FIELD_ID in core: {field_id}")
        ids.add(field_id)
        entities[field_id] = str(field["ENTITY_CODE"])

    extension_count = 0
    for package in extension_packages:
        metadata = json.loads((package / "00_metadata.json").read_text(encoding="utf-8"))
        payload = json.loads((package / "10_fields.json").read_text(encoding="utf-8"))
        fields = payload.get("fields")
        if not isinstance(fields, list):
            raise ValueError(f"extension fields payload must be a list: {package}")
        if metadata.get("field_count") != len(fields):
            raise ValueError(
                f"extension field_count mismatch for {package}: declared={metadata.get('field_count')} actual={len(fields)}"
            )
        package_ids: set[str] = set()
        for field in fields:
            field_id = str(field.get("field_id", "")).strip()
            entity = str(field.get("entity_code", "")).strip()
            if not field_id or not entity:
                raise ValueError("extension field requires field_id and entity_code")
            if field_id in ids or field_id in package_ids:
                raise ValueError(f"duplicate canonical FIELD_ID: {field_id}")
            package_ids.add(field_id)
            ids.add(field_id)
            entities[field_id] = entity
        extension_count += len(fields)
    return ids, entities, {"core": len(core_fields), "extensions": extension_count, "total": len(ids)}


def validate_rows(rows: Iterable[dict[str, str]], official_ids: set[str], canonical_ids: set[str], canonical_entities: dict[str, str] | None = None) -> list[str]:
    materialized = list(rows)
    errors: list[str] = []
    mapping_id_counts = Counter(row.get("MAPPING_ID", "") for row in materialized)
    pair_counts = Counter((row.get("EXTERNAL_FIELD_ID", "").strip(), row.get("CANONICAL_FIELD_ID", "").strip()) for row in materialized)
    for mapping_id, count in mapping_id_counts.items():
        if mapping_id and count > 1:
            errors.append(f"duplicate MAPPING_ID: {mapping_id}")
    for (external_id, canonical_id), count in pair_counts.items():
        if external_id and canonical_id and count > 1:
            errors.append(f"duplicate external/canonical mapping pair: {external_id} -> {canonical_id}")

    for index, row in enumerate(materialized, start=2):
        prefix = f"row {index}"
        missing = [name for name in EXPECTED_HEADER if name not in row]
        if missing:
            errors.append(f"{prefix}: missing columns {missing}")
            continue
        mapping_id = row["MAPPING_ID"].strip()
        external_id = row["EXTERNAL_FIELD_ID"].strip()
        canonical_id = row["CANONICAL_FIELD_ID"].strip()
        canonical_entity = row["CANONICAL_ENTITY"].strip()
        if not MAPPING_ID_RE.fullmatch(mapping_id): errors.append(f"{prefix}: invalid MAPPING_ID: {mapping_id!r}")
        if row["STANDARD_VERSION"].strip() != STANDARD_VERSION: errors.append(f"{prefix}: unexpected STANDARD_VERSION")
        if external_id not in official_ids: errors.append(f"{prefix}: unknown external OF-ID: {external_id}")
        if canonical_id not in canonical_ids: errors.append(f"{prefix}: unknown canonical FIELD_ID: {canonical_id}")
        if canonical_entities is not None and canonical_id in canonical_entities and canonical_entity != canonical_entities[canonical_id]:
            errors.append(f"{prefix}: CANONICAL_ENTITY mismatch for {canonical_id}: declared={canonical_entity!r} expected={canonical_entities[canonical_id]!r}")
        if row["MAPPING_STATUS"].strip() not in ALLOWED_MAPPING_STATUSES: errors.append(f"{prefix}: invalid MAPPING_STATUS: {row['MAPPING_STATUS']!r}")
        if row["VALIDATION_STATUS"].strip() not in ALLOWED_VALIDATION_STATUSES: errors.append(f"{prefix}: invalid VALIDATION_STATUS: {row['VALIDATION_STATUS']!r}")
        if row["IMPORT_SUPPORTED"].strip() not in ALLOWED_YES_NO: errors.append(f"{prefix}: IMPORT_SUPPORTED must be YES or NO")
        if row["EXPORT_SUPPORTED"].strip() not in ALLOWED_YES_NO: errors.append(f"{prefix}: EXPORT_SUPPORTED must be YES or NO")
        if row["INFORMATION_LOSS"].strip() not in ALLOWED_INFORMATION_LOSS: errors.append(f"{prefix}: invalid INFORMATION_LOSS: {row['INFORMATION_LOSS']!r}")
        if row["SOURCE_SHA256"].strip().lower() != SOURCE_SHA256: errors.append(f"{prefix}: unexpected SOURCE_SHA256")
        if row["SOURCE_REFERENCE"].strip() != f"official:v2.13.0:{external_id}": errors.append(f"{prefix}: SOURCE_REFERENCE must identify the exact external OF-ID")
        if external_id.endswith("XX") and "PARAMETERIZED_COUNTRY_TEMPLATE_PRESERVED" not in row["TRANSFORMATION_RULE"]: errors.append(f"{prefix}: parameterized XX OF-ID must remain unexpanded")
        if not canonical_entity: errors.append(f"{prefix}: CANONICAL_ENTITY is required")
        if not row["TRANSFORMATION_RULE"].strip(): errors.append(f"{prefix}: TRANSFORMATION_RULE is required")
    return errors


def read_registry(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=";")
        if reader.fieldnames != EXPECTED_HEADER:
            raise ValueError(f"unexpected mapping registry header: {reader.fieldnames!r}")
        return list(reader)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the governed Openfunds mapping registry")
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--sha256-file", type=Path, required=True)
    parser.add_argument("--canonical-package", type=Path, required=True)
    parser.add_argument("--canonical-extension", type=Path, action="append", default=[])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if manifest.get("standard_version") != STANDARD_VERSION: raise ValueError("mapping manifest standard_version mismatch")
    if manifest.get("source_sha256") != SOURCE_SHA256: raise ValueError("mapping manifest source_sha256 mismatch")
    source_sha256 = verify_source_sha256(args.pdf, args.sha256_file)
    official_ids = {str(record["of_id"]) for record in parse_records_from_layout_text(extract_layout_text(args.pdf))}
    if len(official_ids) != manifest.get("official_field_count"): raise ValueError("official field count mismatch")

    canonical_ids, canonical_entities, counts = load_canonical_inventory(args.canonical_package, args.canonical_extension)
    expected_core = manifest.get("canonical_core_field_count", manifest.get("canonical_field_count"))
    expected_extensions = manifest.get("canonical_extension_field_count", 0)
    if counts["core"] != expected_core: raise ValueError(f"canonical core field count mismatch: expanded={counts['core']} manifest={expected_core}")
    if counts["extensions"] != expected_extensions: raise ValueError(f"canonical extension field count mismatch: expanded={counts['extensions']} manifest={expected_extensions}")
    if counts["total"] != manifest.get("canonical_field_count"): raise ValueError(f"canonical field count mismatch: expanded={counts['total']} manifest={manifest.get('canonical_field_count')}")

    rows = read_registry(args.registry)
    errors = validate_rows(rows, official_ids, canonical_ids, canonical_entities)
    if errors: raise ValueError("mapping registry validation failed:\n" + "\n".join(errors))
    mapped_external_ids = {row["EXTERNAL_FIELD_ID"] for row in rows}
    mapped_canonical_ids = {row["CANONICAL_FIELD_ID"] for row in rows}
    print(json.dumps({
        "standard_version": STANDARD_VERSION,
        "source_sha256": source_sha256,
        "official_field_count": len(official_ids),
        "canonical_core_field_count": counts["core"],
        "canonical_extension_field_count": counts["extensions"],
        "canonical_field_count": counts["total"],
        "reviewed_mapping_rows": len(rows),
        "mapped_external_ids": len(mapped_external_ids),
        "unmapped_external_ids": len(official_ids - mapped_external_ids),
        "mapped_canonical_ids": len(mapped_canonical_ids),
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
