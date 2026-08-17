from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "canonical"


class CanonicalTaxonomySqlGeneratorTests(unittest.TestCase):
    def test_generator_preserves_canonical_counts_and_safe_statuses(self) -> None:
        from scripts.generate_canonical_taxonomy_sql import build_sql, load_sources

        sources = load_sources(CANONICAL)
        sql = build_sql(sources)

        expected_counts = {}
        for filename, key in {
            "ASSET_CLASSES_V0_1.csv": "asset_classes",
            "ASSET_SUBCLASSES_V0_1.csv": "asset_subclasses",
            "FUND_SCOPE_ROUTING_V0_1.csv": "fund_scope_routing",
            "CATEGORY_TEMPLATE_MATRIX_V0_1.csv": "category_templates",
            "SCOPE_REFERENCE_OVERRIDES_V0_1.csv": "scope_reference_overrides",
            "ANALYTICS_REFERENCE_REQUIREMENTS_V0_1.csv": "analytics_reference_requirements",
        }.items():
            with (CANONICAL / filename).open("r", encoding="utf-8", newline="") as handle:
                expected_counts[key] = sum(1 for _ in csv.DictReader(handle, delimiter=";"))

        self.assertEqual(len(sources["asset_classes"]), expected_counts["asset_classes"])
        self.assertEqual(len(sources["asset_subclasses"]), expected_counts["asset_subclasses"])
        self.assertEqual(len(sources["fund_scope_routing"]), expected_counts["fund_scope_routing"])
        self.assertEqual(len(sources["category_templates"]), expected_counts["category_templates"])
        self.assertEqual(len(sources["scope_reference_overrides"]), expected_counts["scope_reference_overrides"])
        self.assertEqual(
            len(sources["analytics_reference_requirements"]),
            expected_counts["analytics_reference_requirements"],
        )

        manifest = json.loads((CANONICAL / "MATRIX_MANIFEST_V0_1.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["canonical_status"], "STRUCTURE_PREFILLED")
        self.assertEqual(manifest["production_status"], "NOT_ACTIVE")
        self.assertIn("STRUCTURE_PREFILLED", sql)
        self.assertIn("NOT_ACTIVE", sql)

        lowered = sql.lower()
        self.assertIn("create schema if not exists taxonomy", lowered)
        for table in (
            "taxonomy.asset_class",
            "taxonomy.asset_subclass",
            "taxonomy.fund_scope_routing",
            "taxonomy.category_template",
            "taxonomy.scope_reference_override",
            "taxonomy.analytics_reference_requirement",
            "taxonomy.taxonomy_release",
        ):
            self.assertIn(table, lowered)

        for forbidden in ("drop ", "delete ", "truncate "):
            self.assertNotIn(forbidden, lowered)

    def test_cli_check_is_byte_deterministic(self) -> None:
        from scripts.generate_canonical_taxonomy_sql import build_sql, check_output, load_sources

        expected = build_sql(load_sources(CANONICAL))
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "017.sql"
            output.write_text(expected, encoding="utf-8", newline="\n")
            check_output(output, expected)

            output.write_text(expected + "-- drift\n", encoding="utf-8", newline="\n")
            with self.assertRaisesRegex(ValueError, "does not match deterministic generation"):
                check_output(output, expected)


if __name__ == "__main__":
    unittest.main()
