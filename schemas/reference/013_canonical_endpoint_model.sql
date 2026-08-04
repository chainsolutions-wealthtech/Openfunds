-- CANONICAL ENDPOINT MODEL CONTRACT
-- POSTGRESQL
-- source.endpoint is the only physical canonical endpoint relation.
-- Migrations 003 and 004 are historical creation shapes reconciled by 007.

create schema if not exists source;

create table if not exists source.endpoint_model_contract_registry (
    contract_code text primary key,
    contract_version text not null,
    canonical_schema text not null,
    canonical_relation text not null,
    normalized_view text not null,
    legacy_physical_relation text,
    compatibility_columns text[] not null,
    decided_at date not null,
    source_note text not null,
    updated_at timestamptz not null default now(),
    check (contract_code = 'CANONICAL_ENDPOINT_MODEL'),
    check (canonical_schema = 'source'),
    check (canonical_relation = 'endpoint'),
    check (legacy_physical_relation is null)
);

insert into source.endpoint_model_contract_registry (
    contract_code,
    contract_version,
    canonical_schema,
    canonical_relation,
    normalized_view,
    legacy_physical_relation,
    compatibility_columns,
    decided_at,
    source_note
)
values (
    'CANONICAL_ENDPOINT_MODEL',
    '1.0.0',
    'source',
    'endpoint',
    'source.endpoint_contract',
    null,
    array['url','file_format','publication_frequency','expected_history_start','authentication_type'],
    date '2026-08-05',
    'ADR_026_SOURCE_ENDPOINT_IS_THE_ONLY_PHYSICAL_CANONICAL_RELATION'
)
on conflict (contract_code) do update
set contract_version = excluded.contract_version,
    canonical_schema = excluded.canonical_schema,
    canonical_relation = excluded.canonical_relation,
    normalized_view = excluded.normalized_view,
    legacy_physical_relation = excluded.legacy_physical_relation,
    compatibility_columns = excluded.compatibility_columns,
    decided_at = excluded.decided_at,
    source_note = excluded.source_note,
    updated_at = now();

create or replace view source.endpoint_contract as
select
    endpoint_id,
    endpoint_code,
    organization_id,
    scope_type,
    scope_code,
    endpoint_type,
    coalesce(official_url, data_portal_url, api_base_url, url) as canonical_url,
    official_url,
    data_portal_url,
    api_base_url,
    access_method,
    auth_required,
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
from source.endpoint;

comment on table source.endpoint is
'Only physical canonical endpoint relation. Legacy columns from migration 003 remain compatibility fields; normalized writes use the relational columns established by 004 and reconciled by 007.';

comment on view source.endpoint_contract is
'Versioned normalized endpoint contract. Consumers must prefer this view or the normalized columns of source.endpoint.';

comment on table source.endpoint_model_contract_registry is
'Machine-readable declaration of the canonical endpoint relation and compatibility boundary.';
