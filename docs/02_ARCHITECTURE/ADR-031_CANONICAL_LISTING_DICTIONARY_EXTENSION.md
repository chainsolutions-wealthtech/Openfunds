# ADR-031 — Canonical Listing dictionary extension

- **Status:** ACCEPTED
- **Date:** 2026-08-17

## Context

`data/dictionary/spec_v1/` is explicitly version `1.0.0`, status `VALIDATED_FUND_CORE_SCOPE`, and describes the 143 physical columns introduced by migration 015. Migration 019 adds a new Listing runtime surface with 34 physical columns.

Rewriting the 143-field package would destroy the meaning of the validated migration-015 baseline and make historical mapping/checksum evidence ambiguous.

## Decision

Keep `data/dictionary/spec_v1/` unchanged as the migration-015 canonical core and model forward-only runtime additions as versioned canonical extension packages.

The first extension is:

```text
data/dictionary/extensions/listing_v1/
```

It contains all 34 physical columns of:

```text
fund.listing
fund.listing_identifier
```

from migration `019_SHARE_CLASS_LISTING_CORE`.

For Openfunds mapping validation, the available canonical inventory is the collision-free union:

```text
143 core fields
+ 34 listing_v1 fields
= 177 canonical fields
```

## Governance rules

1. Extension FIELD_IDs must be globally unique against the core and all other extensions.
2. A declared extension `field_count` must equal its physical field payload.
3. The mapping validator fails closed on collisions or count drift.
4. `spec_v1` checksums and 143-field scope are not rewritten by an extension.
5. A semantic break creates a new FIELD_ID or a new extension version.
6. An Openfunds field may reference an extension FIELD_ID only after the corresponding runtime migration and dictionary extension are validated.

## Immediate consequence

SEDOL (`OFST020040`) can be mapped to `LISTING_IDENTIFIER` fields only after the checksum-locked official field record is re-audited. It must not be represented as a Share Class entity identifier merely because migration 018 recognizes the `SEDOL` scheme at the wider identifier vocabulary level.

## Alternatives rejected

- silently expanding `spec_v1` beyond its documented 143 migration-015 fields;
- creating mapping-only pseudo FIELD_IDs with no physical runtime field;
- attaching SEDOL to `fund.entity_identifier` despite its Listing-level Openfunds semantics.
