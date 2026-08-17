# OF-SOURCE-002 — Wave 12 completion

Date: 2026-08-17
Branch: `architecture/africafunds-country-indicators-v0.1`
Status: `VERIFIED_COMPLETE`

## Scope

Wave 12 validated a closed allowlist of four pre-existing `INDEX_PROVIDER` relations only where current primary official evidence demonstrated actual index calculation, management, administration or publication responsibility.

Promoted tuples:

```text
GSE               | INDEX_PROVIDER | GHANA | COUNTRY
CASABLANCA_BOURSE | INDEX_PROVIDER | MAROC | COUNTRY
BRVM              | INDEX_PROVIDER | UEMOA | MONETARY_ZONE
BVMAC             | INDEX_PROVIDER | CEMAC | MONETARY_ZONE
```

Source note:

```text
OFFICIAL_INDEX_PROVIDER_VERIFIED_2026_08_17_WAVE12
```

No organization, role, scope or relationship identity was created, deleted or retargeted.

## Deliberately held PENDING

The following candidates were not promoted because the current evidence or canonical role semantics were not yet strong enough:

```text
JSE  / AFRIQUE_DU_SUD
EGX  / EGYPTE
NSE  / KENYA
NGX  / NIGERIA
BVMT / TUNISIE
```

A validated stock exchange is not automatically a validated primary index provider. Joint benchmark administration, index ownership, methodology responsibility and publication responsibilities must remain distinguishable.

## TDD evidence

Contract:

```text
tests/test_institutional_registry_wave12.py
```

RED run:

```text
GitHub Actions run: 32061240802
```

Observed RED behavior:

- Waves 01–11 stayed green;
- all four selected tuples existed exactly once;
- the Wave 12 uniqueness/identity contract was already green;
- only the expected validation-status and source-note assertions failed because the four rows were still `PENDING`.

This proved that Wave 12 required only a closed status/provenance promotion.

## Governed promotion

Workflow:

```text
.github/workflows/of-source-002-wave12-promote.yml
```

Promotion run:

```text
GitHub Actions run: 32061343812
Conclusion: SUCCESS
```

The workflow enforced:

1. exactly four existing selected rows;
2. every selected row `PENDING` before mutation;
3. no row-identity drift;
4. only `VALIDATION_STATUS` and `SOURCE_NOTE` mutable;
5. all institutional contracts through Wave 12 green on Python 3.11 and 3.12;
6. only `data/reference/ORGANIZATION_SCOPE_ROLES.csv` changed;
7. exact post-state before commit/push.

## Verified post-state

```text
AFRICAN_COUNTRIES: 54
COUNTRY_COVERAGE: 53 / 54
UNCOVERED_COUNTRY: ERYTHREE
ORGANIZATIONS: 141
ORGANIZATION_SCOPE_ROLES: 199
VALIDATED: 178
PENDING: 21
PENDING_STOCK_EXCHANGE: 0
PENDING_INDEX_PROVIDER: 5
```

Post-Wave12 audit:

```text
.github/workflows/of-source-002-post-wave12-audit.yml
GitHub Actions run: 32061485482
Conclusion: SUCCESS
```

All institutional contracts through Wave 12 passed again.

## Exact residual PENDING inventory

```text
FX_REFERENCE_RATE_PROVIDER: 9
INDEX_PROVIDER: 5
MONETARY_UNION: 3
SUPRANATIONAL_AUTHORITY: 2
INTERBANK_MARKET_OPERATOR: 2
TOTAL: 21
```

Scope split:

```text
COUNTRY: 12
MONETARY_ZONE: 9
```

## Effective required-role gaps after Wave 12

Index-provider validation is not used to falsely satisfy regulatory or institutional core groups. The effective gap counts therefore remain:

```text
MONETARY_AUTHORITY: 11
STATISTICS: 3
CAPITAL_MARKET_REGULATION: 18
FUND_REGULATION: 19
INSURANCE_PENSION_REGULATION: 44
EXCHANGE: 17
FISCAL_DEBT: 40
```

## Next institutional gates

### FX series-provider gate

Nine `FX_REFERENCE_RATE_PROVIDER` rows remain. They require evidence of publication/ownership of the relevant official FX reference series, not merely proof that the institution is a central bank.

### Remaining index-provider gate

Five rows remain pending and must be reviewed individually for benchmark administrator/provider semantics.

### Zone-semantics gate

```text
MONETARY_UNION: 3
SUPRANATIONAL_AUTHORITY: 2
INTERBANK_MARKET_OPERATOR: 2
```

These require dedicated semantic evidence. `CMA / MONETARY_UNION` remains specifically blocked until the canonical role is demonstrated to model the Common Monetary Area correctly.

## Safety conclusion

Wave 12 validates provider identity for four index families only. It does not authorize:

- benchmark-selection methodology;
- benchmark licence assumptions;
- WTI or WTI Bench activation;
- production calculations;
- merge/retarget of PR #1;
- changes to `main`.
