-- SOURCE ENDPOINT AND INDICATOR MAPPING MODEL
-- POSTGRESQL
-- ALL TECHNICAL CODES MUST BE UPPERCASE AND WITHOUT ACCENTS.
-- This migration is additive when source.endpoint was already created by 003.

create schema if not exists source;
create schema if not exists ref;

create table if not exists source.endpoint (
    endpoint_id uuid primary key,
    endpoint_code text not null unique,
    organization_id uuid not null references ref.organization(organization_id),
    scope_type text not null check (scope_type in ('COUNTRY','ZONE','REGION','CONTINENT')),
    scope_code text not null,
    endpoint_type text not null check (endpoint_type in ('OFFICIAL_WEBSITE','DATA_PORTAL','API','WEB_PAGE','FILE_DIRECTORY','RSS','SFTP','OTHER')),
    official_url text,
    data_portal_url text,
    api_base_url text,
    access_method text,
    auth_required boolean not null default false,
    file_formats text[],
    expected_frequency text,
    history_start date,
    last_verified_at timestamptz,
    validation_status text not null default 'PENDING' check (validation_status in ('PENDING','VALIDATED','REJECTED','SUPERSEDED')),
    valid_from date,
    valid_to date,
    source_note text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    check (valid_to is null or valid_from is null or valid_to >= valid_from)
);

-- If 003 created source.endpoint first, CREATE TABLE IF NOT EXISTS does not add
-- the relational columns. Add them before creating indexes or mappings.
-- They remain nullable until 007 performs reconciliation and validation.
alter table source.endpoint
    add column if not exists scope_type text,
    add column if not exists scope_code text,
    add column if not exists official_url text,
    add column if not exists data_portal_url text,
    add column if not exists api_base_url text,
    add column if not exists auth_required boolean not null default false,
    add column if not exists file_formats text[],
    add column if not exists expected_frequency text,
    add column if not exists history_start date,
    add column if not exists valid_from date,
    add column if not exists valid_to date,
    add column if not exists source_note text,
    add column if not exists created_at timestamptz not null default now(),
    add column if not exists updated_at timestamptz not null default now();

create table if not exists source.indicator_source_mapping (
    mapping_id uuid primary key,
    mapping_code text not null unique,
    scope_type text not null check (scope_type in ('COUNTRY','ZONE','REGION','CONTINENT')),
    scope_code text not null,
    domain_code text not null,
    indicator_code text not null,
    organization_id uuid not null references ref.organization(organization_id),
    organization_role_code text not null references ref.organization_role(role_code),
    endpoint_id uuid references source.endpoint(endpoint_id),
    provider_series_code text,
    provider_series_name text,
    frequency_native text,
    unit_code text,
    currency_code text,
    is_primary_source boolean not null default false,
    source_priority integer,
    collection_status text not null default 'SOURCE_NOT_IDENTIFIED' check (
        collection_status in (
            'SOURCE_NOT_IDENTIFIED','SOURCE_IDENTIFIED','URL_LINKED','COLLECTION_TESTED',
            'PARTIAL_HISTORY_LOADED','COMPLETE_HISTORY_LOADED','NOT_PUBLISHED',
            'NOT_APPLICABLE','DISCONTINUED','REPLACED'
        )
    ),
    valid_from date,
    valid_to date,
    validation_status text not null default 'PENDING' check (validation_status in ('PENDING','VALIDATED','REJECTED','SUPERSEDED')),
    usage_target text[],
    source_note text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    check (source_priority is null or source_priority > 0),
    check (valid_to is null or valid_from is null or valid_to >= valid_from)
);

create index if not exists idx_endpoint_org_scope on source.endpoint (organization_id, scope_type, scope_code);
create index if not exists idx_mapping_scope_indicator on source.indicator_source_mapping (scope_type, scope_code, indicator_code);
create index if not exists idx_mapping_org_role on source.indicator_source_mapping (organization_id, organization_role_code);
create index if not exists idx_mapping_collection_status on source.indicator_source_mapping (collection_status);
