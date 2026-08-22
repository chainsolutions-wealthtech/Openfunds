#!/usr/bin/env python3
"""Validate sparse Openfunds v2.13.0 review outcomes and merged coverage."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Iterable

try:
    from scripts.parse_openfunds_v2_13_0 import (
        extract_layout_text,
        parse_records_from_layout_text,
        verify_source_sha256,
    )
except ModuleNotFoundError as exc:
    if exc.name != "scripts":
        raise
    from parse_openfunds_v2_13_0 import (
        extract_layout_text,
        parse_records_from_layout_text,
        verify_source_sha256,
    )

STANDARD_VERSION = "2.13.0"
SOURCE_SHA256 = "40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4"
EXPECTED_HEADER = [
    "STANDARD_VERSION",
    "EXTERNAL_FIELD_ID",
    "OUTCOME",
    "REASON_CODE",
    "SOURCE_SHA256",
    "SOURCE_REFERENCE",
    "NOTES",
]
GLOBAL_OUTCOMES = {
    "MAPPED_CANONICAL",
    "MAPPED_DERIVED",
    "NO_CANONICAL_EQUIVALENT",
    "DEFERRED_NOT_REQUIRED_FOR_PRODUCT",
    "GATED_VENDOR_OR_LICENSE",
    "TO_CONFIRM",
}
SPARSE_OUTCOMES = {
    "NO_CANONICAL_EQUIVALENT",
    "DEFERRED_NOT_REQUIRED_FOR_PRODUCT",
    "GATED_VENDOR_OR_LICENSE",
    "TO_CONFIRM",
}


def read_mapping_external_ids(path: Path) -> set[str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=";")
        if not reader.fieldnames or "EXTERNAL_FIELD_ID" not in reader.fieldnames:
            raise ValueError("mapping registry must contain EXTERNAL_FIELD_ID")
        return {
            str(row.get("EXTERNAL_FIELD_ID", "")).strip()
            for row in reader
            if str(row.get("EXTERNAL_FIELD_ID", "")).strip()
        }


def read_outcomes(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=";")
        if reader.fieldnames != EXPECTED_HEADER:
            raise ValueError(f"unexpected review outcomes header: {reader.fieldnames!r}")
        return list(reader)


def validate_outcome_rows(
    rows: Iterable[dict[str, str]],
    official_ids: set[str],
    mapped_external_ids: set[str],
) -> list[str]:
    materialized = list(rows)
    errors: list[str] = []
    external_counts = Counter(
        str(row.get("EXTERNAL_FIELD_ID", "")).strip() for row in materialized
    )
    for external_id, count in external_counts.items():
        if external_id and count > 1:
            errors.append(f"duplicate EXTERNAL_FIELD_ID: {external_id}")

    for index, row in enumerate(materialized, start=2):
        prefix = f"row {index}"
        missing = [name for name in EXPECTED_HEADER if name not in row]
        if missing:
            errors.append(f"{prefix}: missing columns {missing}")
            continue

        version = row["STANDARD_VERSION"].strip()
        external_id = row["EXTERNAL_FIELD_ID"].strip()
        outcome = row["OUTCOME"].strip()
        reason_code = row["REASON_CODE"].strip()
        source_sha = row["SOURCE_SHA256"].strip().lower()
        source_reference = row["SOURCE_REFERENCE"].strip()

        if version != STANDARD_VERSION:
            errors.append(f"{prefix}: unexpected STANDARD_VERSION")
        if external_id not in official_ids:
            errors.append(f"{prefix}: unknown external OF-ID: {external_id}")
        if outcome not in GLOBAL_OUTCOMES:
            errors.append(f"{prefix}: invalid OUTCOME: {outcome!r}")
        elif outcome not in SPARSE_OUTCOMES:
            errors.append(
                f"{prefix}: {outcome} is derived from MAPPING_REGISTRY and must not be stored in the sparse review registry"
            )
        if external_id in mapped_external_ids:
            errors.append(
                f"{prefix}: external OF-ID is already mapped in MAPPING_REGISTRY: {external_id}"
            )
        if not reason_code:
            errors.append(f"{prefix}: REASON_CODE is required")
        if source_sha != SOURCE_SHA256:
            errors.append(f"{prefix}: unexpected SOURCE_SHA256")
        if source_reference != f"official:v2.13.0:{external_id}":
            errors.append(
                f"{prefix}: SOURCE_REFERENCE must identify the exact external OF-ID"
            )
    return errors


def compute_merged_coverage(
    official_ids: set[str],
    mapped_external_ids: set[str],
    outcome_rows: Iterable[dict[str, str]],
) -> dict[str, int]:
    materialized = list(outcome_rows)
    outcome_by_id = {
        str(row["EXTERNAL_FIELD_ID"]).strip(): str(row["OUTCOME"]).strip()
        for row in materialized
    }
    reviewed_nonmapped = {
        external_id
        for external_id, outcome in outcome_by_id.items()
        if outcome in {"NO_CANONICAL_EQUIVALENT", "DEFERRED_NOT_REQUIRED_FOR_PRODUCT"}
    }
    vendor_gated = {
        external_id
        for external_id, outcome in outcome_by_id.items()
        if outcome == "GATED_VENDOR_OR_LICENSE"
    }
    to_confirm = {
        external_id
        for external_id, outcome in outcome_by_id.items()
        if outcome == "TO_CONFIRM"
    }
    reviewed_union = mapped_external_ids | reviewed_nonmapped | vendor_gated | to_confirm
    unreviewed = official_ids - reviewed_union
    return {
        "total_official_ids": len(official_ids),
        "mapped_external_ids": len(mapped_external_ids),
        "reviewed_nonmapped_external_ids": len(reviewed_nonmapped),
        "vendor_gated_external_ids": len(vendor_gated),
        "to_confirm_external_ids": len(to_confirm),
        "unreviewed_external_ids": len(unreviewed),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Openfunds review outcomes")
    parser.add_argument("--outcomes", type=Path, required=True)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--sha256-file", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if manifest.get("standard_version") != STANDARD_VERSION:
        raise ValueError("mapping manifest standard_version mismatch")
    if manifest.get("source_sha256") != SOURCE_SHA256:
        raise ValueError("mapping manifest source_sha256 mismatch")

    source_sha256 = verify_source_sha256(args.pdf, args.sha256_file)
    official_ids = {
        str(record["of_id"])
        for record in parse_records_from_layout_text(extract_layout_text(args.pdf))
    }
    if len(official_ids) != manifest.get("official_field_count"):
        raise ValueError("official field count mismatch")

    mapped_external_ids = read_mapping_external_ids(args.registry)
    if not mapped_external_ids <= official_ids:
        unknown = sorted(mapped_external_ids - official_ids)
        raise ValueError(f"mapping registry contains unknown OF-IDs: {unknown}")

    outcome_rows = read_outcomes(args.outcomes)
    errors = validate_outcome_rows(outcome_rows, official_ids, mapped_external_ids)
    if errors:
        raise ValueError("review outcomes validation failed:\n" + "\n".join(errors))

    coverage = compute_merged_coverage(official_ids, mapped_external_ids, outcome_rows)
    partition_total = sum(
        coverage[key]
        for key in (
            "mapped_external_ids",
            "reviewed_nonmapped_external_ids",
            "vendor_gated_external_ids",
            "to_confirm_external_ids",
            "unreviewed_external_ids",
        )
    )
    if partition_total != len(official_ids):
        raise ValueError(
            f"review coverage does not partition official inventory: partition={partition_total} official={len(official_ids)}"
        )

    print(json.dumps({
        "standard_version": STANDARD_VERSION,
        "source_sha256": source_sha256,
        **coverage,
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
