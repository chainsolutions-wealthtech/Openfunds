#!/usr/bin/env python3
"""Bootstrap, classify, render and verify the governed D00-D17 catalogue."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from country_indicator_catalog import (
    apply_governed_classification,
    build_authoring_package_files,
    build_derived_outputs,
    build_output_manifest,
    canonical_json,
    load_authoring_package,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUTHORING = ROOT / "data/indicator_catalog/v1"
BUILD_DIR = ROOT / "build/indicator_catalog"
FROZEN_SQL = ROOT / "schemas/reference/016_country_indicator_catalog.sql"
MANIFEST = ROOT / "data/indicator_catalog/COUNTRY_INDICATOR_CATALOG_MANIFEST_V1.json"
OUTPUT_PATHS = {
    "json": BUILD_DIR / "COUNTRY_INDICATOR_CATALOG_V1.json",
    "csv": BUILD_DIR / "COUNTRY_INDICATOR_CATALOG_V1.csv",
    "markdown": BUILD_DIR / "COUNTRY_INDICATOR_CATALOG_V1.md",
    "sql": BUILD_DIR / "COUNTRY_INDICATOR_CATALOG_V1.sql",
}


def repo_path(path: Path) -> Path:
    """Resolve a CLI repository path without allowing it to escape the repository."""
    candidate = path if path.is_absolute() else ROOT / path
    resolved = candidate.resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"path escapes repository: {path}") from exc
    return resolved


def write_bootstrap_authoring_package(target: Path) -> None:
    files = build_authoring_package_files(ROOT)
    target.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        (target / name).write_text(content, encoding="utf-8")


def materialize_derived(authoring_dir: Path) -> dict[str, str]:
    package = load_authoring_package(authoring_dir)
    outputs = build_derived_outputs(package)
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    FROZEN_SQL.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    for key, content in outputs.items():
        OUTPUT_PATHS[key].write_text(content, encoding="utf-8")
    FROZEN_SQL.write_text(outputs["sql"], encoding="utf-8")
    MANIFEST.write_text(canonical_json(build_output_manifest(package, outputs)), encoding="utf-8")
    return outputs


def check_derived(authoring_dir: Path) -> None:
    package = load_authoring_package(authoring_dir)
    outputs = build_derived_outputs(package)
    expected_manifest = canonical_json(build_output_manifest(package, outputs))
    checks = {**OUTPUT_PATHS, "frozen_sql": FROZEN_SQL, "manifest": MANIFEST}
    for name, path in checks.items():
        if not path.is_file():
            raise ValueError(f"missing derived artifact: {path.relative_to(ROOT)}")
        if name in outputs:
            expected = outputs[name]
        elif name == "frozen_sql":
            expected = outputs["sql"]
        else:
            expected = expected_manifest
        actual = path.read_text(encoding="utf-8")
        if actual != expected:
            raise ValueError(f"derived artifact drift: {path.relative_to(ROOT)}")


def check_frozen_contract(source: Path, output: Path) -> None:
    """Verify migration 016 from committed authoring state without mutating the tree."""
    source_path = repo_path(source)
    output_path = repo_path(output)
    if source_path.name != "00_metadata.json":
        raise ValueError("--source must be the governed v1/00_metadata.json anchor")
    if not source_path.is_file():
        raise ValueError(f"missing governed source anchor: {source_path.relative_to(ROOT)}")
    if not output_path.is_file():
        raise ValueError(f"missing frozen migration: {output_path.relative_to(ROOT)}")

    authoring_dir = source_path.parent
    package = load_authoring_package(authoring_dir)
    outputs = build_derived_outputs(package)
    expected_sql = outputs["sql"]
    actual_sql = output_path.read_text(encoding="utf-8")
    if actual_sql != expected_sql:
        raise ValueError(
            f"frozen SQL drift: {output_path.relative_to(ROOT)} does not match governed authoring package"
        )

    if not MANIFEST.is_file():
        raise ValueError(f"missing checksum manifest: {MANIFEST.relative_to(ROOT)}")
    expected_manifest = canonical_json(build_output_manifest(package, outputs))
    actual_manifest = MANIFEST.read_text(encoding="utf-8")
    if actual_manifest != expected_manifest:
        raise ValueError("catalogue checksum manifest does not match governed authoring package")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authoring-dir", type=Path, default=DEFAULT_AUTHORING)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--output", type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--bootstrap-authoring", action="store_true")
    mode.add_argument("--apply-governed-classification", action="store_true")
    mode.add_argument("--check-authoring", action="store_true")
    mode.add_argument("--generate-derived", action="store_true")
    mode.add_argument("--check-derived", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()

    try:
        authoring_dir = repo_path(args.authoring_dir)
        if args.bootstrap_authoring:
            write_bootstrap_authoring_package(authoring_dir)
        elif args.apply_governed_classification:
            apply_governed_classification(authoring_dir)
        elif args.generate_derived:
            materialize_derived(authoring_dir)
        elif args.check_derived:
            check_derived(authoring_dir)
        elif args.check:
            if args.source is None or args.output is None:
                raise ValueError("--check requires both --source and --output")
            check_frozen_contract(args.source, args.output)

        package = load_authoring_package(authoring_dir if not args.check else repo_path(args.source).parent)
        print(
            "OK: country indicator catalogue "
            f"domains={len(package['domains'])} indicators={len(package['indicators'])} "
            f"authority={package['authoring_authority']} status={package['status']}"
        )
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
