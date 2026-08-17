# OF-SOURCE-002 — Wave 05 read-only audit — 2026-08-17

```text
TASK_ID: OF-SOURCE-002
LOOP_ID: OF-LOOP-SOURCE-002
WAVE: 05
MODE: READ_ONLY_AUDIT
BASE_HEAD: bc8c61d55c9cd994fc6a92b351de3e5704c37a86
COUNTRY_COVERAGE_BEFORE: 22 / 54
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION_BEFORE: 32
WRITE_GATE: CLOSED_ALLOWLIST + TDD_RED + COLLISION_CHECK
```

## Scope

Wave 05 is intentionally limited to two countries with current primary-source evidence that is sufficiently explicit to avoid inferred institutional roles:

- Lesotho;
- Eswatini.

No endpoint, provider series, historical coverage, runtime database object, benchmark or calculation is promoted by this wave.

## Primary-source evidence

### Lesotho

1. Central Bank of Lesotho — https://centralbank.org.ls/
   - identifies itself as the Central Bank of Lesotho;
   - mandate includes monetary and financial stability.
2. Central Bank of Lesotho, Departments — https://centralbank.org.ls/departments/
   - Financial Markets / Domestic Market functions include regulating securities markets and licensed market participants;
   - Other Financial Institutions Supervision includes Pensions and Securities Supervision, Insurance Supervision and non-bank supervision.
3. Central Bank of Lesotho, Legislation — https://centralbank.org.ls/legislations/
   - publishes Collective Investment Schemes regulations and Capital Markets regulations.
4. Lesotho Bureau of Statistics — https://www.bos.gov.ls/
   - identifies itself as the government department responsible for official statistics.

### Eswatini

1. Central Bank of Eswatini — https://www.centralbank.org.sz/
   - identifies itself as the Central Bank of Eswatini and publishes its central-banking mandate.
2. Financial Services Regulatory Authority — https://www.fsra.co.sz/
   - regulates non-bank financial services including capital markets, insurance and retirement funds.
3. FSRA Capital Markets Development — https://www.fsra.co.sz/about/departments/cmd/
   - explicitly regulates Collective Investment Scheme Managers, securities exchanges, investment advisers, dealers and CSDs.
4. FSRA Securities Exchanges Directory — https://www.fsra.co.sz/directory/se.php
   - lists Eswatini Stock Exchange as the securities exchange.
5. Eswatini Stock Exchange — https://ese.co.sz/
   - current official exchange website.
6. Eswatini Central Statistical Office — https://www.gov.sz/index.php?catid=78&id=687%3Acentral-statistics-office&view=article
   - official government page identifies the CSO and its Statistics Act mandate.

## Collision review

The following organization codes are new relative to `ORGANIZATIONS.csv` at the base head and are reserved by this closed allowlist:

```text
CBL
BOS_LESOTHO
CBE_ESWATINI
FSRA_ESWATINI
ESE
CSO_ESWATINI
```

No existing organization row may be overwritten or renamed.

## Closed organization allowlist

| Code | Country | Type | Official website | Status |
|---|---|---|---|---|
| CBL | LESOTHO | CENTRAL_BANK | https://centralbank.org.ls/ | VALIDATED |
| BOS_LESOTHO | LESOTHO | STATISTICS_OFFICE | https://www.bos.gov.ls/ | VALIDATED |
| CBE_ESWATINI | ESWATINI | CENTRAL_BANK | https://www.centralbank.org.sz/ | VALIDATED |
| FSRA_ESWATINI | ESWATINI | CAPITAL_MARKET_REGULATOR | https://www.fsra.co.sz/ | VALIDATED |
| ESE | ESWATINI | STOCK_EXCHANGE | https://ese.co.sz/ | VALIDATED |
| CSO_ESWATINI | ESWATINI | STATISTICS_OFFICE | https://www.gov.sz/index.php?catid=78&id=687%3Acentral-statistics-office&view=article | VALIDATED |

## Closed role allowlist

```text
CBL             CENTRAL_BANK                  LESOTHO  COUNTRY
CBL             CAPITAL_MARKET_REGULATOR      LESOTHO  COUNTRY
CBL             FUND_REGULATOR                LESOTHO  COUNTRY
CBL             INSURANCE_PENSION_REGULATOR   LESOTHO  COUNTRY
BOS_LESOTHO     STATISTICS_OFFICE             LESOTHO  COUNTRY

CBE_ESWATINI    CENTRAL_BANK                  ESWATINI COUNTRY
FSRA_ESWATINI   CAPITAL_MARKET_REGULATOR      ESWATINI COUNTRY
FSRA_ESWATINI   FUND_REGULATOR                ESWATINI COUNTRY
FSRA_ESWATINI   INSURANCE_PENSION_REGULATOR   ESWATINI COUNTRY
ESE             STOCK_EXCHANGE                ESWATINI COUNTRY
CSO_ESWATINI    STATISTICS_OFFICE             ESWATINI COUNTRY
```

## Explicit non-assertions

- `MASERU_SECURITIES_MARKET` is not added as an independent organization in this wave. Primary evidence establishes a trading platform/market associated with CBL, but this audit does not establish a separate legal organization identity suitable for `ORGANIZATIONS.csv`.
- No `STOCK_EXCHANGE` role is therefore assigned for Lesotho in Wave 05.
- No ministry, debt office, endpoint or collection status is inferred from general institutional competence.

## Expected post-state after GREEN

```text
AFRICAN_COUNTRIES: 54
ORGANIZATIONS: 108 = 88 VALIDATED + 20 PENDING
COUNTRY_COVERAGE: 24 / 54
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 30
ORGANIZATION_SCOPE_ROLES: 166 = 122 VALIDATED + 44 PENDING
```

Wave 05 may be marked complete only after the exact organization and role allowlists are persisted, the institutional registry validator passes on Python 3.11 and 3.12, and no non-allowlisted registry mutation occurs.
