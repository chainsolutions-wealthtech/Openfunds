# Governed PostgreSQL migrations

`migrations/manifest.json` is the only operational migration order.

## Commands

```bash
python scripts/run_migrations.py --plan
DATABASE_URL=postgresql://... python scripts/run_migrations.py --apply
DATABASE_URL=postgresql://... python scripts/run_migrations.py --verify
```

The runner uses `psql`, applies each SQL file and its ledger record in one
transaction, and stores the SHA-256 in
`openfunds_migration.schema_migration`.

## Rules

1. Never modify a migration after it has been applied to a governed database.
2. Add a new forward migration for every normal correction.
3. A checksum mismatch, unknown ledger row, changed order or changed path stops
   execution.
4. SQL proposals and drafts remain in `excluded_sql`; the runner never executes
   them.
5. Generated migrations are materialized by the generator declared in the
   manifest before hashing and application.
6. `DROP`, data deletion and production deployment are not authorized merely
   because a migration is listed.

## Existing databases

A database without the migration ledger is handled by replaying the governed,
idempotent migrations and recording them only after successful execution. CI
tests this adoption path after removing only the ledger from an initialized
database.

## Repair procedure

For an ordinary defect, create a new migration.

For an exceptional manual database repair:

- stop automated application;
- record the incident, affected database and exact evidence;
- obtain explicit approval;
- apply reviewed SQL manually in a transaction;
- add a forward migration representing the repaired final state;
- reconcile the ledger only through a separately reviewed, auditable action.

The runner has no automatic checksum override or silent baseline mode.
