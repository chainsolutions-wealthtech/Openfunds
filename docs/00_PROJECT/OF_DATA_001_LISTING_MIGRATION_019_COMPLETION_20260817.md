# OF-DATA-001 — Listing migration 019 — completion — 2026-08-17

## Verdict

`019_SHARE_CLASS_LISTING_CORE` is **VERIFIED_COMPLETE** on the governed branch.

The migration is additive and forward-only. It does not rewrite migrations 015 or 018 and it does not activate any production data load.

## Runtime model delivered

### `fund.listing`

A listing is a market occurrence of a canonical `SHARE_CLASS`, separate from the legal/economic identity stored in `fund.entity`.

Key governed properties:

- composite FK to `fund.entity(entity_id, entity_type)` with `entity_type = SHARE_CLASS`;
- optional `exchange_organization_id` to `ref.organization`;
- optional ISO-10383-style `venue_mic` locator;
- optional trading currency reference to `ref.currency`;
- primary-listing flag;
- explicit business-date knowledge statuses;
- system-time/current-version fields;
- validation status and raw-source lineage;
- at least one venue locator (`exchange_organization_id` or `venue_mic`) is mandatory.

### `fund.listing_identifier`

Listing-specific identifiers are separated from `fund.entity_identifier`.

Initial schemes:

- `SEDOL`
- `TICKER`
- `LOCAL_CODE`
- `OTHER`

This separation prevents a listing-level identifier from being misrepresented as the stable identity of a Share Class.

## TDD evidence

Clean RED run: `32070633515`.

The historical migration, country-indicator, Fund/SubFund/ShareClass and identifier-extension contracts were green. The only failures were the deliberately absent migration-019 manifest entry and SQL artifact.

GREEN run: `32070768364`.

The following all passed on PostgreSQL 16:

1. migration-runner unit tests;
2. D00-D17 country-indicator catalogue tests;
3. fund-domain and identifier-extension tests;
4. Listing model unit contract;
5. governed plan 001→019;
6. apply to an empty database;
7. second apply / idempotence;
8. ledger verification;
9. runtime assertions;
10. Fund/SubFund/ShareClass fixtures;
11. adoption of an initialized database after ledger removal.

Runtime fixtures additionally proved that:

- a Share Class can own a listing with a MIC;
- a SEDOL can be attached to the listing;
- a listing with neither exchange organization nor MIC is rejected;
- unsupported identifier schemes remain rejected.

## Openfunds consequence

`OFST020040` (SEDOL) must no longer be forced into `fund.entity_identifier`. It may be mapped only after the migration-019 physical fields are present in a governed canonical dictionary inventory.

## Remaining gates

- validate the `listing_v1` dictionary extension;
- union the extension with the immutable 143-field migration-015 core for mapping validation;
- re-audit the checksum-locked official `OFST020040` record;
- create a dedicated SEDOL mapping batch only if field semantics and licensing/export constraints are explicitly preserved.
