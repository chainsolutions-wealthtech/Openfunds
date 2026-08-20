-- 036 BENCHMARK COMPONENT IDENTIFIERS
-- PostgreSQL
-- Forward-only extension. Vendor identifiers are kept in a dedicated, versioned
-- relation and are not collapsed into component names or generic ticker fields.

create table if not exists fund.benchmark_component_identifier (
    benchmark_component_identifier_id uuid primary key,
    benchmark_component_id uuid not null references fund.share_class_benchmark_component(benchmark_component_id),
    identifier_scheme text not null check (identifier_scheme in ('BLOOMBERG','RIC')),
    identifier_value text not null check (btrim(identifier_value) <> ''),
    normalized_value text not null check (btrim(normalized_value) <> ''),
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

create unique index if not exists ux_benchmark_component_identifier_current
    on fund.benchmark_component_identifier (benchmark_component_id, identifier_scheme, normalized_value)
    where is_current;

create index if not exists ix_benchmark_component_identifier_component
    on fund.benchmark_component_identifier (benchmark_component_id);

comment on table fund.benchmark_component_identifier is
'Versioned vendor identifiers attached to normalized benchmark components. Runtime use of proprietary identifiers remains subject to project usage/licensing governance.';
