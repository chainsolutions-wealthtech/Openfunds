#!/usr/bin/env python3
"""Governed PostgreSQL migration runner for Openfunds."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "migrations/manifest.json"
ID_RE = re.compile(r"^[A-Z0-9_]+$")
FORBIDDEN_SQL = re.compile(
    r"(?im)^\s*\\|^\s*(begin|commit|rollback|start\s+transaction)\s*;"
)


class MigrationError(RuntimeError):
    """Raised when migration governance or execution fails."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sql_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def safe_repo_path(root: Path, raw_path: str) -> Path:
    posix = PurePosixPath(raw_path)
    if posix.is_absolute() or ".." in posix.parts or not posix.parts:
        raise MigrationError(f"unsafe repository path: {raw_path}")
    resolved = (root / Path(*posix.parts)).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise MigrationError(f"path escapes repository: {raw_path}") from exc
    return resolved


def load_manifest(path: Path = DEFAULT_MANIFEST, *, materialize: bool = True) -> dict[str, Any]:
    manifest_path = path.resolve()
    root = manifest_path.parents[1]
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MigrationError(f"cannot load manifest: {exc}") from exc

    if data.get("format_version") != 1 or data.get("database") != "postgresql":
        raise MigrationError("unsupported manifest format or database")
    ledger = data.get("ledger") or {}
    if not ID_RE.fullmatch(str(ledger.get("schema", "")).upper()) or not ID_RE.fullmatch(
        str(ledger.get("table", "")).upper()
    ):
        raise MigrationError("unsafe ledger identifier")

    migrations = data.get("migrations")
    if not isinstance(migrations, list) or not migrations:
        raise MigrationError("manifest must contain migrations")

    seen_ids: set[str] = set()
    seen_orders: set[int] = set()
    seen_paths: set[str] = set()
    previous_order = -1
    for item in migrations:
        if not isinstance(item, dict):
            raise MigrationError("migration entry must be an object")
        migration_id = item.get("id")
        order = item.get("order")
        raw_path = item.get("path")
        if not isinstance(migration_id, str) or not ID_RE.fullmatch(migration_id):
            raise MigrationError(f"invalid migration id: {migration_id}")
        if not isinstance(order, int) or order <= previous_order:
            raise MigrationError("migration orders must be strictly increasing")
        if migration_id in seen_ids or order in seen_orders or raw_path in seen_paths:
            raise MigrationError("duplicate migration id, order or path")
        if not isinstance(raw_path, str) or not raw_path.endswith(".sql"):
            raise MigrationError(f"invalid migration path: {raw_path}")
        target = safe_repo_path(root, raw_path)

        generator = item.get("generator")
        if generator is not None:
            if not isinstance(generator, dict):
                raise MigrationError(f"invalid generator for {migration_id}")
            script = safe_repo_path(root, str(generator.get("script", "")))
            arguments = generator.get("arguments", [])
            if not script.is_file() or not isinstance(arguments, list) or not all(
                isinstance(arg, str) for arg in arguments
            ):
                raise MigrationError(f"invalid generator definition for {migration_id}")
            if materialize:
                subprocess.run(
                    [sys.executable, str(script), *arguments],
                    cwd=root,
                    check=True,
                )

        if not target.is_file():
            raise MigrationError(f"missing migration file: {raw_path}")
        sql = target.read_text(encoding="utf-8")
        if "\r" in sql:
            raise MigrationError(f"CR characters forbidden: {raw_path}")
        if FORBIDDEN_SQL.search(sql):
            raise MigrationError(
                f"transaction/meta-command forbidden in governed migration: {raw_path}"
            )

        item["_absolute_path"] = str(target)
        item["_sha256"] = sha256_file(target)
        previous_order = order
        seen_ids.add(migration_id)
        seen_orders.add(order)
        seen_paths.add(raw_path)

    excluded = data.get("excluded_sql", [])
    if not isinstance(excluded, list):
        raise MigrationError("excluded_sql must be a list")
    for entry in excluded:
        if not isinstance(entry, dict) or not entry.get("reason"):
            raise MigrationError("each excluded SQL path needs a reason")
        raw_path = entry.get("path")
        if not isinstance(raw_path, str):
            raise MigrationError("invalid excluded SQL path")
        safe_repo_path(root, raw_path)
        if raw_path in seen_paths:
            raise MigrationError(f"path both migrated and excluded: {raw_path}")

    data["_root"] = str(root)
    return data


def psql(database_url: str, *, sql: str | None = None, command: str | None = None) -> str:
    args = ["psql", database_url, "-X", "-v", "ON_ERROR_STOP=1", "--no-psqlrc"]
    if command is not None:
        args += ["-At", "-F", "\t", "-c", command]
    result = subprocess.run(
        args,
        input=sql,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        error = result.stderr.strip() or result.stdout.strip()
        raise MigrationError(f"psql failed: {error}")
    return result.stdout


def ledger_names(manifest: dict[str, Any]) -> tuple[str, str]:
    ledger = manifest["ledger"]
    return str(ledger["schema"]), str(ledger["table"])


def ensure_ledger(database_url: str, manifest: dict[str, Any]) -> None:
    schema, table = ledger_names(manifest)
    psql(
        database_url,
        sql=f"""
create schema if not exists {schema};
create table if not exists {schema}.{table} (
    migration_id text primary key,
    migration_order integer not null unique,
    migration_path text not null unique,
    sha256 char(64) not null,
    applied_at timestamptz not null default now(),
    applied_by text not null default current_user,
    runner_version text not null,
    check (sha256 ~ '^[0-9a-f]{{64}}$')
);
""",
    )


def read_ledger(database_url: str, manifest: dict[str, Any]) -> dict[str, dict[str, str]]:
    schema, table = ledger_names(manifest)
    rows = psql(
        database_url,
        command=(
            f"select migration_id, migration_order::text, migration_path, sha256 "
            f"from {schema}.{table} order by migration_order"
        ),
    )
    parsed: dict[str, dict[str, str]] = {}
    for line in rows.splitlines():
        if not line:
            continue
        migration_id, order, path, checksum = line.split("\t")
        parsed[migration_id] = {
            "order": order,
            "path": path,
            "sha256": checksum,
        }
    return parsed


def validate_ledger(manifest: dict[str, Any], ledger: dict[str, dict[str, str]]) -> None:
    expected = {item["id"]: item for item in manifest["migrations"]}
    unknown = sorted(set(ledger) - set(expected))
    if unknown:
        raise MigrationError(f"unknown migration(s) in ledger: {', '.join(unknown)}")
    for migration_id, row in ledger.items():
        item = expected[migration_id]
        if row["order"] != str(item["order"]) or row["path"] != item["path"]:
            raise MigrationError(f"ledger metadata drift for {migration_id}")
        if row["sha256"] != item["_sha256"]:
            raise MigrationError(
                f"checksum drift for {migration_id}; create a new forward migration "
                "or perform an explicitly approved audited repair"
            )


def build_transaction_sql(
    manifest: dict[str, Any], item: dict[str, Any], migration_sql: str
) -> str:
    schema, table = ledger_names(manifest)
    return f"""begin;
set local lock_timeout = '15s';
set local statement_timeout = '5min';
{migration_sql.rstrip()}

insert into {schema}.{table} (
    migration_id, migration_order, migration_path, sha256, runner_version
) values (
    {sql_literal(item['id'])},
    {item['order']},
    {sql_literal(item['path'])},
    {sql_literal(item['_sha256'])},
    '1.0.0'
);
commit;
"""


def apply(database_url: str, manifest: dict[str, Any]) -> None:
    ensure_ledger(database_url, manifest)
    ledger = read_ledger(database_url, manifest)
    validate_ledger(manifest, ledger)
    for item in manifest["migrations"]:
        if item["id"] in ledger:
            print(f"SKIP {item['order']:03d} {item['id']} {item['_sha256']}")
            continue
        migration_sql = Path(item["_absolute_path"]).read_text(encoding="utf-8")
        psql(
            database_url,
            sql=build_transaction_sql(manifest, item, migration_sql),
        )
        print(f"APPLY {item['order']:03d} {item['id']} {item['_sha256']}")
    verify(database_url, manifest)


def verify(database_url: str, manifest: dict[str, Any]) -> None:
    ensure_ledger(database_url, manifest)
    ledger = read_ledger(database_url, manifest)
    validate_ledger(manifest, ledger)
    missing = [item["id"] for item in manifest["migrations"] if item["id"] not in ledger]
    if missing:
        raise MigrationError(f"missing migration(s): {', '.join(missing)}")
    print(f"OK: {len(ledger)} governed migrations verified")


def plan(manifest: dict[str, Any], database_url: str | None = None) -> None:
    ledger: dict[str, dict[str, str]] = {}
    if database_url:
        ensure_ledger(database_url, manifest)
        ledger = read_ledger(database_url, manifest)
        validate_ledger(manifest, ledger)
    for item in manifest["migrations"]:
        status = "APPLIED" if item["id"] in ledger else "PENDING"
        print(
            f"{item['order']:03d} {status:7s} {item['id']} "
            f"{item['_sha256']} {item['path']}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--database-url", default=os.getenv("DATABASE_URL"))
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--verify", action="store_true")
    mode.add_argument("--plan", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        manifest = load_manifest(args.manifest)
        if args.apply or args.verify:
            if not args.database_url:
                raise MigrationError("DATABASE_URL or --database-url is required")
            if args.apply:
                apply(args.database_url, manifest)
            else:
                verify(args.database_url, manifest)
        else:
            plan(manifest, args.database_url)
    except (MigrationError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
