# État de la boucle

```text
LOOP_ID: OF-LOOP-SOURCE-002
TASK_ID: OF-SOURCE-002
LOOP_TYPE: INSTITUTIONAL_COVERAGE
STATUS: EN_COURS
BRANCH: architecture/africafunds-country-indicators-v0.1
WAVE_01_STATUS: VERIFIED_COMPLETE
WAVE_01_DATA_HEAD: 1f85c0df1878743f4a2ac322c2087b0b1a549641
WAVE_01_CI_RUN: 31592700354
CURRENT_WAVE: 02
CURRENT_WAVE_MODE: READ_ONLY_AUDIT
PRODUCTION_DEPLOYED: NO
REAL_HISTORY_LOADED: NO
RUNTIME_DATABASE_CHANGED: NO
```

## Vague 01 vérifiée

```text
ORGANIZATIONS_ADDED: 15
VALIDATED_SCOPE_ROLES_ADDED: 22
COUNTRY_COVERAGE_BEFORE: 7 / 54
COUNTRY_COVERAGE_AFTER: 10 / 54
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 44
```

Un workflow `Institutional Registry` protège désormais les invariants du registre. Le run `31592700354` est vert sur Python 3.11 et 3.12.

Les grands CSV institutionnels restent des inventaires de découverte/revue conformément à ADR-021 ; aucune persistance runtime n’est revendiquée.

## Vague 02

Objectif immédiat : audit read-only des 44 pays sans organisation nationale et des rôles manquants des 10 pays déjà représentés.

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

Toute écriture de vague 02 exige une preuve primaire officielle, une revue des collisions de codes et une allowlist explicite. `FMDQ` reste en revue sémantique et aucune donnée issue de la PR nº2 n’est canonisée automatiquement.
