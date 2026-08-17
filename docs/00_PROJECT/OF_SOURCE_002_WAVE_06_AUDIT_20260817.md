# OF-SOURCE-002 — Wave 06 read-only audit — 2026-08-17

```text
TASK_ID: OF-SOURCE-002
LOOP_ID: OF-LOOP-SOURCE-002
WAVE: 06
MODE: READ_ONLY_AUDIT
BASE_HEAD: f1042f1c5a7ba5e985e06bf84430a888f4101d09
COUNTRY_COVERAGE_BEFORE: 24 / 54
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION_BEFORE: 30
WRITE_GATE: CLOSED_ALLOWLIST + TDD_RED + COLLISION_CHECK
```

## Scope

Wave 06 is deliberately restricted to central-bank and official-statistics identities for four countries:

- Liberia;
- The Gambia;
- Sierra Leone;
- Guinea.

This wave does not infer a capital-market, fund, insurance/pension or stock-exchange role merely from broad financial-sector powers. Those roles remain for separate evidence and modelling review.

## Primary-source evidence

### Liberia

- Central Bank of Liberia — https://www.cbl.org.lr/
- Central Bank of Liberia Data Warehouse — https://www.cbl.org.lr/general/data-warehouse
- Liberia Institute of Statistics and Geo-Information Services — https://lisgis.gov.lr/

### The Gambia

- Central Bank of The Gambia — https://www.cbg.gm/
- Official Government of The Gambia, Gambia Bureau of Statistics — https://gambia.gov.gm/gambia-bureau-of-statistics/

### Sierra Leone

- Bank of Sierra Leone — https://bsl.gov.sl/
- Statistics Sierra Leone — https://www.statistics.sl/

### Guinea

- Banque Centrale de la République de Guinée — https://www.bcrg.gn/
- Institut National de la Statistique — https://www.stat-guinee.org/

## Closed organization allowlist

```text
CBL_LIBERIA     LIBERIA       CENTRAL_BANK
LISGIS          LIBERIA       STATISTICS_OFFICE
CBG             GAMBIE        CENTRAL_BANK
GBOS_GAMBIA     GAMBIE        STATISTICS_OFFICE
BSL             SIERRA_LEONE  CENTRAL_BANK
STATS_SL        SIERRA_LEONE  STATISTICS_OFFICE
BCRG            GUINEE        CENTRAL_BANK
INS_GUINEE      GUINEE        STATISTICS_OFFICE
```

`CBL_LIBERIA` is intentionally used instead of `CBL` because `CBL` is already the governed code for the Central Bank of Lesotho from Wave 05.

## Closed role allowlist

```text
CBL_LIBERIA CENTRAL_BANK      LIBERIA      COUNTRY
LISGIS      STATISTICS_OFFICE LIBERIA      COUNTRY
CBG         CENTRAL_BANK      GAMBIE       COUNTRY
GBOS_GAMBIA STATISTICS_OFFICE GAMBIE       COUNTRY
BSL         CENTRAL_BANK      SIERRA_LEONE COUNTRY
STATS_SL    STATISTICS_OFFICE SIERRA_LEONE COUNTRY
BCRG        CENTRAL_BANK      GUINEE       COUNTRY
INS_GUINEE  STATISTICS_OFFICE GUINEE       COUNTRY
```

## Explicit non-assertions

- no securities-regulator identity is asserted for Liberia in this wave;
- no capital-market regulator or exchange role is asserted for The Gambia in this wave;
- Bank of Sierra Leone supervisory powers and any separate securities-regulator identity are left for a dedicated role-model review;
- BCRG insurance/financial supervision does not automatically become the combined `INSURANCE_PENSION_REGULATOR` role;
- no endpoint, provider series or collection status is promoted.

## Expected post-state after GREEN

```text
AFRICAN_COUNTRIES: 54
ORGANIZATIONS: 116 = 96 VALIDATED + 20 PENDING
COUNTRY_COVERAGE: 28 / 54
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 26
ORGANIZATION_SCOPE_ROLES: 174 = 130 VALIDATED + 44 PENDING
```
