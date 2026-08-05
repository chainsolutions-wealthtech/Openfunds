-- COUNTRY RELATIONSHIP MODEL
-- POSTGRESQL
-- ALL TECHNICAL CODES MUST BE UPPERCASE AND WITHOUT ACCENTS.

create schema if not exists ref;
create schema if not exists source;

create table if not exists ref.entity_relationship (
    relationship_id uuid primary key,
    source_entity_id uuid not null references ref.geographic_entity(geographic_entity_id),
    relationship_type text not null check (
        relationship_type in (
            'BELONGS_TO_REGION',
            'BELONGS_TO_CONTINENT',
            'USES_CURRENCY',
            'BELONGS_TO_MONETARY_ZONE',
            'USES_REFERENCE_CURRENCY',
            'USES_CENTRAL_BANK',
            'USES_NATIONAL_EXCHANGE',
            'USES_COMMON_EXCHANGE',
            'USES_MARKET_SCOPE'
        )
    ),
    target_entity_code text not null,
    relationship_domain text not null check (
        relationship_domain in (
            'GEOGRAPHIC',
            'MONETARY',
            'INSTITUTIONAL',
            'MARKET'
        )
    ),
    relationship_role text not null default 'PRIMARY',
    valid_from date not null,
    valid_to date,
    is_primary boolean not null default true,
    source_id uuid,
    validation_status text not null default 'PENDING' check (
        validation_status in (
            'PENDING',
            'VALIDATED',
            'REJECTED',
            'SUPERSEDED'
        )
    ),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    check (valid_to is null or valid_to >= valid_from),
    unique (
        source_entity_id,
        relationship_type,
        target_entity_code,
        valid_from
    )
);

create index if not exists idx_entity_relationship_source_type
    on ref.entity_relationship (source_entity_id, relationship_type);

create index if not exists idx_entity_relationship_target
    on ref.entity_relationship (target_entity_code);

create index if not exists idx_entity_relationship_active
    on ref.entity_relationship (source_entity_id, relationship_type, valid_from, valid_to);

-- ONE ACTIVE PRIMARY RELATION PER COUNTRY AND RELATIONSHIP TYPE IS ENFORCED
-- BY THE APPLICATION VALIDATION LAYER BECAUSE THE ACTIVE DATE IS TEMPORAL.

-- Create only the historical base view. Later migrations may append columns;
-- replaying 002 on an existing database must never try to remove them.
do $$
begin
    if to_regclass('ref.current_entity_relationship') is null then
        execute $view$
            create view ref.current_entity_relationship as
            select
                relationship_id,
                source_entity_id,
                relationship_type,
                target_entity_code,
                relationship_domain,
                relationship_role,
                valid_from,
                valid_to,
                is_primary,
                source_id,
                validation_status
            from ref.entity_relationship
            where valid_from <= current_date
              and (valid_to is null or valid_to >= current_date)
              and validation_status = 'VALIDATED'
        $view$;
    end if;
end
$$;

-- EXPECTED UEMOA RELATIONS
-- COUNTRY -> AFRICA_OUEST
-- COUNTRY -> AFRICA
-- COUNTRY -> XOF
-- COUNTRY -> UEMOA
-- COUNTRY -> BCEAO
-- COUNTRY -> BRVM
-- COUNTRY -> MARKET_SCOPE UEMOA

-- EXPECTED CEMAC RELATIONS
-- COUNTRY -> AFRICA_CENTRALE
-- COUNTRY -> AFRICA
-- COUNTRY -> XAF
-- COUNTRY -> CEMAC
-- COUNTRY -> BEAC
-- COUNTRY -> BVMAC
-- COUNTRY -> MARKET_SCOPE CEMAC
