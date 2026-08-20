-- 035 SHARE CLASS BENCHMARK COMPONENTS
-- PostgreSQL
-- Forward-only extension. Normalizes composite benchmark source strings into ordered,
-- versioned components. Does not store Openfunds pipe strings as canonical values.

create table if not exists fund.share_class_benchmark_component (
    benchmark_component_id uuid primary key,
    share_class_id uuid not null,
    entity_type text not null default 'SHARE_CLASS' check (entity_type = 'SHARE_CLASS'),
    component_order integer not null check (component_order > 0),
    component_name text not null check (btrim(component_name) <> ''),
    component_weight numeric(20,10) check (component_weight is null or component_weight >= 0),
    effective_from date,
    effective_from_status text not null default 'UNKNOWN' check (
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

create unique index if not exists ux_share_class_benchmark_component_current_order
    on fund.share_class_benchmark_component (share_class_id, component_order)
    where is_current;

create index if not exists ix_share_class_benchmark_component_share_class
    on fund.share_class_benchmark_component (share_class_id);

comment on table fund.share_class_benchmark_component is
'Ordered, versioned benchmark components for a Share Class. Openfunds composite benchmark pipe syntax is normalized into one row per component; optional bracketed source weights become component_weight.';
