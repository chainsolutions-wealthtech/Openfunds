# OF-MAP-002 — Listing Batches 06→09 checkpoint — 2026-08-18

## Statut

```text
BRANCH: architecture/africafunds-country-indicators-v0.1
PR: #1 DRAFT / OPEN / UNMERGED
LAST_REMOTELY_VERIFIED_MAPPING_GREEN: BATCH_05 / RUN 32071858346
LAST_REMOTELY_VERIFIED_CANONICAL_UNION: 177 FIELDS / RUN 32071385088
CURRENT_IMPLEMENTED_CANONICAL_UNION: 180 FIELDS
CURRENT_IMPLEMENTED_MAPPING_ROWS: 28
CURRENT_IMPLEMENTED_EXTERNAL_IDS: 15 / 1869
CURRENT_UNMAPPED_EXTERNAL_IDS: 1854
CURRENT_MAPPED_CANONICAL_IDS: 16 / 180
REMOTE_CI_ATTESTATION_FOR_BATCHES_06_09: NOT_OBSERVABLE_WITH_CURRENT_CONNECTOR
```

Ce document est volontairement fail-closed : `IMPLEMENTED` ne signifie pas `REMOTELY_GREEN`. Le connecteur GitHub disponible dans la conversation ne remonte ni les runs `push` ni des status checks exploitables pour les HEAD concernés. Aucun numéro de run ni verdict GREEN n'est donc inventé.

## Batch 06 — MIC, primary listing, listing date

Mappings implémentés :

```text
MAP-000017  OFST062030 -> OF_FUND_LISTING_VENUE_MIC
MAP-000018  OFST062050 -> OF_FUND_LISTING_IS_PRIMARY
MAP-000019  OFST062000 -> OF_FUND_LISTING_VALID_FROM
MAP-000020  OFST062000 -> OF_FUND_LISTING_VALID_FROM_STATUS
```

Le test historique Batch 05 a été rendu forward-compatible : il protège ses trois mappings SEDOL et le gate de licence sans figer la taille globale du registre.

## Migration 020 — Listing quote-unit semantics

Migration :

```text
020_LISTING_QUOTE_UNIT_SEMANTICS
ORDER: 200
PATH: schemas/fund/020_listing_quote_unit_semantics.sql
```

Ajouts additifs sur `fund.listing` :

```text
trading_quote_unit_code
trading_quote_unit_factor
```

Décision : les codes d'unité de cotation comme `GBX`, `EUX`, `USX` ne sont pas injectés dans `ref.currency` comme s'ils étaient des devises économiques ISO 4217 autonomes.

Le facteur ne peut exister sans code d'unité et aucun facteur n'est inféré silencieusement.

Extension dictionnaire :

```text
data/dictionary/extensions/listing_quote_unit_v1/
FIELD_COUNT: 2
```

FIELD_ID :

```text
OF_FUND_LISTING_TRADING_QUOTE_UNIT_CODE
OF_FUND_LISTING_TRADING_QUOTE_UNIT_FACTOR
```

## Batch 07 — OFST062010 Listing Currency

Mapping implémenté :

```text
MAP-000021
OFST062010
-> OF_FUND_LISTING_TRADING_QUOTE_UNIT_CODE
TRANSFORM: TRIM_AND_UPPERCASE_QUOTE_UNIT_CODE
```

Gates :

```text
NO_PARENT_CURRENCY_INFERENCE
NO_FACTOR_INFERENCE
```

Le champ Openfunds est donc conservé exactement dans la couche quote-unit. `trading_currency_id` et `trading_quote_unit_factor` ne sont pas dérivés du code seul.

## Migration 021 — Listing business status

Migration :

```text
021_LISTING_BUSINESS_STATUS
ORDER: 210
PATH: schemas/fund/021_listing_business_status.sql
```

Ajout :

```text
fund.listing.listing_status
NULLABLE
ALLOWED: PLANNED / ACTIVE / SUSPENDED / DELISTED
```

Décision structurante : `listing_status` est un statut métier de cotation. Il est strictement distinct de `is_current`, qui décrit la version bitemporelle courante de l'assertion.

Aucun `DEFAULT ACTIVE` n'est posé dans le canonique : l'absence de valeur source reste une absence d'assertion.

Extension dictionnaire :

```text
data/dictionary/extensions/listing_status_v1/
FIELD_COUNT: 1
FIELD_ID: OF_FUND_LISTING_LISTING_STATUS
```

## Batch 08 — OFST062045 Status Of Listing

Mapping implémenté :

```text
MAP-000022
OFST062045
-> OF_FUND_LISTING_LISTING_STATUS
TRANSFORM: OPENFUNDS_LISTING_STATUS_TO_CANONICAL_ENUM
```

Valeurs :

```text
planned   -> PLANNED
active    -> ACTIVE
suspended -> SUSPENDED
delisted  -> DELISTED
```

Gate :

```text
EXPLICIT_SOURCE_VALUE_ONLY
NO_DEFAULT_ACTIVE_ON_ABSENCE
```

## Migration 022 — Listing vendor identifier schemes

Migration :

```text
022_LISTING_VENDOR_IDENTIFIER_SCHEMES
ORDER: 220
PATH: schemas/fund/022_listing_vendor_identifier_schemes.sql
```

Le CHECK de `fund.listing_identifier.identifier_scheme` est étendu additivement :

```text
SEDOL
TICKER
LOCAL_CODE
OTHER
BLOOMBERG
RIC
```

`BLOOMBERG` et `RIC` restent des identifiants de Listing. Ils ne sont pas ajoutés à `fund.entity_identifier` et ne sont pas rabattus sur `OTHER` ou `TICKER`.

## Batch 09 — Bloomberg / Reuters RIC

OF-ID :

```text
OFST060000  Bloomberg Code Of Listing
OFST060010  Reuters Code Of Listing
```

Six mappings one-to-many sont implémentés :

```text
MAP-000023..MAP-000025 -> BLOOMBERG value / scheme / normalized value
MAP-000026..MAP-000028 -> RIC value / scheme / normalized value
```

Gate runtime :

```text
IMPORT_SUPPORTED: NO
EXPORT_SUPPORTED: NO
ACTIVATION_GATE: EXPLICIT_PROPRIETARY_IDENTIFIER_USAGE_REVIEW
```

Cette précaution ne prétend pas qu'Openfunds a publié ici la même alerte de licence que pour SEDOL. Elle sépare simplement la validation sémantique du droit d'usage opérationnel d'identifiants propriétaires.

Normalisation : outer trim seulement ; ne pas uppercaser ou réécrire aveuglément un code vendor dont le contenu/suffixe peut être significatif.

## Inventaire canonique courant

```text
CORE migration 015:       143
listing_v1 migration 019:  34
quote_unit_v1 migration 020: 2
listing_status_v1 migration 021: 1
TOTAL IMPLEMENTED:        180
```

Le dernier union GREEN distant attesté reste celui des 177 champs. Les trois champs ajoutés par migrations 020/021 restent structurellement intégrés mais ne doivent pas être décrits comme remotely-green tant que la CI n'est pas observable.

## Couverture mapping courante

```text
REVIEWED_MAPPING_ROWS: 28
MAPPED_EXTERNAL_IDS: 15
UNMAPPED_EXTERNAL_IDS: 1854
MAPPED_CANONICAL_IDS: 16
OFFICIAL_FIELD_COUNT: 1869
```

## Prochaine unité

1. maintenir la recherche d'attestation CI réelle pour migrations 020→022 et Batches 06→09 sans inventer de run ;
2. auditer les prochains champs Listing officiels checksum-lockés ;
3. ne pas mapper `OFST062040 Exchange Place`, explicitement superseded par MIC, sauf justification nouvelle ;
4. auditer les champs ticker/local listing identifier séparément avant mapping ;
5. poursuivre les gaps institutionnels fonctionnels assurance/pension et fiscal/dette ;
6. conserver EGX/NSE/NGX INDEX_PROVIDER et CMA MONETARY_UNION en PENDING tant que la sémantique exacte n'est pas prouvée ;
7. garder SEDOL et Bloomberg/RIC runtime désactivés jusqu'à leurs gates d'usage/licence respectifs ;
8. ne pas fusionner ni retargeter la PR #1 et ne pas toucher `main`.
