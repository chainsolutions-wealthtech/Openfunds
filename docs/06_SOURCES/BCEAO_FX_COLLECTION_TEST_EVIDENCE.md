# BCEAO FX COLLECTION TEST EVIDENCE

## STATUS

The BCEAO daily FX pilot is the first provider series promoted to `COLLECTION_TESTED`.

This status is limited to the live daily snapshot collector. It does not mean that the complete historical archive has already been discovered or loaded.

## CONTROLLED LIVE RUN

- workflow: `BCEAO FX Live Smoke`;
- workflow run ID: `30777722357`;
- workflow run number: `6`;
- tested commit: `8dfed72470acdeabddecf13ef9b6994b59dab80f`;
- parser version: `0.2.0`;
- official source URL: `https://www.bceao.int/fr`;
- retrieval timestamp: `2026-08-03T01:47:58+00:00`;
- source value date: `2026-07-31`.

## RAW ARTIFACT

- media type: `text/html`;
- byte size: `151803`;
- SHA256: `76690835f3a8cd808880c80aeec2e9f078cb6a76c9fae0d8ebe1278ad2421206`;
- GitHub Actions artifact ID: `8842605135`;
- artifact retention: 30 days.

The raw HTML was downloaded twice during the same controlled run. Both downloads produced the same SHA256 and only one content-addressed raw file remained. The idempotence control therefore passed.

## PARSED OBSERVATIONS

Four directly observed provider rows were extracted:

- EUR;
- USD;
- JPY;
- GBP.

For every row, the collector preserved:

- provider currency label;
- buy rate;
- sell rate;
- source quote convention `XOF_PER_1_FOREIGN_CURRENCY`;
- value date;
- raw-artifact lineage;
- parser version.

The controlled run completed with:

- `run_status = SUCCESS`;
- 4 observations;
- 0 warnings;
- 0 errors;
- EUR present;
- USD present;
- SHA256 verified;
- idempotence verified.

## DATE-PARSER CORRECTION

The first live run exposed the exact heading:

```text
Cours des devises du vendredi 31 juillet 2026
```

Parser version `0.1.0` extracted the rates but did not detect this French textual date. The raw artifact was retained, the issue was not hidden, and the pilot was not promoted.

Parser version `0.2.0` added validated French weekday and month parsing. Unit tests were added for:

- `31 juillet 2026`;
- `3 août 2026`;
- rejection of an invalid calendar date such as `31 février 2026`.

The second live run then parsed `2026-07-31` with no warning.

## WHAT COLLECTION_TESTED MEANS HERE

The following are now demonstrated:

1. the official endpoint is reachable from the controlled runner;
2. the raw HTML can be downloaded and retained;
3. a SHA256 can be calculated and verified;
4. the source value date can be parsed;
5. buy and sell values can be extracted separately;
6. EUR and USD are present;
7. localized numbers can be normalized without turning missing values into zero;
8. a second identical run is idempotent;
9. a reproducible manifest is produced;
10. deterministic CI and live CI both pass.

## WHAT IS NOT YET COMPLETE

The following remain separate tasks:

- discovery of all historical daily snapshots or official archive files;
- loading of a multi-date historical series;
- proof of complete historical coverage;
- scheduled daily execution;
- persistence in the canonical observation database;
- canonical inversion from provider quotes to `XOF_EUR` and `XOF_USD`;
- conversion of fund NAV, AUM and other monetary observations;
- coverage and freshness monitoring.

The series is therefore:

```text
COLLECTION_TESTED
NOT YET PARTIAL_HISTORY_LOADED
NOT YET COMPLETE_HISTORY_LOADED
```

## NEXT ACTION

Produce versioned canonical calculated observations:

```text
EUR_XOF BUY / SELL observed
USD_XOF BUY / SELL observed
→ provider midpoint calculated
→ XOF_EUR midpoint inverted
→ XOF_USD midpoint inverted
```

Every calculated rate must preserve the source buy rate, source sell rate, midpoint, inversion formula, raw SHA256, parser version and value date.
