# Governed PostgreSQL migrations

`migrations/manifest.json` is the only operational migration order.

## Commands

```bash
python scripts/run_migrations.py --plan
DATABASE_URL=postgresql://... python scripts/run_migrations.py --apply
DATABASE_URL=postgresql://... python scripts/run_migrations.py --verify
```

The runner uses `psql`, applies each SQL file and its ledger record in one transaction, and stores the SHA-256 in `openfunds_migration.schema_migration`.

## Rules

1. Never modify a migration after it has been applied to a governed database.
2. Add a new forward migration for every normal correction.
3. A checksum mismatch, unknown ledger row, changed order or changed path stops execution.
4. SQL proposals and drafts remain in `excluded_sql`; the runner never executes them.
5. A generated migration is committed as an immutable SQL artifact together with a frozen copy of the exact authoring input used to generate it.
6. Manifest generator hooks are `--check`-only reproducibility checks. They must never create or replace a historical migration during `plan`, `apply` or `verify`.
7. `DROP`, data deletion and production deployment are not authorized merely because a migration is listed.

## Frozen generated migration 012

```text
migrations/sources/012_validated_fx_reference_registry.csv
→ schemas/reference/012_validated_fx_reference_registry.sql
```

Both files are committed and frozen. This command is read-only and must leave the SQL checksum unchanged:

```bash
python scripts/generate_validated_fx_reference_sql.py --check
```

A future change to `data/reference/VALIDATED_FX_REFERENCE_REGISTRY.csv` must not rewrite `012`. It creates the next free forward migration and its own frozen snapshot:

```bash
python scripts/generate_validated_fx_reference_sql.py \
  --write-new \
  --output schemas/reference/015_validated_fx_reference_registry.sql \
  --snapshot-output migrations/sources/015_validated_fx_reference_registry.csv
```

The command is create-only: it refuses `012`, existing outputs, mismatched numbers and paths outside the governed folders. Add the reviewed migration to the manifest with a check-only generator entry pointing to its frozen snapshot.

## Existing databases and concurrency

A database without the ledger is replayed idempotently and recorded only after successful execution. This does not claim exhaustive compatibility with every partially initialized historical database.

Each migration and its ledger row are atomic, but the runner has no global advisory lock for the whole plan. Concurrent production execution remains unauthorized and is a separate hardening subject.

## Repair procedure

For an ordinary defect, create a new migration. Exceptional manual repair requires an incident record, explicit approval, transactional SQL, a forward migration and an auditable ledger reconciliation. The runner has no checksum override or silent baseline mode.
