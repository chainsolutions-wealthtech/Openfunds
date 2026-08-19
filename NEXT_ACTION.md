# Prochaine action autorisée

```text
CURRENT_LOOP: OF-MAP-002 + OF-DATA-001 + OF-LOOP-SOURCE-002 + OF-SOURCE-003
CURRENT_IMPLEMENTED_MIGRATION_CHAIN: 001..026
LAST_REMOTELY_VERIFIED_MIGRATION_CHAIN: 001..019 / RUN 32070768364
CURRENT_IMPLEMENTED_CANONICAL_INVENTORY: 184 = 143_CORE + 41_EXTENSIONS
LAST_REMOTELY_VERIFIED_CANONICAL_UNION: 177 / RUN 32071385088
CURRENT_IMPLEMENTED_MAPPING: BATCH_01..14 / 40_ROWS / 21_OF_IDS / 21_CANONICAL_IDS
LAST_REMOTELY_VERIFIED_MAPPING: BATCH_05 / RUN 32071858346
UNMAPPED_OPENFUNDS_IDS: 1848
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
```

Principes conservés :

- `GBX/EUX/USX` restent des quote-unit codes, pas des fausses devises `ref.currency` ;
- `listing_status` reste distinct de `is_current` ;
- Bloomberg/RIC restent des schemes Listing dédiés et usage-gated ;
- `identifier_subject` distingue `LISTING` de `INAV` ;
- `inception_price` n'infère ni devise ni facteur ;
- `nav_frequency` et `trading_price_frequency` sont deux concepts distincts ;
- `nav_frequency_detail` conserve le texte libre source et ne remplace pas le code de fréquence.

## Inventaire canonique courant

```text
CORE migration 015:                         143
listing_v1:                                  34
listing_quote_unit_v1:                        2
listing_status_v1:                            1
listing_identifier_subject_v1:                1
listing_inception_price_v1:                   1
share_class_trading_price_frequency_v1:       1
share_class_nav_frequency_detail_v1:          1
TOTAL:                                       184
```

Aucune extension ne réécrit `spec_v1` ou `listing_v1` rétroactivement.

## OF-MAP-002 — état courant

```text
REVIEWED_MAPPING_ROWS:   40
MAPPED_EXTERNAL_IDS:     21
UNMAPPED_EXTERNAL_IDS: 1848
MAPPED_CANONICAL_IDS:    21
CANONICAL_FIELDS:       184
```

### Batches 06–11 — Listing

- Batch 06 : MIC, primary listing, listing date + valid_from_status.
- Batch 07 : Listing Currency -> `trading_quote_unit_code`, sans parent/facteur inférés.
- Batch 08 : Status Of Listing -> `listing_status`, sans default ACTIVE implicite.
- Batch 09 : Bloomberg/RIC Listing identifiers, import/export désactivés jusqu'à revue d'usage.
- Batch 10 : iNAV Bloomberg/RIC avec `identifier_subject=INAV`, usage-gated.
- Batch 11 : Inception Price -> `listing.inception_price`, sans inférence de devise/facteur.

### Batches 12–14 — fréquences Share Class

```text
MAP-000038  OFST020300 Valuation Frequency
            -> OF_FUND_SHARE_CLASS_PROFILE_NAV_FREQUENCY

MAP-000039  OFST020310 Trading Price Frequency
            -> OF_FUND_SHARE_CLASS_PROFILE_TRADING_PRICE_FREQUENCY

MAP-000040  OFST020305 Valuation Frequency Detail
            -> OF_FUND_SHARE_CLASS_PROFILE_NAV_FREQUENCY_DETAIL
```

Vocabulaire officiel de fréquence :

```text
daily
twice a week
weekly
twice a month
monthly
quarterly
twice a year
annually
at least annually
```

Mapping canonique réversible en codes uppercase/underscore. Le détail libre reste source-preserving.

## Gates identifiants

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

Auditer les champs Share Class immédiatement voisins depuis la source officielle checksum-lockée, notamment :

```text
OFST020320 NAV Publication Time
puis autres champs opérationnels Share Class compatibles avec le modèle canonique
```

Avant tout mapping : vérifier OF-ID, Field Level, type, dépendances temporelles/timezone, cible canonique existante ou nécessité d'une migration additive.

Ne pas modéliser une heure sans sa sémantique de fuseau si le standard la lie à un champ timezone distinct.

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

Priorité : assurance/pension puis fiscal/dette, preuves primaires officielles uniquement.

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

## Interdictions maintenues

Ne pas inventer de données, ne pas générer 1 869 faux `UNMAPPED`, ne pas réécrire les migrations historiques, ne pas activer les identifiants gated, ne pas modifier `main`, ne pas fusionner/retargeter PR #1 et ne pas créer de nouvelle branche.
