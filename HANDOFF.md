# Handoff Loop Engineering

```text
LOOP_ID: OF-LOOP-DATA-001
TASK_ID: OF-DATA-001
STATUS: VERIFIED_COMPLETE
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
START_HEAD: e79c735b2cda8cc40a237b7deb3e379cc42bf1d9
VALIDATED_TECHNICAL_HEAD: 8ab1e75b2fd94566f9c0538ca33460140787c6bf
```

## Canonical model

```text
STANDALONE FUND -> SHARE_CLASS
UMBRELLA FUND -> SUBFUND -> SHARE_CLASS
```

Stable identity, versioned state/profile, names, identifiers, structural edges
and events are separate. Standalone funds never require a synthetic subfund.

## Entry points

- `docs/01_ARCHITECTURE/ADR-030_FUND_SUBFUND_SHARECLASS_CANONICAL_MODEL.md` ;
- `docs/02_DOMAIN_MODEL/FUND_SUBFUND_SHARECLASS_MODEL_V1.md` ;
- `schemas/fund/015_fund_subfund_shareclass_core.sql` ;
- `tests/test_fund_domain_model.py` ;
- `tests/sql/fund_domain_model_assert.sql` ;
- `docs/00_PROJECT/OF_DATA_001_COMPLETION_20260805.md`.

## Verified evidence

Migration SHA-256:
`5ce14ea3de866c31c0452fccfe77827873dec976be3391b2d323e7daf88ef15d`.

Four workflows succeeded, including PostgreSQL 16, double application, ledger,
country fixtures and adoption without ledger.

## Restart point

Do not infer that `OF-DATA-002` has started. Resolve the current HEAD, read the
completion record and request explicit authorization before selecting the master
format of the canonical dictionary.
