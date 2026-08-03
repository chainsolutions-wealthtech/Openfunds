-- MINIMAL PREREQUISITES FOR APPLYING THE CANONICAL SOURCE AND FX MIGRATIONS.

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

create table if not exists ref.organization (
    organization_id uuid primary key,
    organization_code text not null unique,
    organization_name text not null
);

create table if not exists source.endpoint (
    endpoint_id uuid primary key,
    endpoint_code text not null unique,
    organization_id uuid references ref.organization(organization_id),
    official_url text
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

insert into ref.organization (organization_id, organization_code, organization_name)
values ('00000000-0000-0000-0000-000000000010', 'BCEAO', 'BANQUE CENTRALE DES ETATS DE L AFRIQUE DE L OUEST')
on conflict (organization_code) do nothing;

insert into source.endpoint (endpoint_id, endpoint_code, organization_id, official_url)
values (
    '00000000-0000-0000-0000-000000000020',
    'BCEAO_FX_DAILY',
    '00000000-0000-0000-0000-000000000010',
    'https://www.bceao.int/fr'
)
on conflict (endpoint_code) do nothing;
