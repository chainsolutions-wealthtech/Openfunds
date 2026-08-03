# COUNTRY RELATIONSHIPS VALIDATION

## STATUS

This document validates the structure and internal completeness of `data/reference/COUNTRY_RELATIONSHIPS.csv` against the uploaded planning matrix `04_Matrice_Pays_Domaines.csv` and the current canonical geography model.

It does not assert that every institutional relationship has already been independently verified from an external official source. For that reason, all generated relationship rows currently use `VALIDATION_STATUS=PENDING`.

## SCOPE

- 54 African countries
- 266 explicit relationship rows
- 5 canonical geographic regions
- 1 continental parent
- 8 UEMOA countries
- 6 CEMAC countries
- 4 CMA-linked countries in the source matrix

## REQUIRED RELATIONSHIPS PER COUNTRY

Every country has exactly one active candidate relationship for:

- `BELONGS_TO_REGION`
- `BELONGS_TO_CONTINENT`
- `USES_CURRENCY`
- `USES_MARKET_SCOPE`

Additional relationships are generated only when supported by the source matrix:

### UEMOA

- `BELONGS_TO_MONETARY_ZONE -> UEMOA`
- `USES_CENTRAL_BANK -> BCEAO`
- `USES_COMMON_EXCHANGE -> BRVM`

### CEMAC

- `BELONGS_TO_MONETARY_ZONE -> CEMAC`
- `USES_CENTRAL_BANK -> BEAC`
- `USES_COMMON_EXCHANGE -> BVMAC`

### CMA

- `BELONGS_TO_MONETARY_ZONE -> CMA`
- `USES_REFERENCE_CURRENCY -> ZAR`

No common stock exchange relationship is generated for CMA members because the source matrix does not establish one common exchange for all CMA countries and the national market structure must remain distinct.

## INTERNAL COUNT CHECKS

Base relationships:

- 54 region relationships
- 54 continent relationships
- 54 local-currency relationships
- 54 market-scope relationships
- subtotal: 216

UEMOA additions:

- 8 countries x 3 relationships = 24

CEMAC additions:

- 6 countries x 3 relationships = 18

CMA additions:

- 4 countries x 2 relationships = 8

Total:

- 216 + 24 + 18 + 8 = 266 relationships

## NON-REGRESSION RULES

The relationship model does not replace or merge the following dimensions:

- country
- geographic region
- continent
- monetary zone
- central bank
- stock exchange
- market scope

A fund remains attached to its national country even where market or monetary data is sourced from UEMOA, CEMAC, BCEAO, BEAC, BRVM or BVMAC.

The future taxonomy therefore remains:

`FUND -> COUNTRY -> NATIONAL CATEGORY -> REGIONAL CATEGORY -> AFRICA CATEGORY`

while market-source resolution can separately follow:

`COUNTRY -> MARKET_SCOPE -> MARKET INSTITUTIONS AND SERIES`

## IMPORTANT DATA-QUALITY DECISIONS

1. `VALID_FROM` and `VALID_TO` are intentionally blank because the uploaded planning source does not provide historical legal-effect dates for each relationship.
2. No artificial date such as `1900-01-01` is inserted.
3. All generated rows are marked `PENDING` until checked against official institutional sources.
4. Source terminology is preserved through `SOURCE_NOTE=DERIVED_FROM_04_MATRICE_PAYS_DOMAINES`.
5. No national central bank or national exchange is inferred for countries where the uploaded source does not identify one.
6. The file only materializes relationships supported by the current source matrix and the already approved UEMOA/CEMAC modeling rule.

## NEXT VALIDATION LAYER

The next source-verification work must attach an official source record to each institutional relationship, including:

- official organization name
- official website
- evidence URL
- verification date
- valid-from date where available
- valid-to date where applicable
- reviewer or validation process

Only after that verification should rows move from `PENDING` to `VALIDATED`.
