# Openfunds Product Finalization — Master Design

**Date:** 2026-08-22  
**Status:** DESIGN_APPROVED_IN_CHAT_PENDING_WRITTEN_SPEC_REVIEW  
**Control branch:** `architecture/africafunds-country-indicators-v0.1`  
**PR:** #1 remains DRAFT / OPEN / UNMERGED

## 1. Goal

Bring the repository from its current governed data-model and mapping foundation to a deployable, documented production product without breaking validated history, without rewriting applied migrations, and without activating production infrastructure before a final explicit deployment gate.

The target product must cover the complete vertical chain:

```text
OFFICIAL / PRIMARY SOURCES
→ IMMUTABLE RAW ARTIFACTS
→ NORMALIZATION
→ VALIDATION / QUALITY
→ CANONICAL POSTGRESQL
→ ANALYTICAL CALCULATIONS
→ VERSIONED API
→ WEB APPLICATION
→ OBSERVABILITY / OPERATIONS
→ GOVERNED DEPLOYMENT
```

## 2. Non-negotiable constraints

1. Work only on `architecture/africafunds-country-indicators-v0.1` unless a later explicit governance decision changes this.
2. Do not mutate `main` directly.
3. PR #1 stays Draft/Open/Unmerged until a separate explicit integration gate.
4. No new branch or PR is created without explicit authorization.
5. Every database evolution is forward-only and registered in `migrations/manifest.json`.
6. Historical migrations are immutable after application; repair means a new migration or an explicit audited repair.
7. TDD contract before implementation for every new schema, mapping, API behavior, collector, analytical calculation, and UI flow.
8. `IMPLEMENTED != REMOTELY_GREEN`; remote CI is claimed only from observable workflow evidence.
9. `NULL != 0`; missing dates, currencies, values, benchmarks, holdings, NAVs or statuses are never synthesized.
10. Source observations remain distinct from calculated observations.
11. Openfunds remains the governed exchange/mapping layer; it does not become the physical runtime schema.
12. Vendor-sensitive identifiers remain import/export gated until explicit usage/licensing review is cleared.
13. API/UI never write directly into canonical truth without a governed service boundary.
14. Production deployment, persistent database activation, DNS/subdomain work, TLS and data loading require the final deployment gate.

## 3. Current starting point

At the time this design is written, the repository has already advanced beyond several living documents. The active implementation includes the canonical Fund/SubFund/ShareClass foundation, listing, valuation-time, multicurrency, lifecycle, investment status, ETF/passive/replication, benchmark components, tracked-index structures and mapping batches through the denomination-base work.

The first implementation task after written-spec approval is therefore not a new feature. It is a **state reconciliation task** that makes machine manifests, CI, `STATUS.md`, `NEXT_ACTION.md`, `SUIVI.md`, `TODO.md`, `CHANGELOG.md`, `WORK_LOG.md`, `HANDOFF.md` and the PR body agree with the actual branch HEAD.

## 4. Product decomposition

The finalization is split into eight independently reviewable sub-projects. Each sub-project gets its own detailed implementation plan before code execution.

### A. Canonical Openfunds foundation completion

Purpose: finish the canonical data surface required by the product and define explicit deferment for non-product Openfunds fields.

Required families:

- identity, legal names, aliases and language semantics;
- Fund/SubFund/ShareClass legal structure and umbrella relations;
- lifecycle, investment/dealing status and dates;
- currencies, listings and vendor identifiers;
- benchmark, tracked index and replication;
- fees, dealing terms and eligibility;
- regulatory and disclosure documents;
- distribution/dividend events;
- NAV, AUM and price observation semantics;
- holdings/portfolio disclosure semantics;
- classifications required by taxonomy and peer-group analytics.

Completion does **not** require blindly creating physical fields for all 1,869 Openfunds records. Every official field receives one of the governed outcomes:

```text
MAPPED_CANONICAL
MAPPED_DERIVED
NO_CANONICAL_EQUIVALENT
DEFERRED_NOT_REQUIRED_FOR_PRODUCT
GATED_VENDOR_OR_LICENSE
TO_CONFIRM
```

No fake materialized `UNMAPPED` rows are created simply to inflate coverage.

Exit gate:

- all product-required Openfunds families are mapped and tested;
- unmapped/deferred official IDs are machine-counted and reason-classified;
- migration runner, dictionary validator and mapping validator cover the complete implemented surface;
- no migration or mapping has an unexplained semantic ambiguity.

### B. Durable ingestion and raw-data runtime

Purpose: turn the source model into a reproducible ingestion platform.

Runtime boundaries:

```text
source.organization
→ source.organization_scope_role
→ source.endpoint
→ source.provider_series
→ source.collection_specification
→ source.collection_run
→ source.raw_artifact
→ source.extraction_record
→ canonical observation / entity relation
→ validation decision
```

Raw artifacts are immutable and addressed by SHA-256. The storage interface is S3-compatible so local development and production can use the same contract. Production credentials are environment-only and never committed.

Collectors must be idempotent, retry-safe, source-lineaged and capable of distinguishing collection date, source publication date and business/value date.

Exit gate:

- persistent PostgreSQL configuration contract exists;
- S3-compatible immutable object-store adapter exists;
- collection runs and raw artifacts are replayable;
- duplicate files resolve by content hash rather than filename;
- restore procedure is tested on a non-production environment.

### C. Historical data and analytical engine

Purpose: load governed histories and produce calculations without contaminating source truth.

Initial historical priorities:

- BCEAO/BEAC FX histories;
- African fund NAV/AUM histories where primary or governed source evidence exists;
- distributions/dividends and corporate/fund lifecycle events;
- holdings disclosures where available.

Analytical calculations live separately from observations and include:

- native/EUR/USD conversions with explicit FX lineage;
- return series and cumulative performance;
- volatility and downside volatility;
- drawdown;
- Sharpe and Sortino;
- VaR where data sufficiency criteria are satisfied;
- benchmark-relative return, alpha/beta/R² where applicable;
- peer/category aggregation;
- RFR/MAR handling;
- WTI / WTI Bench only after methodology approval.

Every metric has input sufficiency, frequency, lookback, null policy and methodology tests.

Exit gate:

- calculations are deterministic and reproducible from canonical observations;
- calculated observations never masquerade as source observations;
- methodology metadata is queryable;
- historical gaps are classified, not filled by silent interpolation.

### D. Versioned production API

Purpose: expose the product through a stable service boundary.

Recommended implementation stack for review:

- Python 3.12;
- FastAPI;
- Pydantic models generated/maintained as API contracts;
- PostgreSQL driver with explicit transaction management;
- OpenAPI as a build artifact;
- structured JSON logs.

Repository boundary:

```text
src/openfunds/        reusable domain/query/application services
apps/api/             HTTP transport, dependencies, auth, routers
```

Initial resources:

- health/readiness/version;
- countries/regions/market zones;
- organizations and source lineage;
- funds/subfunds/share classes;
- listings and identifiers;
- NAV/AUM/history;
- distributions and holdings;
- benchmark/tracked index;
- performance/risk analytics;
- taxonomy/categories/peer groups;
- quality/provenance metadata.

API writes, if introduced later, go through governed commands and never arbitrary table mutation.

Exit gate:

- OpenAPI contract is versioned and tested;
- pagination/filter/sort semantics are stable;
- authorization boundaries are tested;
- health/readiness distinguish process health from DB/object-store dependencies;
- integration tests run against PostgreSQL 16.

### E. Web product

Purpose: provide the user-facing AfricaFunds/Openfunds research application.

Recommended implementation stack for review:

- React;
- TypeScript;
- Vite;
- generated/typed API client from OpenAPI;
- component boundaries designed around domain views rather than direct SQL/data assumptions.

Primary journeys:

- global search;
- fund and share-class detail;
- management-company/institution pages;
- screener and filters;
- comparison;
- performance/risk charts;
- benchmark/index view;
- holdings/distributions;
- categories/peer groups;
- source quality and provenance disclosure where useful.

The browser performs presentation calculations only; financial methodology remains server-side.

Exit gate:

- no duplicated financial formula in the browser;
- all screens use typed API contracts;
- responsive accessibility baseline is tested;
- empty/missing data states are explicit rather than rendered as zero.

### F. Security, reliability and CI

Purpose: make every layer safe to operate.

Required controls:

- Python unit/integration tests;
- PostgreSQL migration replay on empty and initialized databases;
- mapping and dictionary validation;
- API contract tests;
- frontend unit/component tests;
- typechecking and linting;
- dependency/security scanning;
- secrets only through environment/secret stores;
- structured logging and correlation IDs;
- request limits and safe timeout defaults;
- metrics for collection runs, API errors, DB connectivity and job failures;
- backup/restore verification.

No test may freeze a historical global count when the intended invariant is append-only extensibility.

### G. Production packaging and deployment readiness

Purpose: make the application deployable without performing the final deployment yet.

Recommended packaging:

```text
Docker image: api
Docker image: web
PostgreSQL 16
S3-compatible object store
reverse proxy / TLS termination
migration job
scheduled collectors / workers
```

Configuration is environment-driven. Domain/subdomain names are not hard-coded into application logic.

Exit gate before any real deployment:

- clean build from repository HEAD;
- all required CI gates observable and green;
- migration plan reviewed;
- database backup/restore procedure tested;
- object-store persistence verified;
- health/readiness endpoints pass;
- rollback procedure documented;
- secrets inventory prepared outside Git;
- explicit human authorization to deploy.

### H. Documentation and operational closure

Documentation is continuous, not a final cleanup phase.

Each accepted implementation unit updates the relevant living documents. At minimum the final repository must contain current versions of:

- `README.md` / `00_START_HERE.md`;
- `ARCHITECTURE.md`;
- `SOURCE_OF_TRUTH.md`;
- `STATUS.md`;
- `NEXT_ACTION.md`;
- `TODO.md`;
- `SUIVI.md`;
- `DECISIONS.md` / ADRs;
- `CHANGELOG.md`;
- `WORK_LOG.md`;
- `HANDOFF.md`;
- data model documentation;
- source/collector runbook;
- API/OpenAPI documentation;
- deployment runbook;
- backup/restore runbook;
- incident/rollback runbook.

Documentation distinguishes historical statements from current state rather than deleting history.

## 5. Repository target structure

The existing repository remains authoritative. New application code is added without moving historical assets unless a separately approved refactor is justified.

Target additions:

```text
src/openfunds/
  domain/
  application/
  repositories/
  analytics/
  ingestion/
  quality/

apps/api/
  app/
  tests/

apps/web/
  src/
  tests/

ops/
  docker/
  migrations/
  runbooks/

schemas/
data/
scripts/
tests/
docs/
```

This structure prevents the API, collectors and UI from each reimplementing domain logic.

## 6. Dependency order

```text
A0 State reconciliation
→ A Canonical completion
→ B Durable ingestion runtime
→ C Historical/analytics core
→ D API
→ E Web
→ F Cross-layer hardening
→ G Deployment readiness
→ FINAL HUMAN DEPLOYMENT GATE
→ production server + subdomain
```

Subsets of B and C may proceed in parallel only when they do not change the same canonical contracts.

## 7. Error and quality strategy

All errors are classified into deterministic categories such as validation failure, unsupported source semantics, transient source failure, persistence failure, dependency failure and authorization failure.

Source errors never mutate prior validated records. Recollection creates a new run. Corrections create a new version. Failed analytical calculations produce explicit failure/insufficient-data status rather than zero or fabricated values.

## 8. Testing strategy

Every task follows:

```text
RED CONTRACT
→ MINIMAL IMPLEMENTATION
→ LOCAL/CI TEST WIRING
→ DIFF REVIEW
→ DOCUMENTATION
→ CHECKPOINT
```

Database tests exercise PostgreSQL 16. Mapping tests verify official checksum-locked Openfunds v2.13.0 semantics. API tests verify both payload and failure contracts. Frontend tests verify user-visible states including null/empty/error/loading cases.

## 9. Completion definition

The project is not “finished” because files exist. Final completion requires all of the following:

- required product canonical fields and relationships implemented;
- official Openfunds mapping coverage reason-classified for all records;
- persistent DB/object-store contracts implemented and tested;
- selected source histories loaded through reproducible collectors;
- analytics reproducible and methodology-documented;
- API implemented and contract-tested;
- web application implemented against typed API contracts;
- CI/security/observability/backup gates green;
- current documentation reconciled;
- deployment package reproducible;
- final deployment explicitly authorized and verified on the target server/subdomain.

## 10. First execution sub-project

The first sub-project after this written design is approved is **Canonical Foundation Completion and State Reconciliation**. Its dedicated specification is:

`docs/superpowers/specs/2026-08-22-openfunds-canonical-foundation-completion-design.md`

No new application/API/UI subsystem should be implemented before that sub-project reaches its exit gate.