from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from collectors.common import (
    CollectionResult,
    fetch_bytes,
    persist_raw_artifact,
    write_result_manifest,
)
from collectors.fx_html_common import (
    DivClassTextBlockParser,
    FxObservation,
    TableTextParser,
    detect_value_date,
    normalize_decimal,
    visible_html_text,
)

COLLECTOR_CODE = "BEAC_FX_SNAPSHOT"
PARSER_VERSION = "0.2.0"
DEFAULT_URL = "https://www.beac.int/index.php/accueil"

PAIR_TO_FOREIGN_CURRENCY = {
    "EUR/XAF": "EUR",
    "USD/XAF": "USD",
    "GBP/XAF": "GBP",
    "CHF/XAF": "CHF",
    "JPY/XAF": "JPY",
    "CAD/XAF": "CAD",
    "SEK/XAF": "SEK",
    "ZAR/XAF": "ZAR",
    "MAD/XAF": "MAD",
    "SAR/XAF": "SAR",
    "AED/XAF": "AED",
    "CNY/XAF": "CNY",
    "DKK/XAF": "DKK",
}


def _normalize_pair_label(raw: str) -> str:
    return "".join(raw.upper().split())


def rows_to_observations(rows: Iterable[list[str]], value_date: str | None) -> list[FxObservation]:
    observations: list[FxObservation] = []
    for row in rows:
        if len(row) < 3:
            continue
        provider_label = row[0].strip()
        normalized_pair = _normalize_pair_label(provider_label)
        foreign_currency = PAIR_TO_FOREIGN_CURRENCY.get(normalized_pair)
        if foreign_currency is None:
            continue
        try:
            buy = normalize_decimal(row[-2])
            sell = normalize_decimal(row[-1])
        except ValueError:
            continue
        observations.append(
            FxObservation(
                value_date=value_date,
                provider_currency_label=provider_label,
                provider_buy_rate=buy,
                provider_sell_rate=sell,
                canonical_currency_code=foreign_currency,
                quote_convention_source="XAF_PER_1_FOREIGN_CURRENCY",
                quality_status="OBSERVED_DIRECT",
            )
        )
    return observations


def _deduplicate_observations(
    observations: Iterable[FxObservation],
) -> tuple[list[FxObservation], list[str]]:
    by_currency: dict[str, FxObservation] = {}
    warnings: list[str] = []
    for item in observations:
        code = item.canonical_currency_code
        if not code:
            continue
        existing = by_currency.get(code)
        if existing is None:
            by_currency[code] = item
            continue
        if (
            existing.provider_buy_rate == item.provider_buy_rate
            and existing.provider_sell_rate == item.provider_sell_rate
            and existing.value_date == item.value_date
        ):
            continue
        warnings.append(f"CONFLICTING_DUPLICATE_PAIR:{code}")
    return [by_currency[code] for code in sorted(by_currency)], warnings


def parse_beac_fx_html(payload: bytes) -> tuple[list[FxObservation], list[str]]:
    text = payload.decode("utf-8", errors="replace")

    table_parser = TableTextParser()
    table_parser.feed(text)

    div_parser = DivClassTextBlockParser("taux_de_change")
    div_parser.feed(text)

    value_date = detect_value_date(visible_html_text(payload))
    parsed = rows_to_observations(
        [*table_parser.rows, *div_parser.rows],
        value_date,
    )
    observations, warnings = _deduplicate_observations(parsed)

    if value_date is None:
        warnings.append("VALUE_DATE_NOT_FOUND")
    expected = {"EUR", "USD"}
    found = {item.canonical_currency_code for item in observations}
    for missing in sorted(expected - found):
        warnings.append(f"EXPECTED_CURRENCY_NOT_FOUND:{missing}")
    return observations, warnings


def run(url: str, output_dir: Path) -> CollectionResult:
    payload, media_type = fetch_bytes(url)
    artifact = persist_raw_artifact(payload, url, media_type, output_dir / "raw", "beac_fx")
    observations, warnings = parse_beac_fx_html(payload)
    errors: list[str] = []
    status = "SUCCESS"
    if not observations:
        status = "FAILED"
        errors.append("NO_FX_OBSERVATIONS_PARSED")
    result = CollectionResult(
        collector_code=COLLECTOR_CODE,
        run_status=status,
        raw_artifact=artifact,
        observations=[item.__dict__ for item in observations],
        warnings=warnings,
        errors=errors,
        parser_version=PARSER_VERSION,
    )
    write_result_manifest(result, output_dir / "manifests" / f"{artifact.sha256}.json")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect and parse the BEAC FX snapshot.")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/collections/beac_fx"))
    args = parser.parse_args()
    result = run(args.url, args.output_dir)
    print(f"{result.collector_code}: {result.run_status}; observations={len(result.observations)}")
    return 0 if result.run_status == "SUCCESS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
