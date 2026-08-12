# OF-SOURCE-002 — Wave 01 completion attestation — 2026-08-12

```text
TASK_ID: OF-SOURCE-002
LOOP_ID: OF-LOOP-SOURCE-002
WAVE: 01
STATUS: VERIFIED_COMPLETE_WAVE / GLOBAL_TASK_EN_COURS
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
WAVE_DATA_HEAD: 1f85c0df1878743f4a2ac322c2087b0b1a549641
PRODUCTION_DEPLOYED: NO
RUNTIME_DATABASE_CHANGED: NO
HISTORY_LOADED: NO
NEW_BRANCH_CREATED: NO
NEW_PR_CREATED: NO
PR2_MODIFIED: NO
```

## Baseline

Avant la vague 01 :

```text
AFRICAN_COUNTRIES: 54
ORGANIZATIONS: 40 = 20 VALIDATED + 20 PENDING
COUNTRIES_WITH_COUNTRY_SCOPED_ORGANIZATION: 7
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 47
ORGANIZATION_SCOPE_ROLES: 70 = 26 VALIDATED + 44 PENDING
SOURCE_ENDPOINTS: 43 = 20 VALIDATED + 23 PENDING
```

## Changements de la vague

Quinze organisations dont l'identité et le rôle principal ont été vérifiés sur des domaines officiels ont été ajoutées au registre de découverte/revue :

```text
BOTSWANA: BOB, NBFIRA, BSE, STATISTICS_BOTSWANA
NAMIBIE: BON, NAMFISA, NSX, NSA_NAMIBIA
ETHIOPIE: NBE, ECMA, ESX, ESS_ETHIOPIA
UEMOA: AMF_UMOA, UMOA_TITRES
CEMAC: COSUMAF
```

Vingt-deux relations organisation-rôle-périmètre vérifiées ont été ajoutées pour les rôles suivants :

```text
CENTRAL_BANK
CAPITAL_MARKET_REGULATOR
FUND_REGULATOR
INSURANCE_PENSION_REGULATOR
STOCK_EXCHANGE
STATISTICS_OFFICE
GOVERNMENT_SECURITIES_AGENCY
```

`FMDQ` n'a pas été intégré : l'identité institutionnelle est connue, mais le rattachement exact à la taxonomie de rôles du dépôt reste à arbitrer avant écriture.

## État après vague 01

```text
ORGANIZATIONS: 55 = 35 VALIDATED + 20 PENDING
COUNTRIES_WITH_COUNTRY_SCOPED_ORGANIZATION: 10
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 44
ORGANIZATION_SCOPE_ROLES: 92 = 48 VALIDATED + 44 PENDING
SOURCE_ENDPOINTS: 43 = 20 VALIDATED + 23 PENDING
```

Les trois nouveaux pays avec au moins une organisation nationale sont `BOTSWANA`, `NAMIBIE` et `ETHIOPIE`. Les organisations UEMOA/CEMAC restent correctement au niveau zone et ne sont pas comptées comme institutions nationales des pays membres.

## Contrôle exécutable ajouté

```text
scripts/validate_institutional_registry.py
tests/test_institutional_registry.py
.github/workflows/institutional-registry.yml
```

Le contrôle vérifie notamment :

- 54 pays attendus ;
- unicité et syntaxe des codes techniques ;
- références organisation/rôle/scope ;
- scopes pays/zone existants ;
- statuts autorisés ;
- URL officielle obligatoire pour une organisation `VALIDATED` ;
- URL canonique obligatoire pour un endpoint `VALIDATED` ;
- présence de l'allowlist de vague 01 et de ses relations `VALIDATED`.

## Preuve TDD

### RED initial

```text
RUN: 31592435103
PYTHON_3_11: FAILURE
PYTHON_3_12: FAILURE
CAUSES ATTENDUES:
- validateur absent ;
- 15 organisations absentes ;
- 22 relations absentes.
```

### RED intermédiaire

Après ajout du validateur :

```text
RUN: 31592516832
VALIDATOR_CLI: PASS
EXISTING_REGISTRY_INVARIANTS: PASS
WAVE01_ORGANIZATIONS: FAIL attendu
WAVE01_SCOPE_ROLES: FAIL attendu
```

### GREEN final

```text
RUN: 31592700354
HEAD: 1f85c0df1878743f4a2ac322c2087b0b1a549641
WORKFLOW: Institutional Registry
CONCLUSION: SUCCESS
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
TESTS: 4 / 4 PASS
```

## Limites conservées

Cette vague ne :

- crée aucun endpoint spécialisé ;
- ne crée aucune provider series ;
- ne crée aucune collection specification ;
- ne crée aucune preuve de collecte ;
- ne modifie aucun schéma ou migration runtime ;
- ne charge aucune observation ni historique ;
- ne configure aucune base PostgreSQL persistante ;
- ne modifie ni PR nº2, ni `main`, ni la cible de PR nº1 ;
- ne crée aucune branche ou PR.

Conformément à ADR-021, `ORGANIZATIONS.csv` et `ORGANIZATION_SCOPE_ROLES.csv` restent des inventaires de découverte/revue. PostgreSQL ne devient cohérent avec de nouveaux objets institutionnels qu'après une migration gouvernée dédiée, non réalisée dans cette vague.

## Point de reprise

`OF-SOURCE-002` reste `EN_COURS`.

La prochaine unité est `OF-SOURCE-002 / WAVE_02`, d'abord en lecture seule : mesurer les rôles manquants des 10 pays désormais présents et rechercher les institutions officielles des 44 pays encore sans organisation nationale. Les priorités sont les rôles explicitement requis par le TODO : banque centrale, statistiques, finances, dette, bourse, régulation fonds et assurance/pension. Toute non-applicabilité doit être prouvée et explicite ; aucune institution ne doit être inventée pour forcer une matrice complète.
