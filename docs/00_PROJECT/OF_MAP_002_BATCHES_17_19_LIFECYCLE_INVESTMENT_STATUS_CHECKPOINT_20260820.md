# OF-MAP-002 — Checkpoint Batches 17–19 — 2026-08-20

## Scope

This checkpoint records the forward-only Share Class lifecycle and investment-status wave implemented on `architecture/africafunds-country-indicators-v0.1`.

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

Batch 17 maps `OFST020545 Share Class Lifecycle` to `OF_FUND_FUND_ENTITY_STATE_LIFECYCLE_PHASE` without collapsing the seven source phases.

## Migration 030 — lifecycle event types

No new physical field is introduced. `fund.entity_event.event_type` is extended additively with:

```text
SUBSCRIPTION_PERIOD_START
SUBSCRIPTION_PERIOD_END
DORMANCY_START
DORMANCY_END
LIQUIDATION_START
TERMINATION
```

Existing event types remain valid. This event model is required because Openfunds lifecycle semantics permit active/dormant cycles to repeat over time.

Batch 18 maps seven official lifecycle dates as versionable events:

```text
OFST020558 Subscription Period Start Date
OFST020559 Subscription Period End Date
OFST020560 Share Class Launch Date
OFST020562 Dormant Start Date
OFST020563 Dormant End Date
OFST020564 Liquidation Start Date
OFST020566 Termination Date
```

Each date maps to `event_type + effective_date + effective_date_status=KNOWN`, rather than being collapsed into one pair of entity-state boundaries.

## Migration 031 — Share Class investment status

Investment/dealing access is explicitly distinct from lifecycle.

Adds to `fund.share_class_profile`:

```text
investment_status
investment_status_description
investment_status_date
investment_status_date_status
```

Canonical status values:

```text
OPEN
SOFT_CLOSED
HARD_CLOSED
CLOSED_FOR_REDEMPTION
CLOSED_FOR_SUBSCRIPTION_AND_REDEMPTION
```

Date knowledge coupling prevents invented dates: `KNOWN` requires a real date; `UNKNOWN` requires NULL.

Dictionary extension: `data/dictionary/extensions/share_class_investment_status_v1/` (4 fields).

Batch 19 maps:

```text
OFST023100 Investment Status
OFST023105 Investment Status Description
OFST023110 Investment Status Date
```

## Structural state after Batch 19

```text
CURRENT_IMPLEMENTED_MIGRATION_CHAIN: 001..031
CANONICAL_CORE_FIELDS: 143
CANONICAL_EXTENSION_FIELDS: 66
CANONICAL_FIELDS_TOTAL: 209
REVIEWED_MAPPING_ROWS: 72
MAPPED_OPENFUNDS_IDS: 38
UNMAPPED_OPENFUNDS_IDS: 1831
MAPPED_CANONICAL_IDS: 35
```

The governed migration runner is wired through migration 031. OF-MAP-002 is wired through Batch 19 and the 209-field canonical union. These are implementation statements only; remote CI attestation remains unavailable through the connected status surface.

## Staged next migration 032 — Share Class ETF flag

Official `OFST010580 Is ETF` is Share Class-level. Migration 032 and its one-field dictionary extension are implemented structurally:

```text
fund.share_class_profile.is_etf boolean NULL
OF_FUND_SHARE_CLASS_PROFILE_IS_ETF
```

The Batch20 RED contract also exists. The mapping registry row is deliberately not written yet because the connector currently truncates large reads of the 72-line registry and mutation requires complete-file replacement. No blind replacement is allowed under the zero-regression rule.

## Non-regression invariants

- lifecycle_phase does not overwrite lifecycle_status;
- investment_status does not overwrite lifecycle_phase;
- recurring dormancy is represented through events, not one static start/end pair;
- source dates are never synthesized when absent;
- historical core dictionary and listing_v1 remain unchanged;
- SEDOL and Bloomberg/RIC runtime usage gates remain unchanged;
- ETF is Share Class-level and is never inferred at Fund level;
- implemented does not mean remotely GREEN without observable CI evidence.

## Next safe work

Close Batch20 only after the complete current registry can be reconstructed and re-read without truncation risk. Then audit ETF/index fields (`OFST023800+`) as a normalized index/benchmark domain; do not flatten index name, currency, Bloomberg/RIC identifiers and benchmark semantics into one text field.
