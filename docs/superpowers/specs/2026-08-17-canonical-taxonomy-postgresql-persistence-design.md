# Canonical Taxonomy PostgreSQL Persistence Design

## Objective

Persist the already-tested canonical fund taxonomy in PostgreSQL without changing its semantics, without creating a competing source of authoring, and without activating unvalidated methodologies or production calculations.

## Existing authoritative inputs

The Git-reviewed canonical authoring inputs remain:

- `data/canonical/ASSET_CLASSES_V0_1.csv`
- `data/canonical/ASSET_SUBCLASSES_V0_1.csv`
- `data/canonical/FUND_SCOPE_ROUTING_V0_1.csv`
- `data/canonical/CATEGORY_TEMPLATE_MATRIX_V0_1.csv`
- `data/canonical/SCOPE_REFERENCE_OVERRIDES_V0_1.csv`
- `data/canonical/ANALYTICS_REFERENCE_REQUIREMENTS_V0_1.csv`
- `data/canonical/MATRIX_MANIFEST_V0_1.json`

These files are authoring/review surfaces in Git. PostgreSQL becomes the runtime source of truth only after the governed migration is applied.

## Chosen architecture

A deterministic generator reads the existing canonical CSV/JSON inputs and materializes one frozen forward migration, `schemas/taxonomy/017_canonical_fund_taxonomy_v0_1.sql`. The migration is registered as order `170` in `migrations/manifest.json`, after migration 016.

The generator supports a `--check` mode analogous to the existing generated migrations. The committed SQL artifact must byte-match a fresh deterministic generation from the committed canonical inputs.

The migration is additive and idempotent. It creates the taxonomy tables only if absent, inserts/upserts the V0.1 canonical taxonomy deterministically, and does not alter Fund/SubFund/ShareClass identity data or any existing migration.

## Runtime model

The migration creates a dedicated `taxonomy` schema with focused tables for:

1. `taxonomy.asset_class`
2. `taxonomy.asset_subclass`
3. `taxonomy.fund_scope_routing`
4. `taxonomy.category_template`
5. `taxonomy.scope_reference_override`
6. `taxonomy.analytics_reference_requirement`
7. `taxonomy.taxonomy_release`

Every row carries the canonical code from the authoring source and enough status metadata to preserve the existing semantics. No candidate benchmark, risk-free rate, MAR, WTI or WTI Bench object is promoted beyond the status already present in the source files.

`taxonomy.taxonomy_release` records the V0.1 release and its source-manifest digest so runtime state can be reconciled with Git authoring inputs.

## Safety invariants

- no `DROP`, `DELETE` or `TRUNCATE`;
- no modification of migrations 001–016;
- no production activation;
- no fabricated business-validity dates;
- no replacement of `NULL` by zero;
- no reinterpretation of market-zone routing;
- UEMOA/CEMAC routing semantics remain unchanged;
- generated SQL is deterministic and checksum-governed by the migration runner;
- a second application must leave the same logical state;
- checksum drift after application remains a hard failure in the existing migration runner.

## Test strategy

TDD is mandatory.

1. Add unit tests for the generator and exact source counts before the generator exists.
2. Verify RED.
3. Implement deterministic SQL generation.
4. Generate and commit migration 017.
5. Register migration 017 in the governed manifest with a `--check` generator contract.
6. Add PostgreSQL 16 integration tests that apply the full governed migration chain twice and assert exact taxonomy counts and representative routing semantics.
7. Run Python 3.11 and 3.12 unit tests plus PostgreSQL integration CI.

Expected source counts at design time are derived from committed files, not hard-coded assumptions in documentation. The tests are the authoritative executable contract.

## Documentation and continuity

On GREEN, update:

- `TODO.md`
- `SUIVI.md`
- `CHANGELOG.md`
- `data/canonical/README.md`
- `DECISIONS.md` with a new accepted ADR recording the taxonomy authoring/runtime rule
- PR #1 body if its status statements are stale

The documentation must explicitly preserve `STRUCTURE_PREFILLED` / `NOT_ACTIVE` until benchmark methodologies and live source series are validated.

## Rejected alternatives

### Manual SQL seed

Rejected because it would duplicate taxonomy semantics and drift from the canonical CSV authoring surfaces.

### Runtime CSV loading without governed migration

Rejected because PostgreSQL is the accepted runtime source of truth and schema/data evolution is governed by the migration ledger.

### Modifying migration 015 or another existing migration

Rejected because applied migrations are checksum-immutable; changes must be forward-only.

## Acceptance criteria

The work is complete when:

- a deterministic generator exists and passes `--check`;
- migration 017 is registered at order 170;
- full migration plan loads successfully;
- PostgreSQL 16 applies the chain twice without logical drift;
- taxonomy row counts equal the committed canonical inputs;
- representative UEMOA/CEMAC and standalone-country routing assertions pass;
- no methodology is activated;
- all affected permanent project documents reflect the new state.
