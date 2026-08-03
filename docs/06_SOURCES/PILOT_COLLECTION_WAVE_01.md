# PILOT COLLECTION WAVE 01

## PURPOSE

Move the first priority series from SOURCE_IDENTIFIED to ENDPOINT_VERIFIED and SPECIFICATION_DRAFTED, then to COLLECTION_TESTED only after a reproducible collection run stores the raw artifact, hash, parser version, extracted values, validation results and canonical observations.

## SCOPE

Wave 01 covers:

- UEMOA / BCEAO policy rates;
- UEMOA / BCEAO daily FX reference values;
- UEMOA / BCEAO monthly interbank reference statistics;
- CEMAC / BEAC monetary-policy decisions;
- CEMAC / BEAC daily indicative FX values;
- Nigeria / CBN Monetary Policy Committee decisions.

This wave deliberately starts with monetary and FX data because they are prerequisites for money-market benchmarks, risk-free-rate conventions and daily LOCAL/EUR/USD conversion.

## STATUS VOCABULARY

- SOURCE_IDENTIFIED: organization and broad source are known.
- ENDPOINT_VERIFIED: an official page or directory has been opened and confirmed to contain the intended information.
- SPECIFICATION_DRAFTED: discovery, extraction, parsing and quality rules are documented but not executed as a production collector.
- COLLECTION_TESTED: at least one controlled run has downloaded and hashed a raw artifact, parsed expected fields, passed checks and produced non-duplicated staging observations.
- PARTIAL_HISTORY_LOADED: more than one period has been loaded, but full available history is not yet proven complete.
- COMPLETE_HISTORY_LOADED: all accessible official history has been inventoried, collected, reconciled and coverage-tested.

No series in this wave is marked COLLECTION_TESTED yet.

## VERIFIED ENDPOINT CHARACTERISTICS

### BCEAO POLICY RATES

The official BCEAO policy-rate directory lists dated rate publications and monetary-policy material. The collector must discover all pages, preserve each linked document and extract decision date, effective date and every distinct published rate.

### BCEAO FX

The official BCEAO site publishes a value-dated table containing buy and sell rates. The raw HTML snapshot must be retained daily. Provider quote labels must be preserved before normalization to the canonical rule: one unit of source currency equals X units of target currency.

### BCEAO INTERBANK STATISTICS

Monthly statistical bulletins contain interbank reference rates, market volumes and liquidity information. The bulletin month, publication date, document URL, page/table location and units must be retained.

### BEAC POLICY RATES

The official BEAC monetary-policy decision directory lists dated decision documents. The collector must not merge tender, marginal-lending and deposit-facility rates into one generic rate.

### BEAC FX

The official BEAC homepage displays value-dated indicative buy and sell rates. Daily snapshots and exact source quote direction are required.

### CBN MONETARY POLICY DECISIONS

The official CBN decision timeline reports dated MPC decisions, the Monetary Policy Rate and related corridor and reserve decisions. Each meeting is an event; a maintained rate is still a new decision event and must not be discarded as a duplicate observation.

## REQUIRED RAW LINEAGE

Every run must store:

- collection_run_id;
- provider_series_id;
- requested URL;
- final resolved URL;
- retrieval timestamp;
- HTTP status;
- media type;
- original filename when applicable;
- SHA256;
- byte size;
- parser version;
- discovery rule version;
- validation profile;
- source publication date;
- source value date or effective date.

## REQUIRED OUTPUT OBJECTS

### POLICY-RATE EVENT

- organization_code;
- scope_code;
- meeting_date;
- decision_date;
- effective_date;
- rate_type;
- old_value when explicitly known;
- new_value;
- unit;
- decision_document_id;
- raw_artifact_id;
- extraction_location;
- validation_status.

### FX OBSERVATION

- value_date;
- provider_pair_label;
- provider_quote_direction;
- buy_rate;
- sell_rate;
- midpoint when calculated;
- canonical_source_currency;
- canonical_target_currency;
- canonical_rate;
- transformation_formula;
- raw_artifact_id;
- quality_status.

### INTERBANK OBSERVATION

- economic_period;
- market_segment;
- maturity;
- rate_type;
- rate_value;
- volume_value;
- currency;
- unit;
- publication_date;
- raw_artifact_id;
- page_or_table_reference.

## NON-REGRESSION RULES

1. Country remains the national classification root.
2. UEMOA and CEMAC series are stored once at zone scope and referenced by member-country categories through MARKET_SCOPE.
3. Native values and labels are preserved before canonical normalization.
4. Missing values remain NULL and are never converted to zero.
5. Buy, sell and midpoint rates remain distinct.
6. Decision date and effective date remain distinct.
7. A maintained policy rate is stored as a decision event without fabricating a new effective-value change.
8. Revisions create new vintages; they do not overwrite prior source values.
9. Regional and Africa analytics use the converted fund-level series, not copied local metrics.
10. COLLECTION_TESTED cannot be assigned without stored raw artifacts and passed test cases.

## EXIT CRITERIA FOR WAVE 01

Wave 01 is complete when every pilot series has:

- an exact official endpoint;
- a provider-series record;
- a versioned collection specification;
- one successful discovery run;
- one successful parse run;
- raw artifact and SHA256;
- documented canonical transformation;
- deduplication and revision tests;
- staging observations;
- coverage report;
- status COLLECTION_TESTED or a documented blocker.

## NEXT IMPLEMENTATION ACTION

Implement the discovery and parsing jobs in this order:

1. BCEAO FX daily snapshot;
2. BEAC FX daily snapshot;
3. CBN MPC decision timeline;
4. BCEAO policy-rate document directory;
5. BEAC decision-document directory;
6. BCEAO monthly interbank bulletin directory and parser.
