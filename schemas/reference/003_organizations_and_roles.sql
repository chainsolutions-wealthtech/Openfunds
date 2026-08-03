-- ORGANIZATIONS AND INSTITUTIONAL ROLES
-- POSTGRESQL
-- TECHNICAL CODES MUST BE UPPERCASE AND WITHOUT ACCENTS.

create schema if not exists ref;
create schema if not exists source;

create table if not exists ref.organization_role (
    role_code text primary key,
    role_domain text not null,
    name_fr_canonical text not null,
    name_en text,
    description text,
    can_be_country_scope boolean not null default false,
    can_be_zone_scope boolean not null default false,
    can_be_regional_scope boolean not null default false,
    can_be_continent_scope boolean not null default false,
    is_data_provider_role boolean not null default false,
    is_regulatory_role boolean not null default false,
    is_market_infrastructure_role boolean not null default false,
    is_active boolean not null default true,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists ref.organization (
    organization_id uuid primary key,
    organization_code text not null unique,
    organization_type text not null,
    name_fr_canonical text not null,
    name_en text,
    acronym text,
    primary_scope_code text,
    primary_country_code text,
    primary_zone_code text,
    official_website text,
    data_portal_url text,
    is_public_authority boolean not null default false,
    is_market_infrastructure boolean not null default false,
    is_data_provider boolean not null default false,
    valid_from date,
    valid_to date,
    validation_status text not null default 'PENDING' check (
        validation_status in ('PENDING','VALIDATED','REJECTED','SUPERSEDED')
    ),
    source_note text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    check (valid_to is null or valid_from is null or valid_to >= valid_from)
);

create table if not exists ref.organization_scope_role (
    organization_scope_role_id uuid primary key,
    organization_id uuid not null references ref.organization(organization_id),
    role_code text not null references ref.organization_role(role_code),
    scope_entity_code text not null,
    scope_entity_type text not null check (
        scope_entity_type in ('COUNTRY','MONETARY_ZONE','MARKET_ZONE','REGION','CONTINENT','GLOBAL')
    ),
    relationship_role text not null default 'PRIMARY',
    is_primary boolean not null default true,
    valid_from date,
    valid_to date,
    validation_status text not null default 'PENDING' check (
        validation_status in ('PENDING','VALIDATED','REJECTED','SUPERSEDED')
    ),
    source_id uuid,
    source_note text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    check (valid_to is null or valid_from is null or valid_to >= valid_from),
    unique (organization_id, role_code, scope_entity_code, valid_from)
);

create table if not exists source.endpoint (
    endpoint_id uuid primary key,
    organization_id uuid not null references ref.organization(organization_id),
    endpoint_code text not null unique,
    endpoint_type text not null check (
        endpoint_type in ('OFFICIAL_WEBSITE','DATA_PORTAL','API','WEB_PAGE','FILE_DIRECTORY','RSS','SFTP','OTHER')
    ),
    url text not null,
    access_method text,
    file_format text,
    authentication_type text,
    publication_frequency text,
    expected_history_start date,
    terms_of_use_url text,
    robots_policy_status text,
    last_verified_at timestamptz,
    validation_status text not null default 'PENDING' check (
        validation_status in ('PENDING','VALIDATED','REJECTED','SUPERSEDED')
    ),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create index if not exists idx_organization_scope_role_scope
    on ref.organization_scope_role (scope_entity_code, role_code);

create index if not exists idx_organization_scope_role_organization
    on ref.organization_scope_role (organization_id);

create index if not exists idx_source_endpoint_organization
    on source.endpoint (organization_id);

create or replace view ref.current_organization_scope_role as
select
    osr.organization_scope_role_id,
    o.organization_code,
    osr.role_code,
    osr.scope_entity_code,
    osr.scope_entity_type,
    osr.relationship_role,
    osr.is_primary,
    osr.valid_from,
    osr.valid_to,
    osr.validation_status
from ref.organization_scope_role osr
join ref.organization o on o.organization_id = osr.organization_id
where (osr.valid_from is null or osr.valid_from <= current_date)
  and (osr.valid_to is null or osr.valid_to >= current_date)
  and osr.validation_status = 'VALIDATED';
