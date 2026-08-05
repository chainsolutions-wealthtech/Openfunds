-- 015 CANONICAL FUND / SUBFUND / SHARE CLASS CORE
-- PostgreSQL
-- OF-DATA-001
--
-- This migration deliberately avoids the legacy draft table names fund.fund and
-- fund.share_class. Existing manually-created draft tables are left untouched.
-- The canonical model uses a stable entity supertype, versioned profiles,
-- versioned names and identifiers, explicit structure relationships and events.

create schema if not exists fund;

create table if not exists fund.entity (
    entity_id uuid primary key,
    entity_type text not null check (entity_type in ('FUND','SUBFUND','SHARE_CLASS')),
    canonical_code text not null unique,
    created_at timestamptz not null default now(),
    retired_at timestamptz,
    check (canonical_code ~ '^[A-Z0-9][A-Z0-9_:-]*$'),
    check (retired_at is null or retired_at >= created_at),
    unique (entity_id, entity_type)
);

create table if not exists fund.entity_state (
    entity_state_id uuid primary key,
    entity_id uuid not null references fund.entity(entity_id),
    lifecycle_status text not null check (
        lifecycle_status in (
            'PENDING','ACTIVE','SUSPENDED','CLOSED','LIQUIDATED',
            'MERGED','DISSOLVED','UNKNOWN'
        )
    ),
    domicile_country_id uuid references ref.geographic_entity(geographic_entity_id),
    effective_from date,
    effective_from_status text not null check (
        effective_from_status in ('KNOWN','APPROXIMATE','UNKNOWN','NOT_APPLICABLE')
    ),
    effective_to date,
    effective_to_status text not null default 'NOT_APPLICABLE' check (
        effective_to_status in ('KNOWN','APPROXIMATE','UNKNOWN','NOT_APPLICABLE')
    ),
    recorded_at timestamptz not null default now(),
    superseded_at timestamptz,
    is_current boolean not null default true,
    validation_status text not null default 'PENDING' check (
        validation_status in ('PENDING','VALIDATED','REJECTED','SUPERSEDED')
    ),
    source_artifact_id uuid references source.raw_artifact(raw_artifact_id),
    source_locator jsonb,
    source_note text,
    check (
        (effective_from_status in ('KNOWN','APPROXIMATE') and effective_from is not null)
        or
        (effective_from_status in ('UNKNOWN','NOT_APPLICABLE') and effective_from is null)
    ),
    check (
        (effective_to_status in ('KNOWN','APPROXIMATE') and effective_to is not null)
        or
        (effective_to_status in ('UNKNOWN','NOT_APPLICABLE') and effective_to is null)
    ),
    check (effective_to is null or effective_from is null or effective_to >= effective_from),
    check (
        (is_current and superseded_at is null)
        or
        (not is_current and superseded_at is not null)
    )
);

create unique index if not exists ux_fund_entity_state_current
    on fund.entity_state (entity_id)
    where is_current;

create table if not exists fund.fund_profile (
    fund_profile_id uuid primary key,
    fund_id uuid not null,
    entity_type text not null default 'FUND' check (entity_type = 'FUND'),
    structure_type text not null check (structure_type in ('STANDALONE','UMBRELLA')),
    legal_form_code text not null,
    has_legal_personality boolean,
    base_currency_id uuid references ref.currency(currency_id),
    effective_from date,
    effective_from_status text not null check (
        effective_from_status in ('KNOWN','APPROXIMATE','UNKNOWN','NOT_APPLICABLE')
    ),
    effective_to date,
    effective_to_status text not null default 'NOT_APPLICABLE' check (
        effective_to_status in ('KNOWN','APPROXIMATE','UNKNOWN','NOT_APPLICABLE')
    ),
    recorded_at timestamptz not null default now(),
    superseded_at timestamptz,
    is_current boolean not null default true,
    validation_status text not null default 'PENDING' check (
        validation_status in ('PENDING','VALIDATED','REJECTED','SUPERSEDED')
    ),
    source_artifact_id uuid references source.raw_artifact(raw_artifact_id),
    source_locator jsonb,
    source_note text,
    foreign key (fund_id, entity_type)
        references fund.entity(entity_id, entity_type),
    check (legal_form_code ~ '^[A-Z0-9][A-Z0-9_:-]*$'),
    check (
        (effective_from_status in ('KNOWN','APPROXIMATE') and effective_from is not null)
        or
        (effective_from_status in ('UNKNOWN','NOT_APPLICABLE') and effective_from is null)
    ),
    check (
        (effective_to_status in ('KNOWN','APPROXIMATE') and effective_to is not null)
        or
        (effective_to_status in ('UNKNOWN','NOT_APPLICABLE') and effective_to is null)
    ),
    check (effective_to is null or effective_from is null or effective_to >= effective_from),
    check (
        (is_current and superseded_at is null)
        or
        (not is_current and superseded_at is not null)
    )
);

create unique index if not exists ux_fund_profile_current
    on fund.fund_profile (fund_id)
    where is_current;

create table if not exists fund.subfund_profile (
    subfund_profile_id uuid primary key,
    subfund_id uuid not null,
    entity_type text not null default 'SUBFUND' check (entity_type = 'SUBFUND'),
    compartment_type text not null default 'COMPARTMENT' check (
        compartment_type in ('COMPARTMENT','PORTFOLIO','SERIES','OTHER')
    ),
    base_currency_id uuid references ref.currency(currency_id),
    effective_from date,
    effective_from_status text not null check (
        effective_from_status in ('KNOWN','APPROXIMATE','UNKNOWN','NOT_APPLICABLE')
    ),
    effective_to date,
    effective_to_status text not null default 'NOT_APPLICABLE' check (
        effective_to_status in ('KNOWN','APPROXIMATE','UNKNOWN','NOT_APPLICABLE')
    ),
    recorded_at timestamptz not null default now(),
    superseded_at timestamptz,
    is_current boolean not null default true,
    validation_status text not null default 'PENDING' check (
        validation_status in ('PENDING','VALIDATED','REJECTED','SUPERSEDED')
    ),
    source_artifact_id uuid references source.raw_artifact(raw_artifact_id),
    source_locator jsonb,
    source_note text,
    foreign key (subfund_id, entity_type)
        references fund.entity(entity_id, entity_type),
    check (
        (effective_from_status in ('KNOWN','APPROXIMATE') and effective_from is not null)
        or
        (effective_from_status in ('UNKNOWN','NOT_APPLICABLE') and effective_from is null)
    ),
    check (
        (effective_to_status in ('KNOWN','APPROXIMATE') and effective_to is not null)
        or
        (effective_to_status in ('UNKNOWN','NOT_APPLICABLE') and effective_to is null)
    ),
    check (effective_to is null or effective_from is null or effective_to >= effective_from),
    check (
        (is_current and superseded_at is null)
        or
        (not is_current and superseded_at is not null)
    )
);

create unique index if not exists ux_subfund_profile_current
    on fund.subfund_profile (subfund_id)
    where is_current;

create table if not exists fund.share_class_profile (
    share_class_profile_id uuid primary key,
    share_class_id uuid not null,
    entity_type text not null default 'SHARE_CLASS' check (entity_type = 'SHARE_CLASS'),
    currency_id uuid not null references ref.currency(currency_id),
    distribution_policy text not null default 'UNKNOWN' check (
        distribution_policy in ('ACCUMULATING','DISTRIBUTING','MIXED','UNKNOWN')
    ),
    hedging_policy text not null default 'UNKNOWN' check (
        hedging_policy in ('HEDGED','UNHEDGED','PARTIALLY_HEDGED','UNKNOWN')
    ),
    nav_frequency text,
    is_representative boolean not null default false,
    effective_from date,
    effective_from_status text not null check (
        effective_from_status in ('KNOWN','APPROXIMATE','UNKNOWN','NOT_APPLICABLE')
    ),
    effective_to date,
    effective_to_status text not null default 'NOT_APPLICABLE' check (
        effective_to_status in ('KNOWN','APPROXIMATE','UNKNOWN','NOT_APPLICABLE')
    ),
    recorded_at timestamptz not null default now(),
    superseded_at timestamptz,
    is_current boolean not null default true,
    validation_status text not null default 'PENDING' check (
        validation_status in ('PENDING','VALIDATED','REJECTED','SUPERSEDED')
    ),
    source_artifact_id uuid references source.raw_artifact(raw_artifact_id),
    source_locator jsonb,
    source_note text,
    foreign key (share_class_id, entity_type)
        references fund.entity(entity_id, entity_type),
    check (
        (effective_from_status in ('KNOWN','APPROXIMATE') and effective_from is not null)
        or
        (effective_from_status in ('UNKNOWN','NOT_APPLICABLE') and effective_from is null)
    ),
    check (
        (effective_to_status in ('KNOWN','APPROXIMATE') and effective_to is not null)
        or
        (effective_to_status in ('UNKNOWN','NOT_APPLICABLE') and effective_to is null)
    ),
    check (effective_to is null or effective_from is null or effective_to >= effective_from),
    check (
        (is_current and superseded_at is null)
        or
        (not is_current and superseded_at is not null)
    )
);

create unique index if not exists ux_share_class_profile_current
    on fund.share_class_profile (share_class_id)
    where is_current;

create table if not exists fund.entity_event (
    event_id uuid primary key,
    event_type text not null check (
        event_type in (
            'LAUNCH','RENAME','MERGER','ABSORPTION','SPLIT',
            'MANAGEMENT_TRANSFER','DOMICILE_TRANSFER','LEGAL_FORM_CHANGE',
            'SUSPENSION','REACTIVATION','CLOSURE','LIQUIDATION','OTHER'
        )
    ),
    effective_date date,
    effective_date_status text not null check (
        effective_date_status in ('KNOWN','APPROXIMATE','UNKNOWN','NOT_APPLICABLE')
    ),
    publication_date date,
    event_summary text not null,
    recorded_at timestamptz not null default now(),
    validation_status text not null default 'PENDING' check (
        validation_status in ('PENDING','VALIDATED','REJECTED','SUPERSEDED')
    ),
    source_artifact_id uuid references source.raw_artifact(raw_artifact_id),
    source_locator jsonb,
    source_note text,
    check (
        (effective_date_status in ('KNOWN','APPROXIMATE') and effective_date is not null)
        or
        (effective_date_status in ('UNKNOWN','NOT_APPLICABLE') and effective_date is null)
    )
);

create table if not exists fund.event_participant (
    event_participant_id uuid primary key,
    event_id uuid not null references fund.entity_event(event_id),
    entity_id uuid references fund.entity(entity_id),
    organization_id uuid references ref.organization(organization_id),
    participant_role text not null check (
        participant_role in (
            'SUBJECT','PREDECESSOR','SUCCESSOR','SURVIVING_ENTITY',
            'ABSORBED_ENTITY','SOURCE_ENTITY','TARGET_ENTITY',
            'TRANSFERRED_ENTITY','FROM_MANAGER','TO_MANAGER',
            'FORMER_DOMICILE','NEW_DOMICILE','OTHER'
        )
    ),
    note text,
    check ((entity_id is not null)::integer + (organization_id is not null)::integer = 1)
);

create unique index if not exists ux_event_entity_participant
    on fund.event_participant (event_id, entity_id, participant_role)
    where entity_id is not null;

create unique index if not exists ux_event_organization_participant
    on fund.event_participant (event_id, organization_id, participant_role)
    where organization_id is not null;

create table if not exists fund.entity_name (
    entity_name_id uuid primary key,
    entity_id uuid not null references fund.entity(entity_id),
    event_id uuid references fund.entity_event(event_id),
    name_role text not null check (
        name_role in ('LEGAL_NAME','DISPLAY_NAME','SHORT_NAME','FORMER_NAME','ALIAS')
    ),
    name_text text not null,
    normalized_name text not null,
    language_code text not null default 'und',
    effective_from date,
    effective_from_status text not null check (
        effective_from_status in ('KNOWN','APPROXIMATE','UNKNOWN','NOT_APPLICABLE')
    ),
    effective_to date,
    effective_to_status text not null default 'NOT_APPLICABLE' check (
        effective_to_status in ('KNOWN','APPROXIMATE','UNKNOWN','NOT_APPLICABLE')
    ),
    recorded_at timestamptz not null default now(),
    superseded_at timestamptz,
    is_current boolean not null default true,
    validation_status text not null default 'PENDING' check (
        validation_status in ('PENDING','VALIDATED','REJECTED','SUPERSEDED')
    ),
    source_artifact_id uuid references source.raw_artifact(raw_artifact_id),
    source_locator jsonb,
    source_note text,
    check (btrim(name_text) <> ''),
    check (btrim(normalized_name) <> ''),
    check (
        (effective_from_status in ('KNOWN','APPROXIMATE') and effective_from is not null)
        or
        (effective_from_status in ('UNKNOWN','NOT_APPLICABLE') and effective_from is null)
    ),
    check (
        (effective_to_status in ('KNOWN','APPROXIMATE') and effective_to is not null)
        or
        (effective_to_status in ('UNKNOWN','NOT_APPLICABLE') and effective_to is null)
    ),
    check (effective_to is null or effective_from is null or effective_to >= effective_from),
    check (
        (is_current and superseded_at is null)
        or
        (not is_current and superseded_at is not null)
    )
);

create unique index if not exists ux_entity_open_primary_name
    on fund.entity_name (entity_id, name_role, language_code)
    where is_current
      and effective_to is null
      and name_role in ('LEGAL_NAME','DISPLAY_NAME','SHORT_NAME');

create unique index if not exists ux_entity_name_version
    on fund.entity_name (
        entity_id,
        name_role,
        language_code,
        normalized_name,
        coalesce(effective_from, '-infinity'::date),
        effective_from_status
    )
    where is_current;

create table if not exists fund.entity_identifier (
    entity_identifier_id uuid primary key,
    entity_id uuid not null references fund.entity(entity_id),
    event_id uuid references fund.entity_event(event_id),
    identifier_scheme text not null check (
        identifier_scheme in (
            'ISIN','LEI','REGULATOR_ID','LOCAL_CODE',
            'OPENFUNDS_ID','INTERNAL_LEGACY_ID','OTHER'
        )
    ),
    identifier_value text not null,
    normalized_value text not null,
    issuer_organization_id uuid references ref.organization(organization_id),
    effective_from date,
    effective_from_status text not null check (
        effective_from_status in ('KNOWN','APPROXIMATE','UNKNOWN','NOT_APPLICABLE')
    ),
    effective_to date,
    effective_to_status text not null default 'NOT_APPLICABLE' check (
        effective_to_status in ('KNOWN','APPROXIMATE','UNKNOWN','NOT_APPLICABLE')
    ),
    recorded_at timestamptz not null default now(),
    superseded_at timestamptz,
    is_current boolean not null default true,
    validation_status text not null default 'PENDING' check (
        validation_status in ('PENDING','VALIDATED','REJECTED','SUPERSEDED')
    ),
    source_artifact_id uuid references source.raw_artifact(raw_artifact_id),
    source_locator jsonb,
    source_note text,
    check (btrim(identifier_value) <> ''),
    check (btrim(normalized_value) <> ''),
    check (
        (effective_from_status in ('KNOWN','APPROXIMATE') and effective_from is not null)
        or
        (effective_from_status in ('UNKNOWN','NOT_APPLICABLE') and effective_from is null)
    ),
    check (
        (effective_to_status in ('KNOWN','APPROXIMATE') and effective_to is not null)
        or
        (effective_to_status in ('UNKNOWN','NOT_APPLICABLE') and effective_to is null)
    ),
    check (effective_to is null or effective_from is null or effective_to >= effective_from),
    check (
        (is_current and superseded_at is null)
        or
        (not is_current and superseded_at is not null)
    )
);

create unique index if not exists ux_entity_identifier_current
    on fund.entity_identifier (
        identifier_scheme,
        coalesce(issuer_organization_id, '00000000-0000-0000-0000-000000000000'::uuid),
        normalized_value
    )
    where is_current
      and effective_to is null
      and validation_status <> 'REJECTED';

create table if not exists fund.structure_relationship (
    structure_relationship_id uuid primary key,
    parent_entity_id uuid not null,
    parent_entity_type text not null,
    child_entity_id uuid not null,
    child_entity_type text not null,
    relationship_type text not null check (
        relationship_type in (
            'FUND_HAS_SUBFUND',
            'FUND_HAS_SHARE_CLASS',
            'SUBFUND_HAS_SHARE_CLASS'
        )
    ),
    effective_from date,
    effective_from_status text not null check (
        effective_from_status in ('KNOWN','APPROXIMATE','UNKNOWN','NOT_APPLICABLE')
    ),
    effective_to date,
    effective_to_status text not null default 'NOT_APPLICABLE' check (
        effective_to_status in ('KNOWN','APPROXIMATE','UNKNOWN','NOT_APPLICABLE')
    ),
    recorded_at timestamptz not null default now(),
    superseded_at timestamptz,
    is_current boolean not null default true,
    validation_status text not null default 'PENDING' check (
        validation_status in ('PENDING','VALIDATED','REJECTED','SUPERSEDED')
    ),
    source_artifact_id uuid references source.raw_artifact(raw_artifact_id),
    source_locator jsonb,
    source_note text,
    foreign key (parent_entity_id, parent_entity_type)
        references fund.entity(entity_id, entity_type),
    foreign key (child_entity_id, child_entity_type)
        references fund.entity(entity_id, entity_type),
    check (parent_entity_id <> child_entity_id),
    check (
        (relationship_type = 'FUND_HAS_SUBFUND'
            and parent_entity_type = 'FUND'
            and child_entity_type = 'SUBFUND')
        or
        (relationship_type = 'FUND_HAS_SHARE_CLASS'
            and parent_entity_type = 'FUND'
            and child_entity_type = 'SHARE_CLASS')
        or
        (relationship_type = 'SUBFUND_HAS_SHARE_CLASS'
            and parent_entity_type = 'SUBFUND'
            and child_entity_type = 'SHARE_CLASS')
    ),
    check (
        (effective_from_status in ('KNOWN','APPROXIMATE') and effective_from is not null)
        or
        (effective_from_status in ('UNKNOWN','NOT_APPLICABLE') and effective_from is null)
    ),
    check (
        (effective_to_status in ('KNOWN','APPROXIMATE') and effective_to is not null)
        or
        (effective_to_status in ('UNKNOWN','NOT_APPLICABLE') and effective_to is null)
    ),
    check (effective_to is null or effective_from is null or effective_to >= effective_from),
    check (
        (is_current and superseded_at is null)
        or
        (not is_current and superseded_at is not null)
    )
);

create unique index if not exists ux_structure_current_parent
    on fund.structure_relationship (child_entity_id)
    where is_current
      and effective_to is null;

create unique index if not exists ux_structure_current_edge
    on fund.structure_relationship (
        parent_entity_id,
        child_entity_id,
        relationship_type,
        coalesce(effective_from, '-infinity'::date),
        effective_from_status
    )
    where is_current;

create or replace view fund.current_entity_state as
select *
from fund.entity_state
where is_current
  and superseded_at is null
  and validation_status = 'VALIDATED';

create or replace view fund.current_fund_profile as
select *
from fund.fund_profile
where is_current
  and superseded_at is null
  and validation_status = 'VALIDATED';

create or replace view fund.current_subfund_profile as
select *
from fund.subfund_profile
where is_current
  and superseded_at is null
  and validation_status = 'VALIDATED';

create or replace view fund.current_share_class_profile as
select *
from fund.share_class_profile
where is_current
  and superseded_at is null
  and validation_status = 'VALIDATED';

create or replace view fund.current_legal_name as
select *
from fund.entity_name
where is_current
  and superseded_at is null
  and effective_to is null
  and name_role = 'LEGAL_NAME'
  and validation_status = 'VALIDATED';

create or replace function fund.enforce_structure_relationship()
returns trigger
language plpgsql
as $$
declare
    v_structure_type text;
begin
    if not new.is_current or new.effective_to is not null then
        return new;
    end if;

    if new.relationship_type = 'FUND_HAS_SUBFUND' then
        select structure_type
        into v_structure_type
        from fund.current_fund_profile
        where fund_id = new.parent_entity_id;

        if v_structure_type is distinct from 'UMBRELLA' then
            raise exception
                'FUND_HAS_SUBFUND requires a current validated UMBRELLA fund profile for %',
                new.parent_entity_id;
        end if;

        if not exists (
            select 1
            from fund.current_subfund_profile
            where subfund_id = new.child_entity_id
        ) then
            raise exception
                'FUND_HAS_SUBFUND requires a current validated subfund profile for %',
                new.child_entity_id;
        end if;

    elsif new.relationship_type = 'FUND_HAS_SHARE_CLASS' then
        select structure_type
        into v_structure_type
        from fund.current_fund_profile
        where fund_id = new.parent_entity_id;

        if v_structure_type is distinct from 'STANDALONE' then
            raise exception
                'FUND_HAS_SHARE_CLASS requires a current validated STANDALONE fund profile for %',
                new.parent_entity_id;
        end if;

        if not exists (
            select 1
            from fund.current_share_class_profile
            where share_class_id = new.child_entity_id
        ) then
            raise exception
                'FUND_HAS_SHARE_CLASS requires a current validated share-class profile for %',
                new.child_entity_id;
        end if;

    elsif new.relationship_type = 'SUBFUND_HAS_SHARE_CLASS' then
        if not exists (
            select 1
            from fund.current_subfund_profile
            where subfund_id = new.parent_entity_id
        ) then
            raise exception
                'SUBFUND_HAS_SHARE_CLASS requires a current validated subfund profile for %',
                new.parent_entity_id;
        end if;

        if not exists (
            select 1
            from fund.current_share_class_profile
            where share_class_id = new.child_entity_id
        ) then
            raise exception
                'SUBFUND_HAS_SHARE_CLASS requires a current validated share-class profile for %',
                new.child_entity_id;
        end if;

        if not exists (
            select 1
            from fund.structure_relationship umbrella_relation
            join fund.current_fund_profile umbrella_profile
              on umbrella_profile.fund_id = umbrella_relation.parent_entity_id
             and umbrella_profile.structure_type = 'UMBRELLA'
            where umbrella_relation.relationship_type = 'FUND_HAS_SUBFUND'
              and umbrella_relation.child_entity_id = new.parent_entity_id
              and umbrella_relation.is_current
              and umbrella_relation.effective_to is null
              and umbrella_relation.validation_status = 'VALIDATED'
        ) then
            raise exception
                'SUBFUND_HAS_SHARE_CLASS requires the subfund to belong to a current validated umbrella fund';
        end if;
    end if;

    return new;
end
$$;

do $$
begin
    if not exists (
        select 1
        from pg_trigger
        where tgrelid = 'fund.structure_relationship'::regclass
          and tgname = 'trg_enforce_structure_relationship'
          and not tgisinternal
    ) then
        create trigger trg_enforce_structure_relationship
        before insert or update
        on fund.structure_relationship
        for each row
        execute function fund.enforce_structure_relationship();
    end if;
end
$$;

create or replace view fund.current_share_class_path as
with current_relationship as (
    select *
    from fund.structure_relationship
    where is_current
      and superseded_at is null
      and effective_to is null
      and validation_status = 'VALIDATED'
)
select
    share_profile.share_class_id,
    case
        when direct_relationship.relationship_type = 'SUBFUND_HAS_SHARE_CLASS'
        then direct_relationship.parent_entity_id
        else null
    end as subfund_id,
    case
        when direct_relationship.relationship_type = 'FUND_HAS_SHARE_CLASS'
        then direct_relationship.parent_entity_id
        else umbrella_relationship.parent_entity_id
    end as fund_id,
    direct_relationship.structure_relationship_id as direct_relationship_id,
    umbrella_relationship.structure_relationship_id as umbrella_relationship_id
from fund.current_share_class_profile share_profile
join current_relationship direct_relationship
  on direct_relationship.child_entity_id = share_profile.share_class_id
 and direct_relationship.relationship_type in (
     'FUND_HAS_SHARE_CLASS',
     'SUBFUND_HAS_SHARE_CLASS'
 )
left join current_relationship umbrella_relationship
  on direct_relationship.relationship_type = 'SUBFUND_HAS_SHARE_CLASS'
 and umbrella_relationship.relationship_type = 'FUND_HAS_SUBFUND'
 and umbrella_relationship.child_entity_id = direct_relationship.parent_entity_id;

create or replace view fund.structure_quality_issue as
select
    subfund_profile.subfund_id as entity_id,
    'SUBFUND'::text as entity_type,
    'MISSING_CURRENT_FUND_PARENT'::text as issue_code
from fund.current_subfund_profile subfund_profile
where not exists (
    select 1
    from fund.structure_relationship relationship
    where relationship.child_entity_id = subfund_profile.subfund_id
      and relationship.relationship_type = 'FUND_HAS_SUBFUND'
      and relationship.is_current
      and relationship.effective_to is null
      and relationship.validation_status = 'VALIDATED'
)
union all
select
    share_profile.share_class_id,
    'SHARE_CLASS'::text,
    'MISSING_CURRENT_FUND_OR_SUBFUND_PARENT'::text
from fund.current_share_class_profile share_profile
where not exists (
    select 1
    from fund.structure_relationship relationship
    where relationship.child_entity_id = share_profile.share_class_id
      and relationship.relationship_type in (
          'FUND_HAS_SHARE_CLASS',
          'SUBFUND_HAS_SHARE_CLASS'
      )
      and relationship.is_current
      and relationship.effective_to is null
      and relationship.validation_status = 'VALIDATED'
);

create index if not exists idx_entity_state_country
    on fund.entity_state (domicile_country_id, lifecycle_status);

create index if not exists idx_entity_name_lookup
    on fund.entity_name (entity_id, name_role, normalized_name);

create index if not exists idx_entity_identifier_lookup
    on fund.entity_identifier (entity_id, identifier_scheme, normalized_value);

create index if not exists idx_structure_parent
    on fund.structure_relationship (parent_entity_id, relationship_type);

create index if not exists idx_event_effective_date
    on fund.entity_event (event_type, effective_date);

comment on schema fund is
'Canonical investment-fund identity and structure domain. No fund history is loaded merely by creating this schema.';

comment on table fund.entity is
'Stable canonical identity supertype for FUND, SUBFUND and SHARE_CLASS. Names and external identifiers are versioned separately.';

comment on table fund.structure_relationship is
'Versioned structural edges. Standalone funds link directly to share classes; umbrella funds link to subfunds, which link to share classes. No synthetic subfund is required.';

comment on view fund.current_share_class_path is
'Current canonical path from each share class to an optional subfund and mandatory fund, derived from validated structural relationships.';
