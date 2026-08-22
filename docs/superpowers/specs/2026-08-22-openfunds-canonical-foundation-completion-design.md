# Openfunds Canonical Foundation Completion — Design

**Date:** 2026-08-22  
**Status:** PENDING_WRITTEN_SPEC_REVIEW  
**Parent design:** `docs/superpowers/specs/2026-08-22-openfunds-product-finalization-design.md`

## 1. Objective

Close the canonical and Openfunds-mapping foundation to a state that is internally consistent, testable, reason-classified and ready to support durable ingestion, analytics and an API.

This sub-project includes reconciliation of the current branch state before any further feature work.

## 2. Current observed starting state

The branch already contains forward-only migrations through migration 039 and mapping work through Batch 27 / `MAP-000093`. Several machine and living documents still reflect older milestones. Remote GitHub status visibility for recent commits has repeatedly returned no usable checks, so no recent GREEN claim may be inferred.

The first implementation unit therefore reconciles reality before extending the model.

## 3. Task A0 — State reconciliation gate

A0 must make the following surfaces agree with the actual branch HEAD:

- `migrations/manifest.json`;
- `data/openfunds/mapping/v2.13.0/mapping_manifest.json`;
- `.github/workflows/migration-runner.yml`;
- `.github/workflows/of-map-002-mapping-registry.yml`;
- `STATUS.md`;
- `NEXT_ACTION.md`;
- `CURRENT_ITERATION.md`;
- `LOOP_STATE.md`;
- `TODO.md`;
- `SUIVI.md`;
- `CHANGELOG.md`;
- `WORK_LOG.md`;
- `HANDOFF.md`;
- PR #1 body.

A0 rules:

1. Historical sections are preserved; current-state sections may supersede them explicitly.
2. No count is guessed. Counts are derived from authoritative machine packages or exact registry content.
3. Migration 039 and Batch 27 are wired into both CI surfaces before the state is called structurally closed.
4. PR #1 remains Draft/Open/Unmerged.
5. If remote checks remain unobservable, status remains `PENDING_REMOTE_CI_ATTESTATION`.

A0 exit gate:

```text
MACHINE_MANIFESTS_ALIGNED
CI_SURFACES_ALIGNED
LIVING_DOCS_ALIGNED
PR_BODY_ALIGNED
NO_HISTORICAL_REWRITE
NO_UNSUPPORTED_GREEN_CLAIM
```

## 4. Product-required canonical families

After A0, Openfunds work proceeds family-by-family rather than numerical OF-ID order.

### A1 — Identity, names and legal structure

Canonical requirements:

- official/legal/display names separated;
- language and transliteration metadata explicit where source provides it;
- alias/history retained rather than overwritten;
- umbrella/subfund/share-class relationships remain versioned;
- manufacturer, management company, investment manager and other organization roles remain distinct;
- mergers, transfers and renames represented as events/relations rather than destructive updates.

No free-text legal role may be silently collapsed onto another role because names look similar.

### A2 — Dealing, eligibility and fees

Canonical requirements:

- subscription/redemption dealing frequency;
- dealing cut-off semantics and timezone dependencies;
- minimum investment and minimum holding with explicit currency/unit context;
- subscription/redemption fees separated from ongoing/management/performance fees;
- fee rate, basis, cap/floor and applicability represented explicitly when Openfunds semantics require them;
- investor eligibility and distribution-country semantics remain distinct from fund domicile.

Unknown fee values remain null. “No fee” is represented only from an explicit source assertion.

### A3 — Regulatory and document model

Canonical requirements:

- document type;
- language;
- jurisdiction/applicability;
- publication/effective date knowledge status;
- source URL/artifact identity;
- checksum/provenance;
- document relationships to Fund/SubFund/ShareClass.

Prospectus, KID/KIID/PRIIPs, annual/semi-annual reports and other disclosures are not stored as unrelated URL columns on profile tables.

### A4 — Distribution and lifecycle cash events

Canonical requirements:

- distribution policy remains profile-level;
- actual dividend/distribution events are event/observation records;
- ex-date, record date, payment date and amount/currency semantics remain independent;
- absence of an event is not zero distribution.

### A5 — NAV, AUM and price observation semantics

Canonical requirements:

- NAV per share/unit, total net assets/AUM and market/listing prices remain distinct observation types;
- bid/offer values are never promoted to NAV without explicit source semantics;
- observation currency and quote-unit semantics are explicit;
- source date/publication date/retrieval time are distinct;
- corrections/versioning preserve prior observations;
- quality status and provenance travel with observations.

This model must support known African source patterns, including sources publishing only bid/offer or only total net assets.

### A6 — Holdings and portfolio disclosure

Canonical requirements:

- disclosure date and effective/as-of date;
- holding identifier/name;
- instrument type;
- quantity when available;
- market value and currency when available;
- portfolio weight when available;
- source artifact/cell or row provenance;
- explicit handling of aggregate/top-N disclosures versus complete portfolios.

A top-10 portfolio must never be marked as a complete holding set unless the source explicitly states completeness.

### A7 — Classification and analytics prerequisites

Canonical requirements:

- asset class/sub-asset class/category relationships;
- national/regional/Africa category scope;
- benchmark and tracked-index links;
- peer-group membership;
- risk-free-rate and MAR references;
- sufficient metadata for later WTI / WTI Bench methodology.

Classification assignments are versioned and source-lineaged.

## 5. Openfunds outcome registry

The existing mapping registry remains the authoritative list of reviewed mappings. A supplementary machine-readable outcome registry is introduced only if the current validator cannot express official IDs that are intentionally not mapped.

For every official Openfunds v2.13.0 record, one final review outcome must be derivable:

```text
MAPPED_CANONICAL
MAPPED_DERIVED
NO_CANONICAL_EQUIVALENT
DEFERRED_NOT_REQUIRED_FOR_PRODUCT
GATED_VENDOR_OR_LICENSE
TO_CONFIRM
```

Rules:

- one official ID can map to multiple canonical targets when semantics require decomposition;
- a deferred outcome must contain a reason code, not prose only;
- `TO_CONFIRM` remains a live blocker and is not counted as finished;
- parameterized `XX` templates remain templates until a separate governed expansion rule exists;
- official descriptions are referenced by checksum-locked source identity rather than copied into ad-hoc code comments as authority.

## 6. Migration design rules

Every new physical change follows the established migration ledger.

Required properties:

- monotonically increasing migration order;
- additive DDL unless a separately approved repair migration is required;
- no historical migration edit;
- no data rewrite merely to populate a new field from assumptions;
- constraints encode only semantics that are certain;
- nullable columns are preferred to invented defaults;
- repeated concepts become normalized relations rather than pipe-delimited canonical strings;
- vendor identifiers use dedicated schemes and project gates.

## 7. Dictionary rules

Every physical field introduced by a migration is represented in a governed dictionary extension with:

- stable field ID;
- canonical entity;
- physical schema/table/column;
- datatype/nullability;
- definition;
- normalization rule;
- validation constraints;
- provenance requirement;
- historical/bitemporal expectation;
- Openfunds mapping status where relevant.

Dictionary extension metadata field counts must exactly match the physical fields represented by the package.

## 8. Mapping workflow

Each mapping batch follows:

```text
1. verify official OF-ID semantics from checksum-locked v2.13.0 source
2. inspect existing canonical targets
3. create RED mapping contract
4. create migration/dictionary only if no suitable target exists
5. append reviewed mapping rows only
6. inspect exact Git diff
7. reconcile mapping manifest
8. wire dictionary and batch tests into OF-MAP-002
9. wire migrations into migration-runner when applicable
10. update living docs/checkpoint
11. re-lock PR/head and attempt remote CI observation
```

Any unexpected historical registry line modification is treated as a regression and repaired before continuation.

## 9. Testing requirements

### Unit

- migration registration/order;
- DDL invariant tests;
- dictionary metadata and field tests;
- mapping batch tests;
- validator negative tests for duplicate IDs, wrong entity targets, illegal schemes and silent inference.

### PostgreSQL integration

- apply on empty PostgreSQL 16;
- apply twice for idempotent runner behavior;
- verify ledger/checksums;
- assert new objects and constraints;
- assert historical canonical objects remain present;
- verify excluded proposal schemas/tables are not accidentally activated.

### Openfunds integration

- official PDF checksum verified;
- mapped OF-ID exists in official inventory;
- canonical target exists in core or extension dictionary;
- canonical entity matches dictionary entity;
- global counts are derived, not frozen in historical batch tests.

## 10. Documentation requirements

At every accepted family checkpoint:

- append `CHANGELOG.md`;
- update current `SUIVI.md` state;
- update `NEXT_ACTION.md`;
- reconcile `STATUS.md` when milestone state changes;
- update `TODO.md` task state;
- write a dated checkpoint under `docs/00_PROJECT/` for substantial waves;
- update PR #1 body when the externally visible project state materially changes.

No prior completion report is rewritten to match a later state.

## 11. Completion criteria for this sub-project

Canonical Foundation Completion is complete only when:

1. A0 reconciliation is closed.
2. All product-required families A1–A7 have canonical structures and tests.
3. Openfunds v2.13.0 official IDs have review outcomes sufficient to calculate complete reason-classified coverage.
4. No `TO_CONFIRM` remains in a product-required family.
5. All recent migrations are wired into the migration runner.
6. All mapping/dictionary tests are wired into OF-MAP-002.
7. Recent CI is either directly GREEN or explicitly recorded as unobservable/pending; no invented state.
8. Living documentation and PR #1 describe the same branch reality.
9. No production deployment or real-data activation has occurred.

## 12. Handoff to the next sub-project

After this sub-project passes its exit gate, the next design/plan is **Durable Ingestion and Raw-Data Runtime**, which implements persistent PostgreSQL configuration, immutable S3-compatible raw artifacts, collection-run orchestration and replay-safe ingestion.