from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

from collectors.common import (
    CollectionResult,
    fetch_bytes,
    persist_raw_artifact,
    write_result_manifest,
)

COLLECTOR_CODE = "BCEAO_FX_SNAPSHOT"
PARSER_VERSION = "0.1.0"
DEFAULT_URL = "https://www.bceao.int/fr"


@dataclass(frozen=True)
class FxObservation:
    value_date: str | None
    provider_currency_label: str
    provider_buy_rate: str
    provider_sell_rate: str
    canonical_currency_code: str | None
    quote_convention_source: str
    quality_status: str


class TableTextParser(HTMLParser):
    """Collect text by HTML table row and cell without external dependencies."""

    def __init__(self) -> None:
        super().__init__()
        self.rows: list[list[str]] = []
        self._row: list[str] | None = None
        self._cell_parts: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "tr":
            self._row = []
        elif tag in {"td", "th"} and self._row is not None:
            self._cell_parts = []

    def handle_data(self, data: str) -> None:
        if self._cell_parts is not None:
            self._cell_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"td", "th"} and self._cell_parts is not None and self._row is not None:
            value = " ".join("".join(self._cell_parts).split())
            self._row.append(unescape(value))
            self._cell_parts = None
        elif tag == "tr" and self._row is not None:
            if any(cell for cell in self._row):
                self.rows.append(self._row)
            self._row = None


CURRENCY_ALIASES = {
    "EURO": "EUR",
    "EUR": "EUR",
    "DOLLAR US": "USD",
    "DOLLAR USA": "USD",
    "DOLLAR AMERICAIN": "USD",
    "USD": "USD",
    "LIVRE STERLING": "GBP",
    "GBP": "GBP",
    "YEN JAPONAIS": "JPY",
    "JPY": "JPY",
}


def normalize_decimal(raw: str) -> str:
    cleaned = raw.replace("\u00a0", " ").replace(" ", "").strip()
    if not cleaned:
        raise ValueError("empty numeric value")
    if cleaned.count(",") == 1 and cleaned.count(".") == 0:
        cleaned = cleaned.replace(",", ".")
    elif cleaned.count(",") > 0 and cleaned.count(".") > 0:
        # The final separator is treated as decimal; the other as thousands.
        if cleaned.rfind(",") > cleaned.rfind("."):
            cleaned = cleaned.replace(".", "").replace(",", ".")
        else:
            cleaned = cleaned.replace(",", "")
    try:
        value = Decimal(cleaned)
    except InvalidOperation as exc:
        raise ValueError(f"invalid numeric value: {raw!r}") from exc
    if value <= 0:
        raise ValueError(f"non-positive FX rate: {raw!r}")
    return format(value, "f")


def detect_value_date(text: str) -> str | None:
    patterns = [
        r"(?:date\s+de\s+valeur|cours\s+du)\s*[:\-]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{4})",
        r"(\d{4}-\d{2}-\d{2})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            raw = match.group(1)
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
                return raw
            day, month, year = re.split(r"[/-]", raw)
            return f"{year}-{int(month):02d}-{int(day):02d}"
    return None


def rows_to_observations(rows: Iterable[list[str]], value_date: str | None) -> list[FxObservation]:
    observations: list[FxObservation] = []
    for row in rows:
        if len(row) < 3:
            continue
        label = row[0].strip()
        canonical = CURRENCY_ALIASES.get(label.upper())
        if canonical is None:
            continue
        try:
            buy = normalize_decimal(row[-2])
            sell = normalize_decimal(row[-1])
        except ValueError:
            continue
        observations.append(
            FxObservation(
                value_date=value_date,
                provider_currency_label=label,
                provider_buy_rate=buy,
                provider_sell_rate=sell,
                canonical_currency_code=canonical,
                quote_convention_source="XOF_PER_1_FOREIGN_CURRENCY",
                quality_status="OBSERVED_DIRECT",
            )
        )
    return observations


def parse_bceao_fx_html(payload: bytes) -> tuple[list[FxObservation], list[str]]:
    text = payload.decode("utf-8", errors="replace")
    parser = TableTextParser()
    parser.feed(text)
    value_date = detect_value_date(" ".join(re.sub(r"<[^>]+>", " ", text).split()))
    observations = rows_to_observations(parser.rows, value_date)
    warnings: list[str] = []
    if value_date is None:
        warnings.append("VALUE_DATE_NOT_FOUND")
    expected = {"EUR", "USD"}
    found = {item.canonical_currency_code for item in observations}
    for missing in sorted(expected - found):
        warnings.append(f"EXPECTED_CURRENCY_NOT_FOUND:{missing}")
    return observations, warnings


def run(url: str, output_dir: Path) -> CollectionResult:
    payload, media_type = fetch_bytes(url)
    artifact = persist_raw_artifact(payload, url, media_type, output_dir / "raw", "bceao_fx")
    observations, warnings = parse_bceao_fx_html(payload)
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
    parser = argparse.ArgumentParser(description="Collect and parse the BCEAO FX snapshot.")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/collections/bceao_fx"))
    args = parser.parse_args()
    result = run(args.url, args.output_dir)
    print(f"{result.collector_code}: {result.run_status}; observations={len(result.observations)}")
    return 0 if result.run_status == "SUCCESS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
