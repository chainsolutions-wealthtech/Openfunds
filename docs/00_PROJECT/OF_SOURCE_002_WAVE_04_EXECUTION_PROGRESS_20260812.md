# OF-SOURCE-002 — Wave 04 execution progress — 2026-08-12

```text
TASK_ID: OF-SOURCE-002
LOOP_ID: OF-LOOP-SOURCE-002
WAVE: 04
GLOBAL_TASK_STATUS: EN_COURS
WAVE_STATUS: EXECUTION_IN_PROGRESS_NOT_YET_ATTESTED_COMPLETE
NEW_BRANCH_CREATED: NO
NEW_PR_CREATED: NO
MAIN_MODIFIED: NO
PR2_MODIFIED: NO
RUNTIME_DATABASE_CHANGED: NO
HISTORY_LOADED: NO
```

## Read-only gate

Audit et allowlist fermée :

```text
docs/00_PROJECT/OF_SOURCE_002_WAVE_04_AUDIT_20260812.md
15 organisations
21 relations organisation-rôle
```

Pays : Angola, Mozambique, Cabo Verde, Seychelles.

## TDD

### RED

```text
HEAD: 2b1d1481b921c3c138ff5370706cf6c96c765424
RUN: 31596828224
EXPECTED: 8 tests historiques verts / 2 tests Wave 04 rouges
```

### Étape intermédiaire organisations

```text
HEAD: 48be294908461c7a2ca2f625fa8664d1173768d3
RUN: 31597214758
ORGANIZATIONS_ADDED: 15
EXPECTED_CONTRACT_STATE: organisations Wave 04 vertes / relations Wave 04 encore rouges
```

Organisations intégrées :

```text
ANGOLA: BNA, CMC_ANGOLA, BODIVA, INE_ANGOLA
MOZAMBIQUE: BANCO_MOCAMBIQUE, BVM_MOZAMBIQUE, INE_MOZAMBIQUE
CABO_VERDE: BCV, AGMVM, BVC, INE_CABO_VERDE
SEYCHELLES: CBS, FSA_SEYCHELLES, MERJ_EXCHANGE, NBS_SEYCHELLES
```

## Append des relations — mécanisme gouverné

Le connecteur d'écriture exige le SHA exact du blob pour remplacer `ORGANIZATION_SCOPE_ROLES.csv`. Afin de ne jamais deviner ce SHA ni réécrire un CSV tronqué, un workflow one-shot idempotent a été ajouté :

```text
.github/workflows/of-source-002-wave04-append.yml
```

Ce workflow :

1. ne peut ajouter que les 21 relations de l'allowlist Wave 04 ;
2. refuse tout état partiellement intégré ;
3. interdit explicitement `BANCO_MOCAMBIQUE / INSURANCE_PENSION_REGULATOR` ;
4. exécute le validateur et les tests sur Python 3.11 ;
5. exécute le validateur et les tests sur Python 3.12 ;
6. exige le post-état exact suivant avant push :

```text
AFRICAN_COUNTRIES: 54
ORGANIZATIONS: 102 = 82 VALIDATED + 20 PENDING
COUNTRY_COVERAGE: 22 / 54
ORGANIZATION_SCOPE_ROLES: 155 = 111 VALIDATED + 44 PENDING
```

7. ne committe que `data/reference/ORGANIZATION_SCOPE_ROLES.csv` si les contrôles passent.

## Gate de clôture

La vague 04 ne doit être marquée `VERIFIED_COMPLETE_WAVE` qu'après preuve GitHub que :

- les 21 relations sont présentes dans le registre ;
- le rôle interdit Mozambique reste absent ;
- le run de validation est `SUCCESS` pour Python 3.11 et 3.12 ;
- les comptes post-état sont ceux attendus ;
- aucun autre fichier de données n'a été modifié par l'append.

`OF-SOURCE-002 / WAVE_05` ne doit pas commencer avant satisfaction de ce gate.
