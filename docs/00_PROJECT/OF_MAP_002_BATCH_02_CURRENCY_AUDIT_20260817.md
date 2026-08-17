# OF-MAP-002 — Batch 02 Currency Audit — 2026-08-17

## Scope

This batch is intentionally limited to two Openfunds v2.13.0 currency fields whose semantics match existing canonical reference-currency fields without inventing a new entity or lifecycle rule.

| Openfunds OF-ID | Official meaning | Canonical target | Mapping |
|---|---|---|---|
| `OFST010410` | Fund Currency — base/accounting currency of the fund, ISO 4217 | `OF_FUND_FUND_PROFILE_BASE_CURRENCY_ID` | `ISO_4217_TO_REF_CURRENCY_UUID` |
| `OFST020540` | Share Class Currency — reference currency of the share class, ISO 4217 | `OF_FUND_SHARE_CLASS_PROFILE_CURRENCY_ID` | `ISO_4217_TO_REF_CURRENCY_UUID` |

Official references:

- https://openfunds.org/OFST010410
- https://www.openfunds.org/snippets/OFST020540.html

## Canonical semantics

The governed dictionary already states that:

- `fund.fund_profile.base_currency_id` is the declared base currency of the fund or subfund and is distinct from share-class currency;
- `fund.share_class_profile.currency_id` is the currency in which the share-class NAV is published;
- both columns reference `ref.currency` and therefore require deterministic ISO 4217 code resolution rather than direct string storage.

## Decision

Only the following two reviewed mappings may be added in Batch 02:

```text
MAP-000005  OFST010410 -> OF_FUND_FUND_PROFILE_BASE_CURRENCY_ID
MAP-000006  OFST020540 -> OF_FUND_SHARE_CLASS_PROFILE_CURRENCY_ID
```

Both are `TRANSFORMED`, not `DIRECT`, because the external value is an ISO 4217 code while the canonical value is a UUID foreign key.

Transformation:

```text
ISO_4217_TO_REF_CURRENCY_UUID
```

Import and export are both supported because the governed currency reference allows deterministic code-to-UUID resolution and reverse ISO 4217 lookup.

## Explicit exclusions

Batch 02 does not map:

- Fund Launch Date (`OFST010240`);
- Share Class Launch Date (`OFST020560`);
- lifecycle status;
- legal names;
- listing currencies;
- index currencies;
- subscription/redemption currencies.

Those fields require separate semantic decisions and must not be inferred from this batch.

## Expected post-state

```text
REVIEWED_MAPPING_ROWS: 6
MAPPED_EXTERNAL_IDS: 4
UNMAPPED_EXTERNAL_IDS: 1865
MAPPED_CANONICAL_IDS: 6
```

## Gate

The registry may be changed only after a RED contract proves that the two exact rows are absent while all pre-existing mapping-validator tests remain green.
