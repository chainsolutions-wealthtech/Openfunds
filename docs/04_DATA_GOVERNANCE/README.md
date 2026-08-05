# AfricaFunds Country Data Extension — Documentation Index

## Status

- Proposal status: **Draft for review**
- Target repository: `chainsolutions-wealthtech/Openfunds`
- Base architecture: `architecture/canonical-model-v1-bootstrap`
- Extension version: `0.1.0`

## Purpose

This directory documents the country-level economic, monetary, fiscal, market and fund-data extension of the canonical Openfunds model. It does not replace the accepted architecture. It extends the existing Country-Centric model with a governed indicator catalogue, country-series mappings, collection specifications, observations, coverage controls and benchmark usages.

## Core documents

1. [`Africa_Country_Indicator_Framework_v0.1.md`](Africa_Country_Indicator_Framework_v0.1.md) — hierarchy and complete D00–D17 indicator catalogue.
2. [`Africa_Country_Data_Collection_Workflow_v0.1.md`](Africa_Country_Data_Collection_Workflow_v0.1.md) — end-to-end ingestion, validation, canonicalisation and publication workflow.
3. [`Africa_Macro_Indicator_Usage_Map_v0.1.md`](Africa_Macro_Indicator_Usage_Map_v0.1.md) — how raw series feed ratios, country pages, risk scores and benchmarks.
4. [`../../02_DOMAIN_MODEL/Reference/Country_Statistical_And_Financial_Indicator_Model_v0.1.md`](../../02_DOMAIN_MODEL/Reference/Country_Statistical_And_Financial_Indicator_Model_v0.1.md) — canonical relational model.
5. [`../../03_PILOTS/Tunisia/Tunisia_Country_Data_Pilot_v0.1.md`](../../03_PILOTS/Tunisia/Tunisia_Country_Data_Pilot_v0.1.md) — Tunisia source and benchmark pilot.
6. [`../../../schemas/reference/country_indicator_information_model_v0.1.sql`](../../../schemas/reference/country_indicator_information_model_v0.1.sql) — non-destructive SQL proposal.

## Machine-readable reference datasets

The `data/reference/` directory contains UTF-8 CSV files using `;` as separator:

- `african_countries_v0.1.csv` — 54-country registry;
- `country_source_roles_v0.1.csv` — canonical institution roles and domains;
- `country_coverage_status_overrides_v0.1.csv` — current non-default coverage states;
- `country_benchmark_plan_v0.1.csv` — standard benchmark products and required inputs;
- `country_data_quality_rules_v0.1.csv` — shared validation rules;
- `country_indicator_relational_model_v0.1.csv` — relational implementation map.

The 420 definitions are intentionally stored in reviewable documentation blocks instead of a duplicated country matrix. The complete 22,680 country × indicator view is generated from the country registry, indicator catalogue, source mappings and coverage overrides.

## Architectural rule

The 420 indicators are catalogue definitions. They must **not** become 420 columns on a country table. The runtime model is relational:

```text
Country
  -> Indicator definition
  -> Country-indicator relationship
  -> Provider series mapping
  -> Source endpoint
  -> Collection specification
  -> Raw extraction
  -> Validated observation
  -> Canonical observation
  -> Calculated index / benchmark / API view model
```

## Safety

This contribution contains no destructive migration, removes no existing file and does not alter accepted architecture documents. It is intended for review and incremental integration.
