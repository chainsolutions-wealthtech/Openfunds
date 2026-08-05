# OF-ARCH-004 completion record

```text
DATE: 2026-08-05
STATUS: IMPLEMENTED_AND_TESTED
TASK: OF-ARCH-004
VALIDATED_IMPLEMENTATION_SHA: 5a6ed3da39571e331e8317e3759cd7068165c66d
GOVERNED_MIGRATION_RUN_ID: 30965690163
GOVERNED_MIGRATION_RESULT: SUCCESS
```

## Delivered

- `migrations/manifest.json`: unique operational order;
- `scripts/run_migrations.py`: plan/apply/verify runner;
- `schemas/migrations/001_reference_market_core.sql`: minimal stable bootstrap;
- `migrations/README.md`: operating and repair procedure;
- `.github/workflows/migration-runner.yml`: PostgreSQL 16 verification;
- `tests/test_migration_runner.py`: governance and drift tests;
- `docs/01_ARCHITECTURE/ADR-028_GOVERNED_MIGRATION_RUNNER.md`.

## Acceptance matrix

```text
UNIQUE_ORDER: YES
RUNTIME_LEDGER: YES
SHA256_RECORDED: YES
ATOMIC_MIGRATION_AND_LEDGER: YES
EMPTY_DATABASE_TEST: PASSED
EXISTING_DATABASE_ADOPTION_TEST: PASSED
IDEMPOTENT_SECOND_RUN: PASSED
CHECKSUM_DRIFT_BLOCKED: PASSED
UNKNOWN_LEDGER_ENTRY_BLOCKED: PASSED
REPAIR_PROCEDURE: DOCUMENTED
PROPOSALS_EXCLUDED: YES
DESTRUCTIVE_DATA_OPERATION: NO
PRODUCTION_DEPLOYMENT: NO
```

## Existing-database compatibility fixes

The CI adoption scenario identified and verified two monotonic replay fixes:

1. migration 002 no longer replaces an enriched
   `ref.current_entity_relationship` view with fewer columns;
2. migration 006 no longer reconverts `market.fx_observation.fx_rate` when it is
   already `numeric(38,18)` and referenced by the current view.

Both fixes preserve data and avoid dropping runtime views.

## Corrected OF-ARCH-002 statement

`source.source_endpoint` is present only inside
`schemas/reference/country_indicator_information_model_v0.1.sql`, a file whose
header says `Proposal only` and `not a migration`. It is preserved but excluded
from the operational manifest. No governed runtime migration creates it.

## Completed gate chain

```text
OF-ARCH-001: COMPLETE
OF-SOURCE-001: COMPLETE
OF-ARCH-002: COMPLETE
OF-ARCH-003: COMPLETE
OF-ARCH-004: COMPLETE
```

The next functional gate is `OF-DATA-001`; it was not started by this work.
