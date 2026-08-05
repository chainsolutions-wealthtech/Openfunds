-- Country Statistical and Financial Indicator Model v0.1
-- Proposal only. Non-destructive: no DROP, DELETE, TRUNCATE or UPDATE statements.
-- This file is not a migration and must be reviewed against the canonical schema before execution.

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS ref;
CREATE SCHEMA IF NOT EXISTS source;
CREATE SCHEMA IF NOT EXISTS market;
CREATE SCHEMA IF NOT EXISTS quality;
CREATE SCHEMA IF NOT EXISTS calc;

CREATE TABLE IF NOT EXISTS ref.indicator_domain (
    indicator_domain_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    canonical_code text NOT NULL UNIQUE,
    canonical_name text NOT NULL,
    description text,
    display_order integer,
    valid_from date NOT NULL DEFAULT CURRENT_DATE,
    valid_to date,
    recorded_at timestamptz NOT NULL DEFAULT now(),
    superseded_at timestamptz
);

CREATE TABLE IF NOT EXISTS ref.indicator_definition (
    indicator_definition_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    indicator_domain_id uuid NOT NULL REFERENCES ref.indicator_domain(indicator_domain_id),
    canonical_code text NOT NULL UNIQUE,
    canonical_name text NOT NULL,
    definition text NOT NULL,
    data_nature text NOT NULL CHECK (data_nature IN ('RAW','METADATA','EVENT','CALCULATED')),
    expected_frequency text,
    canonical_unit text,
    preferred_source_role text,
    utility_description text,
    benchmark_usage text,
    priority_code text,
    minimum_history text,
    is_mandatory boolean NOT NULL DEFAULT true,
    valid_from date NOT NULL DEFAULT CURRENT_DATE,
    valid_to date,
    recorded_at timestamptz NOT NULL DEFAULT now(),
    superseded_at timestamptz
);

CREATE TABLE IF NOT EXISTS ref.country_indicator_relationship (
    country_indicator_relationship_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    country_id uuid NOT NULL, -- FK to canonical country/geographic entity after schema reconciliation
    indicator_definition_id uuid NOT NULL REFERENCES ref.indicator_definition(indicator_definition_id),
    applicability_status text NOT NULL,
    coverage_status text NOT NULL DEFAULT 'NOT_STARTED',
    preferred_frequency text,
    preferred_unit text,
    monetary_union_country_id uuid,
    successor_relationship_id uuid,
    valid_from date NOT NULL DEFAULT CURRENT_DATE,
    valid_to date,
    source_assertion_id uuid,
    recorded_at timestamptz NOT NULL DEFAULT now(),
    superseded_at timestamptz,
    UNIQUE (country_id, indicator_definition_id, valid_from)
);

CREATE TABLE IF NOT EXISTS source.source_endpoint (
    source_endpoint_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organisation_id uuid NOT NULL,
    endpoint_type text NOT NULL,
    url text NOT NULL,
    http_method text NOT NULL DEFAULT 'GET',
    content_type text,
    authentication_type text,
    request_headers_json jsonb,
    request_parameters_json jsonb,
    landing_page_url text,
    download_url text,
    api_url text,
    methodology_url text,
    publication_calendar_url text,
    terms_of_use_url text,
    priority integer NOT NULL DEFAULT 1,
    valid_from date NOT NULL DEFAULT CURRENT_DATE,
    valid_to date,
    recorded_at timestamptz NOT NULL DEFAULT now(),
    superseded_at timestamptz
);

CREATE TABLE IF NOT EXISTS source.provider_series_mapping (
    provider_series_mapping_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    country_indicator_relationship_id uuid NOT NULL REFERENCES ref.country_indicator_relationship(country_indicator_relationship_id),
    source_endpoint_id uuid REFERENCES source.source_endpoint(source_endpoint_id),
    provider_series_code text,
    provider_series_label text NOT NULL,
    provider_language_code text,
    provider_frequency text,
    provider_unit text,
    provider_multiplier numeric,
    seasonal_adjustment text,
    mapping_status text NOT NULL DEFAULT 'PROPOSED',
    predecessor_mapping_id uuid,
    valid_from date NOT NULL DEFAULT CURRENT_DATE,
    valid_to date,
    recorded_at timestamptz NOT NULL DEFAULT now(),
    superseded_at timestamptz
);

CREATE TABLE IF NOT EXISTS source.data_collection_specification (
    collection_specification_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_series_mapping_id uuid NOT NULL REFERENCES source.provider_series_mapping(provider_series_mapping_id),
    collection_method text NOT NULL,
    schedule_expression text,
    extractor_type text,
    parser_name text,
    parser_version text,
    selector_or_path text,
    worksheet_selector text,
    header_row_rule text,
    date_extraction_rule text,
    value_extraction_rule text,
    unit_conversion_rule text,
    locale_rule text,
    thousands_separator_rule text,
    decimal_separator_rule text,
    missing_value_rule text,
    duplicate_rule text,
    revision_rule text,
    retry_policy_json jsonb,
    validation_rule_set_id uuid,
    quality_threshold numeric,
    valid_from date NOT NULL DEFAULT CURRENT_DATE,
    valid_to date,
    recorded_at timestamptz NOT NULL DEFAULT now(),
    superseded_at timestamptz
);

CREATE TABLE IF NOT EXISTS source.source_document (
    source_document_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_endpoint_id uuid REFERENCES source.source_endpoint(source_endpoint_id),
    original_filename text,
    source_url text NOT NULL,
    publication_date date,
    retrieved_at timestamptz NOT NULL,
    mime_type text,
    byte_size bigint,
    sha256 text NOT NULL,
    object_storage_uri text,
    licence text,
    http_metadata_json jsonb,
    collection_run_id uuid,
    UNIQUE (sha256)
);

CREATE TABLE IF NOT EXISTS source.extraction_record (
    extraction_record_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_document_id uuid NOT NULL REFERENCES source.source_document(source_document_id),
    collection_specification_id uuid REFERENCES source.data_collection_specification(collection_specification_id),
    source_page integer,
    worksheet_name text,
    table_name text,
    row_reference text,
    column_reference text,
    cell_reference text,
    xml_json_path text,
    raw_label text,
    raw_value text,
    extracted_at timestamptz NOT NULL DEFAULT now(),
    parser_version text,
    extraction_status text NOT NULL
);

CREATE TABLE IF NOT EXISTS quality.validation_decision (
    validation_decision_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_set_id uuid,
    decision_status text NOT NULL,
    confidence_score numeric,
    severity text,
    decision_reason text,
    decided_by text,
    decided_at timestamptz NOT NULL DEFAULT now(),
    evidence_json jsonb
);

CREATE TABLE IF NOT EXISTS market.statistical_observation (
    statistical_observation_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_series_mapping_id uuid NOT NULL REFERENCES source.provider_series_mapping(provider_series_mapping_id),
    period_start date,
    period_end date,
    observation_date date NOT NULL,
    publication_date date,
    vintage_date date NOT NULL,
    numeric_value numeric,
    text_value text,
    unit text,
    multiplier numeric,
    observation_status text,
    seasonal_adjustment text,
    extraction_record_id uuid REFERENCES source.extraction_record(extraction_record_id),
    validation_decision_id uuid REFERENCES quality.validation_decision(validation_decision_id),
    valid_from timestamptz NOT NULL DEFAULT now(),
    valid_to timestamptz,
    recorded_at timestamptz NOT NULL DEFAULT now(),
    superseded_at timestamptz,
    UNIQUE (provider_series_mapping_id, observation_date, vintage_date, recorded_at)
);

CREATE TABLE IF NOT EXISTS quality.country_data_coverage (
    country_id uuid NOT NULL,
    indicator_definition_id uuid NOT NULL REFERENCES ref.indicator_definition(indicator_definition_id),
    coverage_status text NOT NULL,
    source_status text,
    first_observation_date date,
    last_observation_date date,
    observation_count bigint,
    expected_observation_count bigint,
    completeness_ratio numeric,
    freshness_status text,
    quality_status text,
    method_break_count integer NOT NULL DEFAULT 0,
    benchmark_readiness text,
    next_action text,
    calculated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (country_id, indicator_definition_id)
);

CREATE INDEX IF NOT EXISTS ix_statistical_observation_series_date
    ON market.statistical_observation(provider_series_mapping_id, observation_date);
CREATE INDEX IF NOT EXISTS ix_country_indicator_status
    ON ref.country_indicator_relationship(country_id, coverage_status);
CREATE INDEX IF NOT EXISTS ix_source_document_publication_date
    ON source.source_document(publication_date);
