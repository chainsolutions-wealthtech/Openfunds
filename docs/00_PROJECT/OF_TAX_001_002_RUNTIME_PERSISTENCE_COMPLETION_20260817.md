# OF-TAX-001 / OF-TAX-002 — Runtime Persistence Completion Evidence

**Date:** 2026-08-17  
**Branch:** `architecture/africafunds-country-indicators-v0.1`  
**Scope:** structural taxonomy persistence only  
**Production activation:** explicitly excluded

## Verified canonical authoring state

| Authoring object | Verified rows |
|---|---:|
| Asset classes | 4 |
| Asset subclasses | 7 |
| Country/market routing | 54 |
| Category templates | 9 |
| Scope/reference overrides | 11 |
| Analytics/reference requirements | 25 |

The existing canonical matrix still expands deterministically to 486 country/category routing rules and 432 category/reference blocks.

## Implemented persistence

- deterministic generator: `scripts/generate_canonical_taxonomy_sql.py`;
- frozen immutable source snapshot: `migrations/sources/017_canonical_taxonomy_v0_1/`;
- frozen SQL migration: `schemas/taxonomy/017_canonical_fund_taxonomy_v0_1.sql`;
- governed manifest entry: `017_CANONICAL_FUND_TAXONOMY_V0_1`, order 170;
- PostgreSQL runtime schema: `taxonomy`;
- runtime release record preserving `STRUCTURE_PREFILLED` / `NOT_ACTIVE`.

## TDD evidence

### RED — generator

The Python 3.11/3.12 generator contract was committed before `scripts.generate_canonical_taxonomy_sql` existed and failed as expected.

### GREEN — generator

The same contract passed on both Python versions after the deterministic generator was implemented.

### RED — PostgreSQL

A PostgreSQL 16 contract was executed against an empty database before migration application and failed while the unit/generator paths remained green.

### GREEN — PostgreSQL

Workflow `Canonical Taxonomy Migration`, run `32058160324`:

```text
Python 3.11 generator/check/plan     SUCCESS
Python 3.12 generator/check/plan     SUCCESS
PostgreSQL 16 service                SUCCESS
apply governed migrations 001..017  SUCCESS
verify governed ledger              SUCCESS
runtime taxonomy contract            SUCCESS
second governed apply               SUCCESS
17 migrations skipped               SUCCESS
no second APPLY                     SUCCESS
second ledger verify                SUCCESS
second runtime contract             SUCCESS
```

## Runtime assertions verified

The PostgreSQL contract checks that runtime counts equal the canonical authoring inputs and that representative routes remain unchanged:

```text
BEN -> BENIN        -> MARKET_ZONE UEMOA -> BRVM  -> XOF
CIV -> COTE_DIVOIRE -> MARKET_ZONE UEMOA -> BRVM  -> XOF
CMR -> CAMEROUN     -> MARKET_ZONE CEMAC -> BVMAC -> XAF
GAB -> GABON        -> MARKET_ZONE CEMAC -> BVMAC -> XAF
NGA -> NIGERIA      -> COUNTRY NIGERIA   ->       -> NGN
MAR -> MAROC        -> COUNTRY MAROC     ->       -> MAD
```

It also verifies that every category template remains `STRUCTURE_PREFILLED`, every template remains `NOT_ACTIVE`, the runtime release digest matches the frozen V0.1 manifest, and migration 017 appears in the governed ledger at order 170.

## What this completion does not claim

This completion does **not** mean:

- a persistent production database is configured;
- fund histories are loaded;
- WTI is calculated;
- WTI Bench is validated or live;
- market benchmarks are all licensed/validated;
- risk-free rates or MAR conventions are finalized;
- Openfunds field mapping is complete;
- API/UI is implemented;
- production deployment is authorized.

## Status decision

`OF-TAX-001` structural population and governed runtime persistence are verified complete.

`OF-TAX-002` deterministic structural category generation and persistence are verified complete for V0.1. Activation and methodological validation remain intentionally separated into `OF-BENCH-*`, `OF-CALC-*`, source-validation and production tasks.
