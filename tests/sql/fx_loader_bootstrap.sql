-- MINIMAL PREREQUISITES FOR APPLYING THE CANONICAL REFERENCE, SOURCE AND FX MIGRATIONS.
-- Organizations and endpoints are deliberately not redefined here: the integration
-- tests exercise the real 003, 004 and 007 migrations in their canonical order.

create schema if not exists ref;
create schema if not exists source;
create schema if not exists market;

create table if not exists ref.currency (
    currency_id uuid primary key,
    iso_code char(3) not null unique,
    name_fr text not null,
    name_en text,
    decimal_places smallint not null default 2,
    is_active boolean not null default true
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
    unique (observation_date, source_currency_id, target_currency_id, source_id)
);

insert into ref.currency (currency_id, iso_code, name_fr, name_en, decimal_places)
values
    ('00000000-0000-0000-0000-000000000001', 'XOF', 'FRANC CFA BCEAO', 'CFA FRANC BCEAO', 0),
    ('00000000-0000-0000-0000-000000000002', 'EUR', 'EURO', 'EURO', 2),
    ('00000000-0000-0000-0000-000000000003', 'USD', 'DOLLAR US', 'US DOLLAR', 2)
on conflict (iso_code) do nothing;

\ir ../../schemas/reference/003_organizations_and_roles.sql
\ir ../../schemas/reference/004_source_endpoints_and_indicator_mapping.sql
\ir ../../schemas/reference/007_source_endpoint_reconciliation.sql
