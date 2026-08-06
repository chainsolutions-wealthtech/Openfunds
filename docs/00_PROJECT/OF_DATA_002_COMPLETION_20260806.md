# OF-DATA-002 — Rapport de clôture du dictionnaire canonique

```text
DATE: 2026-08-06
TASK_ID: OF-DATA-002
LOOP_ID: OF-LOOP-DATA-002
STATUS: VERIFIED_COMPLETE
BRANCH: architecture/africafunds-country-indicators-v0.1
START_HEAD: 0a48c14999a5f173fa5ab3ce4b91109e24092c2c
INITIAL_TECHNICAL_HEAD: 2d4c8c860aedce30a25cfc9ffcda1ab6ec820a43
MANIFEST_ALIGNMENT_HEAD: ecb2713c6b7ba591bc86b977ca7d35c455465174
VALIDATED_TECHNICAL_HEAD: 1fb49075abdfb958e152accf915c37ac86b9a54e
PRODUCTION_DEPLOYED: NO
REAL_FUND_DATA_LOADED: NO
OF_DATA_003_STARTED: NO
```

## 1. Résultat fonctionnel

Le cœur canonique Fund/SubFund/ShareClass dispose désormais d’un dictionnaire
machine-readable complet pour toutes les colonnes physiques créées par la
migration gouvernée `015_FUND_SUBFUND_SHARECLASS_CORE`.

```text
PHYSICAL_TABLES: 10
PHYSICAL_FIELDS: 143
ATTRIBUTES_PER_EXPANDED_FIELD: 36
AUTHORING_FORMAT: GOVERNED_JSON_PACKAGE
CSV_DELIMITER: ;
OPENFUNDS_IDENTIFIERS_INVENTED: 0
```

La déclaration de complétude est strictement limitée à `CANONICAL_FUND_CORE`.
Elle ne couvre pas les autres schémas, D00–D17, les objets métier non encore
présents dans le runtime ni le mapping officiel Openfunds.

## 2. Source d’authoring unique

```text
data/dictionary/spec_v1/
```

Le paquet contient neuf fichiers gouvernés :

1. `00_metadata.json` ;
2. `10_tables_identity.json` ;
3. `11_tables_profiles_events.json` ;
4. `12_tables_names_identifiers_structure.json` ;
5. `20_column_semantics.json` ;
6. `21_column_semantics.json` ;
7. `22_column_semantics.json` ;
8. `30_allowed_values.json` ;
9. `31_foreign_keys.json`.

La séparation en paquet évite un fichier monolithique difficile à réviser tout
en conservant une seule source logique d’authoring. Les sorties générées ne sont
pas éditées manuellement.

## 3. Contrat des champs

Chaque champ expansé contient exactement :

```text
FIELD_ID
TECHNICAL_NAME
FUNCTIONAL_NAME_FR
FUNCTIONAL_NAME_EN
DEFINITION
DEFINITION_EN
DOMAIN_CODE
ENTITY_CODE
DATA_TYPE
FORMAT
UNIT_CODE
CURRENCY_RULE
NULLABILITY
CARDINALITY
ALLOWED_VALUES
CONSTRAINTS
VALIDATION_RULE
NORMALIZATION_RULE
CALCULATION_RULE
SOURCE_ROLE
SOURCE_PRIORITY_RULE
HISTORY_METHOD
SENSITIVITY_LEVEL
CONFIDENCE_RULE
OPENFUNDS_FIELD_ID
EXTERNAL_MAPPINGS
EXAMPLE_VALUE
STATUS
SCHEMA_VERSION
CREATED_AT
UPDATED_AT
PHYSICAL_SCHEMA
PHYSICAL_TABLE
PHYSICAL_COLUMN
PROVENANCE_PATH
DEFINITION_SOURCE
```

Les identifiants suivent :

```text
OF_<DOMAIN>_<ENTITY>_<FIELD>
```

Les IDs et les noms techniques sont uniques. Un changement sémantique doit créer
un nouvel identifiant ou une nouvelle version ; un simple renommage physique doit
conserver une trace de compatibilité.

## 4. Couverture physique

| Entité | Table | Champs |
|---|---|---:|
| `FUND_ENTITY` | `fund.entity` | 5 |
| `FUND_ENTITY_STATE` | `fund.entity_state` | 15 |
| `FUND_PROFILE` | `fund.fund_profile` | 18 |
| `SUBFUND_PROFILE` | `fund.subfund_profile` | 16 |
| `SHARE_CLASS_PROFILE` | `fund.share_class_profile` | 19 |
| `FUND_ENTITY_EVENT` | `fund.entity_event` | 11 |
| `FUND_EVENT_PARTICIPANT` | `fund.event_participant` | 6 |
| `FUND_ENTITY_NAME` | `fund.entity_name` | 18 |
| `FUND_ENTITY_IDENTIFIER` | `fund.entity_identifier` | 18 |
| `FUND_STRUCTURE_RELATIONSHIP` | `fund.structure_relationship` | 17 |
| **Total** |  | **143** |

Le test compare chaque colonne du paquet à la déclaration SQL top-level de la
migration `015`. Les lignes SQL de continuation telles que `references` ne sont
pas interprétées comme des colonnes.

## 5. Sorties reproductibles

Le générateur :

```text
scripts/generate_canonical_field_dictionary.py
```

s’appuie sur :

```text
scripts/canonical_field_dictionary.py
```

et produit :

```text
build/dictionary/CANONICAL_FIELD_DICTIONARY_V1.json
build/dictionary/CANONICAL_FIELD_DICTIONARY_V1.csv
build/dictionary/CANONICAL_FIELD_DICTIONARY_V1.md
```

Le CSV est UTF-8 et séparé par `;`.

### Empreintes gouvernées

```text
AUTHORITATIVE_PACKAGE_SHA256
e07ded9d02a0c334ac8c2e0368d24d903d82f35716585a46d6ddf7c375e18e95

EXPANDED_JSON_SHA256
dadc834e31b677bbd4e3e5e4406d985a73724d5f3fd86530518b08b7d086eeb4

CSV_SHA256
374c10b8ac9d92d0f025400933cfcb2e41970f1f4f7bd4f95d9bce08e536f068

MARKDOWN_SHA256
3827b74da9c40f561608b196e047bf8254f8c20e0b58fac33b6ca485b13d2138
```

Le manifeste `1.0.2` relie également le JSON Schema, la bibliothèque, le
générateur, les tests et le workflow à leurs blobs Git réels.

## 6. Politique Openfunds

Aucun catalogue officiel Openfunds versionné, licencié et archivé n’est présent
dans le dépôt. La règle vérifiée pour les 143 champs est donc :

```text
OPENFUNDS_FIELD_ID = null
openfunds_mapping_status = NOT_MAPPED_OFFICIAL_CATALOGUE_UNAVAILABLE
```

Aucun identifiant externe n’a été inventé. `OF-MAP-001` puis `OF-MAP-002`
restent les portes obligatoires pour un mapping officiel.

## 7. Preuves CI finales

### Canonical Field Dictionary

```text
RUN_ID: 31113488180
HEAD_SHA: 1fb49075abdfb958e152accf915c37ac86b9a54e
CONCLUSION: SUCCESS
```

| Job | Résultat |
|---|---|
| `validate-dictionary (3.11)` | `SUCCESS` |
| `validate-dictionary (3.12)` | `SUCCESS` |

Chaque job a réussi :

- la génération et la vérification du manifeste ;
- les sept tests contractuels ;
- la publication des artefacts de revue.

### Artefacts

| Nom | ID | Taille | Digest |
|---|---:|---:|---|
| `canonical-field-dictionary-py3.11` | `8972675555` | 34 300 octets | `sha256:a237c13e85fc486dcab515b3508fd92479596438acdb327679920d442596b67f` |
| `canonical-field-dictionary-py3.12` | `8972676098` | 34 300 octets | `sha256:a237c13e85fc486dcab515b3508fd92479596438acdb327679920d442596b67f` |

Les deux versions Python produisent donc des archives de même taille et de même
digest.

### Collector Tests

```text
RUN_ID: 31113488273
HEAD_SHA: 1fb49075abdfb958e152accf915c37ac86b9a54e
CONCLUSION: SUCCESS
```

Les jobs suivants sont verts :

- Python 3.11 unit tests ;
- Python 3.12 unit tests ;
- BCEAO FX fixture smoke test ;
- PostgreSQL FX loader integration, y compris double chargement, idempotence,
  lignée et observations courantes.

## 8. Chronologie transparente des corrections

### Commit initial

```text
2d4c8c860aedce30a25cfc9ffcda1ab6ec820a43
feat(dictionary): establish canonical fund field catalogue [OF-DATA-002]
```

Il a ajouté les 18 nouveaux fichiers du dictionnaire et modifié
`DATA_DICTIONARY.md`, sans SQL ni migration.

### Correction du manifeste

Le premier workflow a démontré que les empreintes attendues du JSON expansé et
du CSV provenaient d’une variante locale, alors que le paquet et le Markdown
étaient stables. Aucun résultat n’a été déclaré vert prématurément.

```text
ecb2713c6b7ba591bc86b977ca7d35c455465174
fix(dictionary): align manifest with committed generator outputs [OF-DATA-002]
```

Ce commit a uniquement aligné le manifeste sur les sorties du générateur
réellement commité et remplacé des SHA-256 non prouvés de l’implémentation par
les blobs Git observables.

### Correction du test SQL

Le workflow suivant a validé le manifeste mais montré que l’extracteur de test
acceptait une ligne SQL indentée de continuation `references` comme colonne.

```text
1fb49075abdfb958e152accf915c37ac86b9a54e
fix(dictionary): parse governed SQL columns at top level [OF-DATA-002]
```

Ce commit a limité l’extraction aux déclarations top-level et mis à jour la
référence du blob de test dans le manifeste. Le SQL, le paquet et les sorties
n’ont pas changé.

Aucun force-push, squash, amendement, réécriture ou suppression d’historique n’a
été utilisé.

## 9. Matrice d’acceptation

```text
AUTHORING_FORMAT_SELECTED: YES
SINGLE_LOGICAL_AUTHORING_SOURCE: YES
PHYSICAL_TABLE_COUNT_10: PASSED
PHYSICAL_FIELD_COUNT_143: PASSED
REQUIRED_ATTRIBUTE_COUNT_36: PASSED
FIELD_ID_UNIQUENESS: PASSED
TECHNICAL_NAME_UNIQUENESS: PASSED
MIGRATION_015_COLUMN_RECONCILIATION: PASSED
CSV_UTF8_SEMICOLON: PASSED
OUTPUT_REPRODUCIBILITY: PASSED
PACKAGE_SHA256: PASSED
EXPANDED_JSON_SHA256: PASSED
CSV_SHA256: PASSED
MARKDOWN_SHA256: PASSED
PYTHON_3_11: PASSED
PYTHON_3_12: PASSED
ARTIFACT_DIGEST_EQUALITY: PASSED
OPENFUNDS_IDENTIFIER_INVENTION: ZERO
RUNTIME_SCHEMA_MODIFIED: NO
REAL_DATA_IMPORTED: NO
PRODUCTION_DEPLOYED: NO
```

## 10. Limites et travaux différés

Cette boucle ne fournit pas encore :

- le catalogue D00–D17 ;
- le dictionnaire exhaustif de `ref.*`, `source.*` et `market.*` ;
- les objets NAV, AUM, dividendes, portefeuilles, frais, documents, prestataires,
  réglementaire, ESG et analytiques non présents dans le runtime ;
- le catalogue officiel Openfunds ;
- un mapping Openfunds → canonique ;
- des données réelles de fonds ;
- une base persistante de production ;
- une API ou une UI.

## 11. Prochaine porte

```text
NEXT_CANDIDATE: OF-DATA-003
TITLE: Centraliser les définitions D00-D17
STATUS: NOT_STARTED
AUTHORIZATION: REQUIRED
```

`OF-DATA-003` devra commencer par un audit dynamique des définitions existantes,
figer le nombre réel d’objets et distinguer explicitement `RAW`, `METADATA`,
`EVENT` et `CALCULATED`. Il ne doit pas transformer une définition documentaire
en série collectée, complète ou active sans preuve séparée.
