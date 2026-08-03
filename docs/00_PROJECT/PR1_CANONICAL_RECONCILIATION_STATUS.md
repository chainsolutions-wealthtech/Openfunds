# PR1 CANONICAL RECONCILIATION STATUS

## STATUS

IN PROGRESS — NON DESTRUCTIVE

## OBJECTIVE

Reconcile the country-indicator framework from PR #1 with the accepted canonical geography, country, market-zone and fund-relationship model without changing the validated taxonomy, category hierarchy, reference-block roles, WTI naming or WTI Bench independence principles.

## CANONICAL SOURCES OF TRUTH

- `data/reference/AFRICA_REGIONS.csv` — canonical continent and region registry.
- `data/reference/AFRICA_COUNTRIES.csv` — canonical country registry.
- `data/reference/MARKET_ZONES.csv` — canonical common monetary and market zones.
- `data/reference/COUNTRY_RELATIONSHIPS.csv` — canonical normalised country relationships; still to be brought into this PR branch from the base branch.

The legacy `data/reference/african_countries_v0.1.csv` remains a source/proposal file and must not become a competing canonical country registry.

## PRESERVED PR1 ASSETS

- D00–D17 indicator documentation.
- 420 shared indicator, metadata, event and calculated-product definitions.
- Country-indicator relational design.
- Source roles and coverage states.
- Data-quality rules.
- Benchmark product plan.
- Collection and validation workflow.
- Tunisia pilot.
- PostgreSQL proposal.

## NON REGRESSION RULES

1. Country remains the national classification root.
2. Region and Africa remain geographic aggregation levels.
3. UEMOA and CEMAC remain common market/monetary scopes in parallel with geography.
4. Each category and subcategory retains four distinct reference roles: PRIMARY MARKET INDEX, SECONDARY MARKET INDEX, WTI and WTI BENCH.
5. `WTI - [CATEGORY OR SUBCATEGORY]` remains the canonical published naming family.
6. WTI measures observed eligible peer-fund performance.
7. WTI Bench remains an independent market or strategic-allocation benchmark.
8. Local observations are preserved and EUR/USD series are explicit daily converted observations with FX lineage.
9. Regional and Africa analytics are recalculated from converted fund-level series, not copied from local rankings.
10. No historical fact, date, source, series or observation is invented.

## COMPLETED IN THIS RECONCILIATION PASS

- Added canonical `AFRICA_REGIONS.csv` to the PR branch.
- Added canonical `MARKET_ZONES.csv` to the PR branch.
- Added canonical `AFRICA_COUNTRIES.csv` to the PR branch.
- Recorded the canonical/source-of-truth precedence rules in this document.

## REMAINING RECONCILIATION ACTIONS

1. Bring `COUNTRY_RELATIONSHIPS.csv`, its validation document and SQL relationship model into the PR branch.
2. Compare `african_countries_v0.1.csv` with `AFRICA_COUNTRIES.csv`; retain only non-conflicting enrichment fields.
3. Map the 420 definitions to canonical domain and indicator codes in uppercase without accents.
4. Link every country-indicator applicability record to a country or market-zone canonical code.
5. Link benchmark-plan products to category reference-block roles without replacing WTI naming.
6. Add currencies and explicit LOCAL/EUR/USD FX-pair rules.
7. Add organisations, source endpoints and collection specifications.
8. Generate categories, subcategories and reference blocks only after the canonical registries pass validation.

## DEFINITION OF DONE

The reconciliation is complete when the PR contains one non-duplicated canonical registry for geography/countries/zones, the full D00–D17 catalogue, canonical country-indicator relationships, source and quality models, and explicit mappings from input series to market indices, WTI, WTI Bench, metrics, rankings, APIs and Atomic Design view models.
