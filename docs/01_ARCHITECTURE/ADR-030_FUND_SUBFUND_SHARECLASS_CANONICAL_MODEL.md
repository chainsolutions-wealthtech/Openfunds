# ADR-030 — Canonical Fund / SubFund / ShareClass model

```text
STATUS: ACCEPTED
DATE: 2026-08-05
TASK: OF-DATA-001
MIGRATION: 015_FUND_SUBFUND_SHARECLASS_CORE
```

## Context

`ADR-009` accepted the separation of fund, compartment and share class, but the
existing SQL proposal contained only `fund.fund` and `fund.share_class`. It could
not represent an umbrella product, a real compartment, historical names,
identifier changes, mergers or management transfers without ambiguity.

The model must also cover standalone SICAV, FCP or unit trusts without inventing
a synthetic compartment.

## Decision

The canonical runtime hierarchy is:

```text
STANDALONE
FUND -> SHARE_CLASS

UMBRELLA
FUND -> SUBFUND -> SHARE_CLASS
```

### Entity meanings

- `FUND`: legal vehicle or standalone collective investment product;
- `SUBFUND`: real compartment, portfolio or series inside an umbrella fund;
- `SHARE_CLASS`: investable class carrying class-specific currency and policies.

A sponsor, fund group or management company remains an organization. It is not
represented as an additional fund level.

## Stable identity and versioned facts

`fund.entity` is the stable identity supertype. The following facts are stored
separately and may be versioned:

- lifecycle and domicile;
- legal/structural profile;
- current and former names and aliases;
- ISIN, LEI, regulator and local identifiers;
- structural parentage;
- legal and operational events.

A name change does not create a new entity. A merger may connect predecessor,
successor, surviving and absorbed entities through event participants.

## Structural rules

```text
FUND_HAS_SUBFUND
requires FUND.structure_type = UMBRELLA

FUND_HAS_SHARE_CLASS
requires FUND.structure_type = STANDALONE

SUBFUND_HAS_SHARE_CLASS
requires a real SUBFUND attached to a current UMBRELLA FUND
```

A current subfund or share class has at most one current structural parent.
Standalone funds therefore do not receive a fake subfund row.

## Temporal and provenance rules

Business dates use the accepted statuses:

```text
KNOWN
APPROXIMATE
UNKNOWN
NOT_APPLICABLE
```

`UNKNOWN` and `NOT_APPLICABLE` require a `NULL` date. System knowledge is
preserved with `recorded_at`, `superseded_at` and `is_current`.

Every versioned fact can reference a raw artifact and a structured source
locator. Absence of an artifact during early manual validation does not authorize
a production or historical-coverage claim.

## Migration and compatibility

Migration `015` creates new canonical tables under `fund.*`. It deliberately
does not create or alter the legacy proposal tables `fund.fund` and
`fund.share_class`. The proposal
`schemas/taxonomy/fund_relationship_information_model_v0.1.sql` remains in Git
as superseded research history and remains excluded from the operational
manifest.

No fund record is loaded by the migration itself. Clean PostgreSQL 16 execution,
idempotent replay, adoption without a ledger and fixture-based structural tests
are required before completion.

## Alternatives rejected

1. **Always create a subfund:** rejected because it invents an economic object for
   standalone vehicles.
2. **Put names and ISIN directly on one fund row:** rejected because changes and
   aliases would overwrite identity history.
3. **Use one generic parent column without constrained edge types:** rejected
   because invalid fund/subfund/share-class paths would remain possible.
4. **Promote the existing draft unchanged:** rejected because it lacks the
   complete compartment and event model.

## Consequences

- Morocco-style standalone SICAVs may link directly to share classes;
- Tunisia-style umbrellas may expose real compartments and class paths;
- Nigeria-style standalone unit trusts may contain several classes;
- rename, merger, liquidation and management-transfer evidence remains explicit;
- fund history imports remain blocked until sources are mapped and durable raw
  storage is available;
- service-provider mandates and taxonomy memberships remain separate follow-up
  relations, not overloaded structural edges.
