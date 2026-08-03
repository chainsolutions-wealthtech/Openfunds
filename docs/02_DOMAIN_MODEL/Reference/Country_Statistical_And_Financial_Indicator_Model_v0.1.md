# Country Statistical and Financial Indicator Model — v0.1

## Status

Draft extension of the accepted Country-Centric Market Universe.

## 1. Purpose

Add canonical country-level statistical and financial series without turning `country` into an oversized table. The model maps provider-specific series to common indicator definitions while retaining source terminology, history, revisions, provenance and quality.

## 2. Core entities

```text
indicator_domain
indicator_definition
country_indicator_relationship
provider_series_mapping
source_endpoint
data_collection_specification
source_document
extraction_record
statistical_observation
quality_decision
country_data_coverage
calculation_methodology
calculation_run
calculated_observation
```

## 3. Indicator definition

An indicator definition stores stable semantics: canonical code, domain, label, definition, nature, expected frequency, unit family, preferred source role, minimum history, priority, mandatory status and intended uses. It does not store country observations.

## 4. Country relationship

The country-indicator relationship states whether an indicator is required, applicable, published, discontinued, unavailable or represented by a monetary-union series. It also stores preferred frequency, preferred unit, risk-free hierarchy role, coverage status and validity dates.

## 5. Provider mapping

A provider series mapping preserves official provider code, official label, local language, frequency, unit, multiplier, seasonal adjustment, methodology URL, successor/predecessor mapping and validity. A single canonical indicator may have several provider mappings across time or sources.

## 6. Observation model

Observations use a generic statistical structure for scalar series and specialised structures for securities, auctions, yield curves, FX, NAVs and portfolios. Common fields include series, period start/end, observation date, publication date, vintage date, value, unit, status, source assertion, extraction record, quality decision and bitemporal fields.

## 7. Coverage projection

Coverage is a derived governance projection showing source status, first/last observation, count, expected count, completeness, freshness, quality, method breaks, next action and benchmark readiness. It is rebuildable from canonical metadata and observations.

## 8. Compatibility with funds and benchmarks

Country indicators provide inputs to index definitions and fund category reference blocks. The four reference roles remain Primary Market Index, Secondary Market Index, WTI and WTI Bench. Indicator definitions do not embed category membership; relationships connect benchmarks and categories.

## 9. API resources

Suggested resource families:

```text
/indicator-domains
/indicators
/countries/{country_id}/indicators
/country-series
/statistical-observations
/source-endpoints
/collection-specifications
/data-coverage
/calculation-methodologies
/calculation-runs
```

## 10. Non-goals

- no 420-column country table;
- no silent replacement of official data;
- no overwriting revisions;
- no direct UI access to physical tables;
- no destructive migration in this proposal.
