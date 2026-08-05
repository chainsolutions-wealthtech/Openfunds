# FX DAILY STAGING AND PERSISTENCE POLICY

## PURPOSE

This policy defines the prospective daily collection of the validated BCEAO/XOF and BEAC/XAF exchange-rate snapshots.

It separates four distinct states:

```text
LIVE SOURCE ACCESS
→ TEMPORARY STAGING
→ PERSISTENT OBSERVATION STORAGE
→ HISTORICAL COVERAGE VALIDATION
```

A successful scheduled workflow does not by itself prove persistent storage or complete history.

## PIPELINE

The common pipeline is:

```text
pipelines.fx_daily
```

Its canonical code is:

```text
DAILY_AFRICA_FX_SNAPSHOTS
```

Current version:

```text
0.1.0
```

The pipeline orchestrates:

```text
BCEAO_XOF
├── BCEAO_FX_SNAPSHOT
├── XOF_EUR
└── XOF_USD

BEAC_XAF
├── BEAC_FX_SNAPSHOT
├── XAF_EUR
└── XAF_USD
```

## SCHEDULE

The GitHub Actions workflow is:

```text
.github/workflows/fx-daily-staging.yml
```

The provisional schedule is:

```text
20:15 UTC
MONDAY TO FRIDAY
```

Cron expression:

```text
15 20 * * 1-5
```

This schedule is a collection check time, not a claim that both institutions publish a new value every business day before 20:15 UTC.

The source value date remains authoritative. The workflow execution date must never replace it.

Scheduled workflows become active from the repository default branch after merge. The pull-request trigger exists only to validate the workflow before merge.

## OUTPUT STRUCTURE

A run produces:

```text
artifacts/daily/fx/
├── bceao_xof/
│   ├── raw/
│   ├── manifests/
│   └── staging/canonical_fx.json
├── beac_xaf/
│   ├── raw/
│   ├── manifests/
│   └── staging/canonical_fx.json
└── coverage/daily_fx_coverage.json
```

The coverage manifest records separately for each source:

- collector code;
- source URL;
- local currency;
- parser version;
- collection status;
- canonical transformation status;
- database status;
- raw SHA256;
- raw size and media type;
- retrieval timestamp;
- source value date;
- observed currency codes;
- canonical pairs and rates;
- warnings and errors;
- raw-retention status;
- history status.

## STATUS RULES

### `STAGING_ONLY`

The live source and canonical transformations succeeded, but persistent database loading was not requested.

### `STAGING_ONLY_DATABASE_NOT_CONFIGURED`

Persistent loading was requested, but the secret below was absent:

```text
OPENFUNDS_DATABASE_URL
```

This is not a failed collection, but it is not persistent storage.

### `SUCCESS`

Both sources were collected and transformed, and all expected observations were loaded successfully into a configured PostgreSQL database.

### `PARTIAL`

At least one source or persistence operation failed while another succeeded.

### `FAILED`

No source completed the collection and canonical transformation path.

## POSTGRESQL CONFIGURATION

Persistent loading requires the GitHub Actions secret:

```text
OPENFUNDS_DATABASE_URL
```

The target database must already contain the applicable canonical migrations and reference seeds, including:

```text
003_ORGANIZATIONS_AND_ROLES
004_SOURCE_ENDPOINTS_AND_INDICATOR_MAPPING
005_PROVIDER_SERIES_AND_COLLECTION_SPECIFICATIONS
006_FX_OBSERVATION_LINEAGE
007_SOURCE_ENDPOINT_RECONCILIATION
008_BCEAO_FX_COLLECTION_SEED
009_BEAC_FX_COLLECTION_SEED
010_BEAC_FX_PARSER_V0_2
011_BEAC_FX_COLLECTION_VALIDATION
```

The scheduled workflow does not automatically deploy production migrations. Schema deployment and data collection remain separate operational responsibilities.

## RAW ARTIFACT RETENTION

The current GitHub Actions workflow uploads the complete daily bundle as an Actions artifact with a requested retention period of 90 days.

This status is represented as:

```text
GITHUB_ACTIONS_ARTIFACT_90_DAYS
```

This is temporary operational evidence, not durable object storage.

A permanent production implementation still requires an append-only raw-artifact store such as:

```text
OBJECT STORAGE
CONTENT-ADDRESSED FILE SYSTEM
OR OTHER IMMUTABLE ARCHIVE
```

The permanent storage URI must be written into `source.raw_artifact.storage_uri`.

## IDEMPOTENCE

The existing loader uses deterministic identities and current-version rules.

For the same source content, value date, parser version and methodology:

```text
FIRST LOAD
→ INSERTED

SECOND IDENTICAL LOAD
→ SKIPPED_IDENTICAL
```

A changed source value for an existing logical date must create a new version and supersede the former current version. It must not overwrite the old source observation destructively.

## HISTORY STATUS

Every daily coverage entry currently records:

```text
CURRENT_SNAPSHOT_ONLY
```

Neither BCEAO nor BEAC may move to `PARTIAL_HISTORY_LOADED` solely because a workflow has been scheduled.

A source can move to `PARTIAL_HISTORY_LOADED` only after all of the following are true:

1. at least two distinct source value dates are stored durably;
2. raw artifacts are durably addressable by SHA256;
3. canonical observations are present in persistent PostgreSQL;
4. duplicate and revision checks pass;
5. a coverage report shows the dates actually held;
6. known missing dates are distinguished from non-publication days;
7. the status change is recorded in the reference registry.

A source can move to `COMPLETE_HISTORY_LOADED` only after the official accessible archive has been inventoried and coverage-tested from its verified start date.

## NON-REGRESSION RULES

1. XOF and XAF must never share provider-series codes or loader profiles.
2. Provider buy and sell observations remain distinct.
3. Midpoints and inversions remain calculated observations.
4. The source value date is mandatory.
5. Missing observations never become zero.
6. One failed source must not erase the successful artifact from another source.
7. Temporary artifact retention must never be presented as permanent storage.
8. A scheduled workflow must never be presented as historical completeness.
9. Regional and Africa calculations remain downstream of persistent canonical observations.
10. No WTI, WTI Bench or market index is produced by this staging workflow.

## CURRENT CAPABILITY

```text
BCEAO LIVE COLLECTION                  VALIDATED
BEAC LIVE COLLECTION                   VALIDATED
XOF_EUR / XOF_USD TRANSFORMATION       VALIDATED
XAF_EUR / XAF_USD TRANSFORMATION       VALIDATED
POSTGRESQL LOADER ON EPHEMERAL DB      VALIDATED
DAILY DUAL-SOURCE ORCHESTRATOR         IMPLEMENTED
DAILY WORKFLOW                         IMPLEMENTED
TEMPORARY 90-DAY ACTIONS ARTIFACT      IMPLEMENTED
PERSISTENT PRODUCTION DATABASE         CONFIGURATION REQUIRED
PERMANENT RAW OBJECT STORAGE           NOT IMPLEMENTED
HISTORICAL BACKFILL                    NOT IMPLEMENTED
PARTIAL HISTORY STATUS                 NOT REACHED
COMPLETE HISTORY STATUS                NOT REACHED
FX-BASED FUND CONVERSION IN PROD       NOT YET ACTIVATED
INDEX / WTI / WTI BENCH                NOT CALCULATED
```

## NEXT STEP

The next required implementation is a persistent coverage layer:

```text
PERSISTENT DAILY OBSERVATIONS
→ SERIES COVERAGE VIEW
→ DISTINCT VALUE-DATE COUNT
→ FIRST AND LAST DATE
→ BUSINESS-DAY GAP ANALYSIS
→ SOURCE NON-PUBLICATION CALENDAR
→ HISTORICAL BACKFILL INVENTORY
```

Until the production database and permanent raw store are configured, the daily workflow remains a validated staging mechanism rather than a complete historical ingestion service.
