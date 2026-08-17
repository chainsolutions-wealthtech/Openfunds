# OF-MAP-002 — Batch 02 completion — 2026-08-17

## Result

Batch 02 is closed and validated.

```text
BATCH: BATCH_02_FUND_SHARE_CLASS_CURRENCIES
RED_RUN: 32067675732
GREEN_RUN: 32067722365
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
OFFICIAL_PDF_INTEGRATION: SUCCESS
CANONICAL_DICTIONARY_INTEGRATION: SUCCESS
REPOSITORY_UNCHANGED_GUARD: SUCCESS
```

## Added mappings

```text
MAP-000005  OFST010410  -> OF_FUND_FUND_PROFILE_BASE_CURRENCY_ID
MAP-000006  OFST020540  -> OF_FUND_SHARE_CLASS_PROFILE_CURRENCY_ID
```

Both mappings are deterministic ISO 4217 reference transformations:

```text
MAPPING_STATUS: TRANSFORMED
TRANSFORMATION_RULE: ISO_4217_TO_REF_CURRENCY_UUID
INFORMATION_LOSS: NONE
IMPORT_SUPPORTED: YES
EXPORT_SUPPORTED: YES
VALIDATION_STATUS: VALIDATED
```

## Cumulative OF-MAP-002 coverage

```text
OFFICIAL_OF_IDS: 1869
CANONICAL_FIELD_IDS: 143
REVIEWED_MAPPING_ROWS: 6
MAPPED_EXTERNAL_IDS: 4
UNMAPPED_EXTERNAL_IDS: 1865
MAPPED_CANONICAL_IDS: 6
```

No synthetic rows were generated for the 1,865 unreviewed Openfunds fields.

## What this completion does not imply

It does not validate launch dates, lifecycle, names, benchmark/index fields, listing currencies, subscription/redemption currencies, fees, documents, regulatory fields or dynamic NAV fields. Those require separate semantic batches.
