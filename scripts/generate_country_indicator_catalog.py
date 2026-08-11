#!/usr/bin/env python3
"""Bootstrap the governed D00-D17 machine-readable authoring package."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from country_indicator_catalog import build_authoring_package_files, load_authoring_package

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUTHORING = ROOT / "data/indicator_catalog/v1"


def write_authoring_package(target: Path) -> None:
    files = build_authoring_package_files(ROOT)
    target.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        (target / name).write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authoring-dir", type=Path, default=DEFAULT_AUTHORING)
    parser.add_argument("--bootstrap-authoring", action="store_true")
    parser.add_argument("--check-authoring", action="store_true")
    args = parser.parse_args()

    try:
        if args.bootstrap_authoring:
            write_authoring_package(args.authoring_dir)
        if args.check_authoring or args.bootstrap_authoring:
            package = load_authoring_package(args.authoring_dir)
            print(
                "OK: country indicator authoring package "
                f"domains={len(package['domains'])} indicators={len(package['indicators'])} "
                f"authority={package['authoring_authority']}"
            )
            return 0
        parser.error("choose --bootstrap-authoring or --check-authoring")
    except (OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
