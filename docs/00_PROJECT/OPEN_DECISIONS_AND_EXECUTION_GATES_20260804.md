# Open decisions and execution gates — 2026-08-04

## 1. Preserved execution order

```text
OF-ARCH-001
→ OF-SOURCE-001
→ OF-ARCH-002
→ OF-ARCH-003
→ OF-ARCH-004
```

No proposed topic in this audit silently changes that order.

## 2. Existing critical decisions

### Gate G1 — ADR-021 / OF-ARCH-001

Choose one governed authoring representation for small references and define generated/controlled derivatives.

Exit criteria:

- master representation declared;
- CSV/SQL divergence blocked by an automated control;
- BCEAO/BEAC statuses reconciled;
- review and release method documented.

### Gate G2 — OF-SOURCE-001

Synchronize BCEAO/BEAC organizations, roles, endpoints, mappings, provider series and specifications without changing existing identities or observations.

### Gate G3 — OF-ARCH-002

Unify `source.endpoint` and the proposal-only `source.source_endpoint`.

### Gate G4 — ADR-022 / OF-ARCH-003

Represent unknown business dates without fabricated dates and without confusing collection/recording timestamps.

### Gate G5 — ADR-023 / OF-ARCH-004

Select and govern a migration runner/policy. Flyway, Sqitch, dbmate, Atlas, Alembic and a minimal internal runner remain candidates; none is selected here.

Required tests:

- empty database;
- existing database;
- repeated execution;
- partial migration/recovery;
- drift between master references and generated seeds.

## 3. Further P0 gates

- Fund/SubFund/ShareClass final model.
- Machine-readable canonical dictionary.
- Centralized D00-D17 catalogue.
- Official Openfunds catalogue and license.
- Field-by-field Openfunds mapping.

## 4. Proposed topics recorded without implementation

### Local market versus national level

The requested identifier `OF-GEO-001` collides with an existing completed task named “Référentiel pays et régions”. A new identifier must be selected before issue creation. Candidate only: `OF-GEO-003` or `OF-MARKET-001`.

Decision required:

- legal country;
- local-market scope;
- regulatory scope;
- geographic region;
- category naming and API implications.

### Investment scope

`OF-SCOPE-001` has no observed collision. It remains proposed.

Decision required:

- investment geography;
- mandate and benchmark hierarchy;
- legal domicile as fallback only;
- currency and regulatory implications.

### Workbook reproducibility

`OF-EXPORT-001` has no observed collision. It remains proposed.

Gate:

- workbook generated from repository inputs;
- deterministic sheet/column/row counts;
- native/EUR/USD identifiers reproduced;
- manifest and checksum verified;
- no manual workbook correction becomes canonical.

### Documentation state alignment

`OF-DOC-002` has no observed collision. It remains proposed. This baseline commit documents the discrepancy but does not close all future documentation-governance work.

## 5. Pull-request gates

Before any later integration to `main`:

- PR #1 remains open and draft until independent review;
- all deterministic tests green;
- current changed-file count reviewed;
- branch-triggered workflows reviewed for default-branch operation;
- no P0 proposal silently treated as accepted;
- no production/history claim introduced;
- exact head SHA checked immediately before merge;
- merge policy explicitly selected.

## 6. PR #2 gate

Do not close PR #2 until its three unique detailed Markdown documents are preserved or deliberately rejected with rationale. The two CSVs are already preserved exactly in `research_queue`.
