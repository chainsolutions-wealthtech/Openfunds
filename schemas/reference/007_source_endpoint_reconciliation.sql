-- SOURCE ENDPOINT SCHEMA RECONCILIATION
-- POSTGRESQL
-- Reconciles the legacy endpoint shape from 003_organizations_and_roles.sql
-- with the relational endpoint shape from 004_source_endpoints_and_indicator_mapping.sql.
-- No source row is deleted and no URL is overwritten destructively.

create schema if not exists ref;
create schema if not exists source;

create table if not exists source.endpoint (
    endpoint_id uuid primary key,
    organization_id uuid not null references ref.organization(organization_id),
    endpoint_code text not null unique
);

alter table source.endpoint
    add column if not exists scope_type text,
    add column if not exists scope_code text,
    add column if not exists endpoint_type text,
    add column if not exists url text,
    add column if not exists official_url text,
    add column if not exists data_portal_url text,
    add column if not exists api_base_url text,
    add column if not exists access_method text,
    add column if not exists auth_required boolean not null default false,
    add column if not exists authentication_type text,
    add column if not exists file_format text,
    add column if not exists file_formats text[],
    add column if not exists publication_frequency text,
    add column if not exists expected_frequency text,
    add column if not exists expected_history_start date,
    add column if not exists history_start date,
    add column if not exists terms_of_use_url text,
    add column if not exists robots_policy_status text,
    add column if not exists last_verified_at timestamptz,
    add column if not exists validation_status text not null default 'PENDING',
    add column if not exists valid_from date,
    add column if not exists valid_to date,
    add column if not exists source_note text,
    add column if not exists created_at timestamptz not null default now(),
    add column if not exists updated_at timestamptz not null default now();

-- The legacy model required URL even when the endpoint was represented by one
-- of the more precise official_url, data_portal_url or api_base_url columns.
alter table source.endpoint
    alter column url drop not null;

-- Preserve the original generic URL while deriving the typed URL columns.
update source.endpoint
set official_url = coalesce(
        official_url,
        case when endpoint_type = 'OFFICIAL_WEBSITE' then url end
    ),
    data_portal_url = coalesce(
        data_portal_url,
        case
            when endpoint_type in ('DATA_PORTAL','WEB_PAGE','FILE_DIRECTORY','RSS','SFTP','OTHER')
            then url
        end
    ),
    api_base_url = coalesce(
        api_base_url,
        case when endpoint_type = 'API' then url end
    )
where official_url is null
   or data_portal_url is null
   or api_base_url is null;

-- Restore a generic compatibility URL without losing the typed representation.
update source.endpoint
set url = coalesce(url, official_url, data_portal_url, api_base_url)
where url is null;

-- Harmonize singular and plural file-format fields.
update source.endpoint
set file_formats = case
        when file_format is null or btrim(file_format) = '' then file_formats
        else regexp_split_to_array(file_format, '\s*,\s*')
    end
where file_formats is null;

update source.endpoint
set file_format = array_to_string(file_formats, ',')
where file_format is null
  and file_formats is not null;

-- Harmonize frequency and history fields used by the two prior definitions.
update source.endpoint
set expected_frequency = coalesce(expected_frequency, publication_frequency),
    publication_frequency = coalesce(publication_frequency, expected_frequency),
    history_start = coalesce(history_start, expected_history_start),
    expected_history_start = coalesce(expected_history_start, history_start);

-- Derive the boolean authentication flag from a meaningful legacy value.
update source.endpoint
set auth_required = true
where coalesce(btrim(authentication_type), '') <> ''
  and upper(btrim(authentication_type)) not in ('NONE','NO_AUTH','PUBLIC','PUBLIC_WEB');

-- Recreate harmonized validation constraints with stable names.
alter table source.endpoint
    drop constraint if exists endpoint_reconciled_scope_type_check,
    drop constraint if exists endpoint_reconciled_type_check,
    drop constraint if exists endpoint_reconciled_validation_status_check,
    drop constraint if exists endpoint_reconciled_validity_check,
    drop constraint if exists endpoint_reconciled_url_check;

alter table source.endpoint
    add constraint endpoint_reconciled_scope_type_check
        check (
            scope_type is null
            or scope_type in ('COUNTRY','ZONE','REGION','CONTINENT')
        ),
    add constraint endpoint_reconciled_type_check
        check (
            endpoint_type is null
            or endpoint_type in (
                'OFFICIAL_WEBSITE','DATA_PORTAL','API','WEB_PAGE',
                'FILE_DIRECTORY','RSS','SFTP','OTHER'
            )
        ),
    add constraint endpoint_reconciled_validation_status_check
        check (validation_status in ('PENDING','VALIDATED','REJECTED','SUPERSEDED')),
    add constraint endpoint_reconciled_validity_check
        check (valid_to is null or valid_from is null or valid_to >= valid_from),
    add constraint endpoint_reconciled_url_check
        check (
            validation_status <> 'VALIDATED'
            or url is not null
            or official_url is not null
            or data_portal_url is not null
            or api_base_url is not null
        );

create index if not exists idx_endpoint_reconciled_org_scope
    on source.endpoint (organization_id, scope_type, scope_code);

create index if not exists idx_endpoint_reconciled_validation
    on source.endpoint (validation_status);

create index if not exists idx_endpoint_reconciled_frequency
    on source.endpoint (expected_frequency);

create or replace view source.current_endpoint as
select
    endpoint_id,
    endpoint_code,
    organization_id,
    scope_type,
    scope_code,
    endpoint_type,
    coalesce(url, official_url, data_portal_url, api_base_url) as canonical_url,
    url,
    official_url,
    data_portal_url,
    api_base_url,
    access_method,
    auth_required,
    authentication_type,
    file_formats,
    expected_frequency,
    history_start,
    terms_of_use_url,
    robots_policy_status,
    last_verified_at,
    validation_status,
    valid_from,
    valid_to,
    source_note,
    created_at,
    updated_at
from source.endpoint
where validation_status = 'VALIDATED'
  and (valid_from is null or valid_from <= current_date)
  and (valid_to is null or valid_to >= current_date);

comment on table source.endpoint is
'Canonical reconciled registry of official websites, data portals, APIs, web pages and file directories. Legacy and relational endpoint fields are preserved for compatibility.';

comment on view source.current_endpoint is
'Validated currently effective endpoints with a non-destructive canonical URL resolution.';
