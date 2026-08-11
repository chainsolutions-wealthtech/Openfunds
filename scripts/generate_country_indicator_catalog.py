#!/usr/bin/env python3
"""Bootstrap, classify and verify the governed D00-D17 authoring package."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from country_indicator_catalog import (
    apply_governed_classification,
    build_authoring_package_files,
    load_authoring_package,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUTHORING = ROOT / "data/indicator_catalog/v1"


def write_bootstrap_authoring_package(target: Path) -> None:
    files = build_authoring_package_files(ROOT)
    target.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        (target / name).write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authoring-dir", type=Path, default=DEFAULT_AUTHORING)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--bootstrap-authoring", action="store_true")
    mode.add_argument("--apply-governed-classification", action="store_true")
    mode.add_argument("--check-authoring", action="store_true")
    args = parser.parse_args()

    try:
        if args.bootstrap_authoring:
            write_bootstrap_authoring_package(args.authoring_dir)
        elif args.apply_governed_classification:
            apply_governed_classification(args.authoring_dir)
        package = load_authoring_package(args.authoring_dir)
        print(
            "OK: country indicator authoring package "
            f"domains={len(package['domains'])} indicators={len(package['indicators'])} "
            f"authority={package['authoring_authority']} status={package['status']}"
        )
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
