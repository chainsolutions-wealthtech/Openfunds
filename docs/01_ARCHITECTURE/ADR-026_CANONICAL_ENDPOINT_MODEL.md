# ADR-026 — Canonical endpoint model

```text
STATUS: ACCEPTED
DATE: 2026-08-05
TASK: OF-ARCH-002
```

## Context

Migrations `003_organizations_and_roles.sql` and
`004_source_endpoints_and_indicator_mapping.sql` historically define two shapes
of the same physical runtime relation: `source.endpoint`.

A separate `source.source_endpoint` definition is present only in
`schemas/reference/country_indicator_information_model_v0.1.sql`. That file is
explicitly marked `Proposal only` and `not a migration`. It is retained as
research history, rejected from the governed runtime path and excluded by
`migrations/manifest.json`.

Migration `007_source_endpoint_reconciliation.sql` preserves and reconciles the
two historical `source.endpoint` shapes additively.

## Decision

```text
CANONICAL PHYSICAL RUNTIME RELATION
source.endpoint

NORMALIZED CONTRACT VIEW
source.endpoint_contract

CURRENT VALIDATED VIEW
source.current_endpoint

PARALLEL PROPOSAL
source.source_endpoint — PRESERVED BUT NOT EXECUTED
```

New code and governed migrations must target `source.endpoint` and its normalized
columns:

- `scope_type` and `scope_code`;
- `official_url`, `data_portal_url`, `api_base_url`;
- `auth_required`;
- `file_formats`;
- `expected_frequency`;
- `history_start`;
- validation and validity fields.

The following columns remain compatibility fields for historical migrations and
existing rows:

- `url`;
- `file_format`;
- `authentication_type`;
- `publication_frequency`;
- `expected_history_start`.

They are synchronized by migration 007 and do not constitute a second runtime
model.

## Implementation

Migration `013_canonical_endpoint_model.sql`:

- declares the canonical relation in a machine-readable registry;
- publishes the normalized `source.endpoint_contract` view;
- records compatibility columns;
- creates no competing endpoint table;
- deletes and renames nothing.

The CI tests apply migrations in both historical orders and the governed
migration runner additionally asserts that `source.source_endpoint` is absent
from the runtime database.

## Foreign keys

The canonical endpoint relation is the target of endpoint foreign keys from:

- `source.indicator_source_mapping`;
- `source.provider_series`.

No governed runtime FK targets the proposal relation.

## Consequences

- one physical runtime endpoint model;
- compatibility retained for historical migrations;
- normalized contract available to consumers;
- proposal preserved without accidental execution;
- no destructive migration required.

## Non-goals

This decision does not:

- delete the proposal file;
- remove compatibility columns;
- change source validation statuses;
- deploy to production;
- alter any collected observation.
