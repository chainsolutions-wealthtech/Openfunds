# Prochaine action autorisée

```text
CURRENT_LOOP: OF-MAP-002 + OF-DATA-001 + OF-LOOP-SOURCE-002 + OF-SOURCE-003
CURRENT_IMPLEMENTED_MIGRATION_CHAIN: 001..038
LAST_REMOTELY_VERIFIED_MIGRATION_CHAIN: 001..019 / RUN 32070768364
CURRENT_STRUCTURAL_CANONICAL_INVENTORY: 294 = 143_CORE + 151_EXTENSIONS (includes migration 038 structure)
LAST_MAPPING_MANIFEST_CLOSED_CANONICAL_SCOPE: BATCH_24 / 260_FIELDS
LAST_REMOTELY_VERIFIED_CANONICAL_UNION: 177 / RUN 32071385088
CURRENT_CLOSED_MAPPING_REGISTRY: BATCH_01..25 / 86_ROWS / 47_OF_IDS / 49_CANONICAL_IDS
BATCH_26_TRACKED_INDEX_IDENTIFIERS: RED_CONTRACT + MIGRATION_038 + DICTIONARY_EXTENSION_READY / REGISTRY_ROWS_NOT_YET_WRITTEN
LAST_REMOTELY_VERIFIED_MAPPING: BATCH_05 / RUN 32071858346
UNMAPPED_OPENFUNDS_IDS_AFTER_BATCH25: 1822
STATUS: FORWARD_ONLY_WORK_IN_PROGRESS_WITH_FAIL_CLOSED_REMOTE_CI
WRITE_GATE: VERIFIED_OF_ID + VERIFIED_FIELD_LEVEL + VERIFIED_CANONICAL_TARGET + EXPLICIT_TRANSFORMATION + USAGE_GATE + TDD_CONTRACT + APPEND_ONLY_DIFF_REVIEW
```

## Gouvernance

Travail exclusivement sur `architecture/africafunds-country-indicators-v0.1`.

PR #1 : **DRAFT / OPEN / UNMERGED**. Ne pas toucher `main`, ne pas retargeter/fusionner la PR, ne pas la passer Ready, ne pas activer production, ne pas déployer et ne pas créer de branche supplémentaire.

La surface GitHub connectée ne fournit toujours pas d'attestation exploitable des checks récents. Donc :

```text
IMPLEMENTED != REMOTELY_GREEN
```

Ne jamais inventer de numéro de run ou de verdict CI.

## Chaîne de migrations implémentée

```text
020_LISTING_QUOTE_UNIT_SEMANTICS
021_LISTING_BUSINESS_STATUS
022_LISTING_VENDOR_IDENTIFIER_SCHEMES
023_LISTING_IDENTIFIER_SUBJECT
024_LISTING_INCEPTION_PRICE
025_SHARE_CLASS_TRADING_PRICE_FREQUENCY
026_SHARE_CLASS_NAV_FREQUENCY_DETAIL
027_VALUATION_TIME_SEMANTICS
028_SHARE_CLASS_MULTICURRENCY_DEALING
029_ENTITY_LIFECYCLE_PHASE
030_ENTITY_LIFECYCLE_EVENT_TYPES
031_SHARE_CLASS_INVESTMENT_STATUS
032_SHARE_CLASS_ETF_FLAG
033_FUND_PASSIVE_FLAG
034_FUND_REPLICATION_METHODOLOGY
035_SHARE_CLASS_BENCHMARK_COMPONENTS
036_BENCHMARK_COMPONENT_IDENTIFIERS
037_SHARE_CLASS_TRACKED_INDEX
038_TRACKED_INDEX_IDENTIFIERS
```

Aucune migration historique n'est réécrite. Toutes les évolutions 020+ sont forward-only.

## Vague ETF / benchmark / index

### Batch 20 — ETF Share Class

`OFST010580` -> `fund.share_class_profile.is_etf`.

ETF reste une assertion Share Class et n'est jamais inféré depuis un attribut Fund.

### Batch 21 — Fund passive

`OFST010720` -> `fund.fund_profile.is_passive`.

Passif/index-tracking Fund ne signifie pas automatiquement ETF Share Class.

### Batch 22 — réplication

```text
OFST010900 -> fund_profile.replication_methodology_first_level
OFST010901 -> fund.replication_methodology_detail rows
```

Les valeurs pipe d'un mode hybrid sont normalisées en lignes ; aucun pipe string canonique.

### Batch 23 — benchmark

`OFST023200 Benchmark` -> `fund.share_class_benchmark_component` : ordre, nom source-preserved et poids explicite optionnel.

Les benchmarks composites sont normalisés en composantes ordonnées.

### Batch 24 — benchmark Bloomberg tickers

`OFST023205` -> `fund.benchmark_component_identifier`, aligné par ordre de composante.

Import/export restent `NO` derrière `EXPLICIT_PROPRIETARY_IDENTIFIER_USAGE_REVIEW`.
Ce gate est une politique projet et ne doit pas être présenté comme un avertissement de licence Openfunds.

### Batch 25 — tracked ETF index

Migration 037 : `fund.share_class_tracked_index`.

Mappings fermés dans le registre :

```text
MAP-000083 OFST023800 -> INDEX_NAME
MAP-000084 OFST023805 -> INDEX_CURRENCY_ID
MAP-000085 OFST023805 -> INDEX_CURRENCY_MODE
MAP-000086 OFST023810 -> INDEX_TYPE
```

Invariants critiques :

- valeur `OFST023805` non vide : ISO4217 explicite ;
- valeur `OFST023805` vide : `LOCAL_CURRENCY`, `index_currency_id = NULL` ;
- aucune inférence depuis la devise de Share Class ;
- index type réversible : PRICE / PERFORMANCE / PERFORMANCE_NET_DIVIDENDS / PERFORMANCE_GROSS_DIVIDENDS ;
- benchmark et tracked index restent deux concepts distincts ; leur cohérence peut être validée mais pas fusionnée silencieusement.

Le commit de Batch25 a été vérifié append-only : exactement quatre lignes nouvelles, aucune ligne historique modifiée.

## Batch 26 — tracked-index vendor identifiers : RED en cours

Migration 038 existe et est enregistrée :

```text
fund.tracked_index_identifier
identifier_scheme: BLOOMBERG | RIC
```

Extension dictionnaire :

`data/dictionary/extensions/tracked_index_identifier_v1/` — 16 champs physiques.

Contrat RED : `tests/test_openfunds_mapping_batch26.py`.

Mappings attendus, **non encore écrits dans le registre** :

```text
OFST023820 Bloomberg Code Of Underlying Index
  -> IDENTIFIER_VALUE / IDENTIFIER_SCHEME=BLOOMBERG / NORMALIZED_VALUE

OFST023830 Reuters Code Of Underlying Index
  -> IDENTIFIER_VALUE / IDENTIFIER_SCHEME=RIC / NORMALIZED_VALUE
```

Règles :

- 6 lignes attendues `MAP-000087..092` ;
- `ONE_TO_MANY` ;
- import/export `NO` jusqu'à revue explicite d'usage propriétaire ;
- `TRACKED_INDEX_SUBJECT_REQUIRED` ;
- RIC est case-sensitive : trim outer whitespace seulement, aucune conversion upper/lower ;
- le gate d'usage est projet, pas un avertissement Openfunds inventé.

## État de couverture fermé au Batch25

```text
REVIEWED_MAPPING_ROWS:    86
MAPPED_EXTERNAL_IDS:      47
UNMAPPED_EXTERNAL_IDS:  1822
MAPPED_CANONICAL_IDS:     49
```

Le manifest OF-MAP doit encore être réconcilié de Batch24 vers Batch25, puis vers Batch26 seulement après écriture append-only vérifiée des six lignes 087..092.

## CI structurelle

`OF-MAP-002` est câblé jusqu'aux contrats B25/B26 et aux extensions 037/038.

`migration-runner` est câblé à 38 migrations et exécute les tests de modèles 037/038 ; il vérifie l'existence de :

```text
fund.share_class_tracked_index
fund.tracked_index_identifier
```

Ce câblage ne constitue pas une attestation GREEN distante.

## Invariants permanents

- quote-unit ≠ devise économique ;
- Listing status ≠ `is_current` ;
- Listing identity ≠ iNAV identity ;
- lifecycle phase ≠ broad lifecycle status ;
- investment status ≠ lifecycle phase ;
- reference Share Class currency ≠ additional dealing currencies ;
- timezone label ≠ timezone IANA ;
- absence de date source ≠ date inventée ;
- ETF Share Class ≠ passive Fund ;
- benchmark ≠ tracked index ;
- vendor identifier ≠ display name ;
- Reuters/RIC case must be preserved ;
- local index currency ≠ inferred Share Class currency.

## Gates identifiants

```text
SEDOL: IMPORT/EXPORT NO — EXPLICIT_SEDOL_LICENSING_CLEARANCE
BLOOMBERG/RIC: IMPORT/EXPORT NO — EXPLICIT_PROPRIETARY_IDENTIFIER_USAGE_REVIEW
```

## Prochaine unité sûre

1. reverrouiller le registre au SHA contenant `MAP-000086` ;
2. écrire uniquement `MAP-000087..092` pour Batch26 ;
3. vérifier le diff du commit : exactement six lignes ajoutées, zéro modification historique ;
4. réconcilier le mapping manifest à Batch25 puis Batch26 ;
5. revalider PR/head/checks ;
6. mettre à jour `OPENFUNDS_MAPPING.md`, `SUIVI.md`, `TODO.md`, `CHANGELOG.md` et le corps PR #1 ;
7. continuer le prochain groupe officiel seulement après RED ;
8. poursuivre en parallèle OF-SOURCE-003 et les gaps institutionnels avec preuves primaires.

## Couverture institutionnelle inchangée

```text
ORGANIZATION_SCOPE_ROLES: 199 = 195 VALIDATED + 4 PENDING
COUNTRY_COVERAGE: 53 / 54
UNCOVERED: ERYTHREE
PENDING: EGX INDEX_PROVIDER / NSE INDEX_PROVIDER / NGX INDEX_PROVIDER / CMA MONETARY_UNION
```

## Gaps fonctionnels

```text
COUNTRIES_COMPLETE_FOR_7_REQUIRED_GROUPS: 0 / 54
CAPITAL_MARKET_REGULATION_MISSING:       18
EXCHANGE_MISSING:                        17
FISCAL_DEBT_MISSING:                     40
FUND_REGULATION_MISSING:                 19
INSURANCE_PENSION_REGULATION_MISSING:    44
MONETARY_AUTHORITY_MISSING:              11
STATISTICS_MISSING:                       3
```

## Blockers externes

```text
ERYTHREE                PRIMARY_OFFICIAL_SOURCE_NOT_VERIFIED
PERSISTENT_DB           OPENFUNDS_DATABASE_URL / DURABLE_RUNTIME_NOT_CONFIGURED
IMMUTABLE_RAW_STORE     NOT_CONFIGURED
SEDOL_RUNTIME           EXPLICIT_LICENSING_CLEARANCE_REQUIRED
BLOOMBERG_RIC_RUNTIME   EXPLICIT_PROPRIETARY_IDENTIFIER_USAGE_REVIEW_REQUIRED
COMPLETE_HISTORIES      NOT_LOADED
BENCHMARK_RFR_MAR       NOT_FULLY_VALIDATED
WTI_WTI_BENCH           NOT_ACTIVE
PRODUCTION_API_UI       NOT_IMPLEMENTED
PRODUCTION_DEPLOY       NOT_CONFIGURED
```

## Checkpoint courant

`docs/00_PROJECT/OF_MAP_002_BATCHES_21_26_AND_MIGRATIONS_033_038_CHECKPOINT_20260821.md`

## Interdictions maintenues

Ne pas inventer de données, ne pas matérialiser 1 869 faux `UNMAPPED`, ne pas réécrire les migrations ou mappings historiques, ne pas activer les identifiants gated, ne pas inférer une devise absente, ne pas modifier `main`, ne pas fusionner/retargeter PR #1 et ne pas créer de nouvelle branche.
