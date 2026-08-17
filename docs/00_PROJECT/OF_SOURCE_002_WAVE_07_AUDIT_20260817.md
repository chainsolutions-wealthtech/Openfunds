# OF-SOURCE-002 — Wave 07 read-only audit — 2026-08-17

```text
TASK_ID: OF-SOURCE-002
LOOP_ID: OF-LOOP-SOURCE-002
WAVE: 07
MODE: READ_ONLY_AUDIT
BASE_HEAD: e852163843596ee4e700d86a7cf4d517e1ff2494
COUNTRY_COVERAGE_BEFORE: 28 / 54
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION_BEFORE: 26
WRITE_GATE: CLOSED_ALLOWLIST + TDD_RED + COLLISION_CHECK
```

## Scope
Wave 07 adds only the national official-statistics institutions for the eight UEMOA member countries still lacking country-scoped organizations. BCEAO, AMF-UMOA, UMOA-Titres and BRVM remain zone-scoped and are not duplicated.

## Primary-source evidence
- Benin — INStaD: https://www.instad.bj/
- Burkina Faso — INSD: https://www.insd.bf/
- Côte d'Ivoire — ANStat: https://www.anstat.ci/
- Guinea-Bissau — INE-GB: https://stat-guinebissau.com/
- Mali — INSTAT: https://www.instat-mali.org/
- Niger — INS: https://www.stat-niger.org/
- Senegal — ANSD: https://www.ansd.sn/
- Togo — INSEED: https://inseed.tg/

## Closed organization allowlist
```text
INSTAD_BENIN       BENIN          STATISTICS_OFFICE
INSD_BURKINA       BURKINA_FASO   STATISTICS_OFFICE
ANSTAT_CIV         COTE_DIVOIRE   STATISTICS_OFFICE
INE_GUINEE_BISSAU  GUINEE_BISSAU STATISTICS_OFFICE
INSTAT_MALI        MALI           STATISTICS_OFFICE
INS_NIGER          NIGER          STATISTICS_OFFICE
ANSD_SENEGAL       SENEGAL        STATISTICS_OFFICE
INSEED_TOGO        TOGO           STATISTICS_OFFICE
```

## Closed role allowlist
Each organization receives only `STATISTICS_OFFICE` on its sovereign `COUNTRY` scope.

## Explicit non-assertions
BCEAO, AMF-UMOA, UMOA-Titres and BRVM are not copied to country scope. No country-specific central-bank, market-regulator, fund-regulator, exchange, endpoint, series or history status is inferred.

## Expected post-state after GREEN
```text
AFRICAN_COUNTRIES: 54
ORGANIZATIONS: 124 = 104 VALIDATED + 20 PENDING
COUNTRY_COVERAGE: 36 / 54
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 18
ORGANIZATION_SCOPE_ROLES: 182 = 138 VALIDATED + 44 PENDING
```
