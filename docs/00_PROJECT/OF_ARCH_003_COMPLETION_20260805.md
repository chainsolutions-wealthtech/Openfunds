# OF-ARCH-003 completion record

```text
DATE: 2026-08-05
STATUS: IMPLEMENTED_AND_TESTED
TASK: OF-ARCH-003
```

## Resolved conflict

The source CSV permits an empty `VALID_FROM`, while the historical SQL table required `valid_from NOT NULL`.

The database now preserves an unknown date as `NULL` with an explicit knowledge status instead of inventing a business date.

## Implemented vocabulary

```text
KNOWN
APPROXIMATE
UNKNOWN
NOT_APPLICABLE
```

## Implemented controls

- nullable `valid_from`;
- explicit start/end status columns;
- consistency checks between values and statuses;
- known historical rows migrated to `KNOWN`;
- open-ended known relationships use `valid_to_status=NOT_APPLICABLE`;
- unknown starts excluded from the current view;
- not-applicable boundaries supported without dates;
- duplicate unknown temporal identities blocked;
- invalid `KNOWN + NULL` combinations rejected;
- PostgreSQL 16 double-application test.

## Acceptance criteria

```text
BUSINESS_DATE_SEPARATE_FROM_SYSTEM_TIME: YES
KNOWN_APPROXIMATE_UNKNOWN_NOT_APPLICABLE: YES
ARTIFICIAL_DATE_INSERTED: NO
CSV_SQL_UNKNOWN_DATE_SEMANTICS_ALIGNED: YES
CURRENT_VIEW_DETERMINISTIC: YES
MIGRATION_ADDITIVE: YES
IDEMPOTENCE_TESTED: YES
```

## Exact continuation point

```text
OF-ARCH-004
```

The next task must introduce a governed migration registry and runner without reordering or silently marking previously applied migrations.
