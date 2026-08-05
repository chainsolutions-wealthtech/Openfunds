from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from collectors import bceao_fx, beac_fx
from collectors.common import (
    CollectionResult,
    persist_raw_artifact,
    write_result_manifest,
)
from pipelines.fx_daily import FxSourceConfig, run_daily_fx_pipeline


FIXTURE_ROOT = Path(__file__).parent / "fixtures"


def fixture_collector(
    *,
    fixture_name: str,
    parser,
    collector_code: str,
    parser_version: str,
    filename_prefix: str,
):
    fixture_path = FIXTURE_ROOT / fixture_name

    def run(url: str, output_dir: Path) -> CollectionResult:
        payload = fixture_path.read_bytes()
        artifact = persist_raw_artifact(
            payload,
            url,
            "text/html",
            output_dir / "raw",
            filename_prefix,
        )
        observations, warnings = parser(payload)
        result = CollectionResult(
            collector_code=collector_code,
            run_status="SUCCESS",
            raw_artifact=artifact,
            observations=[asdict(item) for item in observations],
            warnings=warnings,
            errors=[],
            parser_version=parser_version,
        )
        write_result_manifest(
            result,
            output_dir / "manifests" / f"{artifact.sha256}.json",
        )
        return result

    return run


class DailyFxPipelineTests(unittest.TestCase):
    def test_builds_two_source_coverage_without_claiming_history(self) -> None:
        source_configs = (
            FxSourceConfig(
                source_code="BCEAO_XOF",
                collector_code=bceao_fx.COLLECTOR_CODE,
                collector_url="https://fixture.test/bceao",
                local_currency_code="XOF",
                loader_profile_code="BCEAO_XOF",
                collector_run=fixture_collector(
                    fixture_name="bceao_fx_sample.html",
                    parser=bceao_fx.parse_bceao_fx_html,
                    collector_code=bceao_fx.COLLECTOR_CODE,
                    parser_version=bceao_fx.PARSER_VERSION,
                    filename_prefix="bceao_fixture",
                ),
            ),
            FxSourceConfig(
                source_code="BEAC_XAF",
                collector_code=beac_fx.COLLECTOR_CODE,
                collector_url="https://fixture.test/beac",
                local_currency_code="XAF",
                loader_profile_code="BEAC_XAF",
                collector_run=fixture_collector(
                    fixture_name="beac_fx_sample.html",
                    parser=beac_fx.parse_beac_fx_html,
                    collector_code=beac_fx.COLLECTOR_CODE,
                    parser_version=beac_fx.PARSER_VERSION,
                    filename_prefix="beac_fixture",
                ),
            ),
        )

        with TemporaryDirectory() as directory:
            output_dir = Path(directory)
            result = run_daily_fx_pipeline(
                output_dir=output_dir,
                source_configs=source_configs,
                raw_retention_status="UNIT_TEST_TEMPORARY",
            )

            self.assertEqual("STAGING_ONLY", result["overall_status"])
            self.assertEqual("NO_FULL_HISTORY_CLAIM", result["history_claim"])
            self.assertFalse(result["persistent_database_configured"])
            self.assertEqual(2, result["source_count"])

            by_source = {entry["source_code"]: entry for entry in result["sources"]}
            self.assertEqual(
                ["XOF_EUR", "XOF_USD"],
                by_source["BCEAO_XOF"]["canonical_pairs"],
            )
            self.assertEqual(
                ["XAF_EUR", "XAF_USD"],
                by_source["BEAC_XAF"]["canonical_pairs"],
            )
            self.assertEqual(
                "CURRENT_SNAPSHOT_ONLY",
                by_source["BCEAO_XOF"]["history_status"],
            )
            self.assertEqual(
                "CURRENT_SNAPSHOT_ONLY",
                by_source["BEAC_XAF"]["history_status"],
            )
            self.assertEqual(
                "NOT_REQUESTED",
                by_source["BCEAO_XOF"]["database_status"],
            )
            self.assertEqual(
                "NOT_REQUESTED",
                by_source["BEAC_XAF"]["database_status"],
            )
            self.assertEqual([], by_source["BCEAO_XOF"]["warnings"])
            self.assertEqual([], by_source["BEAC_XAF"]["warnings"])

            coverage_path = output_dir / "coverage" / "daily_fx_coverage.json"
            self.assertTrue(coverage_path.exists())
            persisted = json.loads(coverage_path.read_text(encoding="utf-8"))
            self.assertEqual(result["overall_status"], persisted["overall_status"])

            for source_code in ("bceao_xof", "beac_xaf"):
                self.assertTrue((output_dir / source_code / "raw").exists())
                self.assertTrue((output_dir / source_code / "manifests").exists())
                self.assertTrue(
                    (output_dir / source_code / "staging" / "canonical_fx.json").exists()
                )

    def test_records_database_not_configured_without_false_persistence_claim(self) -> None:
        source_configs = (
            FxSourceConfig(
                source_code="BCEAO_XOF",
                collector_code=bceao_fx.COLLECTOR_CODE,
                collector_url="https://fixture.test/bceao",
                local_currency_code="XOF",
                loader_profile_code="BCEAO_XOF",
                collector_run=fixture_collector(
                    fixture_name="bceao_fx_sample.html",
                    parser=bceao_fx.parse_bceao_fx_html,
                    collector_code=bceao_fx.COLLECTOR_CODE,
                    parser_version=bceao_fx.PARSER_VERSION,
                    filename_prefix="bceao_fixture",
                ),
            ),
        )

        with TemporaryDirectory() as directory:
            result = run_daily_fx_pipeline(
                output_dir=Path(directory),
                source_configs=source_configs,
                persist_postgres=True,
                database_url=None,
            )

        self.assertEqual(
            "STAGING_ONLY_DATABASE_NOT_CONFIGURED",
            result["overall_status"],
        )
        self.assertEqual(
            "NOT_CONFIGURED",
            result["sources"][0]["database_status"],
        )
        self.assertFalse(result["persistent_database_configured"])


if __name__ == "__main__":
    unittest.main()
