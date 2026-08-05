from __future__ import annotations

import csv
import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/generate_validated_fx_reference_sql.py"
FROZEN = ROOT / "schemas/reference/012_validated_fx_reference_registry.sql"
SPEC = importlib.util.spec_from_file_location("fx_registry", SCRIPT)
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class Tests(unittest.TestCase):
    def test_render_is_deterministic(self):
        self.assertEqual(mod.render(), mod.render())

    def test_frozen_migration_is_reproducible(self):
        self.assertTrue(FROZEN.is_file())
        self.assertEqual(FROZEN.read_text(encoding="utf-8"), mod.render(mod.FROZEN_SOURCE))
        before = FROZEN.read_bytes()
        mod.check_frozen(mod.FROZEN_SOURCE, FROZEN)
        self.assertEqual(FROZEN.read_bytes(), before)

    def test_two_snapshot_pilots_only(self):
        rows = mod.load(ROOT / "data/reference/VALIDATED_FX_REFERENCE_REGISTRY.csv")
        self.assertEqual({row["PILOT_CODE"] for row in rows}, {"BCEAO_XOF", "BEAC_XAF"})
        sql = mod.render()
        self.assertNotIn("'PARTIAL_HISTORY_LOADED'", sql)
        self.assertNotIn("'COMPLETE_HISTORY_LOADED'", sql)
        self.assertIn("30777722357", sql)
        self.assertIn("30779605759", sql)

    def test_corrupt_evidence_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.csv"
            shutil.copy(ROOT / "data/reference/VALIDATED_FX_REFERENCE_REGISTRY.csv", path)
            with path.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle, delimiter=";"))
            fields = list(rows[0])
            rows[0]["RAW_SHA256"] = "BAD"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields, delimiter=";", lineterminator="\n")
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaises(ValueError):
                mod.load(path)

    def test_frozen_012_cannot_be_rewritten(self):
        with self.assertRaises(SystemExit):
            mod.write_new(mod.ACTIVE_SOURCE, FROZEN, mod.FROZEN_SOURCE)

    def test_new_forward_migration_is_create_only(self):
        output = FROZEN.parent / "999_test_validated_fx_reference_registry.sql"
        snapshot = mod.FROZEN_SOURCE_DIR / "999_test_validated_fx_reference_registry.csv"
        self.addCleanup(output.unlink, missing_ok=True)
        self.addCleanup(snapshot.unlink, missing_ok=True)
        output.unlink(missing_ok=True)
        snapshot.unlink(missing_ok=True)
        mod.write_new(mod.ACTIVE_SOURCE, output, snapshot)
        self.assertEqual(output.read_text(encoding="utf-8"), mod.render(snapshot))
        self.assertEqual(snapshot.read_text(encoding="utf-8"), mod.ACTIVE_SOURCE.read_text(encoding="utf-8"))
        with self.assertRaises(SystemExit):
            mod.write_new(mod.ACTIVE_SOURCE, output, snapshot)


if __name__ == "__main__":
    unittest.main()
