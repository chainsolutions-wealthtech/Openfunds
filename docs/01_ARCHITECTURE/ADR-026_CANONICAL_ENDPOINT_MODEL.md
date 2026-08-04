# ADR-026 — Canonical endpoint model

```text
STATUS: ACCEPTED
DATE: 2026-08-05
TASK: OF-ARCH-002
```

## Context

Migrations `003_organizations_and_roles.sql` and `004_source_endpoints_and_indicator_mapping.sql` historically define two shapes of the same physical relation: `source.endpoint`.

No `source.source_endpoint` relation exists in the repository. The previously documented conflict between two physical tables was therefore inaccurate. The real issue was the coexistence of legacy and normalized columns within one relation.

Migration `007_source_endpoint_reconciliation.sql` already preserves and reconciles both shapes additively.

## Decision

```text
CANONICAL PHYSICAL RELATION
source.endpoint

NORMALIZED CONTRACT VIEW
source.endpoint_contract

CURRENT VALIDATED VIEW
source.current_endpoint

PARALLEL LEGACY RELATION
NONE
```

New code and migrations must target `source.endpoint` and its normalized columns:

- `scope_type` and `scope_code`;
- `official_url`, `data_portal_url`, `api_base_url`;
- `auth_required`;
- `file_formats`;
- `expected_frequency`;
- `history_start`;
- validation and validity fields.

The following columns remain compatibility fields for historical migrations and existing rows:

- `url`;
- `file_format`;
- `authentication_type`;
- `publication_frequency`;
- `expected_history_start`.

They are preserved non-destructively and synchronized by migration 007. They are not a second endpoint model.

## Implementation

Migration `013_canonical_endpoint_model.sql`:

- declares the canonical relation in a machine-readable registry;
- publishes the normalized `source.endpoint_contract` view;
- records compatibility columns;
- adds no competing endpoint table;
- deletes and renames nothing.

The CI tests apply migrations in both historical orders:

```text
003 → seed → 004 → 007 → 005 → 013
004 → seed → 007 → 005 → 013
```

Both paths are reapplied to verify idempotence.

## Foreign keys

The canonical endpoint relation is the target of the endpoint foreign keys from:

- `source.indicator_source_mapping`;
- `source.provider_series`.

No FK points to a parallel endpoint relation.

## Consequences

- one physical endpoint model;
- compatibility retained for historical migrations;
- normalized contract available to consumers;
- future creation of `source.source_endpoint` is treated as a regression;
- no destructive migration is required.

## Non-goals

This decision does not:

- choose the global migration runner (`OF-ARCH-004`);
- remove compatibility columns;
- change source validation statuses;
- deploy to production;
- alter any collected observation.
