from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migrations" / "manifest.json"
DICTIONARY_VALUES = ROOT / "data" / "dictionary" / "spec_v1" / "30_allowed_values.json"
MIGRATION = ROOT / "schemas" / "fund" / "018_extended_security_identifier_schemes.sql"

REQUIRED_SCHEMES = {"WKN", "SEDOL", "VALOR"}


class IdentifierSchemeExtensionTests(unittest.TestCase):
    def test_dictionary_exposes_required_security_identifier_schemes(self) -> None:
        values = json.loads(DICTIONARY_VALUES.read_text(encoding="utf-8"))
        schemes = set(values["entity_identifier.identifier_scheme"])
        self.assertTrue(REQUIRED_SCHEMES.issubset(schemes), REQUIRED_SCHEMES - schemes)
        self.assertIn("ISIN", schemes)
        self.assertIn("LEI", schemes)
        self.assertIn("OTHER", schemes)

    def test_migration_018_is_registered_forward_only(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        entries = [m for m in manifest["migrations"] if m["id"] == "018_EXTENDED_SECURITY_IDENTIFIER_SCHEMES"]
        self.assertEqual(1, len(entries))
        self.assertEqual(180, entries[0]["order"])
        self.assertEqual("schemas/fund/018_extended_security_identifier_schemes.sql", entries[0]["path"])

    def test_migration_018_only_widens_identifier_scheme_constraint(self) -> None:
        sql = MIGRATION.read_text(encoding="utf-8")
        lowered = sql.lower()
        self.assertIn("alter table fund.entity_identifier", lowered)
        for scheme in REQUIRED_SCHEMES:
            self.assertIn(f"'{scheme}'", sql)
        self.assertNotIn("delete from", lowered)
        self.assertNotIn("truncate", lowered)
        self.assertNotIn("drop table", lowered)
        self.assertNotIn("update fund.entity_identifier", lowered)


if __name__ == "__main__":
    unittest.main()
