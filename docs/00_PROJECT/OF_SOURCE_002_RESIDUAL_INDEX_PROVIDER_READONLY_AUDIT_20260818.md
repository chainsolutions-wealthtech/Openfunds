# OF-SOURCE-002 — Residual INDEX_PROVIDER read-only audit — 2026-08-18

## Scope

Read-only semantic re-audit of the three residual country-scoped `INDEX_PROVIDER` relations:

```text
EGX  INDEX_PROVIDER  EGYPTE
NSE  INDEX_PROVIDER  KENYA
NGX  INDEX_PROVIDER  NIGERIA
```

No registry row was promoted, rewritten or deleted by this audit.

## Decision rule

`STOCK_EXCHANGE` does not imply `INDEX_PROVIDER`.

Promotion requires current primary official evidence that the organization itself owns, administers, calculates, maintains, licenses or otherwise assumes an explicit provider/administrator responsibility for the relevant index family. Merely displaying an index value, publishing market comparison charts, or hosting an index page is insufficient.

## EGX / Egypt

Primary official EGX search surfaces expose index methodology pages, including an `EGX 30 Methodology Brochure` and an `Index Rules / Methodology EGX70 EWI` page on `egx.com.eg` / `www.egx.com.eg`.

Observed official URLs during this audit:

```text
https://www.egx.com.eg/getdoc/b9d895c5-7c71-4601-820c-c1b5fb19ebbb/EGX-30-Methodology-Brochure_ar.aspx
https://www.egx.com.eg/en/indexrulesmethodologyegx70-ewi.aspx?nav=16
```

Automated retrieval of both official pages was rejected by the EGX edge/application layer, so the exact provider/administrator wording could not be inspected and preserved in this audit.

Verdict:

```text
RELATION: EGX / INDEX_PROVIDER / EGYPTE
STATUS: PENDING
REASON: OFFICIAL_METHODOLOGY_SURFACE_EXISTS_BUT_PROVIDER_ADMINISTRATOR_WORDING_NOT_ATTESTED
```

Do not infer provider responsibility solely from the existence of an EGX-branded methodology page.

## NSE / Kenya

The current official `nse.co.ke` domain is accessible and identifies Nairobi Securities Exchange Plc / NSE on its operated Academy surfaces. However, current primary-domain searches performed for `NSE 20 Share Index`, `NSE 25 Share Index`, `NSE All Share Index`, `index methodology`, and `index rules` did not expose a sufficiently inspectable current official methodology/provider document.

Verdict:

```text
RELATION: NSE / INDEX_PROVIDER / KENYA
STATUS: PENDING
REASON: CURRENT_PRIMARY_PROVIDER_OR_ADMINISTRATOR_PROOF_NOT_RETRIEVED
```

Do not substitute third-party index descriptions for primary evidence.

## NGX / Nigeria

Current official NGX surfaces visibly use the `NGX All-Share-Index` and provide historical/market-comparison data through NGX investor-relations pages. Official NGX Group material also states that the group provides market-data and licensing services through its market-infrastructure businesses.

Observed official surfaces during this audit include:

```text
https://investorsrelation.ngxgroup.com/
https://web.ngxgroup.com/xhire/about
```

This is evidence that NGX publishes/distributes market and index-related information. It is not, by itself, sufficiently explicit proof that the exact canonical organization row is the legal index administrator/provider responsible for calculation, governance or methodology of the All-Share Index.

Verdict:

```text
RELATION: NGX / INDEX_PROVIDER / NIGERIA
STATUS: PENDING
REASON: INDEX_DISPLAY_AND_MARKET_DATA_DISTRIBUTION_PROVEN_BUT_PROVIDER_ADMINISTRATOR_SEMANTICS_NOT_EXPLICIT
```

## Post-audit registry truth

No data mutation is authorized from this audit. The residual semantic backlog therefore remains:

```text
EGX  INDEX_PROVIDER  EGYPTE   PENDING
NSE  INDEX_PROVIDER  KENYA    PENDING
NGX  INDEX_PROVIDER  NIGERIA  PENDING
CMA  MONETARY_UNION  CMA      PENDING
```

## Re-entry gate

A future promotion must attach primary official text demonstrating one or more of:

```text
INDEX_OWNERSHIP
INDEX_ADMINISTRATION
INDEX_CALCULATION_RESPONSIBILITY
INDEX_METHODOLOGY_GOVERNANCE
INDEX_LICENSING_RESPONSIBILITY
```

If the official evidence instead identifies another administrator/provider, evolve the registry relationship to that organization rather than forcing the exchange row.
