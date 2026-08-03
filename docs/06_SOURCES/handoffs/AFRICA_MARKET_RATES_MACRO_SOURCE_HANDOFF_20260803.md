# Africa Market, Rates and Macro Source Handoff — 2026-08-03

## 1. Purpose

This handoff makes verified official-source research available to the contributor working on PR #1 without modifying, replacing or bypassing the canonical registries already present on `architecture/africafunds-country-indicators-v0.1`.

This contribution is intentionally additive. The files in this directory are review inputs. They are not competing sources of truth and must not be loaded automatically into PostgreSQL.

## 2. Scope

The research covers eleven country or common-market scopes:

- MAROC;
- GHANA;
- UEMOA;
- TUNISIE;
- EGYPTE;
- NIGERIA;
- KENYA;
- CEMAC;
- BOTSWANA;
- NAMIBIE;
- ETHIOPIE.

It identifies official organizations and source pages for:

- central-bank and policy rates;
- overnight or money-market reference rates;
- deposit, savings, lending and overdraft rates;
- treasury bills, government bonds and yield curves;
- equity-market indices and historical levels;
- monetary, financial and macroeconomic statistics;
- official fund-regulator and market-infrastructure sources.

## 3. Repository alignment

The canonical integration chain remains:

```text
COUNTRY OR ZONE
→ ORGANIZATION
→ ORGANIZATION SCOPE ROLE
→ SOURCE ENDPOINT
→ COUNTRY OR ZONE INDICATOR SOURCE MAPPING
→ PROVIDER SERIES
→ COLLECTION SPECIFICATION
→ COLLECTION RUN
→ RAW ARTIFACT
→ VALIDATED OBSERVATION
→ MARKET INDEX / WTI / WTI BENCH / METRIC
```

The only canonical files to be enriched after review are:

1. `data/reference/ORGANIZATIONS.csv`;
2. `data/reference/ORGANIZATION_SCOPE_ROLES.csv`;
3. `data/reference/SOURCE_ENDPOINTS.csv`;
4. `data/reference/COUNTRY_OR_ZONE_INDICATOR_SOURCE_MAPPING.csv`;
5. `data/reference/PROVIDER_SERIES.csv`;
6. `data/reference/COLLECTION_SPECIFICATIONS.csv`;
7. `data/reference/PILOT_COLLECTION_READINESS.csv` when a source enters an implementation wave;
8. `data/reference/COLLECTION_TEST_EVIDENCE.csv` only after a real reproducible collection run.

Do not create a second country, organization, endpoint or provider-series registry.

## 4. Current repository state observed before this handoff

At review time, the active draft PR contained:

- 54 African countries;
- 18 D00–D17 domains;
- 420 indicator, metadata, event and calculated-product definitions;
- 40 organizations, of which 20 were VALIDATED and 20 PENDING;
- 70 organization-scope-role relationships, of which 26 were VALIDATED;
- 43 source endpoints, of which 20 were VALIDATED;
- 55 indicator-source mappings, all at SOURCE_IDENTIFIED;
- 50 provider-series rows, all still PENDING;
- 17 collection specifications, all still PENDING;
- validated live BCEAO and BEAC FX collectors;
- no complete historical backfill;
- no production-persistent raw object store;
- no WTI or WTI Bench calculation yet.

The source branch was 131 commits ahead and 7 commits behind its current base. Reconcile that branch independently of this handoff; do not use this source-only PR to alter the branch strategy.

## 5. New organizational coverage available

### Botswana

Proposed organizations:

- `BOB` — Bank of Botswana — CENTRAL_BANK;
- `NBFIRA` — Non-Bank Financial Institutions Regulatory Authority — CAPITAL_MARKET_REGULATOR / FUND_REGULATOR;
- `BSE` — Botswana Stock Exchange — STOCK_EXCHANGE / INDEX_PROVIDER;
- `STATISTICS_BOTSWANA` — Statistics Botswana — STATISTICS_OFFICE.

### Namibia

Proposed organizations:

- `BON` — Bank of Namibia — CENTRAL_BANK;
- `NAMFISA` — Namibia Financial Institutions Supervisory Authority — CAPITAL_MARKET_REGULATOR / FUND_REGULATOR;
- `NSX` — Namibian Stock Exchange — STOCK_EXCHANGE / INDEX_PROVIDER;
- `NSA_NAMIBIA` — Namibia Statistics Agency — STATISTICS_OFFICE.

### Ethiopia

Proposed organizations:

- `NBE` — National Bank of Ethiopia — CENTRAL_BANK;
- `ECMA` — Ethiopian Capital Market Authority — CAPITAL_MARKET_REGULATOR;
- `ESX` — Ethiopian Securities Exchange — STOCK_EXCHANGE / INDEX_PROVIDER / FIXED_INCOME_MARKET_OPERATOR;
- `ESS_ETHIOPIA` — Ethiopian Statistical Service — STATISTICS_OFFICE.

### Common-market organizations to add or complete

- `AMF_UMOA` — Autorité des Marchés Financiers de l'UMOA;
- `UMOA_TITRES` — UMOA-Titres;
- `COSUMAF` — Commission de Surveillance du Marché Financier de l'Afrique Centrale.

## 6. Critical provider-series enrichment

The present generic policy-rate and debt rows are insufficient for fund analytics. Add separate provider-series records for each economically distinct rate.

### Nigeria

At minimum create or map:

- `PS_NIGERIA_NOFR_ON`;
- `PS_NIGERIA_NOFRI_30D`;
- `PS_NIGERIA_NOFRI_90D`;
- `PS_NIGERIA_NOFRI_180D`;
- `PS_NIGERIA_NIBOR_<TENOR>` when exact tenors are verified;
- `PS_NIGERIA_NITTY_<TENOR>` when exact tenors are verified;
- `PS_NIGERIA_MPR`;
- `PS_NIGERIA_DEPOSIT_RATE_<TENOR_OR_CATEGORY>`;
- `PS_NIGERIA_LENDING_RATE_<CATEGORY>`;
- `PS_NIGERIA_NGX_ASI`.

The official Nigerian Overnight Reference Rate, NOFR, is the primary overnight risk-free reference. NOFRI supplies compounded indices, including 30, 90 and 180 days. NIBOR and NITTY remain complementary and must not silently replace NOFR.

### Other named monetary references

- MAROC: MONIA;
- GHANA: Inter-Bank Weighted Average Rate, IBWAR;
- UEMOA: BCEAO weighted average interbank rate;
- TUNISIE: TMM;
- EGYPTE: CONIA;
- KENYA: KESONIA;
- CEMAC: TIMP;
- NAMIBIE: Repo Rate;
- ETHIOPIE: overnight and seven-day interbank observations where officially published.

## 7. Mandatory semantic distinctions

Never collapse the following into one generic interest-rate series:

- central-bank policy rate;
- deposit facility;
- marginal lending facility;
- overnight transaction-based risk-free rate;
- interbank offered rate;
- weighted average interbank rate;
- savings rate;
- term-deposit rate;
- lending rate;
- overdraft rate;
- treasury-bill auction yield;
- secondary-market sovereign yield;
- zero-coupon curve rate;
- calculated forward rate.

Every rate must preserve:

- native name;
- native unit;
- currency;
- tenor;
- market layer;
- rate type;
- day-count convention when known;
- compounding convention when known;
- observation date;
- publication date;
- effective date for policy decisions;
- source endpoint;
- source artifact;
- provider-series version.

## 8. Status rules

A verified URL is not a tested collector and a tested collector is not a complete history.

Use these progressions:

```text
SOURCE_IDENTIFIED
→ URL_LINKED / ENDPOINT_VERIFIED
→ SERIES_IDENTIFIED
→ SPECIFICATION_DRAFTED
→ COLLECTION_TESTED
→ PARTIAL_HISTORY_LOADED
→ COMPLETE_HISTORY_LOADED
```

For the records in `OFFICIAL_SOURCE_INVENTORY_20260803.csv`:

- official page identity was verified through desk research;
- no claim is made that each complete history was downloaded;
- do not use COLLECTION_TESTED;
- do not use PARTIAL_HISTORY_LOADED;
- do not use COMPLETE_HISTORY_LOADED;
- keep collection specifications PENDING or SPECIFICATION_REQUIRED until formats, selectors, date rules and parsing rules are executed and tested.

## 9. Collection requirements

Before changing a source to COLLECTION_TESTED, retain:

- requested URL;
- resolved URL;
- HTTP status;
- retrieval timestamp;
- source value or publication date;
- original filename;
- media type;
- byte size;
- SHA-256;
- parser version;
- raw storage URI;
- extracted row, cell, page, table or JSON path;
- validation results;
- deduplication result;
- revision handling result.

Run every first collector twice against identical content. The second execution must be idempotent.

## 10. Yield-curve rules

Do not treat a published auction table as an official zero-coupon curve.

Keep separate:

1. raw auction results;
2. secondary-market quotations;
3. instrument cash-flow definitions;
4. standardised yield observations;
5. interpolated par curve;
6. zero-coupon curve;
7. forward curve.

For UEMOA and CEMAC, do not create a fictional single sovereign curve for the entire currency zone. Preserve the issuer country even when the common central bank or regional agency publishes the data.

## 11. Equity-index rules

For every index distinguish:

- PRICE_INDEX;
- GROSS_TOTAL_RETURN_INDEX;
- NET_TOTAL_RETURN_INDEX;
- RECONSTRUCTED_TOTAL_RETURN_INDEX.

A reconstructed total-return index must never be labelled as an official exchange-published index.

Named index candidates identified by this research include:

- MASI;
- GSE Composite Index;
- BRVM Composite;
- TUNINDEX;
- EGX30 and other broad EGX indices as defined by the selected benchmark methodology;
- NGX All-Share Index;
- NSE All Share Index;
- BVMAC All Share Index;
- Botswana Domestic Company Index;
- NSX Overall and NSX Local;
- Ethiopia: no official broad index should be asserted until ESX publishes and documents one.

## 12. Fund-benchmark usage

Country alone is insufficient to assign a benchmark. The mapping must consider:

- fund or share-class base currency;
- investment geography;
- regulatory category;
- asset class;
- duration or weighted-average maturity;
- prospectus benchmark;
- Islamic or conventional mandate;
- distribution or accumulation policy;
- effective date of the benchmark assignment.

Examples:

- a Nigerian NGN money-market fund may use NOFR/NOFRI or matching NTB tenors according to its mandate;
- a Nigerian USD Eurobond fund must not use NGX ASI or NOFR as its primary performance benchmark;
- an UEMOA sovereign-bond fund must retain issuer-country exposure even when quoted in XOF;
- an equity fund should preferably use a total-return benchmark when available.

## 13. Recommended implementation waves

### Wave 02 — Exact named reference rates

Implement:

- MONIA;
- CONIA;
- NOFR and NOFRI;
- KESONIA;
- TMM;
- IBWAR;
- BCEAO interbank reference;
- BEAC TIMP.

### Wave 03 — Government securities and curves

Implement raw collectors for:

- Morocco Treasury references;
- Ghana 91/182/364-day auctions;
- UMOA-Titres issuer curves;
- Tunisia CMF curves;
- Egypt T-bills and T-bonds;
- Nigeria NTB and FGN bonds;
- Kenya bills and bonds;
- CEMAC public securities;
- Botswana government securities;
- Namibia benchmark yields;
- Ethiopia Treasury bills.

### Wave 04 — Equity indices

Implement official history or documented licensed access for each exchange. Do not screen-scrape licensed historical data in breach of access terms.

### Wave 05 — Macro and banking rates

Implement official CPI, GDP, money supply, reserves, deposit rates, lending rates and related revised vintages.

## 14. Files in this handoff

- `OFFICIAL_SOURCE_INVENTORY_20260803.csv` — machine-readable official source pages;
- `CANONICAL_INTEGRATION_MATRIX_20260803.csv` — proposed canonical actions and codes;
- `NON_REGRESSION_AND_STATUS_RULES_20260803.md` — review and merge guardrails;
- this document — complete contributor instructions.

## 15. Acceptance criteria

This handoff is considered integrated only when:

1. canonical registries remain unique;
2. every added organization has reviewed roles and scope;
3. every endpoint is distinct from the organization;
4. every provider series points to one endpoint and one canonical indicator;
5. exact provider names are preserved;
6. uncertain dates and codes remain null or PENDING;
7. no collection status is overstated;
8. all source artifacts are immutable and hashed;
9. all revisions remain queryable;
10. tests cover codes, URLs, relationships and idempotence;
11. common-zone series are stored once;
12. country-specific sovereign and fund observations retain country identity;
13. WTI and WTI Bench remain separate products;
14. no existing file or data row is deleted by this handoff.

## 16. Contributor action

Review this handoff against the current branch head. Integrate it as a sequence of small commits:

1. organizations and roles;
2. endpoints;
3. source mappings;
4. provider series;
5. collection specifications;
6. collectors and fixtures;
7. PostgreSQL loader changes;
8. coverage reports;
9. documentation status update.

Do not squash source discovery, parser implementation and historical-load claims into one unreviewable status change.
