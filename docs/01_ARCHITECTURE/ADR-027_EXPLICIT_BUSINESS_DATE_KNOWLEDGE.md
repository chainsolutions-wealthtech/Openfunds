# ADR-027 — Explicit business-date knowledge

```text
STATUS: ACCEPTED
DATE: 2026-08-05
TASK: OF-ARCH-003
```

## Context

`COUNTRY_RELATIONSHIPS.csv` preserves unknown validity dates as empty values. The historical SQL migration required `valid_from NOT NULL`, creating pressure to invent a date during import.

An unknown date is not equivalent to an old date, the ingestion date or the beginning of a software epoch.

## Decision

Every temporal boundary carries both a value and a knowledge status:

```text
KNOWN
APPROXIMATE
UNKNOWN
NOT_APPLICABLE
```

Rules:

- `KNOWN`: a date value is mandatory and supported by exact evidence;
- `APPROXIMATE`: a date value is mandatory but its precision is explicitly approximate;
- `UNKNOWN`: the date value must remain `NULL`;
- `NOT_APPLICABLE`: the temporal boundary does not apply and the date value must remain `NULL`.

No artificial date may be inserted to satisfy a database constraint.

## Current-view semantics

A relationship may enter `ref.current_entity_relationship` only when:

- its start is `KNOWN`, `APPROXIMATE` and effective, or `NOT_APPLICABLE`;
- its end is `KNOWN`, `APPROXIMATE` and not expired, or `NOT_APPLICABLE`;
- its validation status is `VALIDATED`.

A boundary marked `UNKNOWN` is never silently interpreted as current.

## Implementation

Migration `014_business_date_semantics.sql`:

- removes the `NOT NULL` requirement from `valid_from`;
- adds `valid_from_status` and `valid_to_status`;
- classifies existing dated rows as `KNOWN`;
- classifies an absent open-ended `valid_to` as `NOT_APPLICABLE`;
- adds value/status consistency constraints;
- adds a deterministic uniqueness index without storing a sentinel date;
- rebuilds the current view with explicit knowledge semantics.

The expression index uses PostgreSQL `-infinity` only as an index comparison expression. It does not store or expose an invented business date.

## Separation from system time

Business validity remains separate from:

- source value date;
- retrieval timestamp;
- collection-run timestamps;
- `created_at` and `updated_at`;
- future bitemporal `recorded_at` and `superseded_at` fields.

## Consequences

- CSV and SQL semantics agree on unknown dates;
- imports can preserve missing evidence honestly;
- current views no longer assume unknown relationships are active;
- exact and approximate evidence remain distinguishable;
- no historical status or date is inferred.

## Non-goals

This ADR does not invent missing dates, validate the 266 relationships, or define the global migration runner.
