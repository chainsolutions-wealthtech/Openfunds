# OF-MAP-002 — Bootstrap du registre de mapping Openfunds v2.13.0 → canonique

Date : 2026-08-17

## Verdict

Le socle technique de `OF-MAP-002` est **GREEN** et prêt à recevoir uniquement des mappings effectivement revus.

Ce jalon ne prétend pas que le mapping Openfunds est complet. Il établit le mécanisme gouverné qui empêchera les mappings inventés, les identifiants inconnus et les dérives de source.

## Sources de vérité verrouillées

```text
OPENFUNDS_VERSION: 2.13.0
OFFICIAL_FIELD_RECORDS: 1869
OFFICIAL_SOURCE_SHA256: 40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4
CANONICAL_DICTIONARY_VERSION: 1.0.0
CANONICAL_FIELD_COUNT: 143
REGISTRY_SEPARATOR: ;
```

Le registre reste volontairement vide à cette étape. Les 1869 champs non revus ne sont pas matérialisés en fausses lignes `UNMAPPED` ; ils sont calculés comme différence entre l'inventaire officiel checksum-locké et les OF-ID réellement présents dans le registre.

## Contrats implémentés

Le validator `scripts/validate_openfunds_mapping_registry.py` :

1. vérifie le SHA-256 du PDF officiel archivé ;
2. reparcourt réellement le PDF et reconstruit les 1869 OF-ID officiels ;
3. reconstruit les 143 FIELD_ID canoniques depuis `data/dictionary/spec_v1/` ;
4. impose le CSV `;` et son en-tête gouverné ;
5. refuse un OF-ID absent de l'inventaire officiel ;
6. refuse un FIELD_ID canonique absent du dictionnaire ;
7. refuse les `MAPPING_ID` dupliqués ;
8. conserve les templates pays `XX` sans expansion ;
9. impose version, checksum, référence de source, statut, information loss et capacités import/export explicites ;
10. n'écrit aucun artefact dans le repository pendant la validation.

## Cycle TDD et incidents utiles

```text
INITIAL_RED_RUN:       32062460096
CAUSE:                 validator absent

UNIT_GREEN_CLI_FAIL:   32064570135
CAUSE:                 import package incompatible avec exécution directe scripts/*.py

CLI_RED_RUN:           32064692636
CAUSE:                 test de non-régression CLI ajouté avant correctif

CLI_FIXED_GUARD_FAIL:  32064744006
CAUSE:                 logique métier GREEN mais bytecode Python rendait git status non vide

FINAL_GREEN_RUN:       32064814922
PYTHON_3_11:           SUCCESS
PYTHON_3_12:           SUCCESS
OFFICIAL_PDF_PARSE:    SUCCESS
CANONICAL_EXPANSION:   SUCCESS
REPO_UNCHANGED_GUARD:  SUCCESS
```

Le garde-fou Git n'a pas été assoupli. `PYTHONDONTWRITEBYTECODE=1` empêche simplement Python de créer des `__pycache__` dans le checkout.

## Baseline vérifiée

```text
REVIEWED_MAPPING_ROWS: 0
MAPPED_EXTERNAL_IDS:   0
UNMAPPED_EXTERNAL_IDS: 1869
MAPPED_CANONICAL_IDS:  0
```

## Règles pour les lots suivants

- aucun mapping ne doit être créé à partir du seul nom d'un champ ;
- chaque OF-ID doit être contrôlé dans le Field List officiel v2.13.0 ;
- la cible doit exister dans le dictionnaire canonique gouverné ;
- une différence de représentation doit être déclarée `TRANSFORMED`, pas `DIRECT` ;
- les constantes, normalisations, one-to-many, many-to-one et pertes d'information doivent être explicites ;
- une ambiguïté reste `TO_CONFIRM` ;
- aucun champ officiel n'est inventé ;
- aucun template `XX` n'est développé en variantes nationales dans le registre maître ;
- le document officiel archivé reste immuable.

## Prochaine unité

Renforcer le validator sur l'unicité du couple `(EXTERNAL_FIELD_ID, CANONICAL_FIELD_ID)` et la cohérence `CANONICAL_ENTITY ↔ FIELD_ID`, puis introduire un premier lot restreint de mappings sémantiquement démontrés.
