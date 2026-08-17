# OF-SOURCE-002 — Wave 11 Exchange-Role Revalidation Audit

**Date:** 2026-08-17  
**Branch:** `architecture/africafunds-country-indicators-v0.1`  
**Mutation scope:** three existing `STOCK_EXCHANGE` rows only  
**New organizations:** none  
**New role rows:** none

## Objective

Close the three remaining country-scoped `STOCK_EXCHANGE` rows that remained `PENDING` after Wave 10, but only after resolving current operator identity from primary institutional sources.

Wave 11 deliberately does **not** promote the associated `INDEX_PROVIDER` rows. Exchange identity and index-calculation/publication responsibility remain distinct roles.

## Verified pre-state

```text
ORGANIZATIONS = 141
ORGANIZATION_SCOPE_ROLES = 199
VALIDATED_SCOPE_ROLES = 171
PENDING_SCOPE_ROLES = 28
PENDING_STOCK_EXCHANGE_ROWS = 3
```

## Closed allowlist

### Egypt — EGX

```text
ORGANIZATION_CODE = EGX
ROLE_CODE = STOCK_EXCHANGE
SCOPE_ENTITY_CODE = EGYPTE
SCOPE_ENTITY_TYPE = COUNTRY
```

Primary evidence:

- Financial Regulatory Authority (Egypt), 2026: FRA publicly identifies the `Egyptian Exchange (EGX)`, its chairman and coordination between FRA and EGX;
- FRA 2026 short-selling preparation notice explicitly refers to trading on EGX and leaders from the Egyptian Exchange.

Evidence URLs:

- `https://fra.gov.eg/en/fra_news/...new-egx-chairman.../`
- `https://fra.gov.eg/en/fra_news/...short-selling-launch-on-egx.../`

Conclusion: `EGX` denotes the Egyptian Exchange and the existing country-scoped `STOCK_EXCHANGE` role is directly supportable.

### Ghana — GSE

```text
ORGANIZATION_CODE = GSE
ROLE_CODE = STOCK_EXCHANGE
SCOPE_ENTITY_CODE = GHANA
SCOPE_ENTITY_TYPE = COUNTRY
```

Primary evidence:

- official Ghana Stock Exchange site identifies GSE as the Ghana Stock Exchange;
- GSE states it was established to provide an efficient securities market and provides a platform for listing and trading securities;
- GSE overview records its recognition as an authorized Stock Exchange and trading commencement.

Evidence URLs:

- `https://gse.com.gh/`
- `https://gse.com.gh/overview/`

Conclusion: the existing `GSE/STOCK_EXCHANGE/GHANA` relation is directly supported.

### Nigeria — NGX

```text
ORGANIZATION_CODE = NGX
ROLE_CODE = STOCK_EXCHANGE
SCOPE_ENTITY_CODE = NIGERIA
SCOPE_ENTITY_TYPE = COUNTRY
```

Primary evidence:

- current Securities and Exchange Commission Nigeria registered-operator registry distinguishes:
  - `Nigerian Exchange Group Plc (NGX Group)` = `Capital Market Holding Company (CMHC)`;
  - `Nigerian Exchange Limited (NGX)` = `Securities Exchange`.
- NGX's own current digital platform terms identify the legal entity as `Nigerian Exchange Limited (“NGX”)`.

Evidence URLs:

- `https://home.sec.gov.ng/for-investors/find-a-registered-operator/?page=31`
- `https://www.invest.ngxgroup.com/terms-and-conditions`

Conclusion: the existing code `NGX` must represent Nigerian Exchange Limited, the exchange operator, not Nigerian Exchange Group Plc. The existing `STOCK_EXCHANGE` role is therefore supportable without introducing a holding-company conflation.

## Explicit exclusions

Wave 11 does not promote:

```text
EGX INDEX_PROVIDER
GSE INDEX_PROVIDER
NGX INDEX_PROVIDER
```

Those roles require direct proof of index ownership/calculation/publication and will be reviewed under a separate series-role wave.

Wave 11 also leaves all FX, monetary-union, supranational and interbank rows unchanged.

## Expected post-state

Exactly three existing rows move from `PENDING` to `VALIDATED`:

```text
ORGANIZATIONS = 141               unchanged
ORGANIZATION_SCOPE_ROLES = 199    unchanged
VALIDATED_SCOPE_ROLES = 174       171 + 3
PENDING_SCOPE_ROLES = 25          28 - 3
PENDING_STOCK_EXCHANGE_ROWS = 0
```

Each promoted row must use:

```text
VALIDATION_STATUS = VALIDATED
SOURCE_NOTE = OFFICIAL_ROLE_VERIFIED_2026_08_17_WAVE11
```

No other field may change.

## TDD gate

Before mutation:

- Waves 01–10 must remain green;
- the three Wave 11 tuples must each exist exactly once;
- Wave 11 must fail only because the exact rows are not yet `VALIDATED` and do not yet carry the Wave 11 source note.

After mutation:

- all Waves 01–11 must pass on Python 3.11 and 3.12;
- exact post-state `199 / 174 / 25` must be asserted;
- only `ORGANIZATION_SCOPE_ROLES.csv` may be committed.
