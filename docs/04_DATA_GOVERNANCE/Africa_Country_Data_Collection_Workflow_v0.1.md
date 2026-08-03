# Africa Country Data Collection Workflow — v0.1

## 1. Objective

Define a repeatable and auditable workflow for collecting economic, financial, market and fund data from official African sources.

## 2. End-to-end flow

```text
Official institution
  -> Source registry
  -> Source endpoint
  -> Collection specification
  -> Scheduled collection run
  -> Immutable raw artefact
  -> Extraction record
  -> Normalisation
  -> Entity and series mapping
  -> Validation rules
  -> Quarantine or canonical observation
  -> Calculation run
  -> Index / benchmark / ratio
  -> API resource
  -> Atomic Design view model
```

## 3. Source registry

Each country records typed organisation roles: central bank, statistics office, ministry of finance, debt office, exchange, securities/fund regulator, insurance/pension regulator, central securities depository and official gazette. Organisations are canonical entities, not text columns.

A source endpoint records the landing page, direct download/API URL, HTTP method, content type, authentication, terms of use, publication calendar, validity dates and priority. One indicator may have several endpoints: primary, archive, fallback and methodology.

## 4. Collection specification

Each country series has a versioned collection specification containing at least:

- collection method and schedule;
- extractor and parser name/version;
- selectors, worksheet and header rules;
- date and value extraction rules;
- locale, decimal and thousands separators;
- missing-value and duplicate rules;
- revision and vintage rules;
- unit conversion;
- validation rule set;
- retry and fallback policy;
- quality threshold;
- valid-from and valid-to dates.

## 5. Raw zone

Original PDF, Excel, CSV, XML, JSON, HTML and images are stored immutably. The source-document record keeps original filename, URL, publication date, retrieval timestamp, MIME type, byte size, SHA-256, licence, HTTP metadata and collection run.

## 6. Extraction and normalisation

The extraction record retains raw text/value and exact source location. Numeric normalisation must handle spaces, non-breaking spaces, comma/point decimal conventions, parentheses for negatives, percentages, multipliers and Excel serial dates. Source labels are preserved.

Normalisation never changes the meaning of a published observation. Suspected source anomalies are flagged rather than corrected blindly.

## 7. Mapping

A provider series mapping links:

```text
country + provider series code + provider label
  -> canonical indicator definition
```

Mappings are historised because providers rename, replace, split or redefine series. Method breaks create successor relationships or separate segments.

## 8. Validation

Validation operates at document, series, observation, security, curve, fund and index levels. Critical rules include readability, deduplication, unit presence, date/frequency compatibility, numeric parseability, revision preservation, entity uniqueness, AUM reconciliation, curve-tenor consistency, price/yield plausibility and no look-ahead bias.

Failed records enter quarantine with severity, error code, evidence, owner and resolution status. Validated records receive a quality decision and confidence score.

## 9. Canonical storage

Canonical storage is PostgreSQL and bitemporal:

- business validity: `valid_from`, `valid_to`;
- system knowledge: `recorded_at`, `superseded_at`;
- source assertion and validation decision;
- correction lineage and replacement links.

Raw, validation, canonical, analytical, API and view-model structures remain separate.

## 10. Calculations

Calculation runs are versioned and reproducible. Each output records input observations, methodology version, parameters, calendar, FX observations, exclusions and quality state. Calculated products include real rates, debt ratios, curve slopes, sovereign spreads, cash indices, rolling T-Bill indices, sovereign total-return indices, equity total-return indices, WTI, WTI Bench and country risk scores.

## 11. Scheduling

| Frequency | Typical objects |
|---|---|
| Intraday / daily | FX, market prices, NAVs, reference rates, indices |
| Weekly | Auctions, central-bank operations, short rates |
| Monthly | CPI, monetary aggregates, credit, trade, fund AUM |
| Quarterly | GDP, balance of payments, banking soundness, public debt |
| Annual | Full national accounts, budgets, demographics and institutional reports |
| Event-driven | Policy decisions, ratings, fund events, methodology and regulation |

## 12. Monitoring

Monitoring covers freshness, expected publication, document count, observation count, schema drift, parser errors, missing dates, outliers, reconciliation gaps, revision magnitude, API availability and licence changes. Alerts do not overwrite data.

## 13. Country onboarding definition of done

A country is onboarded when institutions and endpoints are registered, critical series mappings exist, a sample collection is reproducible, raw artefacts and provenance are stored, validation rules pass or documented exceptions exist, canonical observations are queryable, and at least one country page projection or benchmark can be produced.
