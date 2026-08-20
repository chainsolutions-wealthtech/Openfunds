# Prochaine action autorisée

```text
CURRENT_LOOP: OF-MAP-002 + OF-DATA-001 + OF-LOOP-SOURCE-002 + OF-SOURCE-003
CURRENT_IMPLEMENTED_MIGRATION_CHAIN: 001..032
LAST_REMOTELY_VERIFIED_MIGRATION_CHAIN: 001..019 / RUN 32070768364
CURRENT_IMPLEMENTED_CANONICAL_INVENTORY: 210 = 143_CORE + 67_EXTENSIONS
LAST_REMOTELY_VERIFIED_CANONICAL_UNION: 177 / RUN 32071385088
CURRENT_IMPLEMENTED_MAPPING: BATCH_01..19 / 72_ROWS / 38_OF_IDS / 35_CANONICAL_IDS
BATCH_20_ETF_FLAG: RED_CONTRACT + MIGRATION_032 + DICTIONARY_EXTENSION_READY / REGISTRY_ROW_NOT_WRITTEN_DUE_FULL_FILE_RECONSTRUCTION_GATE
LAST_REMOTELY_VERIFIED_MAPPING: BATCH_05 / RUN 32071858346
UNMAPPED_OPENFUNDS_IDS: 1831
STATUS: FORWARD_ONLY_WORK_IN_PROGRESS_WITH_FAIL_CLOSED_REMOTE_CI_AND_REGISTRY_RECONSTRUCTION_GATES
WRITE_GATE: VERIFIED_OF_ID + VERIFIED_FIELD_LEVEL + VERIFIED_CANONICAL_TARGET + EXPLICIT_TRANSFORMATION + LICENCE_OR_USAGE_GATE + TDD_CONTRACT
```

## Gouvernance

Travail exclusivement sur `architecture/africafunds-country-indicators-v0.1`.

PR #1 : **DRAFT / OPEN / UNMERGED**. Ne pas toucher `main`, ne pas retargeter/fusionner la PR, ne pas activer production, ne pas créer de branche supplémentaire.

Le connecteur GitHub ne remonte toujours aucun check exploitable sur les HEAD récents. Donc :

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
```

## Inventaire canonique courant

```text
CORE migration 015:                              143
listing_v1:                                       34
listing_quote_unit_v1:                             2
listing_status_v1:                                 1
listing_identifier_subject_v1:                     1
listing_inception_price_v1:                        1
share_class_trading_price_frequency_v1:            1
share_class_nav_frequency_detail_v1:               1
valuation_time_semantics_v1:                       4
share_class_multicurrency_dealing_v1:             16
entity_lifecycle_phase_v1:                         1
share_class_investment_status_v1:                  4
share_class_etf_flag_v1:                           1
TOTAL IMPLEMENTED STRUCTURAL FIELDS:              210
```

Aucune extension ne réécrit `spec_v1` ou `listing_v1` rétroactivement.

## OF-MAP-002 — registre fermé jusqu'à Batch 19

```text
REVIEWED_MAPPING_ROWS:   72
MAPPED_EXTERNAL_IDS:     38
UNMAPPED_EXTERNAL_IDS: 1831
MAPPED_CANONICAL_IDS:    35
MAPPED_CANONICAL_UNION: 209
```

### Batches 17–18 — lifecycle

- `OFST020545` -> `entity_state.lifecycle_phase` avec sept phases précises.
- `OFST020558`, `020559`, `020560`, `020562`, `020563`, `020564`, `020566` -> événements versionnables.
- Les cycles `active/dormant` peuvent être répétés ; aucune dormance n'est réduite à une paire de colonnes statiques.

### Batch 19 — investment status

```text
OFST023100 Investment Status
OFST023105 Investment Status Description
OFST023110 Investment Status Date
```

Ces champs décrivent l'accès souscription/rachat et restent distincts de `lifecycle_phase`.

## Batch 20 — ETF flag : gate en cours

Source officielle vérifiée :

```text
OFST010580 Is ETF
FIELD_LEVEL: Share Class
DATA_TYPE: boolean
VALUES: yes / no
```

Migration 032 ajoute uniquement :

```text
fund.share_class_profile.is_etf boolean NULL
```

Extension : `data/dictionary/extensions/share_class_etf_flag_v1/` (1 champ).

Le contrat RED `tests/test_openfunds_mapping_batch20.py` existe. La ligne de registre attendue est :

```text
OFST010580 -> OF_FUND_SHARE_CLASS_PROFILE_IS_ETF
TRANSFORMATION: OPENFUNDS_YES_NO_TO_BOOLEAN
```

**Ne pas écrire MAP-000073 tant que le connecteur ne permet pas de reconstruire et relire la totalité des 72 lignes historiques sans troncature.** Le registre utilise un remplacement complet via Contents API ; un append à l'aveugle serait un risque de régression et est donc interdit.

## Invariants permanents

- quote-unit ≠ devise économique ;
- Listing status ≠ `is_current` ;
- Listing identity ≠ iNAV identity ;
- lifecycle phase ≠ broad lifecycle status ;
- investment status ≠ lifecycle phase ;
- reference Share Class currency ≠ additional dealing currencies ;
- timezone label ≠ timezone IANA ;
- absence de date source ≠ date inventée ;
- ETF est un attribut Share Class, pas Fund.

## Gates identifiants inchangés

```text
SEDOL: IMPORT/EXPORT NO — EXPLICIT_SEDOL_LICENSING_CLEARANCE
BLOOMBERG/RIC: IMPORT/EXPORT NO — EXPLICIT_PROPRIETARY_IDENTIFIER_USAGE_REVIEW
```

## Prochaine unité sûre

1. fermer le gate de reconstruction du registre pour Batch20 ;
2. intégrer 032/Batch20 aux workflows et au mapping manifest seulement après écriture sûre du registre ;
3. auditer les champs ETF/index suivants (`OFST023800+`) avant toute architecture : index name/currency/vendor identifiers ne doivent pas être aplatis dans un seul champ benchmark ;
4. poursuivre en parallèle OF-SOURCE-003 et les gaps institutionnels avec preuves primaires.

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

`docs/00_PROJECT/OF_MAP_002_BATCHES_17_19_LIFECYCLE_INVESTMENT_STATUS_CHECKPOINT_20260820.md`

## Interdictions maintenues

Ne pas inventer de données, ne pas générer 1 869 faux `UNMAPPED`, ne pas réécrire les migrations historiques, ne pas activer les identifiants gated, ne pas modifier `main`, ne pas fusionner/retargeter PR #1 et ne pas créer de nouvelle branche.
