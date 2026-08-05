# ADR-028 — Governed PostgreSQL migration runner

```text
STATUS: ACCEPTED
DATE: 2026-08-05
TASK: OF-ARCH-004
PARTIALLY_SUPERSEDED_BY: ADR-029 for generated migration artifacts
```

## Context

The repository previously relied on workflow-specific SQL lists, leaving order, existing-database adoption, checksum drift and repair implicit. The country-indicator and Fund/SubFund/ShareClass SQL proposals remain excluded from runtime discovery.

## Decision

```text
OPERATIONAL ORDER: migrations/manifest.json
RUNNER: scripts/run_migrations.py
RUNTIME LEDGER: openfunds_migration.schema_migration
CHECKSUM: SHA-256 OF THE EXACT APPLIED FILE
FAILURE POLICY: FAIL CLOSED
```

The runner executes only manifest entries, requires stable IDs and increasing orders, applies migration and ledger row atomically, rejects path traversal/psql meta-commands/nested transactions, fails on checksum/order/path/unknown-ledger drift, and exposes plan/apply/verify without silent baseline or checksum override.

## Generated migration rule superseded by ADR-029

The original implementation materialized generated SQL before hashing. ADR-029 replaces that rule:

```text
GENERATED SQL IS COMMITTED AND FROZEN
EXACT AUTHORING INPUT IS SNAPSHOTTED AND FROZEN
MANIFEST HOOKS ARE CHECK-ONLY
FUTURE CHANGES CREATE FORWARD MIGRATIONS
```

No historical migration may be created or replaced during `plan`, `apply` or `verify`.

## Empty and existing databases

Migration `001_REFERENCE_MARKET_CORE` creates only stable prerequisites. For a database without a ledger, migrations are replayed idempotently and recorded after successful execution. CI validates a fresh PostgreSQL 16 database and an initialized database whose ledger was removed. This is not an exhaustive guarantee for every partially initialized or incompatible historical database.

## Repair policy

Normal repair is forward-only. Exceptional manual repair requires an incident record, explicit approval, transactional SQL and a later forward migration. The runner never rewrites checksums automatically.

## Residual hardening

The runner has no global advisory lock for the entire plan and no exhaustive preflight for all partial legacy states. Concurrent production execution remains unauthorized.
