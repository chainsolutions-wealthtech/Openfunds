# OF-SOURCE-002 — Wave 10 Completion and Residual Inventory

**Date:** 2026-08-17  
**Branch:** `architecture/africafunds-country-indicators-v0.1`  
**Wave:** 10  
**Status:** VERIFIED_COMPLETE

## Purpose

Wave 10 reduced the institutional-role backlog by promoting only exact, pre-existing country-scoped relations with current primary official evidence. No organization, role identity, scope identity, relationship role, primary flag or validity date was created or retargeted.

## TDD evidence

### RED

`Institutional Registry` run `32059337944` executed the Wave 10 contract before mutation.

Verified behavior:

- Waves 01–09 remained green;
- every Wave 10 tuple already existed exactly once;
- Wave 10 failed only because the selected rows were still `PENDING` and retained their prior source notes.

### GREEN

`OF-SOURCE-002 Wave 10 Pending Role Promotion` run `32059405591` completed successfully.

The governed workflow verified:

1. exactly 12 pre-existing rows were selected;
2. every selected row was `PENDING` before promotion;
3. only `VALIDATION_STATUS` and `SOURCE_NOTE` changed;
4. no row identity or scope changed;
5. all institutional contracts Waves 01–10 passed on Python 3.11;
6. all institutional contracts Waves 01–10 passed on Python 3.12;
7. organization count remained 141;
8. role-row count remained 199;
9. exact post-state was `171 VALIDATED / 28 PENDING`;
10. the only modified data file was `data/reference/ORGANIZATION_SCOPE_ROLES.csv`.

## Exact promoted allowlist

```text
SARB                    CENTRAL_BANK              AFRIQUE_DU_SUD
JSE                     STOCK_EXCHANGE            AFRIQUE_DU_SUD
CBK                     CENTRAL_BANK              KENYA
CMA_KENYA               FUND_REGULATOR            KENYA
KNBS                    STATISTICS_OFFICE         KENYA
NATIONAL_TREASURY_KENYA TREASURY                  KENYA
FRA_EGYPT               FUND_REGULATOR            EGYPTE
CAPMAS                  STATISTICS_OFFICE         EGYPTE
MOF_EGYPT               MINISTRY_OF_FINANCE       EGYPTE
DMO_NIGERIA             DEBT_MANAGEMENT_OFFICE    NIGERIA
NBS_NIGERIA             STATISTICS_OFFICE         NIGERIA
INS_TUNISIE             STATISTICS_OFFICE         TUNISIE
```

Every promoted row now carries:

```text
VALIDATION_STATUS = VALIDATED
SOURCE_NOTE = OFFICIAL_ROLE_VERIFIED_2026_08_17_WAVE10
```

## Verified post-Wave10 registry state

```text
AFRICAN_COUNTRIES = 54
COUNTRY_COVERAGE = 53 / 54
UNCOVERED_COUNTRY = ERYTHREE
ORGANIZATIONS = 141
ORGANIZATION_SCOPE_ROLES = 199
VALIDATED_SCOPE_ROLES = 171
PENDING_SCOPE_ROLES = 28
```

Coverage remains 53/54 because Wave 10 only promoted existing roles. Eritrea remains deliberately unpopulated until a current primary official source is verified.

## Post-Wave10 effective role-gap audit

Read-only workflow `OF-SOURCE-002 Post-Wave10 Audit`, run `32059464067`, passed all Waves 01–10 contracts and produced the following effective country+zone gaps:

```text
MONETARY_AUTHORITY              11 countries missing
STATISTICS                       3 countries missing
CAPITAL_MARKET_REGULATION       18 countries missing
FUND_REGULATION                 19 countries missing
INSURANCE_PENSION_REGULATION    44 countries missing
EXCHANGE                        20 countries missing
FISCAL_DEBT                     40 countries missing
```

These figures use validated country roles plus inherited validated monetary-zone roles. They are not equivalent to simple counts of national organizations.

## Exact remaining PENDING families

```text
FX_REFERENCE_RATE_PROVIDER   9
INDEX_PROVIDER               9
STOCK_EXCHANGE               3
MONETARY_UNION               3
SUPRANATIONAL_AUTHORITY      2
INTERBANK_MARKET_OPERATOR    2
TOTAL                       28
```

Scope split:

```text
COUNTRY        17
MONETARY_ZONE  11
```

### Remaining country-scoped rows

```text
AFRIQUE_DU_SUD  SARB FX_REFERENCE_RATE_PROVIDER
AFRIQUE_DU_SUD  JSE INDEX_PROVIDER
EGYPTE          CBE FX_REFERENCE_RATE_PROVIDER
EGYPTE          EGX STOCK_EXCHANGE
EGYPTE          EGX INDEX_PROVIDER
GHANA           BOG FX_REFERENCE_RATE_PROVIDER
GHANA           GSE STOCK_EXCHANGE
GHANA           GSE INDEX_PROVIDER
KENYA           CBK FX_REFERENCE_RATE_PROVIDER
KENYA           NSE INDEX_PROVIDER
MAROC           BAM FX_REFERENCE_RATE_PROVIDER
MAROC           CASABLANCA_BOURSE INDEX_PROVIDER
NIGERIA         CBN FX_REFERENCE_RATE_PROVIDER
NIGERIA         NGX STOCK_EXCHANGE
NIGERIA         NGX INDEX_PROVIDER
TUNISIE         BCT FX_REFERENCE_RATE_PROVIDER
TUNISIE         BVMT INDEX_PROVIDER
```

### Remaining zonal rows

```text
CEMAC  BEAC  FX_REFERENCE_RATE_PROVIDER
CEMAC  BEAC  INTERBANK_MARKET_OPERATOR
CEMAC  BVMAC INDEX_PROVIDER
CEMAC  CEMAC MONETARY_UNION
CEMAC  CEMAC SUPRANATIONAL_AUTHORITY

CMA    CMA   MONETARY_UNION

UEMOA  BCEAO FX_REFERENCE_RATE_PROVIDER
UEMOA  BCEAO INTERBANK_MARKET_OPERATOR
UEMOA  BRVM  INDEX_PROVIDER
UEMOA  UEMOA MONETARY_UNION
UEMOA  UEMOA SUPRANATIONAL_AUTHORITY
```

## Decision for next wave

Wave 11 must first review the three remaining `STOCK_EXCHANGE` rows:

```text
EGX / EGYPTE
GSE / GHANA
NGX / NIGERIA
```

These are institutional identity/function promotions and are semantically simpler than the remaining series roles.

The following families must remain separated into later evidence passes:

- `FX_REFERENCE_RATE_PROVIDER`: requires direct evidence that the institution publishes/owns the relevant reference-rate series;
- `INDEX_PROVIDER`: requires direct evidence for index calculation/publication ownership, not merely exchange existence;
- `INTERBANK_MARKET_OPERATOR`: requires an exact operating/administration mandate, not generic central-bank oversight;
- `MONETARY_UNION` / `SUPRANATIONAL_AUTHORITY`: require a dedicated zone-semantic review, especially for the Common Monetary Area.

## Non-regression statement

Wave 10 did not:

- create or delete organizations;
- create or delete role rows;
- alter `main`;
- merge or retarget PR #1;
- activate production calculations;
- validate FX/index roles by inference;
- change Eritrea's guarded status.
