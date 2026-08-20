# Prochaine action autorisée

```text
CURRENT_LOOP: OF-MAP-002 + OF-DATA-001 + OF-LOOP-SOURCE-002 + OF-SOURCE-003
CURRENT_IMPLEMENTED_MIGRATION_CHAIN: 001..031
LAST_REMOTELY_VERIFIED_MIGRATION_CHAIN: 001..019 / RUN 32070768364
CURRENT_IMPLEMENTED_CANONICAL_INVENTORY: 209 = 143_CORE + 66_EXTENSIONS
LAST_REMOTELY_VERIFIED_CANONICAL_UNION: 177 / RUN 32071385088
CURRENT_IMPLEMENTED_MAPPING: BATCH_01..19 / 72_ROWS / 38_OF_IDS / 35_CANONICAL_IDS
LAST_REMOTELY_VERIFIED_MAPPING: BATCH_05 / RUN 32071858346
UNMAPPED_OPENFUNDS_IDS: 1831
STATUS: FORWARD_ONLY_WORK_IN_PROGRESS_WITH_FAIL_CLOSED_REMOTE_CI_GATES
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

## Migrations implémentées après le dernier GREEN distant

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
```

## Invariants structuraux nouveaux

- `GBX/EUX/USX` restent des quote-unit codes, pas des fausses devises `ref.currency`.
- `listing_status` reste distinct de `is_current`.
- Bloomberg/RIC restent des schemes Listing dédiés et usage-gated.
- `identifier_subject` distingue `LISTING` de `INAV`.
- `inception_price` n'infère ni devise ni facteur.
- `nav_frequency` et `trading_price_frequency` sont distincts.
- `nav_frequency_detail` conserve le texte source.
- un label timezone source n'est jamais transformé silencieusement en zone IANA ; `OFST010252` est conservé séparément.
- la devise de référence Share Class reste unique ; les devises additionnelles sont historisées dans `share_class_dealing_currency`.
- `lifecycle_phase` conserve les sept phases Openfunds et ne remplace pas `lifecycle_status`.
- les dates de dormance/offre/liquidation/termination sont des `entity_event`, ce qui permet les cycles répétés.
- `investment_status` représente l'accès souscription/rachat et reste distinct du lifecycle.
- une date de statut d'investissement absente n'est jamais inventée.

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
TOTAL:                                            209
```

Aucune extension ne réécrit `spec_v1` ou `listing_v1` rétroactivement.

## OF-MAP-002 — état courant

```text
REVIEWED_MAPPING_ROWS:   72
MAPPED_EXTERNAL_IDS:     38
UNMAPPED_EXTERNAL_IDS: 1831
MAPPED_CANONICAL_IDS:    35
CANONICAL_FIELDS:       209
```

### Batches 15–16 — temps et multicurrency

- Batch 15 : `OFST010250`, `010251`, `010252`, `020320`; heure locale + timezone label + IANA + heure publication NAV, sans inférence label→IANA.
- Batch 16 : `OFST020530`, `020535`; flag multidevise + lignes de devises additionnelles, sans écraser `currency_id`.

### Batches 17–18 — lifecycle

- Batch 17 : `OFST020545` -> `entity_state.lifecycle_phase` avec sept phases précises.
- Batch 18 : `OFST020558`, `020559`, `020560`, `020562`, `020563`, `020564`, `020566` -> événements versionnables (`event_type + effective_date + KNOWN`).
- Les cycles `active/dormant` restent représentables plusieurs fois ; aucune date de dormance n'est figée dans une colonne unique.

### Batch 19 — investment status

```text
OFST023100 Investment Status
  -> share_class_profile.investment_status

OFST023105 Investment Status Description
  -> share_class_profile.investment_status_description

OFST023110 Investment Status Date
  -> investment_status_date + investment_status_date_status=KNOWN
```

Valeurs canoniques :

```text
OPEN
SOFT_CLOSED
HARD_CLOSED
CLOSED_FOR_REDEMPTION
CLOSED_FOR_SUBSCRIPTION_AND_REDEMPTION
```

## Gates identifiants inchangés

### SEDOL

```text
IMPORT_SUPPORTED: NO
EXPORT_SUPPORTED: NO
ACTIVATION_GATE: EXPLICIT_SEDOL_LICENSING_CLEARANCE
```

### Bloomberg / RIC

```text
IMPORT_SUPPORTED: NO
EXPORT_SUPPORTED: NO
ACTIVATION_GATE: EXPLICIT_PROPRIETARY_IDENTIFIER_USAGE_REVIEW
```

## Prochaine unité OF-MAP-002

Auditer le prochain domaine depuis le PDF officiel checksum-locké avant toute migration.

Priorité : choisir un champ ou petit groupe qui peut être modélisé sans perte et sans créer de structure parallèle. Les domaines `benchmark`, `fees`, `documents`, `eligibility`, `distributions` et relations complexes doivent être normalisés plutôt qu'aplatis en texte pour accélérer artificiellement la couverture.

Avant tout mapping : vérifier OF-ID, Field Level, type, cardinalité implicite, dépendances et cible canonique existante. TDD RED obligatoire pour toute évolution de schéma.

## Couverture institutionnelle

```text
ORGANIZATION_SCOPE_ROLES: 199 = 195 VALIDATED + 4 PENDING
COUNTRY_COVERAGE: 53 / 54
UNCOVERED: ERYTHREE
PENDING:
  EGX INDEX_PROVIDER EGYPTE
  NSE INDEX_PROVIDER KENYA
  NGX INDEX_PROVIDER NIGERIA
  CMA MONETARY_UNION CMA
```

Ne pas forcer ces quatre cas.

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

Priorité parallèle : assurance/pension puis fiscal/dette, preuves primaires officielles uniquement.

## OF-SOURCE-003

Une organisation validée ne valide jamais automatiquement endpoint, série exacte, fréquence, unité, convention, historique, méthode ou statut de collecte. Continuer indépendamment.

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
