from __future__ import annotations

import csv
import hashlib
import os
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "canonical"
FROZEN = ROOT / "migrations" / "sources" / "017_canonical_taxonomy_v0_1"
DATABASE_URL = os.getenv("DATABASE_URL")


def csv_count(filename: str) -> int:
    with (CANONICAL / filename).open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle, delimiter=";"))


def query(sql: str) -> list[str]:
    if not DATABASE_URL:
        raise unittest.SkipTest("DATABASE_URL is required")
    result = subprocess.run(
        ["psql", DATABASE_URL, "-X", "-v", "ON_ERROR_STOP=1", "-At", "-F", "\t", "-c", sql],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise AssertionError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.splitlines()


class CanonicalTaxonomyPostgresTests(unittest.TestCase):
    def test_runtime_counts_match_canonical_authoring_inputs(self) -> None:
        expected = {
            "taxonomy.asset_class": csv_count("ASSET_CLASSES_V0_1.csv"),
            "taxonomy.asset_subclass": csv_count("ASSET_SUBCLASSES_V0_1.csv"),
            "taxonomy.fund_scope_routing": csv_count("FUND_SCOPE_ROUTING_V0_1.csv"),
            "taxonomy.category_template": csv_count("CATEGORY_TEMPLATE_MATRIX_V0_1.csv"),
            "taxonomy.scope_reference_override": csv_count("SCOPE_REFERENCE_OVERRIDES_V0_1.csv"),
            "taxonomy.analytics_reference_requirement": csv_count("ANALYTICS_REFERENCE_REQUIREMENTS_V0_1.csv"),
        }
        for table, count in expected.items():
            with self.subTest(table=table):
                self.assertEqual(query(f"select count(*) from {table}")[0], str(count))

    def test_representative_market_scope_routing_is_preserved(self) -> None:
        expected = {
            "BEN": ("BENIN", "MARKET_ZONE", "UEMOA", "BRVM", "XOF"),
            "CIV": ("COTE_DIVOIRE", "MARKET_ZONE", "UEMOA", "BRVM", "XOF"),
            "CMR": ("CAMEROUN", "MARKET_ZONE", "CEMAC", "BVMAC", "XAF"),
            "GAB": ("GABON", "MARKET_ZONE", "CEMAC", "BVMAC", "XAF"),
            "NGA": ("NIGERIA", "COUNTRY", "NIGERIA", "", "NGN"),
            "MAR": ("MAROC", "COUNTRY", "MAROC", "", "MAD"),
        }
        for iso3, values in expected.items():
            rows = query(
                "select legal_country_code,local_scope_type,local_scope_code," 
                "coalesce(local_exchange_code,''),local_currency_code "
                f"from taxonomy.fund_scope_routing where legal_country_iso3='{iso3}'"
            )
            self.assertEqual(rows, ["\t".join(values)], iso3)

    def test_taxonomy_remains_structure_prefilled_and_not_active(self) -> None:
        self.assertEqual(
            query("select count(*) from taxonomy.category_template where canonical_status <> 'STRUCTURE_PREFILLED'"),
            ["0"],
        )
        self.assertEqual(
            query("select count(*) from taxonomy.category_template where production_status <> 'NOT_ACTIVE'"),
            ["0"],
        )
        self.assertEqual(
            query("select canonical_status,production_status from taxonomy.taxonomy_release where schema_version='0.1.0'"),
            ["STRUCTURE_PREFILLED\tNOT_ACTIVE"],
        )

    def test_runtime_release_points_to_frozen_manifest_digest(self) -> None:
        digest = hashlib.sha256((FROZEN / "MATRIX_MANIFEST_V0_1.json").read_bytes()).hexdigest()
        self.assertEqual(
            query("select source_manifest_sha256 from taxonomy.taxonomy_release where schema_version='0.1.0'"),
            [digest],
        )

    def test_governed_migration_017_is_in_ledger(self) -> None:
        self.assertEqual(
            query(
                "select migration_order::text || ':' || migration_id "
                "from openfunds_migration.schema_migration "
                "where migration_id='017_CANONICAL_FUND_TAXONOMY_V0_1'"
            ),
            ["170:017_CANONICAL_FUND_TAXONOMY_V0_1"],
        )


if __name__ == "__main__":
    unittest.main()
