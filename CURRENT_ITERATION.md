# Itération courante

```text
LOOP_ID: OF-LOOP-SOURCE-002
ITERATION: 004
TASK_ID: OF-SOURCE-002
STATUS: EN_COURS
DATE: 2026-08-12
LAST_VERIFIED_WAVE: 03
WAVE_03_CI_RUN: 31595575537
CURRENT_WAVE: 04
CURRENT_MODE: READ_ONLY_AUDIT
```

## Hypothèse courante

Les institutions nécessaires à la couverture des 54 pays peuvent être intégrées progressivement sans inventer de rôles, sans confondre organisation, endpoint, série et collecte, et sans transformer un inventaire de découverte en vérité runtime PostgreSQL.

## Résultats cumulés

```text
WAVE_01: +15 organisations / +22 relations / couverture 10 sur 54
WAVE_02: +16 organisations / +22 relations / couverture 14 sur 54
WAVE_03: +16 organisations / +20 relations / couverture 18 sur 54

CURRENT_ORGANIZATIONS: 87 = 67 VALIDATED + 20 PENDING
CURRENT_SCOPE_ROLES: 134 = 90 VALIDATED + 44 PENDING
CURRENT_COUNTRY_COVERAGE: 18 / 54
REMAINING_COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 36
```

La vague 03 a été validée par TDD : RED contrôlé, étape intermédiaire organisations-only, puis GREEN final `Institutional Registry` run `31595575537`, Python 3.11/3.12, 8/8 tests.

## Itération 004 — objectif

1. résoudre le HEAD dynamiquement ;
2. sélectionner un lot de pays parmi les 36 non couverts ;
3. rechercher uniquement des sources officielles primaires actuelles ;
4. séparer identité, rôle, endpoint et collecte ;
5. bloquer tout domaine compromis, ambigu ou obsolète ;
6. vérifier les collisions de codes ;
7. produire une allowlist fermée avant toute nouvelle écriture ;
8. appliquer ensuite RED → organisations → rôles → GREEN si le gate est satisfait.

## Blockers conservés

- `FMDQ` : rôle canonique à arbitrer ;
- `SEC_ZAMBIA` : domaine institutionnel courant non fiable lors de l'audit vague 03 ;
- `IRA/URBRA Uganda` : fonctions assurance/retraite séparées face à un rôle canonique combiné ;
- `RBM FUND_REGULATOR` : preuve CIS/OPC insuffisante.

## Interdictions

Aucun nouvel endpoint, provider series, historique, migration runtime, branche, PR, merge, retargeting ou déploiement n’est autorisé pendant l’audit de vague 04.
