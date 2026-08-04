# OF-ARCH-001 and OF-SOURCE-001 completion record

```text
DATE: 2026-08-05
STATUS: IMPLEMENTED_AND_TESTED
SCOPE: GOVERNED_REFERENCE_AUTHORING_AND_BCEAO_BEAC_FX_SYNCHRONIZATION
```

## Decision

The project distinguishes two authorities:

```text
AUTHORING_AUTHORITY
VALIDATED_FX_REFERENCE_REGISTRY.csv for collection-tested FX pilots

RUNTIME_AUTHORITY
PostgreSQL after deterministic generated SQL is applied
```

This resolves the apparent conflict between `ADR-003` and `ADR-021`. Broad reference CSV files remain discovery inventories. The compact validated registry is the only authoring source for the two tested FX pilots.

## Implemented controls

- UTF-8, semicolon, exact-header and completeness validation;
- exactly two governed pilots: BCEAO/XOF and BEAC/XAF;
- controlled run ID, raw SHA256, value date, parser version and retrieval timestamp;
- stable preservation of identifiers already introduced by migrations 008 and 009;
- deterministic UUIDv5 for newly introduced technical rows;
- deterministic SQL generation;
- generation followed by byte-for-byte `--check`;
- deliberate evidence-corruption unit test;
- PostgreSQL 16 double-application test and SQL assertions;
- explicit prohibition of historical-status overstatement.

## Synchronized runtime objects

For BCEAO/UEMOA/XOF and BEAC/CEMAC/XAF:

- organization validation metadata;
- validated collector endpoint;
- raw snapshot mapping;
- EUR and USD calculated mappings;
- raw and calculated provider series;
- raw and calculated collection specifications;
- links to controlled collection evidence.

## Preserved distinctions

```text
GENERIC DISCOVERY ENDPOINTS
!= VALIDATED COLLECTOR ENDPOINTS

COLLECTION_TESTED
!= PARTIAL_HISTORY_LOADED
!= COMPLETE_HISTORY_LOADED
```

The generated reconciliation uses BCEAO run `30777722357` and BEAC run `30779605759`.

## Acceptance criteria

```text
MASTER_AUTHORING_REPRESENTATION_DECLARED: YES
RUNTIME_TRUTH_PRESERVED_AS_POSTGRESQL: YES
OTHER_REPRESENTATION_GENERATED: YES
BCEAO_BEAC_STATUSES_RECONCILED_AT_RUNTIME: YES
DIVERGENCE_TEST_PRESENT: YES
METHOD_DOCUMENTED: YES
EXISTING_IDS_PRESERVED: YES
EVIDENCE_LINKED: YES
GENERATED_SQL_IDEMPOTENCE_TESTED: YES
HISTORY_STATUS_OVERSTATED: NO
```

## Exact continuation point

```text
OF-ARCH-002
→ OF-ARCH-003
→ OF-ARCH-004
```

`OF-ARCH-002` must unify the endpoint model without undoing migration 007 or creating a parallel endpoint registry.
