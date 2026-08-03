from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN, getcontext
from pathlib import Path
from typing import Any

METHODOLOGY_VERSION = "FX_CANONICAL_0.1.0"
RATE_QUANTUM = Decimal("0.000000000000000001")
SUPPORTED_TARGET_CURRENCIES = {"EUR", "USD"}
SUPPORTED_LOCAL_CURRENCIES = {"XOF", "XAF"}

getcontext().prec = 40


@dataclass(frozen=True)
class CanonicalFxObservation:
    observation_type: str
    value_date: str
    canonical_pair_code: str
    source_currency_code: str
    target_currency_code: str
    canonical_rate: str
    rate_type: str
    provider_currency_label: str
    source_buy_rate: str
    source_sell_rate: str
    source_midpoint: str
    source_quote_convention: str
    transformation_formula: str
    methodology_version: str
    source_raw_sha256: str
    source_url: str
    source_parser_version: str
    quality_status: str


def _positive_decimal(raw: str, field_name: str) -> Decimal:
    try:
        value = Decimal(raw)
    except (InvalidOperation, TypeError) as exc:
        raise ValueError(f"invalid {field_name}: {raw!r}") from exc
    if value <= 0:
        raise ValueError(f"non-positive {field_name}: {raw!r}")
    return value


def _format_rate(value: Decimal) -> str:
    return format(value.quantize(RATE_QUANTUM, rounding=ROUND_HALF_EVEN), "f")


def transform_local_manifest(
    manifest: dict[str, Any], local_currency_code: str
) -> list[CanonicalFxObservation]:
    local_currency = local_currency_code.upper()
    if local_currency not in SUPPORTED_LOCAL_CURRENCIES:
        raise ValueError(f"unsupported local currency: {local_currency_code!r}")

    raw_artifact = manifest.get("raw_artifact") or {}
    raw_sha256 = raw_artifact.get("sha256")
    source_url = raw_artifact.get("source_url")
    parser_version = manifest.get("parser_version")

    if not raw_sha256 or not source_url or not parser_version:
        raise ValueError("manifest lineage is incomplete")

    expected_quote_convention = f"{local_currency}_PER_1_FOREIGN_CURRENCY"
    transformed: list[CanonicalFxObservation] = []
    seen_pairs: set[str] = set()

    for row in manifest.get("observations") or []:
        target_currency = row.get("canonical_currency_code")
        if target_currency not in SUPPORTED_TARGET_CURRENCIES:
            continue

        value_date = row.get("value_date")
        if not value_date:
            raise ValueError(f"missing value_date for {target_currency}")

        quote_convention = row.get("quote_convention_source")
        if quote_convention != expected_quote_convention:
            raise ValueError(
                f"unexpected quote convention for {target_currency}: {quote_convention!r}"
            )

        buy = _positive_decimal(row.get("provider_buy_rate"), "provider_buy_rate")
        sell = _positive_decimal(row.get("provider_sell_rate"), "provider_sell_rate")
        midpoint = (buy + sell) / Decimal(2)
        canonical_rate = Decimal(1) / midpoint
        pair_code = f"{local_currency}_{target_currency}"

        if pair_code in seen_pairs:
            raise ValueError(f"duplicate provider row for {pair_code}")
        seen_pairs.add(pair_code)

        transformed.append(
            CanonicalFxObservation(
                observation_type="CALCULATED_FX",
                value_date=value_date,
                canonical_pair_code=pair_code,
                source_currency_code=local_currency,
                target_currency_code=target_currency,
                canonical_rate=_format_rate(canonical_rate),
                rate_type="MIDPOINT_INVERTED",
                provider_currency_label=str(row.get("provider_currency_label") or ""),
                source_buy_rate=format(buy, "f"),
                source_sell_rate=format(sell, "f"),
                source_midpoint=_format_rate(midpoint),
                source_quote_convention=quote_convention,
                transformation_formula="1 / ((PROVIDER_BUY_RATE + PROVIDER_SELL_RATE) / 2)",
                methodology_version=METHODOLOGY_VERSION,
                source_raw_sha256=raw_sha256,
                source_url=source_url,
                source_parser_version=parser_version,
                quality_status="CALCULATED_INVERTED_MIDPOINT",
            )
        )

    expected_pairs = {
        f"{local_currency}_EUR",
        f"{local_currency}_USD",
    }
    found_pairs = {item.canonical_pair_code for item in transformed}
    missing = expected_pairs - found_pairs
    if missing:
        raise ValueError(f"missing required canonical pairs: {sorted(missing)}")

    return sorted(transformed, key=lambda item: item.canonical_pair_code)


def transform_xof_manifest(manifest: dict[str, Any]) -> list[CanonicalFxObservation]:
    """Backward-compatible BCEAO wrapper."""
    return transform_local_manifest(manifest, "XOF")


def write_canonical_observations(
    observations: list[CanonicalFxObservation], output_path: Path
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "methodology_version": METHODOLOGY_VERSION,
        "observation_count": len(observations),
        "observations": [asdict(item) for item in observations],
    }
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Transform an observed local/foreign FX manifest into canonical LOCAL/EUR and LOCAL/USD observations."
    )
    parser.add_argument("--input-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--local-currency",
        choices=sorted(SUPPORTED_LOCAL_CURRENCIES),
        default="XOF",
    )
    args = parser.parse_args()

    manifest = json.loads(args.input_manifest.read_text(encoding="utf-8"))
    observations = transform_local_manifest(manifest, args.local_currency)
    write_canonical_observations(observations, args.output)
    print(
        f"{METHODOLOGY_VERSION}: wrote {len(observations)} canonical observations to {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
