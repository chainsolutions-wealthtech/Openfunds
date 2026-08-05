-- OPENFUNDS GOVERNED REFERENCE AND MARKET CORE
-- PostgreSQL
-- This migration extracts only the stable prerequisite objects required by the
-- governed reference/source/FX migration chain. It does not finalize the
-- Fund/SubFund/ShareClass model.

create schema if not exists ref;
create schema if not exists source;
create schema if not exists market;
create schema if not exists openfunds_migration;

create table if not exists ref.geographic_entity (
    geographic_entity_id uuid primary key,
    entity_type text not null check (
        entity_type in (
            'CONTINENT','REGION','COUNTRY','MONETARY_ZONE',
            'ECONOMIC_ZONE','MARKET_ZONE'
        )
    ),
    code text not null unique,
    name_fr text not null,
    name_en text,
    parent_geographic_entity_id uuid references ref.geographic_entity(geographic_entity_id),
    valid_from date not null default current_date,
    valid_to date,
    is_active boolean not null default true,
    check (valid_to is null or valid_to >= valid_from)
);

create table if not exists ref.currency (
    currency_id uuid primary key,
    iso_code char(3) not null unique,
    name_fr text not null,
    name_en text,
    decimal_places smallint not null default 2,
    is_active boolean not null default true,
    check (decimal_places between 0 and 8)
);

create table if not exists market.fx_observation (
    fx_observation_id uuid primary key,
    observation_date date not null,
    source_currency_id uuid not null references ref.currency(currency_id),
    target_currency_id uuid not null references ref.currency(currency_id),
    fx_rate numeric(30,12) not null,
    publication_date date,
    source_id uuid,
    quality_status text not null default 'OBSERVED',
    unique (observation_date, source_currency_id, target_currency_id, source_id),
    check (fx_rate > 0),
    check (source_currency_id <> target_currency_id)
);

comment on schema openfunds_migration is
'Governed migration metadata owned by scripts/run_migrations.py.';

comment on table ref.geographic_entity is
'Stable geography prerequisite. Fund persistence remains governed separately by OF-DATA-001.';

comment on table market.fx_observation is
'Base FX observation relation extended additively by migration 006.';
