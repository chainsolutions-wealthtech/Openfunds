#!/usr/bin/env python3
"""Validate the reviewed Openfunds v2.13.0 -> canonical mapping registry.

The registry contains reviewed mappings only. Completeness is computed against the
checksum-locked official Openfunds inventory and the governed canonical dictionary;
unreviewed external fields are never materialized as synthetic rows.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Iterable

from scripts.canonical_field_dictionary import expand, load_package
from scripts.parse_openfunds_v2_13_0 import (
    extract_layout_text,
    parse_records_from_layout_text,
    verify_source_sha256,
)

STANDARD_VERSION = "2.13.0"
SOURCE_SHA256 = "40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4"
EXPECTED_HEADER = [
    "MAPPING_ID",
    "STANDARD_VERSION",
    "EXTERNAL_FIELD_ID",
    "CANONICAL_FIELD_ID",
    "CANONICAL_ENTITY",
    "MAPPING_STATUS",
    "TRANSFORMATION_RULE",
    "INFORMATION_LOSS",
    "IMPORT_SUPPORTED",
    "EXPORT_SUPPORTED",
    "VALIDATION_STATUS",
    "SOURCE_SHA256",
    "SOURCE_REFERENCE",
    "NOTES",
]
ALLOWED_MAPPING_STATUSES = {"DIRECT", "TRANSFORMED", "ONE_TO_MANY", "MANY_TO_ONE", "TO_CONFIRM"}
ALLOWED_VALIDATION_STATUSES = {"PROPOSED", "VALIDATED"}
ALLOWED_YES_NO = {"YES", "NO"}
ALLOWED_INFORMATION_LOSS = {"NONE", "PARTIAL", "YES", "UNKNOWN"}
MAPPING_ID_RE = re.compile(r"^MAP-\d{6}$")


def validate_rows(
    rows: Iterable[dict[str, str]],
    official_ids: set[str],
    canonical_ids: set[str],
) -> list[str]:
    """Return all validation errors without mutating the supplied rows."""

    materialized = list(rows)
    errors: list[str] = []
    counts = Counter(row.get("MAPPING_ID", "") for row in materialized)

    for mapping_id, count in counts.items():
        if mapping_id and count > 1:
            errors.append(f"duplicate MAPPING_ID: {mapping_id}")

    for index, row in enumerate(materialized, start=2):
        prefix = f"row {index}"
        missing = [name for name in EXPECTED_HEADER if name not in row]
        if missing:
            errors.append(f"{prefix}: missing columns {missing}")
            continue

        mapping_id = row["MAPPING_ID"].strip()
        external_id = row["EXTERNAL_FIELD_ID"].strip()
        canonical_id = row["CANONICAL_FIELD_ID"].strip()
        standard_version = row["STANDARD_VERSION"].strip()
        mapping_status = row["MAPPING_STATUS"].strip()
        validation_status = row["VALIDATION_STATUS"].strip()
        source_sha256 = row["SOURCE_SHA256"].strip().lower()
        source_reference = row["SOURCE_REFERENCE"].strip()

        if not MAPPING_ID_RE.fullmatch(mapping_id):
            errors.append(f"{prefix}: invalid MAPPING_ID: {mapping_id!r}")
        if standard_version != STANDARD_VERSION:
            errors.append(f"{prefix}: unexpected STANDARD_VERSION: {standard_version!r}")
        if external_id not in official_ids:
            errors.append(f"{prefix}: unknown external OF-ID: {external_id}")
        if canonical_id not in canonical_ids:
            errors.append(f"{prefix}: unknown canonical FIELD_ID: {canonical_id}")
        if mapping_status not in ALLOWED_MAPPING_STATUSES:
            errors.append(f"{prefix}: invalid MAPPING_STATUS: {mapping_status!r}")
        if validation_status not in ALLOWED_VALIDATION_STATUSES:
            errors.append(f"{prefix}: invalid VALIDATION_STATUS: {validation_status!r}")
        if row["IMPORT_SUPPORTED"].strip() not in ALLOWED_YES_NO:
            errors.append(f"{prefix}: IMPORT_SUPPORTED must be YES or NO")
        if row["EXPORT_SUPPORTED"].strip() not in ALLOWED_YES_NO:
            errors.append(f"{prefix}: EXPORT_SUPPORTED must be YES or NO")
        if row["INFORMATION_LOSS"].strip() not in ALLOWED_INFORMATION_LOSS:
            errors.append(f"{prefix}: invalid INFORMATION_LOSS: {row['INFORMATION_LOSS']!r}")
        if source_sha256 != SOURCE_SHA256:
            errors.append(f"{prefix}: unexpected SOURCE_SHA256: {source_sha256!r}")
        if source_reference != f"official:v2.13.0:{external_id}":
            errors.append(f"{prefix}: SOURCE_REFERENCE must identify the exact external OF-ID")
        if external_id.endswith("XX") and "PARAMETERIZED_COUNTRY_TEMPLATE_PRESERVED" not in row["TRANSFORMATION_RULE"]:
            errors.append(f"{prefix}: parameterized XX OF-ID must remain unexpanded")
        if not row["CANONICAL_ENTITY"].strip():
            errors.append(f"{prefix}: CANONICAL_ENTITY is required")
        if not row["TRANSFORMATION_RULE"].strip():
            errors.append(f"{prefix}: TRANSFORMATION_RULE is required")

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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))

    if manifest.get("standard_version") != STANDARD_VERSION:
        raise ValueError("mapping manifest standard_version mismatch")
    if manifest.get("source_sha256") != SOURCE_SHA256:
        raise ValueError("mapping manifest source_sha256 mismatch")

    source_sha256 = verify_source_sha256(args.pdf, args.sha256_file)
    official_records = parse_records_from_layout_text(extract_layout_text(args.pdf))
    official_ids = {str(record["of_id"]) for record in official_records}
    if len(official_ids) != manifest.get("official_field_count"):
        raise ValueError(
            f"official field count mismatch: parsed={len(official_ids)} manifest={manifest.get('official_field_count')}"
        )

    canonical_spec = load_package(args.canonical_package)
    canonical_fields = expand(canonical_spec)
    canonical_ids = {str(field["FIELD_ID"]) for field in canonical_fields}
    if len(canonical_ids) != manifest.get("canonical_field_count"):
        raise ValueError(
            f"canonical field count mismatch: expanded={len(canonical_ids)} manifest={manifest.get('canonical_field_count')}"
        )

    rows = read_registry(args.registry)
    errors = validate_rows(rows, official_ids, canonical_ids)
    if errors:
        raise ValueError("mapping registry validation failed:\n" + "\n".join(errors))

    mapped_external_ids = {row["EXTERNAL_FIELD_ID"] for row in rows}
    mapped_canonical_ids = {row["CANONICAL_FIELD_ID"] for row in rows}
    summary = {
        "standard_version": STANDARD_VERSION,
        "source_sha256": source_sha256,
        "official_field_count": len(official_ids),
        "canonical_field_count": len(canonical_ids),
        "reviewed_mapping_rows": len(rows),
        "mapped_external_ids": len(mapped_external_ids),
        "unmapped_external_ids": len(official_ids - mapped_external_ids),
        "mapped_canonical_ids": len(mapped_canonical_ids),
    }
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
