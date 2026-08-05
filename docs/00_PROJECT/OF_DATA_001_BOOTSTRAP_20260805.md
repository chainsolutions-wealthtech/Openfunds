# OF-DATA-001 bootstrap — 2026-08-05

```text
TASK: OF-DATA-001
LOOP: OF-LOOP-DATA-001
STATUS: IMPLEMENTATION_IN_PROGRESS
START_HEAD: e79c735b2cda8cc40a237b7deb3e379cc42bf1d9
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
```

## Audit before writing

- the control branch HEAD was resolved at `e79c735b...`;
- documentary baseline `59f647...` remains an ancestor;
- twelve branches and both draft PRs were read;
- no collision was found for `OF-LOOP-DATA-001` or `ADR-030`;
- `ADR-009` is accepted only in principle and requires implementation review;
- the existing taxonomy SQL is a preserved, excluded draft;
- the governed manifest ends at migration `014`;
- no runtime `schemas/fund/` directory exists at the starting HEAD.

## Design selected

```text
STANDALONE: FUND -> SHARE_CLASS
UMBRELLA:   FUND -> SUBFUND -> SHARE_CLASS
```

The model uses stable entity identity plus versioned state, profiles, names,
identifiers, structural relationships and events. A standalone vehicle does not
receive a synthetic subfund.

## Initial allowlist

- `schemas/fund/015_fund_subfund_shareclass_core.sql`;
- `migrations/manifest.json`;
- `.github/workflows/migration-runner.yml`;
- `tests/test_fund_domain_model.py`;
- `tests/sql/fund_domain_model_assert.sql`;
- `docs/01_ARCHITECTURE/ADR-030_FUND_SUBFUND_SHARECLASS_CANONICAL_MODEL.md`;
- `docs/02_DOMAIN_MODEL/FUND_SUBFUND_SHARECLASS_MODEL_V1.md`;
- project loop and handoff documents.

## Explicit exclusions

No production load, historical import, NAV, AUM, document ingestion, taxonomy
activation, service-provider mandates, API, UI, merge, retargeting, new branch or
new PR is authorized by this loop.

## Required validation

- manifest and static unit tests;
- PostgreSQL 16 empty database;
- first apply, second apply and ledger verify;
- Morocco standalone fixture;
- Tunisia umbrella/subfund fixture;
- Nigeria standalone multi-class fixture;
- duplicate identifier rejection;
- second-current-parent rejection;
- invalid direct share class under umbrella rejection;
- adoption after removing only the migration ledger.
