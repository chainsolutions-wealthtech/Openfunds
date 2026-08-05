# Canonical project state — 2026-08-04

## Status scale

```text
DOCUMENTED
PROPOSED
DECIDED
STRUCTURE_PRESENT
IMPLEMENTED
TESTED
COLLECTION_TESTED
PARTIAL_HISTORY_LOADED
COMPLETE_HISTORY_LOADED
PRODUCTION_DEPLOYED
```

A status is never promoted merely because a file, table, code or placeholder exists.

## Current state by domain

| Domain | Current status | Evidence | Explicit limit |
|---|---|---|---|
| Project architecture | DECIDED / DOCUMENTED | ADR-001 to ADR-020, architecture docs | Physical model still incomplete |
| Geography | STRUCTURE_PRESENT | 54 countries, 5 regions, continent, zones | Official/historical validation partial |
| Country relationships | STRUCTURE_PRESENT | 266 relationships | Most validation statuses pending; dates open |
| Currencies and FX pairs | STRUCTURE_PRESENT | 44 currencies, 84 required pairs | Most provider routes not collected |
| BCEAO FX | COLLECTION_TESTED | live/fixture/PostgreSQL tests | snapshot only, no complete history |
| BEAC FX | COLLECTION_TESTED | live/fixture/PostgreSQL tests | snapshot only, no complete history |
| Daily FX orchestration | IMPLEMENTED / TESTED IN STAGING | dual-source pipeline | no durable production persistence |
| Organizations and sources | STRUCTURE_PRESENT / PARTIAL | roles, organizations, endpoints, mappings | 54-country coverage incomplete; CSV/SQL drift |
| D00-D17 catalogue | DOCUMENTED / PROPOSED | approximately 420 definitions | no single machine-readable master catalogue |
| Fund identity model | PROPOSED / PARTIAL | conceptual and SQL proposals | Fund/SubFund/ShareClass unresolved |
| Taxonomy inputs | STRUCTURE_PRESENT / TESTED | 4 classes, 7 subclasses, 9 templates | not production seeded/activated |
| Classification routing | IMPLEMENTED / TESTED | deterministic generator, 486 rules | routing currently uses legal domicile fallback |
| Categories and peer groups | STRUCTURE_PRESENT / TESTED | 432 unique generated structures | no live fund membership universe |
| Reference blocks | STRUCTURE_PRESENT / TESTED | 432 blocks and role slots | provider series/methodologies not validated |
| Excel workbook | DERIVED_REVIEW_EXPORT | v0.4.2 manifest and checksum | binary not canonical; full reproducibility gate open |
| WTI | DECIDED / NOT_IMPLEMENTED | definition and role slots | no calculation engine or eligible NAV history |
| WTI Bench | PROPOSED/PARTIALLY_DECIDED | role slots and candidate methods | not calculated or activated |
| Risk-free rate and MAR | PROPOSED | role slots | series selection not validated |
| Metrics and rankings | NOT_IMPLEMENTED | dependency matrix only | no live calculations |
| Openfunds mapping | DOCUMENTED METHOD / ABSENT IMPLEMENTATION | OPENFUNDS_MAPPING.md | official catalogue and mapping absent |
| Tunisia OPCVM | EXTERNAL_SOURCE_ANALYSED | source analysis | no canonical import in repository |
| Nigeria OPCVM | SOURCE_IDENTIFIED / INGESTION_NOT_IMPLEMENTED | research and requirements | no complete archive loader |
| API/UI | DOCUMENTED / NOT_IMPLEMENTED | architecture | no OpenAPI, server, SDK or frontend |
| Production | NOT_DEPLOYED | staging workflows only | no persistent DB/raw store |

## Semantic reconciliations required

### Legal domicile and local market

The newer matrix uses:

```text
LEGAL_COUNTRY
→ LOCAL_MARKET
→ GEOGRAPHIC_REGION
→ AFRICA
```

Older texts still describe:

```text
COUNTRY
→ NATIONAL_CATEGORY
→ REGIONAL_CATEGORY
→ AFRICA_CATEGORY
```

This is an open decision, not an automatic rewrite.

### Investment scope

Current V0.1 routing starts from legal domicile, asset class and optional subclass. Future routing must separately consider:

```text
LEGAL_DOMICILE_COUNTRY
REGULATORY_SCOPE
INVESTMENT_GEOGRAPHY
PRIMARY_MARKET_SCOPE
DECLARED_BENCHMARK
REFERENCE_CURRENCY
```

No implementation is claimed.

### Excel and generator

The workbook is a review export. The repository must eventually prove that the export is fully reproducible from canonical inputs and a versioned generator. Until then, the workbook cannot become an editing authority.

## Non-active product declaration

The presence of codes such as `WTI_*`, `WTIB_*`, `BM_*`, `RFR_*` and `MAR_*` means structural role prefill only. It does not prove:

- observations;
- histories;
- licenses;
- selected methodologies;
- calculations;
- production publication.
