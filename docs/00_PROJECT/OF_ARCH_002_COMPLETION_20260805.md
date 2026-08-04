# OF-ARCH-002 completion record

```text
DATE: 2026-08-05
STATUS: IMPLEMENTED_AND_TESTED
TASK: OF-ARCH-002
```

## Corrected diagnosis

The repository does not contain a physical `source.source_endpoint` relation.

The historical migrations 003 and 004 define different column shapes for the same table, `source.endpoint`. Migration 007 already reconciles those shapes without deleting source rows or overwriting typed URLs destructively.

## Final canonical model

```text
PHYSICAL CANONICAL TABLE
source.endpoint

NORMALIZED CONTRACT VIEW
source.endpoint_contract

VALIDATED CURRENT VIEW
source.current_endpoint

MACHINE-READABLE DECLARATION
source.endpoint_model_contract_registry
```

## Implemented safeguards

- additive migration `013_canonical_endpoint_model.sql`;
- no table rename, deletion or replacement;
- compatibility fields explicitly recorded;
- normalized contract view;
- CI assertion that `source.source_endpoint` does not exist;
- CI assertion that mapping and provider-series FKs target `source.endpoint`;
- validation that no validated endpoint lacks a canonical URL;
- both migration orders tested and replayed.

## Acceptance criteria

```text
SINGLE_PHYSICAL_MODEL: YES
CANONICAL_RELATION_DECLARED: YES
FOREIGN_KEYS_RECONCILED: YES
ADDITIVE_MIGRATION: YES
ORDER_003_004_TESTED: YES
ORDER_004_FIRST_TESTED: YES
IDEMPOTENCE_TESTED: YES
PARALLEL_ENDPOINT_TABLE: NO
DESTRUCTIVE_CHANGE: NO
```

## Exact continuation point

```text
OF-ARCH-003
→ OF-ARCH-004
```

`OF-ARCH-003` must define unknown business-date semantics without inventing dates or changing collected source-value dates.
