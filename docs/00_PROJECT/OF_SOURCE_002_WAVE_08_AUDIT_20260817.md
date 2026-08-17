# OF-SOURCE-002 — Wave 08 read-only audit — 2026-08-17

```text
TASK_ID: OF-SOURCE-002
LOOP_ID: OF-LOOP-SOURCE-002
WAVE: 08
MODE: READ_ONLY_AUDIT
BASE_COUNTRY_COVERAGE: 36 / 54
WRITE_GATE: CLOSED_ALLOWLIST + TDD_RED + COLLISION_CHECK
```

## Scope
Wave 08 closes country-scoped discovery coverage for 17 of the 18 remaining countries using current primary official sources. Eritrea is deliberately excluded because no current primary official institutional website could be verified sufficiently for `VALIDATED` promotion.

## Closed organization allowlist
```text
INSBU                  BURUNDI                       STATISTICS_OFFICE https://www.insbu.bi/
ICASEES                REPUBLIQUE_CENTRAFRICAINE    STATISTICS_OFFICE https://www.icasees.org/
INS_CAMEROUN            CAMEROUN                      STATISTICS_OFFICE https://ins-cameroun.cm/
INS_RDC                 REPUBLIQUE_DEMOCRATIQUE_DU_CONGO STATISTICS_OFFICE https://insrdc.cd/
INS_CONGO               REPUBLIQUE_DU_CONGO          STATISTICS_OFFICE https://ins-congo.cg/
INSEED_COMORES          COMORES                       STATISTICS_OFFICE https://www.inseed-comores.org/
INSTAD_DJIBOUTI         DJIBOUTI                      STATISTICS_OFFICE https://instad.dj/
DGS_GABON               GABON                         STATISTICS_OFFICE https://instatgabon.org/fr
INEGE                   GUINEE_EQUATORIALE            STATISTICS_OFFICE https://inege.org/
BSC_LIBYA               LIBYE                         STATISTICS_OFFICE https://bsc.ly/
INSTAT_MADAGASCAR       MADAGASCAR                    STATISTICS_OFFICE https://instat.mg/
ANSADE                  MAURITANIE                    STATISTICS_OFFICE https://ansade.mr/
CBOS                    SOUDAN                        CENTRAL_BANK      https://cbos.gov.sd/en
SNBS                    SOMALIE                       STATISTICS_OFFICE https://nbs.gov.so/
NBS_SOUTH_SUDAN         SOUDAN_DU_SUD                 STATISTICS_OFFICE https://nbs.gov.ss/
INE_STP                 SAO_TOME_ET_PRINCIPE          STATISTICS_OFFICE https://www.ine.st/
INSEED_TCHAD            TCHAD                         STATISTICS_OFFICE https://www.inseed.td/
```

## Closed role allowlist
Each statistics institution receives only `STATISTICS_OFFICE` on its sovereign `COUNTRY` scope. `CBOS` receives only `CENTRAL_BANK` for Sudan.

## Eritrea blocker
```text
COUNTRY: ERYTHREE
STATUS: PRIMARY_OFFICIAL_SOURCE_NOT_VERIFIED
ACTION: do not invent organization, URL or validation status
```
Secondary references identify a Bank of Eritrea and statistical functions, but Wave 08 requires a current primary official source. The country remains explicitly uncovered until that gate is satisfied.

## Explicit non-assertions
- CEMAC regional institutions are not copied to member-country scopes;
- broad mandates do not imply fund-regulator, insurance/pension-regulator or capital-market-regulator roles;
- no endpoint, provider series, collection status or history status is promoted;
- no organization is created for Eritrea.

## Expected post-state after GREEN
```text
AFRICAN_COUNTRIES: 54
ORGANIZATIONS: 141 = 121 VALIDATED + 20 PENDING
COUNTRY_COVERAGE: 53 / 54
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 1
ORGANIZATION_SCOPE_ROLES: 199 = 155 VALIDATED + 44 PENDING
UNCOVERED_COUNTRY: ERYTHREE
```
