#!/usr/bin/env python3
"""Checksum-gated structural parser for the official Openfunds v2.13.0 Field List.

The official source PDF remains immutable. This parser extracts a structural inventory
at runtime and emits a summary only by default; it does not rewrite or replace the
official Openfunds document.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path
from typing import Iterable

STANDARD_VERSION = "2.13.0"
EXPECTED_SOURCE_SHA256 = "40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4"

FIELD_ID_PATTERN = r"OF[A-Z]{2}(?:\d{6}|\d{4}XX)"
FIELD_ID_RE = re.compile(rf"^{FIELD_ID_PATTERN}$")
CONCRETE_FIELD_ID_RE = re.compile(r"^OF[A-Z]{2}\d{6}$")
PARAMETERIZED_COUNTRY_ID_RE = re.compile(r"^OF[A-Z]{2}\d{4}XX$")
HEADER_RE = re.compile(
    rf"^\s*OF-ID\s+({FIELD_ID_PATTERN})\s+Field Name\s+(.+?)\s*$"
)
ANY_FIELD_HEADER_RE = re.compile(r"^\s*OF-ID\s+(\S+)\s+Field Name\s+(.+?)\s*$")
FIELD_TAGS_RE = re.compile(r"^\s*Field Tags\b")
KNOWN_SECTION_RE = re.compile(
    r"^\s*(Field Tags|Field Level|Data Type|Description|Values|Example|Introduced / Revoked)\b"
)


def _collapse_whitespace(parts: Iterable[str]) -> str:
    return " ".join(" ".join(parts).split())


def parse_records_from_layout_text(text: str) -> list[dict[str, object]]:
    """Parse structural field records from ``pdftotext -layout`` output.

    The parser intentionally preserves parameterized country-template IDs ending in
    ``XX``. It fails closed on malformed lines that look like actual field-record
    headers and on duplicate OF-IDs.
    """

    lines = text.splitlines()
    headers: list[tuple[int, re.Match[str]]] = []

    for index, line in enumerate(lines):
        valid = HEADER_RE.match(line)
        if valid:
            headers.append((index, valid))
            continue

        broad = ANY_FIELD_HEADER_RE.match(line)
        if broad:
            raise ValueError(
                f"malformed Openfunds field header at line {index + 1}: {line.strip()}"
            )

    records: list[dict[str, object]] = []
    seen: set[str] = set()

    for position, (start, match) in enumerate(headers):
        end = headers[position + 1][0] if position + 1 < len(headers) else len(lines)
        of_id = match.group(1)
        if of_id in seen:
            raise ValueError(f"duplicate Openfunds OF-ID: {of_id}")
        seen.add(of_id)

        field_name_parts = [match.group(2).strip()]
        cursor = start + 1
        while cursor < end:
            line = lines[cursor]
            if FIELD_TAGS_RE.match(line):
                break
            if KNOWN_SECTION_RE.match(line):
                break
            stripped = line.strip()
            if stripped:
                # Wrapped field names are the only non-section content expected
                # between the record header and Field Tags. Page furniture may be
                # encountered in the source; only take compact continuation text.
                field_name_parts.append(stripped)
            cursor += 1

        record = {
            "of_id": of_id,
            "field_name": _collapse_whitespace(field_name_parts),
            "is_parameterized_country_template": bool(
                PARAMETERIZED_COUNTRY_ID_RE.fullmatch(of_id)
            ),
        }
        records.append(record)

    return records


def verify_source_sha256(pdf_path: Path, sha256_file: Path) -> str:
    """Verify the archived PDF against both its sidecar and the governed checksum."""

    sidecar_tokens = sha256_file.read_text(encoding="utf-8").strip().split()
    if not sidecar_tokens:
        raise ValueError("empty SHA256 sidecar")
    sidecar_digest = sidecar_tokens[0].lower()
    if not re.fullmatch(r"[0-9a-f]{64}", sidecar_digest):
        raise ValueError(f"invalid SHA256 sidecar digest: {sidecar_digest!r}")

    actual = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
    if actual != sidecar_digest:
        raise ValueError(
            f"Openfunds archive checksum mismatch: sidecar={sidecar_digest} actual={actual}"
        )
    if actual != EXPECTED_SOURCE_SHA256:
        raise ValueError(
            f"unexpected governed Openfunds v2.13.0 checksum: {actual}"
        )
    return actual


def extract_layout_text(pdf_path: Path) -> str:
    """Extract PDF text using Poppler's deterministic layout mode."""

    pdftotext = shutil.which("pdftotext")
    if not pdftotext:
        raise RuntimeError("pdftotext is required; install poppler-utils")

    with tempfile.TemporaryDirectory(prefix="openfunds-v2-13-0-") as directory:
        output = Path(directory) / "fieldlist.txt"
        completed = subprocess.run(
            [pdftotext, "-layout", str(pdf_path), str(output)],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                "pdftotext failed: " + (completed.stderr.strip() or "unknown error")
            )
        return output.read_text(encoding="utf-8", errors="strict")


def build_summary(records: list[dict[str, object]], source_sha256: str) -> dict[str, object]:
    if not records:
        raise ValueError("no Openfunds field records parsed")

    ids = [str(record["of_id"]) for record in records]
    unique = set(ids)
    if len(unique) != len(ids):
        raise ValueError("duplicate Openfunds OF-ID in parsed inventory")

    concrete = sum(bool(CONCRETE_FIELD_ID_RE.fullmatch(of_id)) for of_id in ids)
    templates = sum(bool(PARAMETERIZED_COUNTRY_ID_RE.fullmatch(of_id)) for of_id in ids)
    if concrete + templates != len(ids):
        raise ValueError("parsed inventory contains an unsupported OF-ID grammar")

    prefix_counts = dict(sorted(Counter(of_id[:4] for of_id in ids).items()))
    return {
        "standard": "Openfunds",
        "standard_version": STANDARD_VERSION,
        "source_sha256": source_sha256,
        "field_id_grammar": r"OF[A-Z]{2}(?:\d{6}|\d{4}XX)",
        "field_records": len(ids),
        "concrete_ids": concrete,
        "parameterized_country_templates": templates,
        "unique_ids": len(unique),
        "first_id": ids[0],
        "last_id": ids[-1],
        "prefix_counts": prefix_counts,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify and structurally inventory the checksum-locked Openfunds v2.13.0 Field List"
    )
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--sha256-file", type=Path, required=True)
    parser.add_argument("--summary-json", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_sha256 = verify_source_sha256(args.pdf, args.sha256_file)
    text = extract_layout_text(args.pdf)
    records = parse_records_from_layout_text(text)
    summary = build_summary(records, source_sha256)
    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
