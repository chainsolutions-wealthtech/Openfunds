# Prochaine action autorisée

```text
CURRENT_LOOP: OF-MAP-002 + OF-DATA-001_LISTING_EXTENSIONS + OF-LOOP-SOURCE-002 + OF-SOURCE-003
CURRENT_TASK: LISTING_BATCHES_06_09_REMOTE_CI_ATTESTATION_PENDING / BATCH_10_CANDIDATE_AUDIT / FUNCTIONAL_INSTITUTIONAL_GAPS
LAST_VERIFIED_WAVE: 15
LAST_REMOTELY_VERIFIED_MIGRATION_CHAIN: 001..019_GREEN / RUN 32070768364
CURRENT_IMPLEMENTED_MIGRATION_CHAIN: 001..022
LAST_REMOTELY_VERIFIED_MAPPING: BATCH_05_GREEN / RUN 32071858346
CURRENT_IMPLEMENTED_MAPPING: BATCH_01..09 / 28_ROWS / 15_OF_IDS
LAST_REMOTELY_VERIFIED_CANONICAL_UNION: 177_FIELDS / RUN 32071385088
CURRENT_IMPLEMENTED_CANONICAL_INVENTORY: 180_FIELDS = 143_CORE + 34_LISTING_V1 + 2_QUOTE_UNIT_V1 + 1_LISTING_STATUS_V1
NEXT_UNIT: BATCH_10_LISTING_IDENTIFIER_OR_INAV_AUDIT + REMOTE_CI_ATTESTATION + FUNCTIONAL_INSTITUTIONAL_GAP_WAVES
STATUS: FORWARD_ONLY_WORK_IN_PROGRESS_WITH_FAIL_CLOSED_REMOTE_CI_GATES
WRITE_GATE: VERIFIED_OF_ID + VERIFIED_OBJECT_LEVEL + VERIFIED_CANONICAL_FIELD_ID + EXPLICIT_TRANSFORMATION + USAGE_OR_LICENCE_GATE + TDD_RED
```

## État gouverné — 18 août 2026

Le travail reste exclusivement sur :

```text
architecture/africafunds-country-indicators-v0.1
```

La PR #1 reste **DRAFT / OPEN / UNMERGED**. Ne pas toucher `main`, ne pas retargeter ou fusionner la PR, ne pas activer de calcul production et ne pas déployer sans gate explicite.

## Règle d'attestation

Le connecteur GitHub disponible dans la conversation ne remonte actuellement pas les runs `push` ni des status checks exploitables pour les nouveaux HEAD. Par conséquent :

```text
IMPLEMENTED != REMOTELY_GREEN
```

Ne jamais inventer un numéro de run ou un verdict CI. Le dernier état distant effectivement attesté reste :

```text
MIGRATIONS: 001..019 GREEN / 32070768364
CANONICAL UNION: 177 FIELDS GREEN / 32071385088
MAPPING: BATCH_05 GREEN / 32071858346
```

## Migrations Listing implémentées après le dernier GREEN distant

```text
020_LISTING_QUOTE_UNIT_SEMANTICS      ORDER 200
021_LISTING_BUSINESS_STATUS           ORDER 210
022_LISTING_VENDOR_IDENTIFIER_SCHEMES ORDER 220
```

### Migration 020

Ajoute à `fund.listing` :

```text
trading_quote_unit_code
trading_quote_unit_factor
```

Décision : `GBX`, `EUX`, `USX` et codes similaires ne sont pas injectés comme fausses devises autonomes dans `ref.currency`.

Aucune devise parentale ni facteur n'est inféré du code seul.

Extension dictionnaire :

```text
data/dictionary/extensions/listing_quote_unit_v1/
FIELD_COUNT: 2
```

### Migration 021

Ajoute :

```text
fund.listing.listing_status
NULLABLE
ALLOWED: PLANNED / ACTIVE / SUSPENDED / DELISTED
```

`listing_status` est un statut métier, strictement distinct du `is_current` bitemporel. Une absence de statut source reste NULL ; aucun `DEFAULT ACTIVE` canonique.

Extension dictionnaire :

```text
data/dictionary/extensions/listing_status_v1/
FIELD_COUNT: 1
```

### Migration 022

Étend les schemes de `fund.listing_identifier` :

```text
SEDOL
TICKER
LOCAL_CODE
OTHER
BLOOMBERG
RIC
```

`BLOOMBERG` et `RIC` restent Listing-level et ne sont pas ajoutés à `fund.entity_identifier`.

## Inventaire canonique courant

```text
CORE migration 015:          143
listing_v1 migration 019:     34
quote_unit_v1 migration 020:   2
listing_status_v1 migration 021: 1
TOTAL IMPLEMENTED:           180
```

Le validateur reste collision-free et accepte plusieurs extensions. Ne jamais réécrire `listing_v1` pour faire croire que les champs 020/021 existaient en migration 019.

## OF-MAP-002 — état implémenté jusqu'à Batch 09

```text
REVIEWED_MAPPING_ROWS: 28
MAPPED_EXTERNAL_IDS: 15
UNMAPPED_EXTERNAL_IDS: 1854
MAPPED_CANONICAL_IDS: 16
CANONICAL_FIELDS_AVAILABLE: 180
```

### Batch 06

```text
MAP-000017  OFST062030 MIC -> LISTING.VENUE_MIC
MAP-000018  OFST062050 Primary Listing -> LISTING.IS_PRIMARY
MAP-000019  OFST062000 Listing Date -> LISTING.VALID_FROM
MAP-000020  OFST062000 Listing Date -> LISTING.VALID_FROM_STATUS=KNOWN
```

Batch 05 a été rendu forward-compatible ; il ne fige plus la taille globale du registre.

### Batch 07 — Listing Currency

```text
MAP-000021
OFST062010 -> OF_FUND_LISTING_TRADING_QUOTE_UNIT_CODE
```

Gates :

```text
NO_PARENT_CURRENCY_INFERENCE
NO_FACTOR_INFERENCE
```

### Batch 08 — Listing business status

```text
MAP-000022
OFST062045 -> OF_FUND_LISTING_LISTING_STATUS
```

Valeurs explicites :

```text
planned   -> PLANNED
active    -> ACTIVE
suspended -> SUSPENDED
delisted  -> DELISTED
```

Gates :

```text
EXPLICIT_SOURCE_VALUE_ONLY
NO_DEFAULT_ACTIVE_ON_ABSENCE
NEVER_MAP_TO_IS_CURRENT
```

### Batch 09 — Bloomberg / RIC Listing identifiers

```text
OFST060000 Bloomberg Code Of Listing
OFST060010 Reuters Code Of Listing
MAP-000023..MAP-000028
```

Schemes dédiés :

```text
BLOOMBERG
RIC
```

Gate runtime :

```text
IMPORT_SUPPORTED: NO
EXPORT_SUPPORTED: NO
ACTIVATION_GATE: EXPLICIT_PROPRIETARY_IDENTIFIER_USAGE_REVIEW
```

Ne pas confondre ce gate de prudence avec l'alerte SEDOL : pour Bloomberg/RIC, la sémantique est validée mais l'usage opérationnel d'identifiants propriétaires reste volontairement séparé.

## SEDOL — gate inchangé

```text
OFST020040
IMPORT_SUPPORTED: NO
EXPORT_SUPPORTED: NO
ACTIVATION_GATE: EXPLICIT_SEDOL_LICENSING_CLEARANCE
```

Ne jamais activer silencieusement ingestion, stockage ou distribution SEDOL.

## Prochaine unité OF-MAP-002

Auditer exclusivement depuis le PDF officiel checksum-locké / pages officielles :

```text
TICKER / LOCAL LISTING IDENTIFIER candidates
OFST060050 iNAV Bloomberg
OFST060060 iNAV Reuters
other Listing-level identifiers or venue metadata
```

Règles :

1. vérifier OF-ID exact, Field Level, type, description et exemples ;
2. distinguer identité de Listing, identité iNAV et donnée calculée ;
3. ne pas rabattre un identifiant vendor sur TICKER/OTHER si le standard le distingue ;
4. ne pas créer de champ canonique avant un RED dédié ;
5. séparer validation sémantique et droit d'usage ;
6. `OFST062040 Exchange Place` reste différé car le standard privilégie MIC `OFST062030`.

## Couverture institutionnelle

```text
ORGANIZATION_SCOPE_ROLES: 199 = 195 VALIDATED + 4 PENDING
COUNTRY_COVERAGE: 53 / 54
UNCOVERED: ERYTHREE
```

Résiduel à ne pas forcer :

```text
EGX  INDEX_PROVIDER   EGYPTE
NSE  INDEX_PROVIDER   KENYA
NGX  INDEX_PROVIDER   NIGERIA
CMA  MONETARY_UNION   CMA
```

Audit récent EGX/NSE/NGX : aucune promotion, faute de preuve primaire suffisamment explicite de responsabilité provider/administrator.

## Gaps fonctionnels institutionnels

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

Priorité : assurance/pension puis fiscal/dette, avec preuves primaires officielles et sans créer d'institution artificielle lorsqu'une fonction n'est pas applicable.

## OF-SOURCE-003

Une organisation validée ne valide jamais automatiquement :

```text
ENDPOINT
SERIE EXACTE
FREQUENCE
UNITE
CONVENTION
HISTORIQUE
METHODE
STATUT DE COLLECTE
```

Continuer indépendamment.

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

## Preuve de checkpoint

```text
docs/00_PROJECT/OF_MAP_002_LISTING_BATCHES_06_09_CHECKPOINT_20260818.md
```

## Interdictions maintenues

Ne pas inventer de données, ne pas générer 1 869 faux `UNMAPPED`, ne pas réécrire les migrations déjà appliquées, ne pas activer les identifiants gated, ne pas fusionner/retargeter PR #1, ne pas modifier `main` et ne pas créer de branche supplémentaire.
