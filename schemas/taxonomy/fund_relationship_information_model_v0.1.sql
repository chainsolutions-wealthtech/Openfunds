-- Fund Relationship Information Model v0.1
-- PostgreSQL draft

create schema if not exists ref;
create schema if not exists fund;
create schema if not exists taxonomy;
create schema if not exists market;
create schema if not exists calc;
create schema if not exists source;
create schema if not exists quality;

create table if not exists ref.geographic_entity (
    geographic_entity_id uuid primary key,
    entity_type text not null check (entity_type in ('CONTINENT','REGION','COUNTRY','MONETARY_ZONE','ECONOMIC_ZONE')),
    code text not null unique,
    name_fr text not null,
    name_en text,
    parent_geographic_entity_id uuid references ref.geographic_entity(geographic_entity_id),
    valid_from date not null default current_date,
    valid_to date,
    is_active boolean not null default true
);

create table if not exists ref.currency (
    currency_id uuid primary key,
    iso_code char(3) not null unique,
    name_fr text not null,
    name_en text,
    decimal_places smallint not null default 2,
    is_active boolean not null default true
);

create table if not exists ref.country_profile (
    country_id uuid primary key references ref.geographic_entity(geographic_entity_id),
    region_id uuid not null references ref.geographic_entity(geographic_entity_id),
    continent_id uuid not null references ref.geographic_entity(geographic_entity_id),
    local_currency_id uuid not null references ref.currency(currency_id),
    iso_alpha2 char(2),
    iso_alpha3 char(3),
    timezone_name text,
    valid_from date not null default current_date,
    valid_to date
);

create table if not exists taxonomy.asset_class (
    asset_class_id uuid primary key,
    code text not null unique,
    name_fr text not null,
    name_en text,
    display_order integer not null,
    is_active boolean not null default true
);

create table if not exists taxonomy.sub_asset_class (
    sub_asset_class_id uuid primary key,
    asset_class_id uuid not null references taxonomy.asset_class(asset_class_id),
    code text not null,
    short_name_fr text,
    name_fr text not null,
    name_en text,
    display_order integer not null,
    is_active boolean not null default true,
    unique (asset_class_id, code)
);

create table if not exists fund.fund (
    fund_id uuid primary key,
    canonical_fund_code text not null unique,
    fund_name text not null,
    country_id uuid not null references ref.geographic_entity(geographic_entity_id),
    base_currency_id uuid references ref.currency(currency_id),
    launch_date date,
    status text,
    valid_from date not null default current_date,
    valid_to date
);

create table if not exists fund.share_class (
    share_class_id uuid primary key,
    fund_id uuid not null references fund.fund(fund_id),
    isin text,
    share_class_name text not null,
    currency_id uuid not null references ref.currency(currency_id),
    nav_frequency text,
    distribution_policy text,
    is_representative boolean not null default false,
    valid_from date not null default current_date,
    valid_to date
);

create table if not exists taxonomy.category (
    category_id uuid primary key,
    geographic_entity_id uuid not null references ref.geographic_entity(geographic_entity_id),
    geographic_level text not null check (geographic_level in ('NATIONAL','REGIONAL','AFRICA')),
    asset_class_id uuid not null references taxonomy.asset_class(asset_class_id),
    sub_asset_class_id uuid references taxonomy.sub_asset_class(sub_asset_class_id),
    parent_category_id uuid references taxonomy.category(category_id),
    category_kind text not null check (category_kind in ('CATEGORY','SUBCATEGORY')),
    generated_name_fr text not null,
    generated_name_en text,
    canonical_code text not null unique,
    valid_from date not null default current_date,
    valid_to date,
    is_active boolean not null default true,
    unique (geographic_entity_id, geographic_level, asset_class_id, sub_asset_class_id, category_kind)
);

create table if not exists taxonomy.category_hierarchy (
    category_hierarchy_id uuid primary key,
    child_category_id uuid not null references taxonomy.category(category_id),
    parent_category_id uuid not null references taxonomy.category(category_id),
    relationship_type text not null check (relationship_type in ('SUBCATEGORY_OF','NATIONAL_TO_REGIONAL','REGIONAL_TO_AFRICA','NATIONAL_TO_AFRICA')),
    valid_from date not null,
    valid_to date,
    unique (child_category_id, parent_category_id, relationship_type, valid_from)
);

create table if not exists taxonomy.fund_classification (
    fund_classification_id uuid primary key,
    fund_id uuid not null references fund.fund(fund_id),
    asset_class_id uuid not null references taxonomy.asset_class(asset_class_id),
    sub_asset_class_id uuid references taxonomy.sub_asset_class(sub_asset_class_id),
    representative_share_class_id uuid references fund.share_class(share_class_id),
    valid_from date not null,
    valid_to date,
    classification_source_id uuid,
    classification_method text,
    validation_status text not null default 'PENDING',
    benchmark_eligibility_status text not null default 'ELIGIBLE',
    exclusion_reason text
);

create table if not exists taxonomy.fund_category_membership (
    membership_id uuid primary key,
    fund_id uuid not null references fund.fund(fund_id),
    category_id uuid not null references taxonomy.category(category_id),
    membership_role text not null check (membership_role in ('PRIMARY_CATEGORY','PRIMARY_SUBCATEGORY','DERIVED_REGIONAL_CATEGORY','DERIVED_REGIONAL_SUBCATEGORY','DERIVED_AFRICA_CATEGORY','DERIVED_AFRICA_SUBCATEGORY')),
    valid_from date not null,
    valid_to date,
    source_classification_id uuid references taxonomy.fund_classification(fund_classification_id),
    validation_status text not null default 'PENDING',
    is_benchmark_eligible boolean not null default true,
    exclusion_reason text,
    unique (fund_id, category_id, membership_role, valid_from)
);

create table if not exists taxonomy.reference_block (
    reference_block_id uuid primary key,
    category_id uuid not null unique references taxonomy.category(category_id),
    block_name_fr text not null,
    block_name_en text,
    geographic_level text not null check (geographic_level in ('NATIONAL','REGIONAL','AFRICA')),
    valid_from date not null default current_date,
    valid_to date,
    is_active boolean not null default true
);

create table if not exists taxonomy.reference_role (
    reference_role_id uuid primary key,
    reference_block_id uuid not null references taxonomy.reference_block(reference_block_id),
    role_type text not null check (role_type in ('PRIMARY_MARKET_INDEX','SECONDARY_MARKET_INDEX','WTI','WTI_BENCH')),
    generated_name_fr text not null,
    generated_name_en text,
    assigned_series_id uuid,
    display_order smallint not null,
    is_required boolean not null default true,
    valid_from date not null default current_date,
    valid_to date,
    unique (reference_block_id, role_type)
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

create table if not exists fund.nav_observation (
    nav_observation_id uuid primary key,
    share_class_id uuid not null references fund.share_class(share_class_id),
    valuation_date date not null,
    publication_date date,
    currency_id uuid not null references ref.currency(currency_id),
    nav_value numeric(30,12) not null,
    adjusted_nav_value numeric(30,12),
    source_id uuid,
    quality_status text not null default 'OBSERVED',
    unique (share_class_id, valuation_date, currency_id, source_id)
);

create table if not exists calc.converted_observation (
    converted_observation_id uuid primary key,
    observation_type text not null,
    source_observation_id uuid not null,
    source_currency_id uuid not null references ref.currency(currency_id),
    target_currency_id uuid not null references ref.currency(currency_id),
    fx_observation_id uuid not null references market.fx_observation(fx_observation_id),
    observation_date date not null,
    source_value numeric(30,12) not null,
    converted_value numeric(30,12) not null,
    conversion_method text not null,
    quality_status text not null,
    calculated_at timestamptz not null default now(),
    unique (observation_type, source_observation_id, target_currency_id)
);

create table if not exists calc.index_definition (
    index_definition_id uuid primary key,
    category_id uuid not null references taxonomy.category(category_id),
    reference_role_id uuid not null references taxonomy.reference_role(reference_role_id),
    index_type text not null check (index_type in ('MARKET_INDEX','WTI','WTI_BENCH')),
    index_name text not null,
    currency_id uuid not null references ref.currency(currency_id),
    base_date date,
    base_value numeric(30,12) not null default 100,
    methodology_version_id uuid,
    publication_status text not null default 'DRAFT',
    valid_from date not null default current_date,
    valid_to date
);

create table if not exists calc.index_observation (
    index_observation_id uuid primary key,
    index_definition_id uuid not null references calc.index_definition(index_definition_id),
    valuation_date date not null,
    previous_level numeric(30,12),
    daily_return numeric(30,16),
    index_level numeric(30,12) not null,
    eligible_member_count integer,
    contributor_count integer,
    excluded_member_count integer,
    coverage_ratio numeric(12,8),
    quality_score numeric(12,8),
    calculation_status text not null,
    methodology_version_id uuid,
    calculation_run_id uuid,
    calculated_at timestamptz not null default now(),
    unique (index_definition_id, valuation_date)
);

create table if not exists calc.wti_fund_contribution (
    contribution_id uuid primary key,
    index_observation_id uuid not null references calc.index_observation(index_observation_id),
    fund_id uuid not null references fund.fund(fund_id),
    share_class_id uuid references fund.share_class(share_class_id),
    previous_nav_date date,
    current_nav_date date,
    previous_adjusted_nav numeric(30,12),
    current_adjusted_nav numeric(30,12),
    fund_return numeric(30,16),
    weight numeric(30,16),
    weighted_contribution numeric(30,16),
    inclusion_status text not null,
    exclusion_reason text
);

create table if not exists calc.wti_bench_component (
    component_id uuid primary key,
    index_definition_id uuid not null references calc.index_definition(index_definition_id),
    component_type text not null,
    component_reference_id uuid not null,
    weight numeric(30,16),
    valid_from date not null,
    valid_to date,
    inclusion_reason text,
    exclusion_reason text,
    quality_status text
);

create table if not exists calc.wti_bench_contribution (
    contribution_id uuid primary key,
    index_observation_id uuid not null references calc.index_observation(index_observation_id),
    component_id uuid not null references calc.wti_bench_component(component_id),
    component_return numeric(30,16),
    component_weight numeric(30,16),
    weighted_contribution numeric(30,16),
    input_quality_status text
);

create index if not exists idx_category_lookup
    on taxonomy.category (geographic_entity_id, asset_class_id, sub_asset_class_id, geographic_level);

create index if not exists idx_fund_membership_lookup
    on taxonomy.fund_category_membership (fund_id, valid_from, valid_to);

create index if not exists idx_nav_observation_lookup
    on fund.nav_observation (share_class_id, valuation_date);

create index if not exists idx_converted_observation_lookup
    on calc.converted_observation (observation_type, source_observation_id, target_currency_id, observation_date);

create index if not exists idx_index_observation_lookup
    on calc.index_observation (index_definition_id, valuation_date);
