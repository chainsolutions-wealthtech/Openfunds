# OF-ARCH-002 completion record

```text
DATE: 2026-08-05
STATUS: IMPLEMENTED_AND_TESTED
TASK: OF-ARCH-002
```

## Corrected diagnosis

The governed runtime migrations use one physical endpoint relation:
`source.endpoint`.

`source.source_endpoint` appears only in
`schemas/reference/country_indicator_information_model_v0.1.sql`, whose header
states `Proposal only` and `not a migration`. The proposal is preserved for
traceability but is excluded from `migrations/manifest.json`.

The historical migrations 003 and 004 define different column shapes for
`source.endpoint`. Migration 007 reconciles those shapes without deleting source
rows or destructively overwriting typed URLs.

## Final canonical model

```text
PHYSICAL CANONICAL RUNTIME TABLE
source.endpoint

NORMALIZED CONTRACT VIEW
source.endpoint_contract

VALIDATED CURRENT VIEW
source.current_endpoint

MACHINE-READABLE DECLARATION
source.endpoint_model_contract_registry

NON-OPERATIONAL PROPOSAL
source.source_endpoint
```

## Implemented safeguards

- additive migration `013_canonical_endpoint_model.sql`;
- no runtime table rename, deletion or replacement;
- compatibility fields explicitly recorded;
- normalized contract view;
- CI assertion that governed migrations do not create `source.source_endpoint`;
- manifest exclusion of the proposal file;
- endpoint foreign keys target `source.endpoint`;
- both historical creation orders tested and replayed.

## Acceptance criteria

```text
SINGLE_RUNTIME_MODEL: YES
CANONICAL_RELATION_DECLARED: YES
FOREIGN_KEYS_RECONCILED: YES
ADDITIVE_MIGRATION: YES
ORDER_003_004_TESTED: YES
ORDER_004_FIRST_TESTED: YES
IDEMPOTENCE_TESTED: YES
PARALLEL_PROPOSAL_PRESERVED: YES
PARALLEL_PROPOSAL_EXECUTED: NO
DESTRUCTIVE_CHANGE: NO
```

## Continuation

`OF-ARCH-003` and `OF-ARCH-004` are governed by ADR-027 and ADR-028.
