# OF-ARCH-005 — Frozen migration 012 implementation

```text
TASK: OF-ARCH-005
LOOP: OF-LOOP-ARCH-005
ADR: ADR-029
STATUS: IMPLEMENTED_PENDING_CI
START_HEAD: d81f78942c18f4f908da8e8500f83d1280eea570
DATE: 2026-08-05
```

## Implemented

- committed frozen source snapshot `migrations/sources/012_validated_fx_reference_registry.csv`;
- committed generated SQL `schemas/reference/012_validated_fx_reference_registry.sql`;
- frozen SQL SHA-256: `fb1e82536717082092e762706f29d51dd834dd5b2f0ea1b10193665f9f48bda0`;
- manifest generator changed to explicit check-only mode;
- generator refuses rewriting `012` and creates future migration/snapshot pairs only when both paths are new;
- CI checks reproducibility without mutation and PostgreSQL idempotence;
- ADR-029 accepted and ADR-028 partially superseded.

## Local verification

```text
python compile: PASS
registry generator unit tests: 6 PASS
frozen SQL check: PASS
migration-runner test syntax: PASS
```

## Not included

- no global advisory lock for the whole migration plan;
- no exhaustive preflight for every partially initialized legacy database;
- no production deployment;
- no merge or PR retargeting;
- `OF-DATA-001` remains not started.

Final status depends on completed GitHub workflow evidence at the final HEAD.
