# OF-ARCH-004 completion record

```text
DATE: 2026-08-05
STATUS: IMPLEMENTED_AND_TESTED_PENDING_CI_RESULT
TASK: OF-ARCH-004
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
EMPTY_DATABASE_TEST: YES
EXISTING_DATABASE_ADOPTION_TEST: YES
IDEMPOTENT_SECOND_RUN: YES
CHECKSUM_DRIFT_BLOCKED: YES
UNKNOWN_LEDGER_ENTRY_BLOCKED: YES
REPAIR_PROCEDURE: YES
PROPOSALS_EXCLUDED: YES
DESTRUCTIVE_DATA_OPERATION: NO
PRODUCTION_DEPLOYMENT: NO
```

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
OF-ARCH-004: COMPLETE AFTER GREEN GOVERNED-MIGRATION CI
```

The next functional gate is `OF-DATA-001`; it is not started by this record.
