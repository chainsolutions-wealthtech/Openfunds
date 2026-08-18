# OF-DATA-001 — Listing quote-unit migration 020 checkpoint — 2026-08-18

## Status

```text
MIGRATION_ID: 020_LISTING_QUOTE_UNIT_SEMANTICS
ORDER: 200
PATH: schemas/fund/020_listing_quote_unit_semantics.sql
IMPLEMENTATION: PRESENT
LOCAL_STATIC_CONTRACT: GREEN_5_OF_5
REMOTE_POSTGRESQL_16_ATTESTATION: NOT_YET_OBSERVABLE
FINAL_STATUS: IMPLEMENTED_NOT_YET_CLOSED
```

This checkpoint is intentionally not a completion report.

## Problem solved structurally

Openfunds `OFST062010 Listing Currency` may carry ordinary currency codes and quote-unit/minor-unit codes such as `GBX`, `EUX` and `USX`.

The canonical `ref.currency` registry represents economic currencies and must not be polluted with quote-unit codes that are not independent economic currencies.

Migration 020 therefore preserves two distinct concepts on `fund.listing`:

```text
trading_currency_id          canonical parent economic currency
trading_quote_unit_code      exact three-character quote-unit code when distinct
trading_quote_unit_factor    positive conversion factor to parent currency when explicitly known
```

A factor may never exist without a quote-unit code. A quote-unit code may exist with a null factor when the scale has not yet been authoritatively verified. Unknown is preferred to invented.

## TDD sequence

The first local RED exposed a test-quality problem because the absent SQL file produced `FileNotFoundError`. The test was corrected before production code so absence becomes an explicit assertion failure.

Clean RED result:

```text
5 TESTS
4 EXPECTED FAILURES
0 ERRORS
1 EXISTING-GUARD SUCCESS
```

The existing guard proving `GBX/EUX/USX` are not injected into `data/reference/CURRENCIES.csv` was already GREEN.

After minimal implementation and manifest registration, the exact static contract was locally GREEN:

```text
5 TESTS
5 SUCCESS
0 FAILURES
0 ERRORS
```

Relevant commits:

```text
70bf295d8db01a768307cd21c7cd94276ac4c677  explicit RED failures
6d1fe296885a33b923ab4ee7bba84498c3cccf00  migration SQL
286448bf8268fd6079d512f5d7f0511ee38a3782  manifest registration
5add12853e933ccbe060188934a021c7bffb9d62  PostgreSQL workflow runtime assertions
```

## PostgreSQL gate prepared

`.github/workflows/migration-runner.yml` now expects 20 governed migrations and is prepared to prove on PostgreSQL 16:

- the two new Listing columns exist;
- a valid uppercase quote-unit code with positive factor is accepted;
- a factor without a quote-unit code is rejected;
- a lowercase quote-unit code is rejected;
- the full migration chain is still applied twice and verified;
- adoption of an initialized database remains tested.

The GitHub connector available in the conversation does not expose push-triggered workflow run listings for this repository, and its PR-run wrapper returned no run for the exact current SHA. Therefore no remote run ID or GREEN conclusion is invented here.

## Gate before Openfunds mapping

Do not map `OFST062010` yet.

Required order:

```text
1. obtain remote PostgreSQL 16 GREEN attestation for migration 020;
2. create an additive dictionary extension for migration 020;
3. union it into the mapping validator with collision guards;
4. model ordinary ISO currency versus quote-unit semantics explicitly;
5. only then add reviewed mapping rows for OFST062010.
```

Do not rewrite `listing_v1` retroactively; migration 020 fields require their own additive dictionary extension/versioned package.
