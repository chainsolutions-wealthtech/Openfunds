# ADR-028 — Governed PostgreSQL migration runner

```text
STATUS: ACCEPTED
DATE: 2026-08-05
TASK: OF-ARCH-004
```

## Context

The repository previously relied on workflow-specific lists of SQL files.
That made order, adoption of an existing database, checksum drift and repair
policy implicit.

Two SQL files are still explicitly non-operational proposals:

- `schemas/reference/country_indicator_information_model_v0.1.sql`;
- `schemas/taxonomy/fund_relationship_information_model_v0.1.sql`.

They must not enter a runtime database through filename discovery.

## Decision

```text
OPERATIONAL ORDER
migrations/manifest.json

RUNNER
scripts/run_migrations.py

RUNTIME LEDGER
openfunds_migration.schema_migration

CHECKSUM
SHA-256 OF THE EXACT APPLIED FILE

FAILURE POLICY
FAIL CLOSED
```

The runner:

- executes only manifest entries;
- requires strictly increasing unique orders and stable IDs;
- materializes declared generated migrations before hashing;
- applies a migration and its ledger row in the same PostgreSQL transaction;
- refuses path traversal, psql meta-commands and nested transaction commands;
- fails on checksum, order, path or unknown-ledger drift;
- supports plan, apply and verify modes;
- has no force, silent baseline or checksum override.

## Empty and existing databases

Migration `001_REFERENCE_MARKET_CORE` creates only the stable prerequisite
objects needed by the governed reference/source/FX chain. It does not adopt the
draft Fund/SubFund/ShareClass model.

For a database without a ledger, migrations are replayed idempotently and
recorded after successful execution. CI validates both:

1. a completely empty PostgreSQL 16 database;
2. an already initialized database whose ledger has been removed.

## Proposal exclusion

The proposal containing `source.source_endpoint` remains preserved for research
history but is excluded from the operational manifest. The runtime canonical
model remains `source.endpoint`, as decided by ADR-026.

## Repair policy

Normal repair is forward-only: create a new migration.

Exceptional manual repair requires an incident record, explicit approval,
reviewed transactional SQL and a later forward migration describing the final
state. The runner never rewrites checksums automatically.

## Consequences

- one executable order;
- reproducible fresh installations;
- controlled adoption of existing databases;
- immutable applied checksums;
- explicit exclusions;
- no production deployment performed by this decision.
