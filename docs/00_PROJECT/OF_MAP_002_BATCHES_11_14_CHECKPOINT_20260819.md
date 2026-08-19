# OF-MAP-002 — Batches 11–14 checkpoint — 2026-08-19

## Scope

Forward-only continuation of the governed Openfunds v2.13.0 mapping registry on `architecture/africafunds-country-indicators-v0.1`.

No merge, retarget, `main` modification, production activation or deployment was performed.

## Implemented migration chain

```text
001..026
```

New migrations in this checkpoint:

```text
024_LISTING_INCEPTION_PRICE
025_SHARE_CLASS_TRADING_PRICE_FREQUENCY
026_SHARE_CLASS_NAV_FREQUENCY_DETAIL
```

## Canonical inventory

```text
CORE:        143
EXTENSIONS:   41
TOTAL:       184
```

New extension packages:

```text
data/dictionary/extensions/listing_inception_price_v1
data/dictionary/extensions/share_class_trading_price_frequency_v1
data/dictionary/extensions/share_class_nav_frequency_detail_v1
```

## Mapping progression

### Batch 11

```text
OFST062020 Inception Price
-> OF_FUND_LISTING_INCEPTION_PRICE
```

No currency or quote-factor inference.

### Batch 12

```text
OFST020300 Valuation Frequency
-> OF_FUND_SHARE_CLASS_PROFILE_NAV_FREQUENCY
```

Reuses the migration-015 core field.

### Batch 13

```text
OFST020310 Trading Price Frequency
-> OF_FUND_SHARE_CLASS_PROFILE_TRADING_PRICE_FREQUENCY
```

Trading-price frequency remains distinct from NAV frequency.

### Batch 14

```text
OFST020305 Valuation Frequency Detail
-> OF_FUND_SHARE_CLASS_PROFILE_NAV_FREQUENCY_DETAIL
```

Free-text source detail is preserved and never replaces the governed NAV frequency code.

## Current material coverage

```text
REVIEWED_MAPPING_ROWS:   40
MAPPED_EXTERNAL_IDS:     21
UNMAPPED_EXTERNAL_IDS: 1848
MAPPED_CANONICAL_IDS:    21
CANONICAL_FIELDS:       184
```

## CI integration

`migration-runner.yml` is structurally aligned to 26 migrations and includes migration 025/026 contract tests and runtime column assertions.

`of-map-002-mapping-registry.yml` includes Batches 11–14 and all current canonical extension packages.

Remote CI attestation remains deliberately unset because the connected GitHub surface currently returns no workflow runs/status checks for the recent exact HEADs.

Last remotely attested baselines remain:

```text
MIGRATIONS 001..019: 32070768364
CANONICAL UNION 177: 32071385088
MAPPING BATCH 05:    32071858346
```

Therefore `IMPLEMENTED` must not be rewritten as `REMOTELY_GREEN` without fresh evidence.

## Next safe unit

Audit `OFST020320 NAV Publication Time` and its timezone dependency before modelling. Do not store a time value without governing how the associated timezone is represented.
