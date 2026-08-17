# OF-MAP-002 — Batch 03 Valor + WKN audit — 2026-08-17

## Context

Migration `018_EXTENDED_SECURITY_IDENTIFIER_SCHEMES` widened the canonical `fund.entity_identifier.identifier_scheme` vocabulary forward-only with `WKN`, `SEDOL` and `VALOR`. PostgreSQL 16 and the governed dictionary now enforce the same vocabulary.

Batch 03 intentionally maps only identifiers whose Openfunds field level is compatible with the canonical Fund/SubFund/ShareClass supertype.

## Included fields

### OFST020010 — Valor

Official Openfunds semantics:

```text
Field Name: Valor
Field Level: Share Class
Data Type: integer
Description: Swiss securities identification number (Valor)
```

Canonical representation:

```text
fund.entity_identifier.identifier_value      decimal string preserving the published integer value
fund.entity_identifier.identifier_scheme     constant VALOR
fund.entity_identifier.normalized_value      canonical decimal string
```

The external integer is converted deterministically to its decimal string because the canonical identifier model stores identifier values as text to preserve scheme-specific identifiers uniformly.

### OFST020015 — WKN

Official Openfunds semantics:

```text
Field Name: WKN
Field Level: Share Class
Data Type: string
Description: German securities identification number (Wertpapierkennnummer)
Example: A1J0A4
```

Canonical representation:

```text
fund.entity_identifier.identifier_value      source value
fund.entity_identifier.identifier_scheme     constant WKN
fund.entity_identifier.normalized_value      trimmed uppercase matching value
```

The original value is preserved separately from the normalized matching value.

## Explicit exclusion — OFST020040 SEDOL

Openfunds currently defines `OFST020040 SEDOL` at **Listing** level, not Share Class level, and notes that licensing requirements may apply to ingesting, storing or distributing the field.

The current canonical runtime has Fund/SubFund/ShareClass entities but no governed Listing entity. Batch 03 therefore does **not** force SEDOL into `fund.entity_identifier`. The `SEDOL` scheme is available in the canonical vocabulary for future compatible entities, but the Openfunds mapping remains blocked until Listing is modeled and licensing policy is reviewed.

## Exact mapping allowlist

```text
MAP-000007 OFST020010 -> OF_FUND_FUND_ENTITY_IDENTIFIER_IDENTIFIER_VALUE
MAP-000008 OFST020010 -> OF_FUND_FUND_ENTITY_IDENTIFIER_IDENTIFIER_SCHEME
MAP-000009 OFST020010 -> OF_FUND_FUND_ENTITY_IDENTIFIER_NORMALIZED_VALUE
MAP-000010 OFST020015 -> OF_FUND_FUND_ENTITY_IDENTIFIER_IDENTIFIER_VALUE
MAP-000011 OFST020015 -> OF_FUND_FUND_ENTITY_IDENTIFIER_IDENTIFIER_SCHEME
MAP-000012 OFST020015 -> OF_FUND_FUND_ENTITY_IDENTIFIER_NORMALIZED_VALUE
```

Expected cumulative state:

```text
REVIEWED_MAPPING_ROWS: 12
MAPPED_EXTERNAL_IDS: 6
UNMAPPED_EXTERNAL_IDS: 1863
MAPPED_CANONICAL_IDS: 6
```

No other Openfunds field is authorized by this batch.
