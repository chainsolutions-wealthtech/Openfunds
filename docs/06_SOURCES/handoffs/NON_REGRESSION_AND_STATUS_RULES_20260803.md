# Non-Regression and Status Rules for Official-Source Integration

## Purpose

These rules are mandatory when integrating the accompanying official-source inventory into the canonical Openfunds/AfricaFunds model.

This handoff must remain additive until the active contributor has reviewed each proposed organization, endpoint, mapping and provider series.

## A. Branch and merge safety

1. Never commit these handoff files directly to `main`.
2. Do not force-push the active contributor's branch.
3. Do not move, rename or delete existing canonical files.
4. Do not resolve the active branch's seven-commit divergence as part of this source handoff.
5. Integrate canonical changes in small reviewed commits.
6. Keep the final PR in draft until reference and collector tests pass.
7. If the target branch advances, compare the new head before updating canonical CSVs.
8. Never use a force ref update for this handoff.

## B. Canonical source-of-truth safety

The following remain the only canonical geography registries:

- `AFRICA_REGIONS.csv`;
- `AFRICA_COUNTRIES.csv`;
- `MARKET_ZONES.csv`;
- `COUNTRY_RELATIONSHIPS.csv`;
- `CURRENCIES.csv`.

Do not create alternative country, currency, monetary-union or market-zone tables.

The handoff inventory is evidence and planning material, not a canonical registry.

## C. Endpoint-model safety

Use the reconciled `source.endpoint` model.

Do not seed a competing `source.source_endpoint` table from the proposal-only country indicator SQL.

An organization is not an endpoint. A homepage is not automatically a provider series. A provider series is not a collection specification.

Preserve the chain:

```text
ORGANIZATION
→ ENDPOINT
→ PROVIDER SERIES
→ COLLECTION SPECIFICATION
→ RUN
→ RAW ARTIFACT
→ EXTRACTION
→ OBSERVATION
```

## D. Status integrity

### Allowed from this handoff

Depending on review evidence:

- SOURCE_IDENTIFIED;
- URL_LINKED;
- ENDPOINT_VERIFIED;
- SERIES_IDENTIFIED;
- SPECIFICATION_REQUIRED;
- SPECIFICATION_DRAFTED.

### Not allowed from desk research alone

- COLLECTION_TESTED;
- PARTIAL_HISTORY_LOADED;
- COMPLETE_HISTORY_LOADED.

### COLLECTION_TESTED gate

Require all of the following:

- real source retrieval;
- raw artifact stored;
- SHA-256 verified;
- source date parsed;
- parser version recorded;
- expected observations parsed;
- quality checks passed;
- duplicate test passed;
- second identical run idempotent;
- evidence row linked to the workflow or controlled execution.

### PARTIAL_HISTORY_LOADED gate

Require:

- at least two distinct historical periods;
- durable raw-artifact storage;
- persistent canonical observations;
- first and last dates;
- observation count;
- known gaps report;
- revision handling test.

### COMPLETE_HISTORY_LOADED gate

Require:

- official archive inventory;
- verified historical start;
- all accessible files or periods assessed;
- missing periods explained;
- duplicate and conflict reconciliation;
- coverage report;
- quality sign-off.

## E. Financial semantics

Never treat these as synonyms:

- policy rate;
- risk-free overnight rate;
- offered interbank rate;
- weighted interbank rate;
- deposit rate;
- savings rate;
- lending rate;
- treasury-bill yield;
- bond yield;
- par-curve rate;
- zero-coupon rate.

Store tenor as a dimension, not in an unparsed label only.

Store native quoted values before transformations.

Store observed and calculated values separately.

Do not infer an official risk-free rate where no official named benchmark was identified.

Do not use the policy rate as a universal risk-free rate.

## F. Nigeria NOFR rule

Use the CBN NOFR as the primary Nigerian overnight risk-free reference after its official introduction.

Keep separate:

- NOFR overnight;
- NOFRI 30 days;
- NOFRI 90 days;
- NOFRI 180 days;
- NIBOR by tenor;
- NITTY or NTB yields by tenor;
- MPR and corridor;
- FGN bond yields.

Do not replace NOFR with NIBOR or NITTY.

Do not collapse all NOFRI tenors into one observation without a tenor dimension.

## G. Common-zone rules

### UEMOA

Store BCEAO, BRVM and zone-level series once at UEMOA scope.

Retain the sovereign issuer country for UMOA-Titres and government-security observations.

Do not manufacture a single UEMOA sovereign curve.

### CEMAC

Store BEAC and BVMAC zone-level series once at CEMAC scope.

Retain the sovereign issuer country for public-security observations.

Do not manufacture a single CEMAC sovereign curve.

## H. Fund and benchmark rules

A fund benchmark cannot be assigned from domicile country alone.

Use:

- fund objective;
- asset class;
- investment geography;
- share-class currency;
- duration or weighted-average maturity;
- prospectus benchmark;
- Islamic or conventional mandate;
- effective dates.

Keep WTI and WTI Bench independent:

- WTI represents eligible observed peer-fund performance;
- WTI Bench represents an independent market or strategic benchmark.

Do not rename or merge those products.

## I. Equity-index rules

Preserve:

- provider index name;
- provider code;
- currency;
- base date;
- base value;
- price or total-return type;
- methodology version;
- constituent history when available;
- licensing restrictions.

Do not label a reconstructed total-return index as official.

Do not claim a broad Ethiopian equity index until ESX documents and publishes one.

## J. Yield-curve rules

Keep raw inputs separate from derived curves.

Required layers:

1. instrument reference data;
2. auction results;
3. secondary-market quotes;
4. observed yield points;
5. par curve;
6. zero-coupon curve;
7. forward curve.

Store:

- issuer;
- instrument;
- ISIN or local identifier;
- auction date;
- settlement date;
- maturity date;
- residual maturity;
- coupon;
- price;
- yield;
- market layer;
- day-count convention;
- compounding convention.

Do not interpolate missing data silently.

## K. Historical and bitemporal rules

Preserve:

- observation date;
- period start and end;
- effective date;
- publication date;
- availability timestamp;
- retrieval timestamp;
- vintage date;
- valid-from and valid-to;
- recorded-at and superseded-at.

A correction creates a new version. It must not overwrite the former published value.

Queries must eventually support:

- latest revised;
- as published;
- as known at a selected historical date.

## L. Raw-source rules

For Excel sources preserve:

- workbook;
- worksheet;
- row;
- column;
- cell;
- original numeric representation.

For PDF sources preserve:

- document;
- page;
- table;
- bounding region or extraction locator.

For HTML/API sources preserve:

- requested and resolved URL;
- selector or JSON path;
- response artifact;
- parser version.

Missing values remain null. They must never become zero.

## M. Number-parsing rules

Country-specific parsers must handle without guessing:

- spaces and non-breaking spaces;
- comma and point decimal separators;
- comma, point and space thousand separators;
- percentages;
- parentheses for negative values;
- Excel numeric cells and formatted display values;
- source-specific missing-value markers.

If the representation is ambiguous, reject or quarantine the observation.

## N. Required tests before canonical integration

1. All technical codes uppercase and without accents.
2. No duplicate organization code.
3. No duplicate endpoint code.
4. No duplicate provider-series code.
5. Organization exists before role or endpoint insertion.
6. Endpoint exists before provider-series insertion.
7. Provider series exists before collection-specification insertion.
8. Scope code resolves to a canonical country or zone.
9. Validated endpoint has at least one canonical URL.
10. Native currency resolves to `CURRENCIES.csv`.
11. Valid-to is not before valid-from.
12. No collection evidence exists without a real run.
13. Collector tests are idempotent.
14. Raw hashes match stored artifacts.
15. Existing BCEAO and BEAC FX tests remain green.

## O. Review completion checklist

- [ ] Active branch head rechecked.
- [ ] Proposed codes checked for collisions.
- [ ] Official identity of every new organization verified.
- [ ] Roles and territorial scopes reviewed.
- [ ] Every endpoint opened and verified.
- [ ] Exact provider-series names preserved.
- [ ] Uncertain fields remain null or PENDING.
- [ ] Licensed sources labelled correctly.
- [ ] Collection statuses not overstated.
- [ ] Reference tests pass.
- [ ] Existing collector tests pass.
- [ ] Documentation and readiness statuses agree.
- [ ] No existing data or file deleted.
