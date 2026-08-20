# OF-MAP-002 — Checkpoint Batches 17–20 — 2026-08-20

## Scope

This checkpoint records the forward-only Share Class lifecycle, investment-status and ETF-classification wave implemented on `architecture/africafunds-country-indicators-v0.1`.

## Governance

- PR #1 remains DRAFT / OPEN / UNMERGED.
- No `main` mutation, retarget, merge, production activation or deployment.
- Recent GitHub Actions/status results are not observable through the connected surface; implemented work must not be reported as remotely GREEN.
- Last remotely attested baselines remain migrations 001..019 (`32070768364`), canonical union 177 (`32071385088`) and mapping Batch 05 (`32071858346`).

## Migration 029 — precise lifecycle phase

Adds nullable `fund.entity_state.lifecycle_phase` without replacing broad `lifecycle_status`.

Allowed precise phases:

```text
PROJECTED
TO_BE_LAUNCHED
OFFERING_PERIOD
ACTIVE
DORMANT
IN_LIQUIDATION
TERMINATED
```

Dictionary extension: `data/dictionary/extensions/entity_lifecycle_phase_v1/` (1 field).

Batch 17 maps `OFST020545 Share Class Lifecycle` without collapsing the seven source phases.

## Migration 030 — lifecycle event types

Extends `fund.entity_event.event_type` additively with subscription-period, dormancy, liquidation-start and termination events. Existing event types remain valid.

Batch 18 maps these lifecycle dates as versionable events:

```text
OFST020558 Subscription Period Start Date
OFST020559 Subscription Period End Date
OFST020560 Share Class Launch Date
OFST020562 Dormant Start Date
OFST020563 Dormant End Date
OFST020564 Liquidation Start Date
OFST020566 Termination Date
```

Each date maps to `event_type + effective_date + effective_date_status=KNOWN`. Repeating dormancy cycles therefore remain representable.

## Migration 031 — Share Class investment status

Adds:

```text
investment_status
investment_status_description
investment_status_date
investment_status_date_status
```

Investment/dealing access remains distinct from lifecycle. Missing dates are never synthesized.

Batch 19 maps `OFST023100`, `OFST023105` and `OFST023110`.

## Migration 032 / Batch 20 — Share Class ETF flag

Official `OFST010580 Is ETF` is Share Class-level. Migration 032 adds only:

```text
fund.share_class_profile.is_etf boolean NULL
```

Dictionary extension:

```text
data/dictionary/extensions/share_class_etf_flag_v1/
FIELD_COUNT: 1
FIELD_ID: OF_FUND_SHARE_CLASS_PROFILE_IS_ETF
```

The registry reconstruction gate was closed safely using the exact Git blob rather than a truncated file view. `MAP-000073` is therefore now present:

```text
OFST010580 -> OF_FUND_SHARE_CLASS_PROFILE_IS_ETF
TRANSFORMATION: OPENFUNDS_YES_NO_TO_BOOLEAN
INFORMATION_LOSS: NONE
IMPORT_SUPPORTED: YES
EXPORT_SUPPORTED: YES
```

No Fund-level ETF inference is permitted.

## Structural state after Batch 20

```text
CURRENT_IMPLEMENTED_MIGRATION_CHAIN: 001..032
CANONICAL_CORE_FIELDS: 143
CANONICAL_EXTENSION_FIELDS: 67
CANONICAL_FIELDS_TOTAL: 210
REVIEWED_MAPPING_ROWS: 73
MAPPED_OPENFUNDS_IDS: 39
UNMAPPED_OPENFUNDS_IDS: 1830
MAPPED_CANONICAL_IDS: 36
```

OF-MAP-002 is wired through Batch20 and the 210-field union. Migration 032 is registered in the governed migration manifest. The migration-runner workflow still requires its final 031→032 count/test wiring before the 032 wave is structurally closed across all CI surfaces; remote CI attestation remains unavailable regardless.

## Non-regression invariants

- lifecycle_phase does not overwrite lifecycle_status;
- investment_status does not overwrite lifecycle_phase;
- recurring dormancy is represented through events;
- source dates are never synthesized when absent;
- ETF is Share Class-level and is never inferred at Fund level;
- historical core dictionary and listing_v1 remain unchanged;
- SEDOL and Bloomberg/RIC runtime usage gates remain unchanged;
- implemented does not mean remotely GREEN without observable CI evidence.

## Next safe work

1. wire migration 032 into `migration-runner.yml` (32 migrations + ETF model test + column assertion) without altering historical runtime assertions;
2. audit ETF/index fields from the official catalogue before creating a benchmark/index relational model;
3. keep index name, currency, identifiers and benchmark semantics normalized rather than flattening them into one text field.
