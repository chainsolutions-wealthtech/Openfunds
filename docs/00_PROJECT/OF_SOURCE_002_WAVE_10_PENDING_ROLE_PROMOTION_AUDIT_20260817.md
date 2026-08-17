# OF-SOURCE-002 — Wave 10 Pending-Role Promotion Audit

**Date:** 2026-08-17  
**Branch:** `architecture/africafunds-country-indicators-v0.1`  
**Mutation scope:** existing `ORGANIZATION_SCOPE_ROLES.csv` rows only  
**New organizations:** none  
**New role rows:** none

## Objective

Reduce the post-Wave09 `PENDING` backlog by promoting only exact, pre-existing country-scoped role rows for which a current official institutional source directly confirms the organization and role.

This wave deliberately excludes FX reference-rate provision, index provision, interbank-market operation and other roles whose exact series/methodology/function require a separate evidence review.

## Preconditions

Post-Wave09 verified state:

```text
ORGANIZATIONS = 141
ORGANIZATION_SCOPE_ROLES = 199
VALIDATED_SCOPE_ROLES = 159
PENDING_SCOPE_ROLES = 40
COUNTRY_COVERAGE = 53 / 54
```

Wave 10 must not change the organization count, total role-row count, role code, scope code, scope type, relationship role, primary flag or validity dates of any selected row.

## Closed promotion allowlist

| Organization | Role | Scope | Type | Primary official evidence | Evidence rationale |
|---|---|---|---|---|---|
| `SARB` | `CENTRAL_BANK` | `AFRIQUE_DU_SUD` | `COUNTRY` | `https://www.resbank.co.za/en/home/about-us` | SARB states its constitutional monetary mandate, financial-stability mandate, banknote issuance, reserves, government-banker and lender-of-last-resort functions. |
| `JSE` | `STOCK_EXCHANGE` | `AFRIQUE_DU_SUD` | `COUNTRY` | `https://www.jse.co.za/` | The official Johannesburg Stock Exchange site identifies the JSE and its listing/trading market functions. |
| `CBK` | `CENTRAL_BANK` | `KENYA` | `COUNTRY` | `https://www.centralbank.go.ke/` | Official Central Bank of Kenya domain and current official CBK subdomains identify the institution and its monetary/financial-stability mandate. |
| `CMA_KENYA` | `FUND_REGULATOR` | `KENYA` | `COUNTRY` | `https://www.cma.or.ke/regulatory-framework/` | CMA publishes the Collective Investment Schemes regulations it supervises. |
| `KNBS` | `STATISTICS_OFFICE` | `KENYA` | `COUNTRY` | `https://www.knbs.or.ke/about/` | KNBS states it is the principal government agency for collecting, analysing and disseminating official statistics. |
| `NATIONAL_TREASURY_KENYA` | `TREASURY` | `KENYA` | `COUNTRY` | `https://www.treasury.go.ke/` | Official National Treasury site exposes budget, public-debt and Treasury functions. |
| `FRA_EGYPT` | `FUND_REGULATOR` | `EGYPTE` | `COUNTRY` | `https://fra.gov.eg/en/lc00-regulations/` | FRA publishes and enforces investment-fund regulations and current fund-sector supervisory decisions. |
| `CAPMAS` | `STATISTICS_OFFICE` | `EGYPTE` | `COUNTRY` | `https://www.capmas.gov.eg/` | Official CAPMAS domain identifies the Central Agency for Public Mobilization and Statistics; its official data catalogue identifies CAPMAS as producer/sponsor of national statistical surveys. |
| `MOF_EGYPT` | `MINISTRY_OF_FINANCE` | `EGYPTE` | `COUNTRY` | `https://mof.gov.eg/en/` | Official site identifies itself as the Ministry of Finance, Arab Republic of Egypt, and publishes Treasury-bill/public-debt surfaces. |
| `DMO_NIGERIA` | `DEBT_MANAGEMENT_OFFICE` | `NIGERIA` | `COUNTRY` | `https://www.dmo.gov.ng/about-dmo` | DMO states it was established to centrally coordinate management of Nigeria's debt and describes debt-management functions. |
| `NBS_NIGERIA` | `STATISTICS_OFFICE` | `NIGERIA` | `COUNTRY` | `https://www.nigerianstat.gov.ng/page/about-us/` | NBS identifies itself as the apex statistical agency coordinating production of official statistics. |
| `INS_TUNISIE` | `STATISTICS_OFFICE` | `TUNISIE` | `COUNTRY` | `https://www.ins.tn/presentation-ins` | INS states it is the central body of the national statistical system and lists collection, processing, analysis and dissemination missions. |

## Explicit exclusions from Wave 10

The following existing pending role classes are **not** promoted in this wave solely because an organization is otherwise verified:

```text
FX_REFERENCE_RATE_PROVIDER
INDEX_PROVIDER
INTERBANK_MARKET_OPERATOR
MONETARY_UNION
SUPRANATIONAL_AUTHORITY
GOVERNMENT_SECURITIES_AGENCY
```

Other pending country roles not listed in the closed allowlist remain unchanged.

In particular, this wave does not promote:

- `EGX/STOCK_EXCHANGE` — official-domain retrieval is not sufficiently stable in the current evidence pass;
- `NGX/STOCK_EXCHANGE` — group/exchange identity requires a dedicated entity-role reconciliation pass;
- Ghana exchange/index pending rows;
- any FX or index row merely because its parent institution is official.

## Expected post-state

Exactly 12 existing rows move from `PENDING` to `VALIDATED`.

```text
ORGANIZATIONS = 141               (unchanged)
ORGANIZATION_SCOPE_ROLES = 199    (unchanged)
VALIDATED_SCOPE_ROLES = 171       (159 + 12)
PENDING_SCOPE_ROLES = 28          (40 - 12)
```

Each promoted row must use:

```text
VALIDATION_STATUS = VALIDATED
SOURCE_NOTE = OFFICIAL_ROLE_VERIFIED_2026_08_17_WAVE10
```

No other field may change.

## TDD gate

Before mutation, `tests/test_institutional_registry_wave10.py` must fail because the exact 12 rows are not yet all `VALIDATED`, while Waves 01–09 remain green.

After mutation, all institutional contracts must pass on Python 3.11 and 3.12 and an exact post-state assertion must prove `199 / 171 / 28` before commit.
