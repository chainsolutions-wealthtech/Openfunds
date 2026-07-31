# Country-Centric Market Universe

## Status

- Decision status: Accepted
- Model version introduced: 0.1.0
- Repository: `chainsolutions-wealthtech/Openfunds`
- Branch: `architecture/canonical-model-v1-bootstrap`

## Purpose

The `Country` object is the principal navigation and discovery entry point for all country-specific financial-market data. A country is not implemented as a single oversized table. It is a canonical entity linked to specialised, historised, source-aware entities.

From a country, clients must be able to discover its currencies, FX pairs, geographic universes, institutions, exchanges, statistics organisations, market indices, yield curves, benchmark rates, regulatory sources, scraping configurations and data-quality status.

## Core principle

```text
Country
  -> Geographic universes
  -> Currency and FX pairs
  -> Institutions
  -> Market infrastructures
  -> Statistical authorities
  -> Market indices
  -> Yield curves and reference rates
  -> Data sources and collection methods
  -> API resources
  -> Atomic Design view models
```

The country is therefore an aggregation root for navigation and read models, but specialised objects remain independently addressable canonical entities.

## 1. Country core entity

The `country` entity contains only stable identity and temporal fields.

```text
country_id
canonical_code
iso_alpha2
iso_alpha3
iso_numeric
un_m49_code
canonical_name
official_name
short_name
sovereignty_type
political_status
recognition_status
valid_from
valid_to
recorded_at
superseded_at
is_current
```

## 2. Geographic universes

A country may belong simultaneously and historically to multiple geographic, economic, monetary, regulatory and investment universes.

### Canonical entities

- `geographic_universe`
- `country_geographic_universe_membership`

### Universe types

- Global
- Continent
- Subcontinent
- Region
- Subregion
- Economic community
- Monetary union
- Customs union
- Investment universe
- Market classification universe
- Regulatory cooperation area
- Statistical reporting area

### Examples

- Africa
- West Africa
- UEMOA
- ECOWAS
- CEMAC
- North Africa
- Sub-Saharan Africa
- Frontier Markets
- Emerging Markets

### Membership attributes

```text
membership_id
country_id
geographic_universe_id
membership_type
membership_status
valid_from
valid_to
source_assertion_id
```

## 3. Currency and FX pairs

The country must expose its local currency or currencies and the standard currency pairs required by the platform.

### Canonical entities

- `currency`
- `country_currency_relationship`
- `fx_pair`
- `country_preferred_fx_pair`
- `fx_rate_observation`
- `fx_data_source`

### Country-currency relationship types

- Primary legal tender
- Secondary legal tender
- Commonly used currency
- Settlement currency
- Reporting currency
- Historical currency
- Parallel-market currency
- Monetary-union currency

### Required preferred FX pairs

For each local currency, the platform should be able to identify at least:

- Local currency / EUR
- EUR / Local currency
- Local currency / USD
- USD / Local currency

The model must not assume one quotation direction. Pair direction, base currency, quote currency and inversion rules are explicit.

### FX pair attributes

```text
fx_pair_id
base_currency_id
quote_currency_id
canonical_symbol
inverse_fx_pair_id
quotation_convention
rate_type
market_type
is_deliverable
is_official
valid_from
valid_to
```

### Country preferred pair attributes

```text
country_preferred_fx_pair_id
country_id
fx_pair_id
usage_type
priority
is_default
valid_from
valid_to
```

## 4. Institutions linked to a country

Institutions are not embedded as text fields in `country`. They are organisation entities linked through typed and historised relationships.

### Common organisation entity

`organisation`

### Organisation roles

- Financial regulator
- Securities regulator
- Fund regulator
- Banking regulator
- Insurance regulator
- Pension regulator
- Central bank
- Debt management office
- Treasury
- Ministry of finance
- National statistics office
- Exchange
- Central securities depository
- Clearing house
- Market operator
- Index provider
- Official gazette publisher
- Tax authority

### Common organisation attributes

```text
organisation_id
legal_name
short_name
organisation_type
country_id
website_url
address_id
email
telephone
lei
regulator_identifier
valid_from
valid_to
```

### Country-organisation relationship

```text
country_organisation_role_id
country_id
organisation_id
role_type
scope
jurisdiction_level
is_primary
valid_from
valid_to
source_assertion_id
```

## 5. Regulators

From a country, clients must be able to retrieve all relevant regulators.

### Minimum business fields

```text
name
short_name
website_url
address
jurisdiction_scope
regulated_product_types
publication_portal_url
data_download_url
licence_registry_url
legal_basis
```

A country can have more than one regulator and regulator responsibilities can change over time.

## 6. Exchanges and market infrastructures

### Canonical entities

- `exchange`
- `trading_venue`
- `market_segment`
- `central_securities_depository`
- `clearing_house`
- `country_market_infrastructure_relationship`

### Minimum exchange fields

```text
exchange_id
name
short_name
mic_code
website_url
market_data_url
listing_directory_url
historical_data_url
trading_currency_id
timezone_id
calendar_id
```

A regional exchange may serve several countries. Therefore, the exchange must not be owned by a single country in the data model. The relation is many-to-many and includes the relationship role.

## 7. Central bank

The country entry point must expose the central bank or monetary authority responsible for the country.

### Minimum fields

```text
organisation_id
name
short_name
website_url
statistics_portal_url
policy_rate_url
yield_curve_url
exchange_rate_url
reserve_data_url
publication_calendar_url
```

For monetary unions, several countries can link to the same central bank.

## 8. Statistics organisations

The country entry point must expose national and regional statistics authorities.

### Minimum fields

```text
organisation_id
name
short_name
website_url
data_portal_url
api_url
publication_calendar_url
methodology_url
```

### Statistical scopes

- Population
- Inflation
- GDP
- Employment
- External trade
- Public finance
- Financial accounts
- Monetary statistics
- Balance of payments
- National accounts

## 9. Unified market indicator model

The following should not be represented as unrelated country columns:

- All Share equity index
- Secondary equity indices
- Money-market index
- Short-term bond index
- Medium-term bond index
- Long-term bond index
- TSR or risk-free/reference rate series

They are specialised instances of a common `market_indicator` or `index` family.

### Canonical entities

- `market_indicator`
- `index_definition`
- `index_classification`
- `index_provider_relationship`
- `index_country_relationship`
- `index_universe_relationship`
- `index_level_observation`
- `yield_curve_definition`
- `yield_curve_point_observation`
- `reference_rate_definition`
- `reference_rate_observation`
- `data_collection_specification`
- `source_endpoint`

## 10. Indicator classifications

### Equity indices

- All Share
- Broad market
- Composite
- Large cap
- Mid cap
- Small cap
- Sector
- Total return
- Price return
- Equal weighted
- Free-float weighted

### Money-market indicators

- Interbank rate
- Treasury bill index
- Money-market fund index
- Overnight rate
- Policy rate
- Deposit rate
- Repo rate

### Bond indicators

- Government bond index
- Corporate bond index
- Aggregate bond index
- Short-term maturity bucket
- Medium-term maturity bucket
- Long-term maturity bucket
- Inflation-linked bond index
- Sukuk index

### Reference rates / TSR

`TSR` must be stored with an explicit canonical definition. It may refer to a Treasury security rate, taux sans risque, total shareholder return, or another country-specific acronym. The model therefore uses `reference_rate_definition` with an unambiguous `rate_type`, while retaining the original local label and acronym.

## 11. Required index and rate fields

Each index, curve or rate definition must support at least:

```text
indicator_id
canonical_name
local_name
short_name
ticker
indicator_type
asset_class
subtype
provider_organisation_id
administrator_organisation_id
calculation_agent_organisation_id
country_id
currency_id
geographic_universe_id
base_date
base_value
calculation_methodology
return_type
weighting_method
publication_frequency
observation_frequency
maturity_bucket
maturity_min_days
maturity_max_days
tenor
status
valid_from
valid_to
```

## 12. Source URL and scraping method

A single URL field is insufficient. Each indicator may have several endpoints and several collection methods over time.

### `source_endpoint`

```text
source_endpoint_id
source_id
indicator_id
endpoint_type
url
http_method
content_type
authentication_type
request_headers_json
request_parameters_json
landing_page_url
download_url
api_url
publication_calendar_url
robots_policy_status
terms_of_use_url
valid_from
valid_to
```

### Endpoint types

- HTML landing page
- HTML table
- CSV
- XLS
- XLSX
- PDF
- JSON API
- XML API
- SOAP API
- GraphQL API
- RSS/Atom
- ZIP archive
- Manual publication
- Email publication

### `data_collection_specification`

```text
collection_specification_id
indicator_id
source_endpoint_id
collection_method
extractor_type
parser_name
parser_version
selector_or_path
worksheet_selector
header_row_rule
date_extraction_rule
value_extraction_rule
unit_conversion_rule
locale_rule
thousands_separator_rule
decimal_separator_rule
missing_value_rule
duplicate_rule
revision_rule
frequency
schedule_expression
timezone_id
retry_policy_json
validation_rule_set_id
quality_threshold
is_active
valid_from
valid_to
```

### Collection methods

- Official API
- Direct file download
- HTML table extraction
- Embedded JSON extraction
- PDF table extraction
- Spreadsheet extraction
- Browser automation
- Manual upload
- Email attachment ingestion
- Partner data feed

The method must be versioned, auditable and replaceable without changing the indicator identity.

## 13. Provenance and data lineage

Every observation must be traceable to its exact origin.

```text
observation
  -> extraction record
  -> source endpoint
  -> downloaded artefact
  -> worksheet/page/table
  -> row/column/cell
  -> parser version
  -> transformation rule
  -> validation decision
```

### Minimum observation provenance

```text
source_assertion_id
source_endpoint_id
source_document_id
source_file_id
source_page
source_table
source_sheet
source_row
source_column
source_cell
retrieved_at
published_at
parser_version
raw_value
normalised_value
confidence_score
validation_status
```

## 14. Country read model

The API may expose an aggregated country profile without denormalising the canonical storage model.

```json
{
  "country": {},
  "geographicUniverses": [],
  "currencies": [],
  "preferredFxPairs": [],
  "regulators": [],
  "exchanges": [],
  "centralBanks": [],
  "statisticsAuthorities": [],
  "equityIndices": [],
  "moneyMarketIndicators": [],
  "bondIndices": {
    "shortTerm": [],
    "mediumTerm": [],
    "longTerm": []
  },
  "referenceRates": [],
  "dataSources": [],
  "qualitySummary": {}
}
```

## 15. API resources

```text
GET /api/v1/countries/{countryId}
GET /api/v1/countries/{countryId}/profile
GET /api/v1/countries/{countryId}/geographic-universes
GET /api/v1/countries/{countryId}/currencies
GET /api/v1/countries/{countryId}/fx-pairs
GET /api/v1/countries/{countryId}/regulators
GET /api/v1/countries/{countryId}/exchanges
GET /api/v1/countries/{countryId}/central-banks
GET /api/v1/countries/{countryId}/statistics-authorities
GET /api/v1/countries/{countryId}/indices
GET /api/v1/countries/{countryId}/indices?assetClass=equity
GET /api/v1/countries/{countryId}/indices?assetClass=fixed-income&maturityBucket=short-term
GET /api/v1/countries/{countryId}/reference-rates
GET /api/v1/countries/{countryId}/sources
GET /api/v1/indices/{indexId}/observations
GET /api/v1/indicators/{indicatorId}/collection-specifications
```

## 16. Atomic Design mapping

### Atoms

- `CountryFlag`
- `CountryName`
- `CountryCode`
- `CurrencyCode`
- `FxPairLabel`
- `InstitutionLink`
- `SourceStatusBadge`
- `ScrapingMethodBadge`
- `IndexValue`
- `MaturityBucketBadge`

### Molecules

- `CountryCurrencyRow`
- `CountryInstitutionRow`
- `CountryIndexRow`
- `CountrySourceRow`
- `FxPairQuote`
- `IndexLatestValue`

### Organisms

- `CountryMarketOverview`
- `CountryInstitutionDirectory`
- `CountryCurrencyAndFxPanel`
- `CountryEquityIndicesPanel`
- `CountryMoneyMarketPanel`
- `CountryBondMarketPanel`
- `CountryReferenceRatesPanel`
- `CountryDataSourcesPanel`
- `CountryDataQualityPanel`

### Templates

- `CountryOverviewTemplate`
- `CountryMarketDataTemplate`
- `CountryInstitutionsTemplate`
- `CountrySourcesTemplate`

### Pages

- `CountryOverviewPage`
- `CountryIndicesPage`
- `CountryRatesPage`
- `CountryInstitutionsPage`
- `CountryDataSourcesPage`

## 17. Extension rule

New country-linked resources can be added without altering the `country` core table. A new object should be introduced whenever the information is multi-valued, time-dependent, source-specific, independently addressable, reusable across countries, or has its own lifecycle.

Possible future extensions include:

- Debt management office
- Treasury auction calendar
- Sovereign yield curve
- Interbank market
- Depository
- Clearing house
- Fund association
- Pension authority
- Insurance authority
- Tax authority
- Official gazette
- Government bond auction results
- Inflation-linked benchmarks
- Commodity indices
- Real-estate indices
- Pension fund indices
- Islamic finance indices
- ESG country indices
- Sovereign ratings
- Country risk measures
- Public holidays and settlement calendars
- Data licensing constraints
- API access credentials and secret references

## 18. Non-negotiable rules

1. The country is an aggregation and navigation root, not a monolithic table.
2. Every relation is typed and historised.
3. Every market indicator is an independent canonical object.
4. Every collection URL is versioned through a source endpoint object.
5. Every extraction method is versioned through a collection specification.
6. Raw, normalised, validated and published values remain distinguishable.
7. API representations are derived contracts and do not redefine canonical storage.
8. Atomic Design components consume API view models and do not directly depend on database tables.
9. Regional institutions and exchanges may relate to several countries.
10. No acronym such as `TSR` is accepted without an explicit canonical definition and local-context mapping.
