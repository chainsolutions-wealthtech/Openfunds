# COLLECTOR CI AND LIVE RUN POLICY

## PURPOSE

Define what the automated collector test workflow validates, what remains outside CI, and the exact conditions required before a provider series may move to `COLLECTION_TESTED`.

## CI WORKFLOW

The workflow is stored at:

```text
.github/workflows/collector-tests.yml
```

It runs on:

- pushes to `architecture/africafunds-country-indicators-v0.1` that affect collectors, tests or the workflow;
- pull requests that affect collectors, tests or the workflow;
- manual `workflow_dispatch` execution.

## AUTOMATED CHECKS

The workflow performs:

1. Python syntax compilation for `collectors/` and `tests/`;
2. unit tests on Python 3.11 and Python 3.12;
3. deterministic BCEAO FX fixture parsing;
4. verification that the fixture produces EUR and USD observations;
5. verification that the fixture value date is parsed without a missing-date warning.

## WHAT CI PROVES

A green CI result proves only that:

- the committed Python files compile in the tested runtimes;
- deterministic parser tests pass;
- the fixture contract is respected;
- supported numerical formats continue to parse as expected;
- zero and missing-value rejection tests pass.

## WHAT CI DOES NOT PROVE

A green CI result does not prove that:

- the live BCEAO site is reachable;
- the live page still uses the same markup;
- the official table contains all expected currencies;
- a raw live artifact was persisted;
- a live SHA256 was recorded;
- staging observations were loaded;
- history is complete;
- the series may be marked `COLLECTION_TESTED`.

## LIVE RUN GATE

A provider series may move to `COLLECTION_TESTED` only after a controlled live execution has produced:

- a successful HTTP response;
- the final resolved URL;
- a persisted raw artifact;
- SHA256 and byte size;
- media type;
- retrieval timestamp;
- parser version;
- parsed observations;
- quality warnings and errors;
- a result manifest;
- a deduplication check;
- a repeat-run idempotence check;
- staging rows linked to the raw artifact.

## NETWORK POLICY

Live network calls are not part of the default pull-request unit-test job. This prevents a temporary source outage, rate limit, markup experiment or network restriction from making deterministic code tests unreliable.

A future scheduled or manually triggered integration workflow may execute live collectors, but its results must be treated as source-monitoring and ingestion evidence, not as unit tests.

## NON-REGRESSION RULES

- Fixtures never become canonical financial observations.
- Live raw artifacts are immutable.
- Missing values remain missing and never become zero.
- Buy and sell rates remain separate observed values.
- Derived midpoint and inverse rates remain calculated observations.
- A parser change requires a parser-version change when output semantics change.
- Historical source corrections create a new vintage rather than replacing old evidence.

## CURRENT BCEAO FX STATUS

```text
COLLECTOR_IMPLEMENTED
FIXTURE_TESTS_DEFINED
CI_WORKFLOW_ADDED
LIVE_RUN_PENDING
COLLECTION_TESTED_NOT_YET_GRANTED
```
