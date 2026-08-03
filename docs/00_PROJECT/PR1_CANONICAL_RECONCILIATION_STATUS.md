# PR1 CANONICAL RECONCILIATION STATUS

## STATUS

IN PROGRESS — NON DESTRUCTIVE

## OBJECTIVE

Reconcile the country-indicator framework from PR #1 with the accepted canonical geography, country, market-zone, currency, organization and fund-relationship model without changing the validated taxonomy, category hierarchy, reference-block roles, WTI naming or WTI Bench independence principles.

## CANONICAL SOURCES OF TRUTH

- `data/reference/AFRICA_REGIONS.csv` — canonical continent and region registry.
- `data/reference/AFRICA_COUNTRIES.csv` — canonical country registry.
- `data/reference/MARKET_ZONES.csv` — canonical common monetary and market zones.
- `data/reference/COUNTRY_RELATIONSHIPS.csv` — canonical normalised country relationships.
- `data/reference/CURRENCIES.csv` — canonical working currency registry pending external ISO/source verification.
- `data/reference/FX_PAIRS.csv` — required daily LOCAL-to-EUR and LOCAL-to-USD pair registry.
- `data/reference/ORGANIZATION_ROLES.csv` — canonical institutional role catalogue.
- `data/reference/ORGANIZATIONS.csv` — canonical organization registry.
- `data/reference/ORGANIZATION_SCOPE_ROLES.csv` — canonical organization × role × scope relationships.

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
10. No historical fact, date, source, series, organization role or observation is invented.
11. An organization is distinct from its web endpoints and may exercise several roles across several scopes.
12. Institutional roles are historized and independently validated.

## COMPLETED IN THIS RECONCILIATION PASS

- Added canonical `AFRICA_REGIONS.csv` to the PR branch.
- Added canonical `MARKET_ZONES.csv` to the PR branch.
- Added canonical `AFRICA_COUNTRIES.csv` to the PR branch.
- Added the complete 266-row `COUNTRY_RELATIONSHIPS.csv` registry.
- Added the country-relationship functional model, validation document and PostgreSQL schema.
- Added `CURRENCIES.csv` with all local currency codes used by the 54-country registry plus EUR and USD.
- Added `FX_PAIRS.csv` with the required daily LOCAL-to-EUR and LOCAL-to-USD pairs.
- Added `docs/05_CURRENCIES/DAILY_CONVERSION_RULES.md`.
- Added `ORGANIZATION_ROLES.csv` with the canonical institutional role vocabulary.
- Added `ORGANIZATIONS.csv` with the first organizations already identified by the accepted market-zone model.
- Added `ORGANIZATION_SCOPE_ROLES.csv` to separate organization identity, role and territorial scope.
- Added `schemas/reference/003_organizations_and_roles.sql`.
- Added `docs/06_SOURCES/ORGANIZATION_AND_INSTITUTIONAL_ROLE_MODEL.md`.
- Recorded the canonical/source-of-truth precedence and non-regression rules.

## IMPORTANT CURRENCY STATUS

Currency codes and required pair relationships are now structurally populated, but provider names, official source URLs, direct/triangulated route decisions, ISO metadata, effective dates and historical FX observations remain `PENDING` until verified and collected.

## IMPORTANT ORGANIZATION STATUS

The organization role vocabulary is structurally complete for the present scope. The initial organization registry only contains institutions already identified by the accepted UEMOA, CEMAC and CMA model: BCEAO, BEAC, BRVM, BVMAC, SARB, JSE, UEMOA, CEMAC and CMA.

National central banks, exchanges, regulators, statistics offices, ministries, treasuries, debt offices, depositories and other official providers for all 54 countries are not yet fully populated. Official websites, data portals, legal effective dates and role evidence remain blank or `PENDING` until source verification.

## REMAINING RECONCILIATION ACTIONS

1. Compare `african_countries_v0.1.csv` with `AFRICA_COUNTRIES.csv`; retain only non-conflicting enrichment fields.
2. Map the 420 definitions to canonical domain and indicator codes in uppercase without accents.
3. Link every country-indicator applicability record to a country or market-zone canonical code.
4. Link benchmark-plan products to category reference-block roles without replacing WTI naming.
5. Complete organizations and institutional roles for all 54 countries and common zones.
6. Create and verify `SOURCE_ENDPOINTS.csv` and collection specifications.
7. Verify currency metadata and select official FX sources and fallback routes.
8. Generate categories, subcategories and reference blocks only after canonical registries pass validation.
9. Load real historical observations and build auditable LOCAL, EUR and USD series.

## DEFINITION OF DONE

The reconciliation is complete when the PR contains one non-duplicated canonical registry for geography, countries, zones, currencies and organizations; the full D00–D17 catalogue; canonical country-indicator relationships; source and quality models; and explicit mappings from input series to market indices, WTI, WTI Bench, metrics, rankings, APIs and Atomic Design view models.
