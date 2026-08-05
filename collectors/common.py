from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class RawArtifact:
    source_url: str
    retrieved_at: str
    media_type: str
    sha256: str
    byte_size: int
    storage_path: str


@dataclass(frozen=True)
class CollectionResult:
    collector_code: str
    run_status: str
    raw_artifact: RawArtifact
    observations: list[dict[str, Any]]
    warnings: list[str]
    errors: list[str]
    parser_version: str


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def fetch_bytes(url: str, timeout_seconds: int = 30) -> tuple[bytes, str]:
    request = Request(
        url,
        headers={
            "User-Agent": "AfricaFunds-Openfunds-Collector/0.1 (+auditable research ingestion)",
            "Accept": "text/html,application/xhtml+xml,application/json,text/plain,*/*",
        },
    )
    with urlopen(request, timeout=timeout_seconds) as response:  # nosec B310: URL is governed by source registry.
        payload = response.read()
        media_type = response.headers.get_content_type() or "application/octet-stream"
    return payload, media_type


def persist_raw_artifact(
    payload: bytes,
    source_url: str,
    media_type: str,
    output_dir: Path,
    filename_prefix: str,
) -> RawArtifact:
    output_dir.mkdir(parents=True, exist_ok=True)
    digest = sha256_hex(payload)
    extension = ".html" if "html" in media_type else ".bin"
    path = output_dir / f"{filename_prefix}_{digest[:16]}{extension}"
    if not path.exists():
        path.write_bytes(payload)
    return RawArtifact(
        source_url=source_url,
        retrieved_at=utc_now_iso(),
        media_type=media_type,
        sha256=digest,
        byte_size=len(payload),
        storage_path=str(path),
    )


def write_result_manifest(result: CollectionResult, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(asdict(result), ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
