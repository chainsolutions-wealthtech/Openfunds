# BEAC FX COLLECTION TEST EVIDENCE

## PURPOSE

This document records the controlled live validation of the BEAC foreign-exchange snapshot collector, canonical XAF/EUR and XAF/USD transformation, and PostgreSQL staging loader.

The evidence proves that one official current snapshot can be downloaded, hashed, parsed, transformed and loaded reproducibly. It does not prove that the full historical series has been collected.

## OFFICIAL SCOPE

- Organization code: `BEAC`
- Market scope: `CEMAC`
- Local currency: `XAF`
- Endpoint code: `BEAC_FX_DAILY`
- Collector code: `BEAC_FX_SNAPSHOT`
- Collector parser version: `0.2.0`
- Canonical methodology version: `FX_CANONICAL_0.1.0`
- PostgreSQL loader profile: `BEAC_XAF`

## SOURCE STRUCTURE DISCOVERED

The official page does not expose the FX values as semantic HTML table rows.

The live artifact renders each pair in a repeated block:

```text
DIV.taux_de_change
├── PROVIDER PAIR LABEL
├── BUY RATE
└── SELL RATE
```

Examples of provider labels include:

```text
EUR/XAF
USD/XAF
GBP/XAF
JPY/XAF
```

The parser therefore supports:

```text
DIV.taux_de_change
+
TABLE FALLBACK
```

The table fallback is retained for compatibility, but the validated live path uses the repeated DIV blocks.

## FIRST LIVE ATTEMPT AND CONTROLLED FAILURE

The first live run was:

```text
WORKFLOW RUN ID: 30779382805
PARSER VERSION: 0.1.0
RESULT: FAILED
```

The HTTP download and raw-artifact persistence succeeded, but the parser returned no FX observations because it expected `TR/TD` table elements.

The failure was not converted into a successful status. The raw artifact was inspected and the parser was revised to version `0.2.0` to read the actual `DIV.taux_de_change` structure.

## SUCCESSFUL LIVE RUN

The successful controlled run was:

```text
WORKFLOW: BEAC FX LIVE SMOKE
WORKFLOW RUN ID: 30779605759
WORKFLOW RUN NUMBER: 2
COMMIT: 14067BA213C48573A935902488A9A2471078BB3D
RESULT: SUCCESS
```

### Raw artifact

```text
SOURCE URL: https://www.beac.int/index.php/accueil
RETRIEVED AT: 2026-08-03T02:34:40+00:00
VALUE DATE: 2026-07-31
MEDIA TYPE: text/html
BYTE SIZE: 175454
SHA256: C93BE111A3997C913917B5AAE425A02FB575FE0B39BFDA67953E237E0A11C23C
```

### Observed currencies

Thirteen provider pairs were parsed:

```text
AED
CAD
CHF
CNY
DKK
EUR
GBP
JPY
MAD
SAR
SEK
USD
ZAR
```

The required EUR and USD pairs were present.

### Validation outcome

```text
OBSERVATION COUNT: 13
WARNING COUNT: 0
ERROR COUNT: 0
RAW FILE COUNT AFTER TWO RUNS: 1
IDEMPOTENCE STATUS: PASSED
```

Two consecutive downloads produced the same content-addressed raw artifact. No duplicate raw file was created.

## OBSERVED PRIMARY VALUES

For value date `2026-07-31`, the required provider observations were:

```text
EUR/XAF BUY  = 655.957
EUR/XAF SELL = 655.957

USD/XAF BUY  = 566.4768
USD/XAF SELL = 574.0791
```

These values remain stored as observed provider data. Buy and sell are not overwritten by a midpoint.

## CANONICAL TRANSFORMATION

The canonical rule is:

```text
1 SOURCE CURRENCY UNIT = X TARGET CURRENCY UNITS
```

The provider convention is:

```text
XAF PER 1 FOREIGN CURRENCY
```

The calculated midpoint and inversion are:

```text
MIDPOINT = (PROVIDER BUY + PROVIDER SELL) / 2
CANONICAL RATE = 1 / MIDPOINT
```

The explicit transformation formula is:

```text
1 / ((PROVIDER_BUY_RATE + PROVIDER_SELL_RATE) / 2)
```

### XAF to EUR

```text
SOURCE MIDPOINT EUR/XAF = 655.957
XAF_EUR = 0.001524490172374104
```

### XAF to USD

```text
SOURCE MIDPOINT USD/XAF = 570.277950000000000000
XAF_USD = 0.001753530887876692
```

The calculated observations preserve:

- source buy rate;
- source sell rate;
- source midpoint;
- source quote convention;
- transformation formula;
- methodology version;
- parser version;
- source URL;
- raw SHA256;
- value date;
- quality status.

## POSTGRESQL LOAD VALIDATION

The workflow applied the canonical source and FX migrations to PostgreSQL 16 and loaded the same live bundle twice.

### First load

```text
PROFILE: BEAC_XAF
ACTION: INSERTED = 6
COLLECTION RUN ID: 904FC9BD-BCC8-5B81-AC5B-A093F987E8E9
RAW ARTIFACT ID: 24714C77-AC33-5084-8801-D8EF25062C89
```

The six current observations were:

```text
EUR -> XAF BUY
EUR -> XAF SELL
USD -> XAF BUY
USD -> XAF SELL
XAF -> EUR MIDPOINT_INVERTED
XAF -> USD MIDPOINT_INVERTED
```

### Second load

```text
ACTION: SKIPPED_IDENTICAL = 6
```

The second load reused the same collection-run and raw-artifact identities. It did not create duplicate observations.

The test also verified that no `XOF` observation was introduced into the CEMAC/XAF bundle.

## REFERENCE STATUS

The following objects are now classified as `COLLECTION_TESTED` and `VALIDATED`:

```text
CEMAC_D09_FX_EUR
CEMAC_D09_FX_USD
PS_CEMAC_BEAC_FX_SNAPSHOT
PS_CEMAC_FX_XAF_EUR
PS_CEMAC_FX_XAF_USD
CS_CEMAC_BEAC_FX_SNAPSHOT
```

The validation is recorded by:

```text
schemas/reference/011_beac_fx_collection_validation.sql
```

## WHAT THIS EVIDENCE PROVES

This evidence proves:

- the official endpoint is accessible from GitHub Actions;
- the current page can be downloaded;
- the raw HTML is retained and hashed;
- the value date is extracted;
- thirteen provider pairs are extracted;
- EUR and USD buy and sell values remain distinct;
- XAF/EUR and XAF/USD are calculated with explicit lineage;
- the bundle loads into PostgreSQL;
- a repeated identical load is idempotent;
- BCEAO/XOF and BEAC/XAF profiles remain separated.

## WHAT THIS EVIDENCE DOES NOT PROVE

This evidence does not prove:

- that the full BEAC FX history has been discovered;
- that more than one value date has been loaded;
- that historical revisions have been encountered and reconciled;
- that a permanent production database contains the observations;
- that raw artifacts are retained beyond the GitHub Actions retention period;
- that a daily production schedule is active;
- that a market index, WTI or WTI Bench has been calculated.

The PostgreSQL database used in the validation workflow is ephemeral and is destroyed after the workflow completes.

## CURRENT STATUS

```text
ENDPOINT VERIFIED                 YES
COLLECTOR IMPLEMENTED             YES
FIXTURE TESTS PASSED              YES
LIVE DOWNLOAD PASSED              YES
RAW SHA256 VERIFIED               YES
VALUE DATE VERIFIED               YES
IDEMPOTENCE VERIFIED              YES
CANONICAL XAF TRANSFORMATION      YES
POSTGRESQL LOAD VERIFIED          YES
COLLECTION_TESTED                 YES
PARTIAL_HISTORY_LOADED            NO
COMPLETE_HISTORY_LOADED           NO
PERSISTENT PRODUCTION STORAGE     NO
DAILY PRODUCTION SCHEDULE         NO
INDEX OR WTI CALCULATION          NO
```

## NEXT IMPLEMENTATION STEP

The next implementation step is to establish durable daily persistence for both BCEAO and BEAC snapshots:

```text
DAILY COLLECTION
→ RAW OBJECT STORAGE
→ SHA256 REGISTRY
→ PERSISTENT POSTGRESQL LOAD
→ COVERAGE CALENDAR
→ GAP DETECTION
→ HISTORICAL BACKFILL DISCOVERY
```

Only after multiple dates are durably stored can the status move from `COLLECTION_TESTED` to `PARTIAL_HISTORY_LOADED`.
