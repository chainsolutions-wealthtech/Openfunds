# État de la boucle

```text
LOOP_ID: OF-LOOP-SOURCE-002
TASK_ID: OF-SOURCE-002
LOOP_TYPE: INSTITUTIONAL_COVERAGE
STATUS: EN_COURS
BRANCH: architecture/africafunds-country-indicators-v0.1
LAST_VERIFIED_WAVE: 03
WAVE_03_DATA_HEAD: 5024a9767b1b9aecf8a6cd52d315ccfbf8384389
WAVE_03_CI_RUN: 31595575537
CURRENT_WAVE: 04
CURRENT_WAVE_MODE: READ_ONLY_AUDIT
PRODUCTION_DEPLOYED: NO
REAL_HISTORY_LOADED: NO
RUNTIME_DATABASE_CHANGED: NO
```

## Progression vérifiée

```text
BASELINE_COUNTRY_COVERAGE: 7 / 54
AFTER_WAVE_01: 10 / 54
AFTER_WAVE_02: 14 / 54
AFTER_WAVE_03: 18 / 54
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 36

ORGANIZATIONS: 87 = 67 VALIDATED + 20 PENDING
ORGANIZATION_SCOPE_ROLES: 134 = 90 VALIDATED + 44 PENDING
SOURCE_ENDPOINTS: 43 UNCHANGED
```

Le workflow `Institutional Registry` protège désormais les invariants et les contrats des trois vagues terminées. Le run final vague 03 `31595575537` est vert sur Python 3.11 et 3.12 avec 8/8 tests.

Les grands CSV institutionnels restent des inventaires de découverte/revue conformément à ADR-021 ; aucune persistance runtime n’est revendiquée.

## Protections actives

```text
FMDQ                  REQUIRES_ROLE_MODEL_REVIEW
SEC_ZAMBIA            CURRENT_OFFICIAL_DOMAIN_INTEGRITY_BLOCKER
UGANDA_IRA_URBRA      COMBINED_ROLE_MODEL_MISMATCH
RBM_FUND_REGULATOR    PRIMARY_CIS_PROOF_NOT_SUFFICIENT
```

## Vague 04

Objectif immédiat : sélectionner un lot contrôlé parmi les 36 pays sans organisation country-scoped et effectuer exclusivement un audit de preuves officielles primaires actuelles.

Priorités de couverture :

```text
CENTRAL_BANK
STATISTICS_OFFICE
MINISTRY_OF_FINANCE / TREASURY / DEBT_MANAGEMENT_OFFICE
STOCK_EXCHANGE ou NOT_APPLICABLE prouvé
CAPITAL_MARKET_REGULATOR
FUND_REGULATOR
INSURANCE_PENSION_REGULATOR
```

Toute écriture de vague 04 exige une source officielle primaire actuelle, une revue des collisions de codes et une allowlist fermée documentée avant le contrat TDD RED.
