# OF-DATA-002 — Bootstrap du dictionnaire canonique

```text
DATE: 2026-08-06
LOOP_ID: OF-LOOP-DATA-002
TASK_ID: OF-DATA-002
START_HEAD: 0a48c14999a5f173fa5ab3ce4b91109e24092c2c
BRANCH: architecture/africafunds-country-indicators-v0.1
STATUS: IMPLEMENTATION_READY_FOR_CI
```

## Audit de départ

Le HEAD de la PR nº 1 a été résolu dynamiquement avant écriture. La PR demeure
ouverte, draft et non fusionnée.

Constats vérifiés :

- `DATA_DICTIONARY.md` définissait les attributs obligatoires mais déclarait le
  catalogue non peuplé ;
- `ADR-024` proposait un format machine-readable sans choisir le format ;
- la migration gouvernée `015` contient dix tables et 143 colonnes physiques
  canoniques ;
- aucun catalogue officiel Openfunds versionné n’est présent ;
- `OF-DATA-003` reste une porte séparée pour le catalogue D00–D17.

## Choix d’implémentation

La première version complète concerne le cœur Fund/SubFund/ShareClass, dépendance
immédiate des futurs imports de fonds.

```text
SOURCE D’AUTHORING
data/dictionary/spec_v1/

ARTEFACTS GÉNÉRÉS
build/dictionary/CANONICAL_FIELD_DICTIONARY_V1.json
build/dictionary/CANONICAL_FIELD_DICTIONARY_V1.csv
build/dictionary/CANONICAL_FIELD_DICTIONARY_V1.md

RÉSUMÉ HUMAIN COMMITÉ ET CONTRÔLÉ
docs/04_DATA_GOVERNANCE/CANONICAL_FIELD_DICTIONARY_V1.md
```

Livrables préparés : JSON Schema, manifeste SHA-256, générateur, tests de
concordance avec la migration `015`, workflow Python 3.11/3.12 et ADR-031.

## Critères de clôture

- exactement 143 champs et dix entités ;
- 36 attributs présents pour chaque champ expansé ;
- IDs et noms techniques uniques ;
- concordance table/colonne exacte avec la migration `015` ;
- CSV UTF-8 séparé par `;` ;
- sorties déterministes et SHA-256 vérifiés ;
- aucun mapping Openfunds inventé ;
- workflows du SHA technique terminés en succès.

## Interdictions conservées

Aucune nouvelle branche, fusion, donnée réelle, migration historique, base
persistante, activation de calcul, import NAV/AUM ou production n’est autorisée
par cette boucle.
