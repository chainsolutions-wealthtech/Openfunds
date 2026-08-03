from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DIR = ROOT / "data" / "canonical"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


class CanonicalFundMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.asset_classes = read_csv(
            CANONICAL_DIR / "ASSET_CLASSES_V0_1.csv"
        )
        cls.asset_subclasses = read_csv(
            CANONICAL_DIR / "ASSET_SUBCLASSES_V0_1.csv"
        )
        cls.scope_routing = read_csv(
            CANONICAL_DIR / "FUND_SCOPE_ROUTING_V0_1.csv"
        )
        cls.templates = read_csv(
            CANONICAL_DIR / "CATEGORY_TEMPLATE_MATRIX_V0_1.csv"
        )
        cls.analytics = read_csv(
            CANONICAL_DIR
            / "ANALYTICS_REFERENCE_REQUIREMENTS_V0_1.csv"
        )

        cls.tempdir = tempfile.TemporaryDirectory()
        cls.output_dir = Path(cls.tempdir.name)
        result = subprocess.run(
            [
                sys.executable,
                str(
                    ROOT
                    / "scripts"
                    / "generate_fund_category_matrices.py"
                ),
                "--output-dir",
                str(cls.output_dir),
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        cls.routing = read_csv(
            cls.output_dir
            / "FUND_CATEGORY_ROUTING_MATRIX_V0_1.csv"
        )
        cls.references = read_csv(
            cls.output_dir
            / "CATEGORY_REFERENCE_MATRIX_V0_1.csv"
        )
        cls.reference_by_category = {
            row["CATEGORY_CODE"]: row
            for row in cls.references
        }

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tempdir.cleanup()

    def test_generator_check(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(
                    ROOT
                    / "scripts"
                    / "generate_fund_category_matrices.py"
                ),
                "--check",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_compact_input_counts(self) -> None:
        self.assertEqual(len(self.asset_classes), 4)
        self.assertEqual(len(self.asset_subclasses), 7)
        self.assertEqual(len(self.scope_routing), 54)
        self.assertEqual(len(self.templates), 9)
        self.assertEqual(len(self.analytics), 25)

    def test_expanded_counts(self) -> None:
        self.assertEqual(len(self.routing), 486)
        self.assertEqual(len(self.references), 432)
        self.assertEqual(
            len({row["CATEGORY_CODE"] for row in self.references}),
            432,
        )
        self.assertEqual(
            len(
                {
                    row["REFERENCE_BLOCK_CODE"]
                    for row in self.references
                }
            ),
            432,
        )

    def test_taxonomy_subclass_rules(self) -> None:
        subclass_by_class: dict[str, set[str]] = {}
        for row in self.asset_subclasses:
            subclass_by_class.setdefault(
                row["ASSET_CLASS_CODE"],
                set(),
            ).add(row["ASSET_SUBCLASS_CODE"])

        self.assertNotIn("ACTIONS", subclass_by_class)
        self.assertNotIn("MONETAIRE", subclass_by_class)
        self.assertEqual(
            subclass_by_class["OBLIGATIONS"],
            {
                "COURT_TERME",
                "MOYEN_TERME",
                "LONG_TERME",
            },
        )
        self.assertEqual(
            subclass_by_class["DIVERSIFIE"],
            {
                "PRUDENT",
                "EQUILIBRE",
                "DYNAMIQUE",
                "FLEXIBLE",
            },
        )

    def test_uemoa_and_cemac_scope_routing(self) -> None:
        routes = {
            row["LEGAL_COUNTRY_CODE"]: row
            for row in self.scope_routing
        }
        uemoa = {
            "BENIN",
            "BURKINA_FASO",
            "COTE_DIVOIRE",
            "GUINEE_BISSAU",
            "MALI",
            "NIGER",
            "SENEGAL",
            "TOGO",
        }
        cemac = {
            "REPUBLIQUE_CENTRAFRICAINE",
            "CAMEROUN",
            "REPUBLIQUE_DU_CONGO",
            "GABON",
            "GUINEE_EQUATORIALE",
            "TCHAD",
        }

        for country in uemoa:
            row = routes[country]
            self.assertEqual(
                row["LOCAL_SCOPE_TYPE"],
                "MARKET_ZONE",
            )
            self.assertEqual(row["LOCAL_SCOPE_CODE"], "UEMOA")
            self.assertEqual(
                row["REGIONAL_SCOPE_CODE"],
                "AFRICA_OUEST",
            )
            self.assertEqual(
                row["CONTINENT_SCOPE_CODE"],
                "AFRICA",
            )

        for country in cemac:
            row = routes[country]
            self.assertEqual(
                row["LOCAL_SCOPE_TYPE"],
                "MARKET_ZONE",
            )
            self.assertEqual(row["LOCAL_SCOPE_CODE"], "CEMAC")
            self.assertEqual(
                row["REGIONAL_SCOPE_CODE"],
                "AFRICA_CENTRALE",
            )
            self.assertEqual(
                row["CONTINENT_SCOPE_CODE"],
                "AFRICA",
            )

    def test_country_market_fallback(self) -> None:
        nigeria = next(
            row
            for row in self.scope_routing
            if row["LEGAL_COUNTRY_CODE"] == "NIGERIA"
        )
        self.assertEqual(
            nigeria["LOCAL_SCOPE_TYPE"],
            "COUNTRY",
        )
        self.assertEqual(
            nigeria["LOCAL_SCOPE_CODE"],
            "NIGERIA",
        )
        self.assertEqual(
            nigeria["REGIONAL_SCOPE_CODE"],
            "AFRICA_OUEST",
        )

    def test_all_routing_targets_exist(self) -> None:
        categories = set(self.reference_by_category)
        for row in self.routing:
            self.assertIn(
                row["LOCAL_CATEGORY_CODE"],
                categories,
            )
            self.assertIn(
                row["REGIONAL_CATEGORY_CODE"],
                categories,
            )
            self.assertIn(
                row["CONTINENT_CATEGORY_CODE"],
                categories,
            )

    def test_every_category_has_required_reference_roles(
        self,
    ) -> None:
        required = {
            "PEER_GROUP_CODE",
            "CATEGORY_WTI_CODE",
            "PRIMARY_BENCHMARK_CODE",
            "SECONDARY_BENCHMARK_CODE",
            "WTI_BENCH_CODE",
            "RISK_FREE_RATE_CODE",
            "MINIMUM_ACCEPTABLE_RETURN_CODE",
            "RANKING_METHOD_CODE",
            "FX_METHOD_CODE",
        }
        for row in self.references:
            for field in required:
                self.assertTrue(
                    row[field],
                    f"{row['CATEGORY_CODE']} missing {field}",
                )
            self.assertEqual(
                row["DEFAULT_REFERENCE_COUNT"],
                "2",
            )
            self.assertEqual(
                row["MAX_REFERENCE_COUNT"],
                "3",
            )

    def test_expected_action_provider_candidates(self) -> None:
        expected = {
            "UEMOA_ACTIONS": "BRVM_COMPOSITE",
            "CEMAC_ACTIONS": "BVMAC_ALL_SHARE",
            "MAROC_ACTIONS": "MASI",
            "GHANA_ACTIONS": "GSE_COMPOSITE",
            "TUNISIE_ACTIONS": "TUNINDEX",
            "NIGERIA_ACTIONS": "NGX_ALL_SHARE",
            "KENYA_ACTIONS": "NSE_ALL_SHARE",
        }
        for category, provider in expected.items():
            self.assertEqual(
                self.reference_by_category[category][
                    "PRIMARY_PROVIDER_SERIES_CANDIDATE_CODE"
                ],
                provider,
            )

    def test_reference_roles_for_key_ratios(self) -> None:
        metrics = {
            row["METRIC_CODE"]: row
            for row in self.analytics
        }
        self.assertEqual(
            metrics["PEER_RANK"]["PEER_GROUP_REQUIRED"],
            "True",
        )
        self.assertEqual(
            metrics["CATEGORY_EXCESS_RETURN"][
                "CATEGORY_WTI_REQUIRED"
            ],
            "True",
        )
        self.assertEqual(
            metrics["INFORMATION_RATIO"][
                "PRIMARY_BENCHMARK_REQUIRED"
            ],
            "True",
        )
        self.assertEqual(
            metrics["SHARPE"]["RISK_FREE_RATE_REQUIRED"],
            "True",
        )
        self.assertEqual(
            metrics["SORTINO"]["MAR_REQUIRED"],
            "True",
        )
        self.assertEqual(
            metrics["JENSEN_ALPHA"][
                "PRIMARY_BENCHMARK_REQUIRED"
            ],
            "True",
        )
        self.assertEqual(
            metrics["JENSEN_ALPHA"][
                "RISK_FREE_RATE_REQUIRED"
            ],
            "True",
        )

    def test_manifest_counts(self) -> None:
        manifest = json.loads(
            (
                self.output_dir
                / "MATRIX_MANIFEST_V0_1.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            manifest["counts"]["countries"],
            54,
        )
        self.assertEqual(
            manifest["counts"]["local_market_scopes"],
            42,
        )
        self.assertEqual(
            manifest["counts"]["regions"],
            5,
        )
        self.assertEqual(
            manifest["counts"]["category_templates"],
            9,
        )
        self.assertEqual(
            manifest["counts"]["routing_rules"],
            486,
        )
        self.assertEqual(
            manifest["counts"][
                "category_reference_blocks"
            ],
            432,
        )


if __name__ == "__main__":
    unittest.main()
