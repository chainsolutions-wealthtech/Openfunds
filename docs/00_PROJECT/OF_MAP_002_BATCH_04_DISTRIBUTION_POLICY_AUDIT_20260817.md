# OF-MAP-002 — Batch 04 Share Class Distribution Policy audit — 2026-08-17

## Scope

Batch 04 maps one Openfunds Core field whose semantics and allowed values align deterministically with an existing canonical Share Class profile field.

## Official source

Openfunds v2.13.0 field:

```text
OF-ID: OFST020400
Field Name: Share Class Distribution Policy
Field Level: Share Class
Data Type: string
Values: accumulating / accumulating & distributing / distributing
```

Official reference:

- https://openfunds.org/OFST020400

## Canonical target

```text
OF_FUND_SHARE_CLASS_PROFILE_DISTRIBUTION_POLICY
ENTITY_CODE: SHARE_CLASS_PROFILE
```

The governed canonical vocabulary already contains:

```text
ACCUMULATING
DISTRIBUTING
MIXED
UNKNOWN
```

## Deterministic transformation

```text
accumulating                -> ACCUMULATING
accumulating & distributing -> MIXED
distributing                -> DISTRIBUTING
```

`UNKNOWN` is a canonical fallback state and is not emitted as an Openfunds value for this field.

## Mapping decision

```text
MAP-000013
OFST020400 -> OF_FUND_SHARE_CLASS_PROFILE_DISTRIBUTION_POLICY
MAPPING_STATUS: TRANSFORMED
TRANSFORMATION_RULE: OPENFUNDS_DISTRIBUTION_POLICY_TO_CANONICAL_ENUM
INFORMATION_LOSS: NONE
IMPORT_SUPPORTED: YES
EXPORT_SUPPORTED: YES
VALIDATION_STATUS: VALIDATED
```

The reverse mapping is deterministic for all three Openfunds values because `MIXED` is reserved here for the Openfunds hybrid value.

## Expected cumulative state at Batch 04 closure

```text
REVIEWED_MAPPING_ROWS: 13
MAPPED_EXTERNAL_IDS: 7
UNMAPPED_EXTERNAL_IDS: 1862
MAPPED_CANONICAL_IDS: 7
```
