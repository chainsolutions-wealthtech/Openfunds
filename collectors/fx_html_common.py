from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from html import unescape
from html.parser import HTMLParser


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
    """Collect normalized text by HTML table row and cell."""

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


FRENCH_MONTHS = {
    "JANVIER": 1,
    "FEVRIER": 2,
    "FÉVRIER": 2,
    "MARS": 3,
    "AVRIL": 4,
    "MAI": 5,
    "JUIN": 6,
    "JUILLET": 7,
    "AOUT": 8,
    "AOÛT": 8,
    "SEPTEMBRE": 9,
    "OCTOBRE": 10,
    "NOVEMBRE": 11,
    "DECEMBRE": 12,
    "DÉCEMBRE": 12,
}

FRENCH_WEEKDAYS_PATTERN = r"(?:lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)"
FRENCH_MONTHS_PATTERN = "|".join(
    sorted((re.escape(month) for month in FRENCH_MONTHS), key=len, reverse=True)
)


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


def _validated_iso_date(year: int, month: int, day: int) -> str | None:
    try:
        return date(year, month, day).isoformat()
    except ValueError:
        return None


def detect_value_date(text: str) -> str | None:
    named_date_pattern = (
        rf"cours\s+des\s+devises\s+du\s+"
        rf"(?:{FRENCH_WEEKDAYS_PATTERN}\s+)?"
        rf"(\d{{1,2}})\s+({FRENCH_MONTHS_PATTERN})\s+(\d{{4}})"
    )
    named_match = re.search(named_date_pattern, text, flags=re.IGNORECASE)
    if named_match:
        day_raw, month_raw, year_raw = named_match.groups()
        month = FRENCH_MONTHS.get(month_raw.upper())
        if month is not None:
            parsed = _validated_iso_date(int(year_raw), month, int(day_raw))
            if parsed is not None:
                return parsed

    numeric_patterns = [
        r"(?:date\s+de\s+valeur|cours\s+du)\s*[:\-]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{4})",
        r"(\d{4}-\d{2}-\d{2})",
    ]
    for pattern in numeric_patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if not match:
            continue
        raw = match.group(1)
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
            year, month, day = (int(part) for part in raw.split("-"))
            return _validated_iso_date(year, month, day)
        day, month, year = (int(part) for part in re.split(r"[/-]", raw))
        return _validated_iso_date(year, month, day)
    return None


def visible_html_text(payload: bytes) -> str:
    text = payload.decode("utf-8", errors="replace")
    return " ".join(re.sub(r"<[^>]+>", " ", text).split())
