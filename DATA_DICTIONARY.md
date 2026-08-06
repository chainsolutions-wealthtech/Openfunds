# DICTIONNAIRE DE DONNÉES CANONIQUE

## 1. Statut du périmètre v1

```text
TASK: OF-DATA-002
SCOPE: CANONICAL_FUND_CORE
STATUS: IMPLEMENTED_AWAITING_CI
DICTIONARY_VERSION: 1.0.0
FIELD_COUNT: 143
ENTITY_COUNT: 10
AUTHORING_FORMAT: JSON_PACKAGE
```

La version 1 inventorie intégralement les colonnes physiques du schéma canonique
`fund.*` introduit par la migration gouvernée
`015_FUND_SUBFUND_SHARECLASS_CORE`. La déclaration de complétude ne s’étend pas
aux autres schémas, aux objets non encore modélisés, à D00–D17 ou au mapping
officiel Openfunds.

## 2. Source d’authoring unique

```text
data/dictionary/spec_v1/
```

Cette spécification compacte contient le contrat des tables et colonnes, les
définitions bilingues, les valeurs par défaut, les énumérations, les clés
étrangères, la gouvernance et les exclusions.

Les sorties suivantes sont générées sous `build/dictionary/` :

```text
CANONICAL_FIELD_DICTIONARY_V1.json   # vue JSON expansée, 143 champs
CANONICAL_FIELD_DICTIONARY_V1.csv    # vue UTF-8 séparée par ;
CANONICAL_FIELD_DICTIONARY_V1.md     # vue humaine
```

Le résumé humain commis est `docs/04_DATA_GOVERNANCE/CANONICAL_FIELD_DICTIONARY_V1.md`. La vue exhaustive est générée sous `build/dictionary/` et publiée comme artefact CI.

Le manifeste est :

```text
data/dictionary/CANONICAL_FIELD_DICTIONARY_MANIFEST_V1.json
```

Les artefacts générés ne sont jamais une source d’authoring concurrente.

## 3. Commandes

Générer les vues complètes et contrôler le manifeste :

```bash
python scripts/generate_canonical_field_dictionary.py \
  --check-manifest
```

Exécuter les tests :

```bash
python -m unittest -v tests.test_canonical_field_dictionary
```

## 4. Attributs obligatoires

Chaque champ expansé possède 36 attributs :

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

## 5. Convention des identifiants

```text
OF_<DOMAIN>_<ENTITY>_<FIELD>
```

Exemples :

```text
OF_FUND_FUND_ENTITY_ENTITY_ID
OF_FUND_FUND_PROFILE_STRUCTURE_TYPE
OF_FUND_SHARE_CLASS_PROFILE_CURRENCY_ID
OF_FUND_FUND_ENTITY_NAME_NORMALIZED_NAME
OF_FUND_FUND_STRUCTURE_RELATIONSHIP_RELATIONSHIP_TYPE
```

Une rupture sémantique crée un nouvel identifiant ou une nouvelle version. Un
renommage technique conserve une trace de compatibilité.

## 6. Couverture

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

Les vues courantes et les projections dérivées ne sont pas dupliquées comme
champs d’authoring.

## 7. Principes sémantiques

- l’identité stable est distincte des noms et identifiants externes ;
- un nom publié est distinct de sa forme normalisée ;
- un fonds autonome ne reçoit pas de faux compartiment ;
- les chemins `FUND → SHARE_CLASS` et `FUND → SUBFUND → SHARE_CLASS` restent
  distincts ;
- états, profils, noms, identifiants et relations sont historisés ;
- événements et participants sont append-only ;
- `NULL`, `UNKNOWN`, `NOT_APPLICABLE` et `NOT_PUBLISHED` restent distincts ;
- date métier et connaissance système restent distinctes ;
- unité et devise ne sont jamais implicites ;
- provenance, localisateur et note de source restent séparés.

## 8. Politique Openfunds

Aucun catalogue officiel Openfunds versionné et archivé n’est disponible dans le
dépôt. La règle obligatoire est donc :

```text
OPENFUNDS_FIELD_ID = null
openfunds_mapping_status = NOT_MAPPED_OFFICIAL_CATALOGUE_UNAVAILABLE
```

Aucun identifiant ou mapping ne doit être inventé. `OF-MAP-001` et
`OF-MAP-002` restent nécessaires.

## 9. Contrôles automatisés

Le workflow `.github/workflows/canonical-field-dictionary.yml` exécute sur
Python 3.11 et 3.12 :

- expansion et validation de la spécification compacte ;
- concordance exacte avec les 143 colonnes de la migration `015` ;
- unicité des IDs et noms techniques ;
- contrôle des attributs, valeurs autorisées et clés étrangères ;
- interdiction des mappings Openfunds inventés ;
- production du CSV `;` ;
- vérification des SHA-256 ;
- génération déterministe de la vue Markdown exhaustive ;
- contrôle du résumé humain commis (périmètre, volumétrie et limites) ;
- publication des trois artefacts générés pour revue.

## 10. Extensions non encore complètes

La v1 ne couvre pas encore `ref.*`, `source.*`, `market.*`, D00–D17, les objets
NAV/AUM/dividendes/portefeuilles/frais/documents/prestataires non modélisés, le
réglementaire, l’ESG, l’analytique ni le mapping officiel Openfunds.

`OF-DATA-003` doit traiter séparément le catalogue D00–D17, sans élargir
silencieusement le statut de cette version.
