from __future__ import annotations

import argparse
import json
import uuid
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable

try:
    import psycopg
    from psycopg.rows import dict_row
except ImportError as exc:  # pragma: no cover - exercised by CLI environments.
    raise SystemExit(
        "psycopg is required. Install requirements/collectors-postgres.txt"
    ) from exc

NAMESPACE = uuid.UUID("8a15dcc4-f0f5-4fb4-99e1-b87da1f1dfc6")


@dataclass(frozen=True)
class FxLoadProfile:
    profile_code: str
    local_currency_code: str
    collection_specification_code: str
    observed_provider_series_code: str
    canonical_provider_series_by_target: dict[str, str]

    @property
    def supported_targets(self) -> frozenset[str]:
        return frozenset(self.canonical_provider_series_by_target)

    @property
    def expected_quote_convention(self) -> str:
        return f"{self.local_currency_code}_PER_1_FOREIGN_CURRENCY"


BCEAO_XOF_PROFILE = FxLoadProfile(
    profile_code="BCEAO_XOF",
    local_currency_code="XOF",
    collection_specification_code="CS_UEMOA_BCEAO_FX_SNAPSHOT",
    observed_provider_series_code="PS_UEMOA_BCEAO_FX_SNAPSHOT",
    canonical_provider_series_by_target={
        "EUR": "PS_UEMOA_FX_XOF_EUR",
        "USD": "PS_UEMOA_FX_XOF_USD",
    },
)

BEAC_XAF_PROFILE = FxLoadProfile(
    profile_code="BEAC_XAF",
    local_currency_code="XAF",
    collection_specification_code="CS_CEMAC_BEAC_FX_SNAPSHOT",
    observed_provider_series_code="PS_CEMAC_BEAC_FX_SNAPSHOT",
    canonical_provider_series_by_target={
        "EUR": "PS_CEMAC_FX_XAF_EUR",
        "USD": "PS_CEMAC_FX_XAF_USD",
    },
)

LOAD_PROFILES = {
    BCEAO_XOF_PROFILE.profile_code: BCEAO_XOF_PROFILE,
    BEAC_XAF_PROFILE.profile_code: BEAC_XAF_PROFILE,
}

# Backward-compatible BCEAO constants used by earlier integrations.
DEFAULT_COLLECTION_SPEC_CODE = BCEAO_XOF_PROFILE.collection_specification_code
DEFAULT_OBSERVED_PROVIDER_SERIES_CODE = BCEAO_XOF_PROFILE.observed_provider_series_code
CANONICAL_PROVIDER_SERIES_BY_TARGET = dict(
    BCEAO_XOF_PROFILE.canonical_provider_series_by_target
)
SUPPORTED_TARGETS = BCEAO_XOF_PROFILE.supported_targets


@dataclass(frozen=True)
class FxLoadRecord:
    observation_date: str
    source_currency_code: str
    target_currency_code: str
    fx_rate: Decimal
    observation_kind: str
    rate_type: str
    provider_series_code: str
    quality_status: str
    validation_status: str
    source_buy_rate: Decimal | None
    source_sell_rate: Decimal | None
    source_midpoint: Decimal | None
    source_quote_convention: str | None
    transformation_formula: str | None
    methodology_version: str | None
    source_parser_version: str
    source_raw_sha256: str
    collected_at: str

    @property
    def logical_key(self) -> tuple[str, str, str, str, str]:
        return (
            self.observation_date,
            self.source_currency_code,
            self.target_currency_code,
            self.rate_type,
            self.provider_series_code,
        )

    @property
    def deterministic_id(self) -> uuid.UUID:
        payload = "|".join(
            [
                *self.logical_key,
                str(self.fx_rate),
                self.source_raw_sha256,
                self.methodology_version or "",
                self.source_parser_version,
            ]
        )
        return uuid.uuid5(NAMESPACE, f"FX_OBSERVATION|{payload}")


def _positive_decimal(raw: Any, field_name: str) -> Decimal:
    value = Decimal(str(raw))
    if value <= 0:
        raise ValueError(f"{field_name} must be positive: {raw!r}")
    return value


def _optional_decimal(raw: Any) -> Decimal | None:
    if raw is None or raw == "":
        return None
    return _positive_decimal(raw, "optional numeric value")


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def build_observed_records(
    manifest: dict[str, Any],
    profile: FxLoadProfile = BCEAO_XOF_PROFILE,
) -> list[FxLoadRecord]:
    raw_artifact = manifest.get("raw_artifact") or {}
    raw_sha256 = str(raw_artifact.get("sha256") or "")
    retrieved_at = str(raw_artifact.get("retrieved_at") or "")
    parser_version = str(manifest.get("parser_version") or "")
    if not raw_sha256 or not retrieved_at or not parser_version:
        raise ValueError("observed manifest lineage is incomplete")

    records: list[FxLoadRecord] = []
    for row in manifest.get("observations") or []:
        foreign_currency = str(row.get("canonical_currency_code") or "").upper()
        if foreign_currency not in profile.supported_targets:
            continue
        value_date = str(row.get("value_date") or "")
        if not value_date:
            raise ValueError(f"missing value date for {foreign_currency}")
        buy = _positive_decimal(row.get("provider_buy_rate"), "provider_buy_rate")
        sell = _positive_decimal(row.get("provider_sell_rate"), "provider_sell_rate")
        midpoint = (buy + sell) / Decimal(2)
        quote = str(row.get("quote_convention_source") or "")
        if quote != profile.expected_quote_convention:
            raise ValueError(
                f"unsupported source quote convention for {profile.profile_code}: {quote!r}"
            )

        common = dict(
            observation_date=value_date,
            source_currency_code=foreign_currency,
            target_currency_code=profile.local_currency_code,
            observation_kind="OBSERVED",
            provider_series_code=profile.observed_provider_series_code,
            quality_status="OBSERVED_DIRECT",
            validation_status="VALIDATED",
            source_buy_rate=buy,
            source_sell_rate=sell,
            source_midpoint=midpoint,
            source_quote_convention=quote,
            transformation_formula=None,
            methodology_version=None,
            source_parser_version=parser_version,
            source_raw_sha256=raw_sha256,
            collected_at=retrieved_at,
        )
        records.append(FxLoadRecord(fx_rate=buy, rate_type="BUY", **common))
        records.append(FxLoadRecord(fx_rate=sell, rate_type="SELL", **common))

    expected_count = len(profile.supported_targets) * 2
    if len(records) != expected_count:
        raise ValueError(
            f"expected {expected_count} observed EUR/USD buy/sell records for "
            f"{profile.profile_code}, got {len(records)}"
        )
    return records


def build_canonical_records(
    payload: dict[str, Any],
    collected_at: str,
    profile: FxLoadProfile = BCEAO_XOF_PROFILE,
) -> list[FxLoadRecord]:
    records: list[FxLoadRecord] = []
    for row in payload.get("observations") or []:
        target = str(row.get("target_currency_code") or "").upper()
        if target not in profile.supported_targets:
            continue
        source_currency = str(row.get("source_currency_code") or "").upper()
        if source_currency != profile.local_currency_code:
            raise ValueError(
                f"canonical source currency mismatch for {profile.profile_code}: "
                f"{source_currency!r}"
            )
        pair_code = str(row.get("canonical_pair_code") or "").upper()
        expected_pair_code = f"{profile.local_currency_code}_{target}"
        if pair_code != expected_pair_code:
            raise ValueError(
                f"canonical pair mismatch for {profile.profile_code}: {pair_code!r}"
            )

        provider_series_code = profile.canonical_provider_series_by_target[target]
        records.append(
            FxLoadRecord(
                observation_date=str(row.get("value_date") or ""),
                source_currency_code=profile.local_currency_code,
                target_currency_code=target,
                fx_rate=_positive_decimal(row.get("canonical_rate"), "canonical_rate"),
                observation_kind="CALCULATED",
                rate_type="MIDPOINT_INVERTED",
                provider_series_code=provider_series_code,
                quality_status=str(row.get("quality_status") or "CALCULATED"),
                validation_status="VALIDATED",
                source_buy_rate=_optional_decimal(row.get("source_buy_rate")),
                source_sell_rate=_optional_decimal(row.get("source_sell_rate")),
                source_midpoint=_optional_decimal(row.get("source_midpoint")),
                source_quote_convention=str(row.get("source_quote_convention") or ""),
                transformation_formula=str(row.get("transformation_formula") or ""),
                methodology_version=str(row.get("methodology_version") or ""),
                source_parser_version=str(row.get("source_parser_version") or ""),
                source_raw_sha256=str(row.get("source_raw_sha256") or ""),
                collected_at=collected_at,
            )
        )

    if {record.target_currency_code for record in records} != profile.supported_targets:
        expected = sorted(
            f"{profile.local_currency_code}_{target}"
            for target in profile.supported_targets
        )
        raise ValueError(f"canonical payload must contain {expected}")
    return records


def _lookup_single_id(
    connection: psycopg.Connection[Any],
    sql: str,
    value: str,
    label: str,
) -> uuid.UUID:
    with connection.cursor(row_factory=dict_row) as cursor:
        cursor.execute(sql, (value,))
        row = cursor.fetchone()
    if not row:
        raise LookupError(f"missing {label}: {value}")
    return row[next(iter(row))]


def _resolve_currency_ids(
    connection: psycopg.Connection[Any], codes: Iterable[str]
) -> dict[str, uuid.UUID]:
    result: dict[str, uuid.UUID] = {}
    for code in sorted(set(codes)):
        result[code] = _lookup_single_id(
            connection,
            "select currency_id from ref.currency where iso_code = %s",
            code,
            "currency",
        )
    return result


def _resolve_provider_series_ids(
    connection: psycopg.Connection[Any], codes: Iterable[str]
) -> dict[str, uuid.UUID]:
    result: dict[str, uuid.UUID] = {}
    for code in sorted(set(codes)):
        result[code] = _lookup_single_id(
            connection,
            "select provider_series_id from source.provider_series where provider_series_code = %s",
            code,
            "provider series",
        )
    return result


def _ensure_collection_lineage(
    connection: psycopg.Connection[Any],
    manifest: dict[str, Any],
    storage_uri: str,
    observation_count: int,
    profile: FxLoadProfile,
) -> tuple[uuid.UUID, uuid.UUID]:
    raw = manifest.get("raw_artifact") or {}
    sha256 = str(raw.get("sha256") or "")
    retrieved_at = str(raw.get("retrieved_at") or "")
    source_url = str(raw.get("source_url") or "")
    media_type = str(raw.get("media_type") or "application/octet-stream")
    byte_size = int(raw.get("byte_size") or 0)
    parser_version = str(manifest.get("parser_version") or "")
    if not all([sha256, retrieved_at, source_url, parser_version, storage_uri]):
        raise ValueError("collection lineage fields are incomplete")

    specification_id = _lookup_single_id(
        connection,
        "select collection_specification_id from source.collection_specification where collection_specification_code = %s",
        profile.collection_specification_code,
        "collection specification",
    )
    run_id = uuid.uuid5(
        NAMESPACE,
        f"COLLECTION_RUN|{profile.collection_specification_code}|{sha256}|{parser_version}",
    )
    artifact_id = uuid.uuid5(
        NAMESPACE,
        f"RAW_ARTIFACT|{profile.collection_specification_code}|{sha256}|{storage_uri}",
    )
    warning_count = len(manifest.get("warnings") or [])
    error_count = len(manifest.get("errors") or [])
    execution_metadata = json.dumps(
        {
            "collector_code": manifest.get("collector_code"),
            "fx_load_profile": profile.profile_code,
            "source_run_status": manifest.get("run_status"),
            "source_raw_sha256": sha256,
        },
        sort_keys=True,
    )

    connection.execute(
        """
        insert into source.collection_run (
            collection_run_id, collection_specification_id, started_at, completed_at,
            run_status, source_url, artifact_count, observation_count,
            warning_count, error_count, parser_version, execution_metadata
        ) values (
            %s, %s, %s::timestamptz, %s::timestamptz,
            'SUCCEEDED', %s, 1, %s, %s, %s, %s, %s::jsonb
        )
        on conflict (collection_run_id) do nothing
        """,
        (
            run_id,
            specification_id,
            retrieved_at,
            retrieved_at,
            source_url,
            observation_count,
            warning_count,
            error_count,
            parser_version,
            execution_metadata,
        ),
    )
    connection.execute(
        """
        insert into source.raw_artifact (
            raw_artifact_id, collection_run_id, source_url, original_filename,
            media_type, sha256, byte_size, retrieved_at, storage_uri, metadata
        ) values (
            %s, %s, %s, %s, %s, %s, %s, %s::timestamptz, %s, %s::jsonb
        )
        on conflict (raw_artifact_id) do nothing
        """,
        (
            artifact_id,
            run_id,
            source_url,
            Path(storage_uri).name,
            media_type,
            sha256,
            byte_size,
            retrieved_at,
            storage_uri,
            json.dumps(
                {
                    "fx_load_profile": profile.profile_code,
                    "parser_version": parser_version,
                },
                sort_keys=True,
            ),
        ),
    )
    return run_id, artifact_id


def _normalized_decimal(value: Any) -> Decimal | None:
    if value is None:
        return None
    return Decimal(str(value))


def _record_matches(row: dict[str, Any], record: FxLoadRecord) -> bool:
    comparisons = {
        "fx_rate": record.fx_rate,
        "source_buy_rate": record.source_buy_rate,
        "source_sell_rate": record.source_sell_rate,
        "source_midpoint": record.source_midpoint,
    }
    for field, expected in comparisons.items():
        if _normalized_decimal(row.get(field)) != expected:
            return False
    return all(
        [
            row.get("observation_kind") == record.observation_kind,
            row.get("source_quote_convention") == record.source_quote_convention,
            row.get("transformation_formula") == record.transformation_formula,
            row.get("methodology_version") == record.methodology_version,
            row.get("source_parser_version") == record.source_parser_version,
            row.get("source_raw_sha256") == record.source_raw_sha256,
            row.get("quality_status") == record.quality_status,
            row.get("validation_status") == record.validation_status,
        ]
    )


def _upsert_record(
    connection: psycopg.Connection[Any],
    record: FxLoadRecord,
    currency_ids: dict[str, uuid.UUID],
    provider_series_ids: dict[str, uuid.UUID],
    collection_run_id: uuid.UUID,
    raw_artifact_id: uuid.UUID,
) -> str:
    source_currency_id = currency_ids[record.source_currency_code]
    target_currency_id = currency_ids[record.target_currency_code]
    provider_series_id = provider_series_ids[record.provider_series_code]

    with connection.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            """
            select *
            from market.fx_observation
            where observation_date = %s::date
              and source_currency_id = %s
              and target_currency_id = %s
              and rate_type = %s
              and provider_series_id = %s
              and is_current
            for update
            """,
            (
                record.observation_date,
                source_currency_id,
                target_currency_id,
                record.rate_type,
                provider_series_id,
            ),
        )
        current = cursor.fetchone()

    if current and _record_matches(current, record):
        return "SKIPPED_IDENTICAL"

    if current:
        connection.execute(
            """
            update market.fx_observation
            set is_current = false,
                system_to = now(),
                validation_status = 'SUPERSEDED'
            where fx_observation_id = %s
            """,
            (current["fx_observation_id"],),
        )

    existing_same_version = connection.execute(
        "select fx_observation_id from market.fx_observation where fx_observation_id = %s",
        (record.deterministic_id,),
    ).fetchone()
    if existing_same_version:
        connection.execute(
            """
            update market.fx_observation
            set is_current = true,
                system_to = null,
                validation_status = %s,
                collection_run_id = %s,
                raw_artifact_id = %s,
                collected_at = %s::timestamptz
            where fx_observation_id = %s
            """,
            (
                record.validation_status,
                collection_run_id,
                raw_artifact_id,
                record.collected_at,
                record.deterministic_id,
            ),
        )
        return "REACTIVATED_VERSION"

    connection.execute(
        """
        insert into market.fx_observation (
            fx_observation_id, observation_date, source_currency_id, target_currency_id,
            fx_rate, quality_status, observation_kind, rate_type, provider_series_id,
            collection_run_id, raw_artifact_id, source_buy_rate, source_sell_rate,
            source_midpoint, source_quote_convention, transformation_formula,
            methodology_version, source_parser_version, source_raw_sha256,
            collected_at, validation_status, is_current
        ) values (
            %s, %s::date, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s::timestamptz, %s, true
        )
        """,
        (
            record.deterministic_id,
            record.observation_date,
            source_currency_id,
            target_currency_id,
            record.fx_rate,
            record.quality_status,
            record.observation_kind,
            record.rate_type,
            provider_series_id,
            collection_run_id,
            raw_artifact_id,
            record.source_buy_rate,
            record.source_sell_rate,
            record.source_midpoint,
            record.source_quote_convention,
            record.transformation_formula,
            record.methodology_version,
            record.source_parser_version,
            record.source_raw_sha256,
            record.collected_at,
            record.validation_status,
        ),
    )
    return "SUPERSEDED_THEN_INSERTED" if current else "INSERTED"


def load_fx_bundle(
    connection: psycopg.Connection[Any],
    manifest: dict[str, Any],
    canonical_payload: dict[str, Any],
    storage_uri: str,
    profile: FxLoadProfile = BCEAO_XOF_PROFILE,
) -> dict[str, Any]:
    observed_records = build_observed_records(manifest, profile)
    collected_at = str((manifest.get("raw_artifact") or {}).get("retrieved_at") or "")
    canonical_records = build_canonical_records(canonical_payload, collected_at, profile)
    records = [*observed_records, *canonical_records]

    currency_ids = _resolve_currency_ids(
        connection,
        [
            code
            for record in records
            for code in (record.source_currency_code, record.target_currency_code)
        ],
    )
    provider_series_ids = _resolve_provider_series_ids(
        connection, [record.provider_series_code for record in records]
    )
    collection_run_id, raw_artifact_id = _ensure_collection_lineage(
        connection,
        manifest,
        storage_uri,
        len(records),
        profile,
    )

    actions: dict[str, int] = {}
    for record in records:
        action = _upsert_record(
            connection,
            record,
            currency_ids,
            provider_series_ids,
            collection_run_id,
            raw_artifact_id,
        )
        actions[action] = actions.get(action, 0) + 1

    return {
        "fx_load_profile": profile.profile_code,
        "local_currency_code": profile.local_currency_code,
        "collection_run_id": str(collection_run_id),
        "raw_artifact_id": str(raw_artifact_id),
        "record_count": len(records),
        "actions": dict(sorted(actions.items())),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Load observed and calculated BCEAO or BEAC FX observations into PostgreSQL."
    )
    parser.add_argument("--dsn", required=True)
    parser.add_argument("--observed-manifest", type=Path, required=True)
    parser.add_argument("--canonical-staging", type=Path, required=True)
    parser.add_argument("--storage-uri")
    parser.add_argument("--summary-output", type=Path)
    parser.add_argument(
        "--profile",
        choices=sorted(LOAD_PROFILES),
        default=BCEAO_XOF_PROFILE.profile_code,
    )
    args = parser.parse_args()

    manifest = _read_json(args.observed_manifest)
    canonical_payload = _read_json(args.canonical_staging)
    storage_uri = args.storage_uri or str(
        (manifest.get("raw_artifact") or {}).get("storage_path") or ""
    )
    profile = LOAD_PROFILES[args.profile]

    with psycopg.connect(args.dsn) as connection:
        summary = load_fx_bundle(
            connection,
            manifest,
            canonical_payload,
            storage_uri,
            profile,
        )

    rendered = json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True)
    print(rendered)
    if args.summary_output:
        args.summary_output.parent.mkdir(parents=True, exist_ok=True)
        args.summary_output.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
