# OF-SOURCE-002 — Wave 14 residual INDEX_PROVIDER audit — 2026-08-17

## Scope

Wave 14 reviews the five residual `INDEX_PROVIDER` relations left after Wave 13. It does **not** infer provider status from `STOCK_EXCHANGE` status alone.

Residual candidates before this wave:

```text
JSE  / AFRIQUE_DU_SUD
EGX  / EGYPTE
NSE  / KENYA
NGX  / NIGERIA
BVMT / TUNISIE
```

## Promotion decision

Only two existing PENDING rows have sufficiently specific primary official evidence in this audit:

```text
JSE;INDEX_PROVIDER;AFRIQUE_DU_SUD;COUNTRY
BVMT;INDEX_PROVIDER;TUNISIE;COUNTRY
```

### JSE

Primary official evidence:

- https://www.jse.co.za/services/indices
- https://www.jse.co.za/market-data/our-market-data-products/index-market-data

The JSE states that the FTSE/JSE Africa Index Series results from a joint venture between JSE Limited and FTSE and provides dedicated index data products, historical data, valuations, constituents and tracker data. This is specific index-series/provider evidence and is stronger than exchange identity alone.

### BVMT

Primary official evidence:

- https://www.bvmt.com.tn/public/BvmtMarketStation/index.html
- https://www.bvmt.com.tn/en-gb/avis-decisions

The Tunis Stock Exchange publishes TUNINDEX/TUNINDEX20 values through its official market station and publishes notices identifying free-float/composition changes used in TUNINDEX and sector-index calculation. This is direct publication/calculation evidence.

## Explicitly retained as PENDING

```text
EGX;INDEX_PROVIDER;EGYPTE;COUNTRY
NSE;INDEX_PROVIDER;KENYA;COUNTRY
NGX;INDEX_PROVIDER;NIGERIA;COUNTRY
```

Reason: current evidence is insufficiently clean to distinguish exchange publication/data display from benchmark-provider/administrator responsibility. These relations remain fail-closed.

## Closed allowlist

Wave 14 may mutate only the two exact existing rows above, and only:

```text
VALIDATION_STATUS: PENDING -> VALIDATED
SOURCE_NOTE: -> OFFICIAL_INDEX_PROVIDER_VERIFIED_2026_08_17_WAVE14
```

No organization, role, scope, relationship, primary flag or validity date may change.

## Expected post-state

```text
TOTAL_SCOPE_ROLES: 199
VALIDATED: 189
PENDING: 10
PENDING_INDEX_PROVIDER: 3
```

Other residual role families remain unchanged:

```text
MONETARY_UNION: 3
SUPRANATIONAL_AUTHORITY: 2
INTERBANK_MARKET_OPERATOR: 2
```
