# OF-SOURCE-002 — Wave 11 completion

Date: 2026-08-17
Branch: `architecture/africafunds-country-indicators-v0.1`
Status: `VERIFIED_COMPLETE`

## Scope

Wave 11 revalidated exactly three pre-existing country-scoped stock-exchange relations. No organization, role, scope or relationship identity was created, deleted or retargeted.

Promoted tuples:

```text
EGX | STOCK_EXCHANGE | EGYPTE | COUNTRY
GSE | STOCK_EXCHANGE | GHANA | COUNTRY
NGX | STOCK_EXCHANGE | NIGERIA | COUNTRY
```

The source-note marker is:

```text
OFFICIAL_ROLE_VERIFIED_2026_08_17_WAVE11
```

## Evidence and identity controls

The Wave 11 audit resolved the remaining operator-identity uncertainty before mutation:

- `EGX` is the Egyptian Exchange operator, not an inferred index-provider role;
- `GSE` is Ghana Stock Exchange in its stock-exchange capacity;
- `NGX` is Nigerian Exchange Limited in its securities-exchange capacity, distinct from Nigerian Exchange Group Plc, the holding company.

Index ownership/publication was deliberately excluded from this wave. The corresponding `INDEX_PROVIDER` rows remain subject to a dedicated series-provider evidence gate.

## TDD gate

The Wave 11 contract was added before data mutation in:

```text
tests/test_institutional_registry_wave11.py
```

The RED run was:

```text
GitHub Actions run: 32060157098
```

Observed RED behavior:

- Waves 01–10 remained green;
- all three selected tuples existed exactly once;
- only the expected Wave 11 assertions failed because the rows were still `PENDING` and carried their former source notes.

This established that the required change was a closed promotion, not a structural rewrite.

## Governed promotion

One-shot workflow:

```text
.github/workflows/of-source-002-wave11-promote.yml
```

Promotion run:

```text
GitHub Actions run: 32060212240
Conclusion: SUCCESS
```

The workflow enforced all of the following:

1. exactly three selected existing rows;
2. every selected row had to be `PENDING` before mutation;
3. no row identity could change;
4. only `VALIDATION_STATUS` and `SOURCE_NOTE` could change;
5. all institutional contracts through Wave 11 had to pass on Python 3.11 and Python 3.12;
6. the only changed data file had to be `data/reference/ORGANIZATION_SCOPE_ROLES.csv`;
7. the exact post-state had to be reached before commit/push.

## Verified post-state

```text
AFRICAN_COUNTRIES: 54
COUNTRY_COVERAGE: 53 / 54
UNCOVERED_COUNTRY: ERYTHREE
ORGANIZATIONS: 141
ORGANIZATION_SCOPE_ROLES: 199
VALIDATED: 174
PENDING: 25
PENDING_STOCK_EXCHANGE: 0
```

Post-Wave11 audit workflow:

```text
.github/workflows/of-source-002-post-wave11-audit.yml
GitHub Actions run: 32060285313
Conclusion: SUCCESS
```

The audit also reran every institutional contract through Wave 11 successfully.

## Exact residual PENDING inventory by role

```text
FX_REFERENCE_RATE_PROVIDER: 9
INDEX_PROVIDER: 9
MONETARY_UNION: 3
SUPRANATIONAL_AUTHORITY: 2
INTERBANK_MARKET_OPERATOR: 2
TOTAL: 25
```

Scope split:

```text
COUNTRY: 14
MONETARY_ZONE: 11
```

There are no remaining `PENDING` `STOCK_EXCHANGE` rows.

## Effective role-gap counts after Wave 11

The effective audit includes valid zonal inheritance rather than duplicating zonal institutions nationally.

```text
MONETARY_AUTHORITY: 11
STATISTICS: 3
CAPITAL_MARKET_REGULATION: 18
FUND_REGULATION: 19
INSURANCE_PENSION_REGULATION: 44
EXCHANGE: 17
FISCAL_DEBT: 40
```

These counts are coverage gaps, not instructions to invent rows. A missing group can require a new institution, a zonal competence, a not-applicable classification, or a stronger source.

## Residual work split

The remaining 25 `PENDING` relations must not be handled as one homogeneous promotion batch.

### Data-series ownership/publication

```text
FX_REFERENCE_RATE_PROVIDER: 9
INDEX_PROVIDER: 9
```

These require direct evidence that the named institution owns, calculates, publishes or is the authoritative provider for the relevant series. Institutional identity alone is insufficient.

### Zone semantics

```text
MONETARY_UNION: 3
SUPRANATIONAL_AUTHORITY: 2
INTERBANK_MARKET_OPERATOR: 2
```

These require a dedicated semantic review of the zone and role model. In particular, `CMA` must not be promoted merely because the Common Monetary Area exists; the canonical role term must match the institutional arrangement being represented.

## Safety conclusions

Wave 11 does not authorize:

- `INDEX_PROVIDER` promotion for EGX, GSE or NGX;
- benchmark activation;
- WTI or WTI Bench activation;
- historical backfill without durable storage;
- production deployment;
- merge or retarget of PR #1;
- any write to `main`.

Wave 11 closes only the remaining pre-existing `STOCK_EXCHANGE` validation backlog.
