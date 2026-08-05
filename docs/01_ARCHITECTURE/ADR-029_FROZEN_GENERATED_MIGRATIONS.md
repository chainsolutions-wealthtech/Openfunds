# ADR-029 — Frozen generated migration artifacts

```text
STATUS: ACCEPTED
DATE: 2026-08-05
TASK: OF-ARCH-005
LOOP: OF-LOOP-ARCH-005
SUPERSEDES: ADR-028 generated-migration materialization rule
```

## Context

Migration `012_VALIDATED_FX_REFERENCE_REGISTRY` was declared with a generator, but its SQL file was absent from Git. Every manifest load could regenerate the historical path from the changing active authoring CSV before checksum validation.

## Decision

```text
ACTIVE AUTHORING FILE
→ NEW IMMUTABLE SOURCE SNAPSHOT
→ NEW IMMUTABLE SQL MIGRATION
→ MANIFEST CHECK-ONLY REPRODUCIBILITY HOOK
→ POSTGRESQL LEDGER SHA-256
```

For `012`:

```text
migrations/sources/012_validated_fx_reference_registry.csv
→ schemas/reference/012_validated_fx_reference_registry.sql
```

Both files are committed and frozen. The manifest invokes the generator only with `--check`, an explicit frozen source and an explicit output. Loading the manifest must never create or replace historical SQL.

A future change to `data/reference/VALIDATED_FX_REFERENCE_REGISTRY.csv` creates a new numbered source snapshot and forward SQL migration; it never rewrites `012`.

## Create-only command

```bash
python scripts/generate_validated_fx_reference_sql.py \
  --write-new \
  --output schemas/reference/015_validated_fx_reference_registry.sql \
  --snapshot-output migrations/sources/015_validated_fx_reference_registry.csv
```

The command rejects `012`, existing files, paths outside the governed directories, numbers ≤ 012 and mismatched SQL/snapshot numbers.

## Consequences

Applied migration identity, path and content become immutable; reproducibility uses the exact historical input; future changes are forward migrations. Each generated migration now requires a frozen source snapshot.

## Residual risks

This closes the generated-migration immutability blocker. It does not add a global advisory lock or exhaustive preflight for every partially initialized historical database. Those remain separate hardening tasks, and concurrent production execution remains unauthorized.

## Verification

1. frozen SQL equals deterministic rendering of the frozen snapshot;
2. check mode leaves its checksum unchanged;
3. overwrite of `012` is rejected;
4. forward creation is create-only;
5. manifest load does not mutate `012`;
6. PostgreSQL 16 applies the governed plan and verifies the ledger.
