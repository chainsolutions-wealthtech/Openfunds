# Préparation de la phase suivante

```text
DATE: 2026-08-05
OBSERVED_HEAD: 202f23d5a5be961d6f8338984b04655eda336a6b
OF_DATA_001_STARTED: NO
OF_DATA_001_READY: NO
```

## 1. Critères déjà remplis

- source d’authoring des deux pilotes FX clarifiée ;
- objets BCEAO/XOF et BEAC/XAF réconciliés ;
- endpoint runtime canonique décidé et testé ;
- dates métier inconnues modélisées sans date inventée ;
- manifeste de 14 migrations et runner présents ;
- installation PostgreSQL 16 vide testée ;
- deuxième application idempotente testée ;
- scénario complet sans ledger testé ;
- propositions SQL exclues du chemin runtime ;
- baseline documentaire conservée ;
- divergence des PR nº 1 et nº 2 auditée.

## 2. Blockers avant OF-DATA-001

### Blocker G1 — immuabilité de la migration 012

```text
TYPE: GOVERNANCE
STATUS: OPEN
```

Le SQL `012` doit devenir un artefact historique figé. Toute modification future
du registre doit créer une nouvelle migration forward.

### Blocker G2 — documentation de gouvernance contradictoire

```text
TYPE: DOCUMENTATION
STATUS: OPEN
```

Les documents permanents conservent des statuts antérieurs :

- TODO ;
- SUIVI ;
- ROADMAP ;
- CHANGELOG ;
- DECISIONS ;
- README ;
- ARCHITECTURE ;
- DATA_MODEL ;
- plan de branches ;
- handoff ;
- description de PR.

Ils ne doivent plus être utilisés seuls pour conclure que les quatre premiers
gates sont ouverts ou que le runner est totalement vérifié. Le présent audit
daté prime jusqu’à leur réconciliation contrôlée.

### Blocker I1 — PR nº 1 non intégrable dans son état actuel

```text
TYPE: INTEGRATION
STATUS: OPEN
```

PR nº 1 :

```text
STATE: OPEN
DRAFT: TRUE
MERGED: FALSE
MERGEABLE: FALSE
BASE_HEAD: 136abf71f0825075361f8c7446e19c6f6476a3a5
HEAD: 202f23d5a5be961d6f8338984b04655eda336a6b
AHEAD_BY: 183
BEHIND_BY: 7
```

Cause : conflit add/add sur
`schemas/reference/002_country_relationships.sql`.

Recommandation : Strategy B, seulement après autorisation et résolution du
blocker G1.

### Blocker I2 — décision de préservation PR nº 2

PR nº 2 :

```text
STATE: OPEN
DRAFT: TRUE
MERGED: FALSE
MERGEABLE: TRUE
HEAD: 81d32b83e6a87d01c4e66c2c2db00199b4553d70
AHEAD_BY_RELATIVE_TO_AFRICAFUNDS: 5
BEHIND_BY_RELATIVE_TO_AFRICAFUNDS: 52
```

Deux CSV sont déjà préservés par blobs identiques :

- `CANONICAL_INTEGRATION_MATRIX_20260803.csv`
- `OFFICIAL_SOURCE_INVENTORY_20260803.csv`

Trois Markdown restent uniques :

- `AFRICA_MARKET_RATES_MACRO_SOURCE_HANDOFF_20260803.md`
- `NON_REGRESSION_AND_STATUS_RULES_20260803.md`
- `PR1_RESEARCH_ASSET_EXPLOITATION_GUIDE_20260803.md`

Aucune fermeture de PR nº 2 ne doit intervenir avant une décision explicite de
préservation.

## 3. Conditions de sortie

Avant de commencer `OF-DATA-001` :

1. décider et implémenter, dans une phase technique séparée, la règle
   d’immuabilité de `012` ;
2. ajouter les tests de non-régénération historique et relancer le runner ;
3. réconcilier les statuts des documents permanents ;
4. actualiser la description de PR nº 1 ;
5. approuver une stratégie d’intégration ;
6. préserver ou rejeter explicitement les trois Markdown uniques de PR nº 2 ;
7. revalider dynamiquement les HEAD, PR et workflows.

## 4. Point exact de reprise

```text
NEXT_TASK
RESOLVE_OF_ARCH_004_GENERATED_MIGRATION_GOVERNANCE_BLOCKER

THEN
RECONCILE_PERMANENT_GOVERNANCE_DOCUMENTS

THEN
AUTHORIZE_AND_PREPARE_PR1_INTEGRATION_STRATEGY

ONLY_AFTER_ALL_GATES
OF-DATA-001
```

Aucune modélisation `Fund / SubFund / ShareClass` n’a été commencée pendant cet
audit.
