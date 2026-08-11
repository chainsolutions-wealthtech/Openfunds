from __future__ import annotations

import importlib.util
import re
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "scripts/country_indicator_catalog.py"
AUTHORING = ROOT / "data/indicator_catalog/v1"

EXPECTED_DOMAIN_COUNTS = {
    "D00": 15,
    "D01": 20,
    "D02": 16,
    "D03": 24,
    "D04": 14,
    "D05": 26,
    "D06": 24,
    "D07": 23,
    "D08": 28,
    "D09": 29,
    "D10": 45,
    "D11": 24,
    "D12": 48,
    "D13": 12,
    "D14": 9,
    "D15": 16,
    "D16": 17,
    "D17": 30,
}
ALLOWED_CANONICAL_NATURES = {"RAW", "METADATA", "EVENT", "CALCULATED"}
GOVERNED_ONLY_FIELDS = {
    "canonical_nature",
    "canonical_nature_status",
    "canonical_nature_provenance",
    "schema_version",
}


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def mirror_projection(item: dict):
    return {key: value for key, value in item.items() if key not in GOVERNED_ONLY_FIELDS}


class CountryIndicatorCatalogLegacyContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not CORE.is_file():
            raise AssertionError(
                "TDD RED: scripts/country_indicator_catalog.py does not exist yet"
            )
        cls.core = load_module(CORE, "country_indicator_catalog")
        cls.catalog = cls.core.parse_legacy_catalog(ROOT)
        cls.items = cls.catalog["indicators"]
        cls.package = cls.core.load_authoring_package(AUTHORING)

    def test_legacy_source_allowlist_is_exact(self):
        expected = {
            "docs/04_DATA_GOVERNANCE/indicator_catalog/D00_gouvernance_et_traçabilite.md",
            "docs/04_DATA_GOVERNANCE/indicator_catalog/Indicators_D01_D03_Identity_Demography_Economy.md",
            "docs/04_DATA_GOVERNANCE/indicator_catalog/Indicators_D04_D06_Prices_Fiscal_Debt.md",
            "docs/04_DATA_GOVERNANCE/indicator_catalog/Indicators_D07_D09_Monetary_Banking_External.md",
            "docs/04_DATA_GOVERNANCE/indicator_catalog/Indicators_D10_D11_Government_Securities_Equities.md",
            "docs/04_DATA_GOVERNANCE/indicator_catalog/Indicators_D12_D14_Funds_Institutionals_Real_Estate.md",
            "docs/04_DATA_GOVERNANCE/indicator_catalog/Indicators_D15_D17_Sectors_Risk_Analytics.md",
        }
        self.assertEqual(expected, set(self.core.LEGACY_FILES))

    def test_catalog_has_exact_domain_and_indicator_counts(self):
        counts = Counter(item["domain_code"] for item in self.items)
        self.assertEqual(EXPECTED_DOMAIN_COUNTS, dict(sorted(counts.items())))
        self.assertEqual(18, len(counts))
        self.assertEqual(420, len(self.items))

    def test_codes_are_canonical_and_unique(self):
        codes = [item["indicator_code"] for item in self.items]
        self.assertEqual(len(codes), len(set(codes)))
        self.assertTrue(all(re.fullmatch(r"D\d{2}\.[A-Z0-9_]+", code) for code in codes))
        self.assertTrue(all(code.startswith(item["domain_code"] + ".") for code, item in zip(codes, self.items)))

    def test_mirror_first_preserves_absence_instead_of_inventing(self):
        by_code = {item["indicator_code"]: item for item in self.items}
        d00 = by_code["D00.SOURCE_ID"]
        self.assertEqual("Brute", d00["source_nature"])
        self.assertIsNotNone(d00["definition_fr"])
        d01 = by_code["D01.OFFICIAL_NAME"]
        self.assertIsNone(d01["source_nature"])
        self.assertIsNone(d01["definition_fr"])
        self.assertEqual("NOT_AUTHORED", d01["definition_fr_status"])
        self.assertIsNone(d01["label_en"])
        self.assertEqual("NOT_AUTHORED", d01["label_en_status"])

    def test_history_is_target_not_loaded_history_claim(self):
        for item in self.items:
            self.assertIn("target_history", item)
            self.assertEqual("NOT_ASSERTED_BY_DEFINITION_CATALOGUE", item["history_status"])

    def test_provenance_is_attached_to_every_definition(self):
        for item in self.items:
            self.assertTrue(item["source_file"].startswith("docs/04_DATA_GOVERNANCE/indicator_catalog/"))
            self.assertRegex(item["source_sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual(item["indicator_code"], item["source_row_key"])

    def test_machine_readable_authoring_package_preserves_legacy_mirror(self):
        self.assertEqual("MACHINE_READABLE_JSON_PACKAGE", self.package["authoring_authority"])
        self.assertEqual("MIRROR_FIRST", self.package["policy"]["strategy"])
        self.assertEqual(18, len(self.package["domains"]))
        self.assertEqual(420, len(self.package["indicators"]))
        legacy = {item["indicator_code"]: mirror_projection(item) for item in self.items}
        authored = {
            item["indicator_code"]: mirror_projection(item)
            for item in self.package["indicators"]
        }
        self.assertEqual(legacy, authored)

    def test_authoring_package_is_partitioned_by_domain(self):
        expected = {"00_metadata.json"} | {f"{code}.json" for code in EXPECTED_DOMAIN_COUNTS}
        self.assertEqual(expected, {path.name for path in AUTHORING.glob("*.json")})

    def test_every_definition_has_governed_canonical_nature(self):
        self.assertEqual("OF-DATA-003-A", self.package["classification_policy"]["decision_id"])
        self.assertEqual(
            ALLOWED_CANONICAL_NATURES,
            set(self.package["classification_policy"]["allowed_values"]),
        )
        for item in self.package["indicators"]:
            self.assertIn(item["canonical_nature"], ALLOWED_CANONICAL_NATURES)
            self.assertEqual("GOVERNED_CLASSIFICATION", item["canonical_nature_status"])
            provenance = item["canonical_nature_provenance"]
            self.assertEqual("OF-DATA-003-A", provenance["decision_id"])
            self.assertIn(provenance["rule"], {
                "DOMAIN_METADATA",
                "EXPLICIT_METADATA_CODE",
                "EXPLICIT_EVENT_CODE",
                "DOMAIN_CALCULATED",
                "DEFAULT_OBSERVED_RAW",
            })
            self.assertEqual("1.0.0", item["schema_version"])

    def test_canonical_nature_examples_are_semantically_separated_from_source(self):
        by_code = {item["indicator_code"]: item for item in self.package["indicators"]}
        expected = {
            "D00.SOURCE_HASH": "METADATA",
            "D01.ISO3": "METADATA",
            "D04.CPI_YOY": "RAW",
            "D07.MPC_DECISION": "EVENT",
            "D10.SECURITY_ISIN": "METADATA",
            "D10.YTM": "RAW",
            "D11.EQUITY_ISIN": "METADATA",
            "D11.CLOSE": "RAW",
            "D12.FUND_CANONICAL_ID": "METADATA",
            "D12.NAV": "RAW",
            "D12.FUND_EVENT": "EVENT",
            "D16.ELECTION": "EVENT",
            "D17.SHARPE": "CALCULATED",
        }
        for code, nature in expected.items():
            self.assertEqual(nature, by_code[code]["canonical_nature"], code)
        self.assertEqual("Brute", by_code["D00.SOURCE_HASH"]["source_nature"])
        self.assertEqual("METADATA", by_code["D00.SOURCE_HASH"]["canonical_nature"])


if __name__ == "__main__":
    unittest.main()
