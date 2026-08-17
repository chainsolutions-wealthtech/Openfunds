# ADR-029 — Canonical Taxonomy Authoring and Runtime Persistence

- **Status:** ACCEPTED
- **Date:** 2026-08-17
- **Task:** `OF-TAX-001`, `OF-TAX-002`
- **Migration:** `017_CANONICAL_FUND_TAXONOMY_V0_1`
- **Migration order:** `170`

## Context

The repository already contained a deterministic canonical fund-taxonomy authoring layer under `data/canonical/`: four asset classes, seven subclasses, 54 country-to-market routing rows, nine category templates, 11 scope/reference overrides, 25 analytics/reference requirements and a release manifest. These inputs generate 486 routing rules and 432 category/reference blocks, but until migration 017 they were not persisted through the governed PostgreSQL migration ledger.

The project already accepts PostgreSQL as runtime source of truth and uses a checksum-governed forward-only migration runner. The migration policy requires committed frozen generated artifacts with frozen source snapshots.

## Decision

The canonical taxonomy uses the following authoring/runtime split:

```text
GIT-REVIEWED CANONICAL CSV/JSON
    = GOVERNED AUTHORING + REVIEW SURFACE

IMMUTABLE MIGRATION SOURCE SNAPSHOT
    = migrations/sources/017_canonical_taxonomy_v0_1/

DETERMINISTIC SQL GENERATOR
    = scripts/generate_canonical_taxonomy_sql.py

FROZEN GENERATED MIGRATION
    = schemas/taxonomy/017_canonical_fund_taxonomy_v0_1.sql

GOVERNED MIGRATION LEDGER
    = migrations/manifest.json / order 170

POSTGRESQL
    = RUNTIME SOURCE OF TRUTH AFTER APPLICATION
```

Future changes to taxonomy semantics must use a new versioned authoring release and a new forward migration. Migration 017 and its frozen source snapshot are immutable after application.

## Persisted runtime objects

Migration 017 creates the additive `taxonomy` schema with:

- `taxonomy.asset_class`;
- `taxonomy.asset_subclass`;
- `taxonomy.fund_scope_routing`;
- `taxonomy.category_template`;
- `taxonomy.scope_reference_override`;
- `taxonomy.analytics_reference_requirement`;
- `taxonomy.taxonomy_release`.

The migration preserves existing canonical identifiers and values. It does not reinterpret country/market-zone routing.

## Production status

Persistence is not production activation.

The V0.1 taxonomy remains:

```text
CANONICAL_STATUS = STRUCTURE_PREFILLED
PRODUCTION_STATUS = NOT_ACTIVE
```

Candidate benchmarks, WTI Bench methodologies, risk-free-rate selections, MAR conventions, provider series and live analytical products remain subject to their own validation gates.

## Safety rules

Migration 017 introduces no `DROP`, `DELETE` or `TRUNCATE`. Existing migrations 001–016 are not modified. Unknown dates are not fabricated. Missing values are not converted to zero. The generated SQL is byte-deterministic from the frozen source snapshot.

## Verification evidence

The implementation followed RED→GREEN TDD:

1. generator contract failed before the generator existed;
2. generator contract passed on Python 3.11 and 3.12;
3. migration 017 was materialized by the generator and byte-checked;
4. the exact V0.1 source inputs were frozen with SHA-256 inventory;
5. the frozen snapshot regenerated the exact committed migration;
6. the governed migration plan exposed `170 PENDING 017_CANONICAL_FUND_TAXONOMY_V0_1`;
7. PostgreSQL 16 applied the complete migration chain 001→017 from an empty database;
8. runtime row counts and representative UEMOA/CEMAC/standalone routing semantics matched the canonical inputs;
9. the ledger verified successfully;
10. a second application produced only governed skips, no new applications, and the runtime contract remained green.

Primary GREEN workflow evidence:

```text
Canonical Taxonomy Migration
run: 32058160324
Python 3.11: SUCCESS
Python 3.12: SUCCESS
PostgreSQL 16: SUCCESS
full chain 001..017: SUCCESS
second apply idempotence: SUCCESS
```

## Consequences

### Positive

- taxonomy is no longer only a CSV/review structure;
- runtime persistence is governed and reproducible;
- authoring and runtime truth are no longer conflated;
- historical migration reproducibility survives future taxonomy versions;
- country/zone routing is executable and regression-tested.

### Constraints retained

- taxonomy remains non-active for production calculations;
- live fund histories are still required for WTI and metrics;
- benchmark/RFR/MAR methodologies still require validation;
- persistent production PostgreSQL remains a separate infrastructure gate;
- the official Openfunds Field List remains a separate mapping gate.

## Rejected alternatives

- manually maintained SQL seeds competing with the canonical CSV/JSON inputs;
- runtime loading directly from mutable CSV files outside the migration ledger;
- rewriting migration 015 or any existing applied migration;
- activating templates merely because they are now persisted.
