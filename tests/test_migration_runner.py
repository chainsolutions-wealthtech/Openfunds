from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

RUNNER_PATH = Path(__file__).resolve().parents[1] / "scripts/run_migrations.py"
SPEC = importlib.util.spec_from_file_location("run_migrations", RUNNER_PATH)
assert SPEC and SPEC.loader
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


class MigrationRunnerTests(unittest.TestCase):
    def make_repo(self, migrations, excluded=None):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        (root / "migrations").mkdir()
        (root / "scripts").mkdir()
        for item in migrations:
            target = root / item["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("select 1;\n", encoding="utf-8")
        manifest = {
            "format_version": 1,
            "database": "postgresql",
            "ledger": {"schema": "openfunds_migration", "table": "schema_migration"},
            "migrations": migrations,
            "excluded_sql": excluded or [],
        }
        path = root / "migrations/manifest.json"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        return tmp, path

    def test_valid_manifest_is_loaded_and_hashed(self):
        tmp, path = self.make_repo([
            {"order": 10, "id": "MIGRATION_001", "path": "sql/001.sql"}
        ])
        self.addCleanup(tmp.cleanup)
        manifest = runner.load_manifest(path, materialize=False)
        item = manifest["migrations"][0]
        self.assertEqual(len(item["_sha256"]), 64)
        self.assertTrue(Path(item["_absolute_path"]).is_file())

    def test_duplicate_order_fails(self):
        tmp, path = self.make_repo([
            {"order": 10, "id": "MIGRATION_001", "path": "sql/001.sql"},
            {"order": 10, "id": "MIGRATION_002", "path": "sql/002.sql"},
        ])
        self.addCleanup(tmp.cleanup)
        with self.assertRaises(runner.MigrationError):
            runner.load_manifest(path, materialize=False)

    def test_path_traversal_fails(self):
        tmp, path = self.make_repo([
            {"order": 10, "id": "MIGRATION_001", "path": "../escape.sql"}
        ])
        self.addCleanup(tmp.cleanup)
        with self.assertRaises(runner.MigrationError):
            runner.load_manifest(path, materialize=False)

    def test_excluded_path_cannot_be_migrated(self):
        migration = {"order": 10, "id": "MIGRATION_001", "path": "sql/001.sql"}
        tmp, path = self.make_repo(
            [migration],
            excluded=[{"path": "sql/001.sql", "reason": "proposal"}],
        )
        self.addCleanup(tmp.cleanup)
        with self.assertRaises(runner.MigrationError):
            runner.load_manifest(path, materialize=False)

    def test_transaction_or_psql_meta_command_fails(self):
        tmp, path = self.make_repo([
            {"order": 10, "id": "MIGRATION_001", "path": "sql/001.sql"}
        ])
        self.addCleanup(tmp.cleanup)
        sql = Path(tmp.name) / "sql/001.sql"
        sql.write_text("begin;\nselect 1;\ncommit;\n", encoding="utf-8")
        with self.assertRaises(runner.MigrationError):
            runner.load_manifest(path, materialize=False)

    def test_checksum_drift_fails(self):
        tmp, path = self.make_repo([
            {"order": 10, "id": "MIGRATION_001", "path": "sql/001.sql"}
        ])
        self.addCleanup(tmp.cleanup)
        manifest = runner.load_manifest(path, materialize=False)
        ledger = {
            "MIGRATION_001": {
                "order": "10",
                "path": "sql/001.sql",
                "sha256": "0" * 64,
            }
        }
        with self.assertRaises(runner.MigrationError):
            runner.validate_ledger(manifest, ledger)

    def test_transaction_records_migration_atomically(self):
        tmp, path = self.make_repo([
            {"order": 10, "id": "MIGRATION_001", "path": "sql/001.sql"}
        ])
        self.addCleanup(tmp.cleanup)
        manifest = runner.load_manifest(path, materialize=False)
        item = manifest["migrations"][0]
        sql = runner.build_transaction_sql(manifest, item, "select 1;\n")
        self.assertTrue(sql.startswith("begin;"))
        self.assertIn("insert into openfunds_migration.schema_migration", sql)
        self.assertTrue(sql.rstrip().endswith("commit;"))


if __name__ == "__main__":
    unittest.main()
