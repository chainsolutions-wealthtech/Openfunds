# Prochaine action autorisée

```text
CURRENT_LOOP: OF-MAP-002 + OF-DATA-001_LISTING_EXTENSIONS + OF-LOOP-SOURCE-002 + OF-SOURCE-003
CURRENT_TASK: OF-MAP-002_BATCH_06_CLOSURE_PENDING / MIGRATION_020_QUOTE_UNIT_RED / OF-SOURCE-002_EN_COURS / OF-SOURCE-003_EN_COURS
LAST_VERIFIED_WAVE: 15
MIGRATION_CHAIN: 001..019_GREEN
CANONICAL_MAPPING_INVENTORY: 177_FIELDS = 143_CORE + 34_LISTING_EXTENSION
OPENFUNDS_MAPPING: BATCH_01..05_VALIDATED / BATCH_06_ROWS_PRESENT_CI_CLOSURE_NOT_YET_ATTESTED
NEXT_UNIT: MIGRATION_020_QUOTE_UNIT_RED_TO_GREEN + BATCH_06_FINAL_CI_ATTESTATION + LISTING_CURRENCY_MAPPING + FUNCTIONAL_INSTITUTIONAL_GAP_WAVES
STATUS: FORWARD_ONLY_WORK_IN_PROGRESS_WITH_FAIL_CLOSED_CI_GATES
WRITE_GATE: VERIFIED_OF_ID + VERIFIED_OBJECT_LEVEL + VERIFIED_CANONICAL_FIELD_ID + EXPLICIT_TRANSFORMATION + LICENCE_GATE + TDD_RED
```

## État courant vérifié — 18 août 2026

Le travail reste sur `architecture/africafunds-country-indicators-v0.1` et la PR #1 reste draft, ouverte et non fusionnée. Ne pas travailler sur `main`, ne pas retargeter/fusionner la PR et ne pas déployer la production tant que les gates correspondants ne sont pas satisfaits.

## Modèle canonique et migrations

La chaîne gouvernée reste vérifiée jusqu'à :

```text
019_SHARE_CLASS_LISTING_CORE
ORDER: 190
FULL_CHAIN_001_TO_019: SUCCESS
POSTGRESQL_16: SUCCESS
SECOND_APPLY_IDEMPOTENCE: SUCCESS
GREEN_RUN: 32070768364
```

Migration 018 a élargi additivement les schemes d'identifiants avec `WKN`, `SEDOL` et `VALOR`. Migration 019 ajoute un vrai modèle de cotation :

```text
fund.listing
fund.listing_identifier
```

Un Listing appartient à une `SHARE_CLASS`, conserve un localisateur de marché (`exchange_organization_id` ou `venue_mic`), une éventuelle devise économique de négociation, son historique et sa provenance. Les identifiants propres à la cotation (`SEDOL`, `TICKER`, `LOCAL_CODE`, `OTHER`) sont séparés de l'identité stable de la Share Class.

Preuves :

```text
docs/00_PROJECT/OF_DATA_001_LISTING_MIGRATION_019_COMPLETION_20260817.md
docs/02_ARCHITECTURE/ADR-031_CANONICAL_LISTING_DICTIONARY_EXTENSION.md
```

### Migration 020 — RED contract uniquement

Un nouveau contrat TDD a été posé pour traiter les unités de cotation sans polluer `ref.currency` :

```text
EXPECTED_ID:   020_LISTING_QUOTE_UNIT_SEMANTICS
EXPECTED_ORDER: 200
EXPECTED_PATH: schemas/fund/020_listing_quote_unit_semantics.sql
TEST: tests/test_listing_quote_unit_model.py
RED_CONTRACT_COMMIT: 6b09abdb57d0e3072403fee8100944adb580fe61
```

Le modèle attendu sépare :

```text
trading_currency_id          devise économique parentale
trading_quote_unit_code      code exact de cotation si unité distincte
trading_quote_unit_factor    facteur vers la devise parentale, seulement s'il est explicitement connu
```

`GBX`, `EUX` et `USX` ne doivent pas être injectés dans `ref.currency` comme de fausses devises canoniques. Aucun SQL de migration 020 n'est encore considéré validé tant que le RED n'est pas observé puis le GREEN PostgreSQL 16 vérifié.

## Dictionnaire canonique disponible au mapping

Le package historique `data/dictionary/spec_v1/` reste la baseline immuable des 143 champs de migration 015.

L'extension additive :

```text
data/dictionary/extensions/listing_v1/
```

porte les 34 champs physiques de migration 019.

Le validateur Openfunds utilise désormais une union collision-free :

```text
CORE_FIELDS:       143
LISTING_EXTENSION:  34
TOTAL:             177
UNION_GREEN_RUN: 32071385088
```

Toute collision de FIELD_ID ou dérive du `field_count` d'une extension échoue fermée. Une extension issue de migration 020 devra être versionnée additivement ; ne pas réécrire silencieusement `listing_v1` comme si les colonnes de 020 avaient toujours appartenu à 019.

## OF-MAP-001 — fermé

```text
OPENFUNDS_VERSION: 2.13.0
DOCUMENT_STATUS: FINAL
DOCUMENT_DATE: 2026-03-23
PDF_PAGES: 745
PDF_BYTES: 2957096
SHA256: 40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4
FIELD_RECORDS: 1869
UNIQUE_OF_IDS: 1869
CONCRETE_IDS: 1849
PARAMETERIZED_COUNTRY_TEMPLATES_XX: 20
```

L'archive reste byte-identical et le parser checksum-gated reste la seule base autorisée pour établir les OF-ID et leurs métadonnées officielles.

## OF-MAP-002 — Batches 01..05 fermés / Batch 06 présent mais non encore clos

Batch 05 reste le dernier lot pleinement attesté :

```text
BATCH05_GREEN_RUN: 32071858346
```

Le registre contient désormais physiquement les quatre lignes de Batch 06 :

```text
MAP-000017  OFST062030 Market Identifier Code -> OF_FUND_LISTING_VENUE_MIC
MAP-000018  OFST062050 Is Primary Listing     -> OF_FUND_LISTING_IS_PRIMARY
MAP-000019  OFST062000 Listing Date           -> OF_FUND_LISTING_VALID_FROM
MAP-000020  OFST062000 Listing Date           -> OF_FUND_LISTING_VALID_FROM_STATUS = KNOWN
```

État matériel après ces lignes :

```text
REVIEWED_MAPPING_ROWS:      20
MAPPED_EXTERNAL_IDS:        11
UNMAPPED_EXTERNAL_IDS:    1858
CANONICAL_FIELDS_AVAILABLE: 177
MAPPED_CANONICAL_IDS:       14
```

Audit officiel Listing :

```text
AUDIT_RUN: 32072168754
BATCH06_RED_RUN: 32072345238
BATCH06_ATTEMPTED_GREEN_RUN: 32072421794
```

`32072421794` a validé l'intégration officielle mais a échoué sur les deux jobs unitaires à cause d'un ancien test Batch 05 qui figeait encore la taille globale du registre à `16`. Ce défaut de forward-compatibility a été corrigé sans toucher aux mappings ni au gate SEDOL :

```text
FIX_COMMIT: 0c7faac110cf5ea626df40c01f74d03a31b4f886
```

Tant qu'un run complet post-correctif n'est pas effectivement observable et attesté, ne pas écrire `BATCH_06_VALIDATED` dans les surfaces de vérité.

### SEDOL — règle spéciale inchangée

Le record officiel checksum-locké de `OFST020040` établit :

```text
FIELD_LEVEL: Listing
DATA_TYPE: string
```

et contient une alerte selon laquelle l'ingestion, le stockage ou la distribution peuvent être soumis à licence.

Les trois mappings SEDOL sont donc sémantiquement `VALIDATED`, sans perte d'information, mais :

```text
IMPORT_SUPPORTED: NO
EXPORT_SUPPORTED: NO
ACTIVATION_GATE: EXPLICIT_SEDOL_LICENSING_CLEARANCE
AUDIT_RUN: 32071520665
```

Ne jamais convertir ce gate de licence en simple détail technique.

Preuve :

```text
docs/00_PROJECT/OF_MAP_002_BATCH_05_SEDOL_COMPLETION_20260817.md
```

## Prochaine unité OF-MAP-002 / Listing Currency

Le PDF officiel a montré :

```text
OFST062010  Listing Currency
FIELD_LEVEL: Listing
```

avec possibilité d'utiliser des codes d'unité mineure tels que `GBX`, `EUX`, `USX` en plus des devises ISO 4217 usuelles. Le référentiel canonique `data/reference/CURRENCIES.csv` ne contient pas ces codes et ne doit pas être détourné pour les stocker comme devises.

Ordre obligatoire :

```text
1. observer le RED migration 020 ;
2. implémenter migration 020 forward-only ;
3. passer PostgreSQL 16 / double apply / adoption ;
4. créer une extension de dictionnaire dédiée à 020 ;
5. unir cette extension au validator sans collision ;
6. seulement alors proposer le mapping OFST062010.
```

Ne pas forcer le facteur 0,01 à partir du suffixe `X` sans preuve explicite de la convention du code concerné. Une valeur connue mais un facteur non prouvé doit rester partiellement modélisée plutôt qu'inventée.

### Autres Listing candidates différés

```text
OFST062040 Exchange Place      DEFERRED: official record recommends MIC OFST062030
OFST062045 Status Of Listing   DEFERRED: requires real business status, never map to is_current
OFST060000 Bloomberg Code      DEFERRED: identifier-scheme semantics to review
OFST060010 Reuters Code / RIC  DEFERRED: identifier-scheme semantics to review
OFST060050 iNAV Bloomberg      DEFERRED: iNAV identity/role semantics to review
OFST060060 iNAV Reuters        DEFERRED: iNAV identity/role semantics to review
```

## Couverture institutionnelle — Waves 01..15

```text
AFRICAN_COUNTRIES: 54
COUNTRY_COVERAGE_WITH_AT_LEAST_ONE_COUNTRY_ORG: 53 / 54
UNCOVERED_COUNTRY: ERYTHREE
ORGANIZATION_SCOPE_ROLES: 199 = 195 VALIDATED + 4 PENDING
```

Résiduel explicite :

```text
EGX  INDEX_PROVIDER   EGYPTE
NSE  INDEX_PROVIDER   KENYA
NGX  INDEX_PROVIDER   NIGERIA
CMA  MONETARY_UNION   CMA
```

Les Waves 14 et 15 ont fermé JSE/BVMT puis les rôles UEMOA/CEMAC/BCEAO/BEAC suffisamment prouvés. Ne pas forcer les quatre cas restants.

## Couverture fonctionnelle institutionnelle — vraie baseline

`195/199` ne signifie pas que 54 pays sont fonctionnellement complets. L'audit post-Wave15 montre :

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

La prochaine boucle institutionnelle doit combler ces fonctions avec preuves primaires officielles, et non simplement réduire les quatre `PENDING` existants.

Priorité de volume : assurance/pension puis fiscal/dette, tout en privilégiant les pays où quelques preuves supplémentaires peuvent fermer un ensemble fonctionnel complet.

## OF-SOURCE-003 — reste actif

La validation institutionnelle ne valide pas automatiquement :

```text
ENDPOINT
SERIE EXACTE
FREQUENCE
UNITE
CONVENTION DE COTATION
HISTORIQUE
METHODE
STATUT DE COLLECTE
```

Continuer indépendamment l'audit des mappings/séries initiaux.

## Blockers externes maintenus

```text
ERYTHREE            PRIMARY_OFFICIAL_SOURCE_NOT_VERIFIED
PERSISTENT_DB       OPENFUNDS_DATABASE_URL / DURABLE_RUNTIME_NOT_CONFIGURED
IMMUTABLE_RAW_STORE NOT_CONFIGURED
SEDOL_RUNTIME       EXPLICIT_LICENSING_CLEARANCE_REQUIRED
COMPLETE_HISTORIES  NOT_LOADED
BENCHMARK_RFR_MAR   NOT_FULLY_VALIDATED
WTI_WTI_BENCH       NOT_ACTIVE
PRODUCTION_API_UI   NOT_IMPLEMENTED
PRODUCTION_DEPLOY   NOT_CONFIGURED
```

## Interdictions maintenues

Ne pas inventer de données ou d'équivalences, ne pas générer 1 869 faux `UNMAPPED`, ne pas importer des historiques réels sans stockage durable, ne pas activer SEDOL sans licence, ne pas activer WTI/WTI Bench, ne pas fusionner/retargeter la PR #1, ne pas modifier `main` et ne pas créer de branche supplémentaire.
