from __future__ import annotations

import importlib.util
import re
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "scripts/country_indicator_catalog.py"

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


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


if __name__ == "__main__":
    unittest.main()
