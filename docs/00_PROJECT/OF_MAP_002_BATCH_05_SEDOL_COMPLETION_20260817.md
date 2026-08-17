# OF-MAP-002 — Batch 05 SEDOL — completion — 2026-08-17

## Verdict

Batch 05 is **SEMANTICALLY VALIDATED / LICENCE GATED**.

`OFST020040` is mapped to the migration-019 `LISTING_IDENTIFIER` model. Runtime import, storage/export activation remains disabled until explicit SEDOL licensing clearance exists.

## Official checksum-locked evidence

Audit workflow: `32071520665`.

Source archive SHA256:

```text
40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4
```

The exact official v2.13.0 record establishes:

```text
OF-ID       OFST020040
Field Name  SEDOL
Field Level Listing
Data Type   string
Introduced  1.2
Example     BVTW3G0
```

The official field record also warns that licensing requirements may apply to ingesting, storing or distributing the data.

The audit was read-only and finished with an unchanged repository guard.

## Canonical prerequisites closed before mapping

SEDOL was deliberately not forced into `fund.entity_identifier` when Batch 03 was built.

The following prerequisites were completed first:

1. migration `019_SHARE_CLASS_LISTING_CORE`;
2. `fund.listing` and `fund.listing_identifier` runtime tables;
3. PostgreSQL 16 GREEN run `32070768364`;
4. canonical `listing_v1` dictionary extension with 34 physical fields;
5. collision-free mapping inventory union: 143 core + 34 extension = 177 fields;
6. union GREEN run `32071385088`.

## TDD

RED run: `32071737609`.

All prior mapping batches and canonical-extension contracts were green. The only Batch 05 failures were the absence of `MAP-000014`, `MAP-000015` and `MAP-000016`.

A historical Batch 04 test then revealed a forward-compatibility defect because it froze the entire registry at 13 rows. The test was corrected to preserve only the Batch 04 invariant, consistent with the already-corrected Batch 02 and Batch 03 contracts.

GREEN run: `32071858346`.

All succeeded:

- Python 3.11 mapping contracts;
- Python 3.12 mapping contracts;
- canonical core+extension union;
- checksum-locked official PDF inventory integration;
- unchanged-repository guard.

## Exact mapping rows

### MAP-000014

```text
OFST020040
→ OF_FUND_LISTING_IDENTIFIER_IDENTIFIER_VALUE
ONE_TO_MANY / IDENTITY
```

### MAP-000015

```text
OFST020040
→ OF_FUND_LISTING_IDENTIFIER_IDENTIFIER_SCHEME
ONE_TO_MANY / CONSTANT_SEDOL
```

### MAP-000016

```text
OFST020040
→ OF_FUND_LISTING_IDENTIFIER_NORMALIZED_VALUE
ONE_TO_MANY / TRIM_AND_UPPERCASE_SEDOL
```

For all three rows:

```text
CANONICAL_ENTITY = LISTING_IDENTIFIER
INFORMATION_LOSS = NONE
VALIDATION_STATUS = VALIDATED
IMPORT_SUPPORTED = NO
EXPORT_SUPPORTED = NO
NOTES contains LICENSE_GATE_REQUIRED
```

## Coverage after Batch 05

```text
OFFICIAL_OPENFUNDS_IDS        1869
REVIEWED_MAPPING_ROWS         16
MAPPED_EXTERNAL_IDS           8
UNMAPPED_EXTERNAL_IDS         1861
CANONICAL_FIELDS_AVAILABLE    177
MAPPED_CANONICAL_IDS          10
```

No synthetic `UNMAPPED` rows are materialized.

## Activation rule

Semantic validation must not be confused with permission to ingest, persist or redistribute SEDOL data.

The three mappings remain inactive for runtime import/export unless a future governed decision records explicit licensing clearance and changes the corresponding gates through a separately reviewed change.

## Next mapping unit

Audit additional Listing-level Openfunds fields from the checksum-locked official PDF, prioritizing fields that can map directly to the migration-019 model such as venue/MIC, listing currency or ticker, while preserving licensing and field-level semantics independently.
