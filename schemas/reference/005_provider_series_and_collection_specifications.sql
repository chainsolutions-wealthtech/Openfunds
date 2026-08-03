-- PROVIDER SERIES AND COLLECTION SPECIFICATIONS
-- POSTGRESQL
-- ALL TECHNICAL CODES MUST BE UPPERCASE AND WITHOUT ACCENTS.

create schema if not exists source;

create table if not exists source.provider_series (
    provider_series_id uuid primary key,
    provider_series_code text not null unique,
    mapping_code text not null,
    organization_id uuid not null references ref.organization(organization_id),
    endpoint_id uuid references source.endpoint(endpoint_id),
    canonical_indicator_code text not null,
    native_series_code text,
    native_series_name text,
    native_series_url text,
    native_frequency text,
    native_unit text,
    native_currency_code text,
    date_start date,
    date_end date,
    publication_lag_days integer,
    revision_policy text,
    history_status text not null default 'SOURCE_IDENTIFIED',
    validation_status text not null default 'PENDING' check (
        validation_status in ('PENDING','VALIDATED','REJECTED','SUPERSEDED')
    ),
    valid_from date,
    valid_to date,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    check (date_end is null or date_start is null or date_end >= date_start),
    check (valid_to is null or valid_from is null or valid_to >= valid_from)
);

create table if not exists source.collection_specification (
    collection_specification_id uuid primary key,
    collection_specification_code text not null unique,
    provider_series_id uuid not null references source.provider_series(provider_series_id),
    collection_method text not null,
    request_method text,
    discovery_rule text,
    file_pattern text,
    sheet_rule text,
    table_or_selector text,
    date_extraction_rule text,
    value_extraction_rule text,
    number_parsing_rule text,
    currency_rule text,
    frequency_check text,
    expected_publication_lag_days integer,
    deduplication_key text,
    revision_handling text,
    raw_artifact_required boolean not null default true,
    hash_required boolean not null default true,
    parser_version text,
    retry_policy text,
    quality_check_profile text,
    implementation_status text not null default 'SPECIFICATION_REQUIRED',
    validation_status text not null default 'PENDING' check (
        validation_status in ('PENDING','VALIDATED','REJECTED','SUPERSEDED')
    ),
    valid_from date,
    valid_to date,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    check (valid_to is null or valid_from is null or valid_to >= valid_from)
);

create table if not exists source.collection_run (
    collection_run_id uuid primary key,
    collection_specification_id uuid not null references source.collection_specification(collection_specification_id),
    started_at timestamptz not null,
    completed_at timestamptz,
    run_status text not null check (
        run_status in ('STARTED','SUCCEEDED','PARTIAL','FAILED','REJECTED')
    ),
    source_url text,
    http_status integer,
    artifact_count integer not null default 0,
    observation_count integer not null default 0,
    warning_count integer not null default 0,
    error_count integer not null default 0,
    parser_version text,
    execution_metadata jsonb,
    created_at timestamptz not null default now()
);

create table if not exists source.raw_artifact (
    raw_artifact_id uuid primary key,
    collection_run_id uuid not null references source.collection_run(collection_run_id),
    source_url text,
    original_filename text,
    media_type text,
    sha256 text not null,
    byte_size bigint,
    retrieved_at timestamptz not null,
    storage_uri text not null,
    publication_date date,
    source_modified_at timestamptz,
    metadata jsonb,
    unique (sha256, storage_uri)
);

create index if not exists idx_provider_series_mapping
    on source.provider_series (mapping_code);

create index if not exists idx_provider_series_indicator
    on source.provider_series (canonical_indicator_code);

create index if not exists idx_collection_spec_provider_series
    on source.collection_specification (provider_series_id);

create index if not exists idx_collection_run_spec_started
    on source.collection_run (collection_specification_id, started_at desc);

create index if not exists idx_raw_artifact_run
    on source.raw_artifact (collection_run_id);
