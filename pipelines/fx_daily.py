from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Iterable

from collectors import bceao_fx, beac_fx
from collectors.common import CollectionResult, utc_now_iso
from collectors.fx_canonical import (
    CanonicalFxObservation,
    transform_local_manifest,
    write_canonical_observations,
)

CollectorRun = Callable[[str, Path], CollectionResult]


@dataclass(frozen=True)
class FxSourceConfig:
    source_code: str
    collector_code: str
    collector_url: str
    local_currency_code: str
    loader_profile_code: str
    collector_run: CollectorRun


DEFAULT_SOURCE_CONFIGS = (
    FxSourceConfig(
        source_code="BCEAO_XOF",
        collector_code=bceao_fx.COLLECTOR_CODE,
        collector_url=bceao_fx.DEFAULT_URL,
        local_currency_code="XOF",
        loader_profile_code="BCEAO_XOF",
        collector_run=bceao_fx.run,
    ),
    FxSourceConfig(
        source_code="BEAC_XAF",
        collector_code=beac_fx.COLLECTOR_CODE,
        collector_url=beac_fx.DEFAULT_URL,
        local_currency_code="XAF",
        loader_profile_code="BEAC_XAF",
        collector_run=beac_fx.run,
    ),
)


def _write_json(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _manifest_from_result(result: CollectionResult) -> dict[str, Any]:
    return asdict(result)


def _canonical_summary(
    observations: Iterable[CanonicalFxObservation],
) -> tuple[list[str], dict[str, str]]:
    items = list(observations)
    return (
        sorted(item.canonical_pair_code for item in items),
        {
            item.canonical_pair_code: item.canonical_rate
            for item in sorted(items, key=lambda row: row.canonical_pair_code)
        },
    )


def _persist_bundle_to_postgres(
    *,
    database_url: str,
    config: FxSourceConfig,
    manifest: dict[str, Any],
    canonical_payload: dict[str, Any],
    storage_uri: str,
) -> dict[str, Any]:
    # Import lazily so staging-only runs do not require psycopg.
    import psycopg

    from loaders.fx_postgres import LOAD_PROFILES, load_fx_bundle

    profile = LOAD_PROFILES[config.loader_profile_code]
    with psycopg.connect(database_url) as connection:
        return load_fx_bundle(
            connection,
            manifest,
            canonical_payload,
            storage_uri,
            profile,
        )


def _process_source(
    *,
    config: FxSourceConfig,
    output_root: Path,
    persist_postgres: bool,
    database_url: str | None,
    raw_retention_status: str,
) -> dict[str, Any]:
    source_root = output_root / config.source_code.lower()
    source_root.mkdir(parents=True, exist_ok=True)

    entry: dict[str, Any] = {
        "source_code": config.source_code,
        "collector_code": config.collector_code,
        "collector_url": config.collector_url,
        "local_currency_code": config.local_currency_code,
        "loader_profile_code": config.loader_profile_code,
        "collection_status": "NOT_STARTED",
        "canonical_status": "NOT_STARTED",
        "database_status": "NOT_REQUESTED",
        "history_status": "CURRENT_SNAPSHOT_ONLY",
        "raw_retention_status": raw_retention_status,
        "warnings": [],
        "errors": [],
    }

    try:
        result = config.collector_run(config.collector_url, source_root)
    except Exception as exc:  # noqa: BLE001: source failures must be recorded per provider.
        entry["collection_status"] = "FAILED"
        entry["errors"] = [f"COLLECTOR_EXCEPTION:{type(exc).__name__}:{exc}"]
        return entry

    manifest = _manifest_from_result(result)
    raw = manifest.get("raw_artifact") or {}
    entry.update(
        {
            "collection_status": result.run_status,
            "parser_version": result.parser_version,
            "raw_sha256": raw.get("sha256"),
            "raw_byte_size": raw.get("byte_size"),
            "raw_media_type": raw.get("media_type"),
            "raw_storage_path": raw.get("storage_path"),
            "retrieved_at": raw.get("retrieved_at"),
            "observed_count": len(result.observations),
            "observed_currency_codes": sorted(
                {
                    str(row.get("canonical_currency_code"))
                    for row in result.observations
                    if row.get("canonical_currency_code")
                }
            ),
            "value_dates": sorted(
                {
                    str(row.get("value_date"))
                    for row in result.observations
                    if row.get("value_date")
                }
            ),
            "warnings": list(result.warnings),
            "errors": list(result.errors),
        }
    )

    if result.run_status != "SUCCESS" or result.errors:
        entry["canonical_status"] = "NOT_ATTEMPTED"
        entry["database_status"] = "NOT_ATTEMPTED"
        return entry

    try:
        canonical_observations = transform_local_manifest(
            manifest,
            config.local_currency_code,
        )
        canonical_path = source_root / "staging" / "canonical_fx.json"
        write_canonical_observations(canonical_observations, canonical_path)
        canonical_pairs, canonical_rates = _canonical_summary(canonical_observations)
        entry.update(
            {
                "canonical_status": "SUCCESS",
                "canonical_methodology_version": "FX_CANONICAL_0.1.0",
                "canonical_observation_count": len(canonical_observations),
                "canonical_pairs": canonical_pairs,
                "canonical_rates": canonical_rates,
                "canonical_storage_path": str(canonical_path),
            }
        )
    except Exception as exc:  # noqa: BLE001: preserve successful raw collection.
        entry["canonical_status"] = "FAILED"
        entry["database_status"] = "NOT_ATTEMPTED"
        entry["errors"].append(
            f"CANONICAL_EXCEPTION:{type(exc).__name__}:{exc}"
        )
        return entry

    if not persist_postgres:
        entry["database_status"] = "NOT_REQUESTED"
        return entry

    if not database_url:
        entry["database_status"] = "NOT_CONFIGURED"
        return entry

    canonical_payload = {
        "methodology_version": "FX_CANONICAL_0.1.0",
        "observation_count": len(canonical_observations),
        "observations": [asdict(item) for item in canonical_observations],
    }
    try:
        database_summary = _persist_bundle_to_postgres(
            database_url=database_url,
            config=config,
            manifest=manifest,
            canonical_payload=canonical_payload,
            storage_uri=str(raw.get("storage_path") or ""),
        )
        entry["database_status"] = "SUCCESS"
        entry["database_load_summary"] = database_summary
    except Exception as exc:  # noqa: BLE001: record provider-specific DB failure.
        entry["database_status"] = "FAILED"
        entry["errors"].append(
            f"DATABASE_EXCEPTION:{type(exc).__name__}:{exc}"
        )
    return entry


def _overall_status(
    entries: list[dict[str, Any]],
    *,
    persist_postgres: bool,
    database_url: str | None,
) -> str:
    source_success = [
        entry.get("collection_status") == "SUCCESS"
        and entry.get("canonical_status") == "SUCCESS"
        for entry in entries
    ]
    if not any(source_success):
        return "FAILED"
    if not all(source_success):
        return "PARTIAL"

    if not persist_postgres:
        return "STAGING_ONLY"
    if not database_url:
        return "STAGING_ONLY_DATABASE_NOT_CONFIGURED"

    database_success = [entry.get("database_status") == "SUCCESS" for entry in entries]
    return "SUCCESS" if all(database_success) else "PARTIAL"


def run_daily_fx_pipeline(
    *,
    output_dir: Path,
    source_configs: Iterable[FxSourceConfig] = DEFAULT_SOURCE_CONFIGS,
    persist_postgres: bool = False,
    database_url: str | None = None,
    raw_retention_status: str = "LOCAL_PATH_ONLY",
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_at = utc_now_iso()
    entries = [
        _process_source(
            config=config,
            output_root=output_dir,
            persist_postgres=persist_postgres,
            database_url=database_url,
            raw_retention_status=raw_retention_status,
        )
        for config in source_configs
    ]
    payload = {
        "pipeline_code": "DAILY_AFRICA_FX_SNAPSHOTS",
        "pipeline_version": "0.1.0",
        "generated_at": generated_at,
        "overall_status": _overall_status(
            entries,
            persist_postgres=persist_postgres,
            database_url=database_url,
        ),
        "persistence_requested": persist_postgres,
        "persistent_database_configured": bool(database_url),
        "history_claim": "NO_FULL_HISTORY_CLAIM",
        "source_count": len(entries),
        "sources": entries,
    }
    _write_json(payload, output_dir / "coverage" / "daily_fx_coverage.json")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect BCEAO and BEAC daily FX snapshots with canonical EUR/USD staging and optional PostgreSQL persistence."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/daily/fx"),
    )
    parser.add_argument(
        "--persist-postgres",
        action="store_true",
        help="Load into PostgreSQL when OPENFUNDS_DATABASE_URL is configured.",
    )
    parser.add_argument(
        "--require-persistence",
        action="store_true",
        help="Fail before collection when persistent PostgreSQL is not configured.",
    )
    parser.add_argument(
        "--raw-retention-status",
        default="LOCAL_PATH_ONLY",
    )
    args = parser.parse_args()

    database_url = os.environ.get("OPENFUNDS_DATABASE_URL")
    persist_postgres = args.persist_postgres or args.require_persistence
    if args.require_persistence and not database_url:
        parser.error(
            "--require-persistence needs OPENFUNDS_DATABASE_URL to be configured"
        )

    result = run_daily_fx_pipeline(
        output_dir=args.output_dir,
        persist_postgres=persist_postgres,
        database_url=database_url,
        raw_retention_status=args.raw_retention_status,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["overall_status"] in {
        "SUCCESS",
        "STAGING_ONLY",
        "STAGING_ONLY_DATABASE_NOT_CONFIGURED",
    } else 1


if __name__ == "__main__":
    raise SystemExit(main())
