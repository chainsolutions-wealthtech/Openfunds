# OF-MAP-002 checkpoint — Batches 21–26 / migrations 033–038

Date: 2026-08-21
Branch: `architecture/africafunds-country-indicators-v0.1`
PR: #1 — DRAFT / OPEN / UNMERGED

## Governance

- GitHub-first; no `main` mutation.
- No PR merge, retarget, ready-for-review transition, production activation or deployment.
- Forward-only schema evolution; historical canonical packages and mapping rows are preserved.
- TDD contracts precede production schema/mapping changes.
- `IMPLEMENTED` is not equivalent to `REMOTELY_GREEN` while recent workflow runs/statuses are not observable through the connected GitHub surface.

## Official Openfunds baseline

- Version: 2.13.0 FINAL (2026-03-23)
- Archived PDF SHA256: `40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4`
- Official field records: 1,869

## Closed implemented units

### Migration 033 / Batch 21 — Fund passive flag

- `fund.fund_profile.is_passive`
- `OFST010720` maps only to the Fund-level passive assertion.
- It does not infer Share Class ETF status.

### Migration 034 / Batch 22 — Fund replication methodology

- `fund_profile.replication_methodology_first_level`
- normalized `fund.replication_methodology_detail` rows for second-level methodology.
- Hybrid pipe-separated details are not stored as a canonical pipe string.

### Migration 035 / Batch 23 — Share Class benchmark components

- `fund.share_class_benchmark_component`
- ordered/versioned benchmark components.
- `OFST023200` decomposes into component order, source-preserved name and optional explicit weight.
- Composite benchmark pipe strings are not retained as the canonical representation.

### Migration 036 / Batch 24 — benchmark component identifiers

- `fund.benchmark_component_identifier`
- Bloomberg/RIC capable vendor-specific identifier relation.
- `OFST023205` Bloomberg tickers align by benchmark component order.
- Runtime import/export stays disabled behind `EXPLICIT_PROPRIETARY_IDENTIFIER_USAGE_REVIEW`.
- That gate is project policy and must not be falsely described as an Openfunds licensing warning.

### Migration 037 / Batch 25 — Share Class tracked index

- `fund.share_class_tracked_index`
- explicit index name, index currency semantics and index type.
- `OFST023805` blank source value means `LOCAL_CURRENCY` with `index_currency_id = NULL`.
- No Share Class currency inference is allowed.
- Index types preserve the four official meanings with reversible canonical codes.
- Batch 25 registry append was verified as exactly `MAP-000083..086` and no historical row modification.

## Current in-progress unit

### Migration 038 / Batch 26 — tracked-index vendor identifiers

Implemented structurally:

- `fund.tracked_index_identifier`
- schemes: `BLOOMBERG`, `RIC`
- versioned/source-lineaged
- one current identifier per scheme per tracked index
- no destructive upper/lower-case normalization
- Reuters/RIC case must be preserved.

Dictionary extension:

- `data/dictionary/extensions/tracked_index_identifier_v1`
- 16 physical fields

RED mapping contract exists:

- `tests/test_openfunds_mapping_batch26.py`
- `OFST023820` expected as Bloomberg tracked-index identifier
- `OFST023830` expected as RIC tracked-index identifier
- 6 mapping rows expected in total (value / scheme / normalized for each field)
- import/export must remain `NO` pending explicit proprietary-identifier usage review.

Batch 26 registry rows are NOT yet written at this checkpoint. The current registry ends at `MAP-000086`.

## Current static counts at Batch 25

```text
CANONICAL_CORE_FIELDS:       143
CANONICAL_EXTENSION_FIELDS:  135  (after migration 037)
CANONICAL_TOTAL_FIELDS:      278
REVIEWED_MAPPING_ROWS:        86
MAPPED_EXTERNAL_IDS:          47
UNMAPPED_EXTERNAL_IDS:      1822
MAPPED_CANONICAL_IDS:         49
```

Migration 038 adds a further 16 canonical physical fields once the mapping manifest is reconciled after Batch 26.

## Remote CI status

No recent run/status is claimed GREEN without direct evidence.

Last remotely attested baselines remain:

```text
MIGRATIONS 001..019: 32070768364
CANONICAL UNION 177: 32071385088
MAPPING BATCH 05:    32071858346
```

Everything newer remains implemented/static-contract and `PENDING_REMOTE_CI_ATTESTATION` until directly observed.

## Exact next safe actions

1. Append only `MAP-000087..092` for Batch 26.
2. Verify the registry commit diff contains exactly six added rows and no historical modification.
3. Reconcile mapping manifest through migration 038 / Batch 26.
4. Wire migrations 037–038 and Batches 25–26 into both governed CI workflows.
5. Re-lock PR/head/check visibility.
6. Reconcile `NEXT_ACTION.md`, `OPENFUNDS_MAPPING.md`, `SUIVI.md`, `TODO.md`, `CHANGELOG.md` and the stale PR body.
7. Continue the next official ETF/index fields only through a new RED contract; do not infer benchmark/index equivalence or currencies silently.
