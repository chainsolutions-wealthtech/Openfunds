-- 034 FUND REPLICATION METHODOLOGY
-- PostgreSQL
-- Forward-only extension. Preserve first-level Fund methodology separately from
-- repeatable second-level detail values; never persist Openfunds pipe strings as
-- one canonical detail value.

alter table fund.fund_profile
    add column if not exists replication_methodology_first_level text;

alter table fund.fund_profile
    drop constraint if exists ck_fund_profile_replication_methodology_first_level;

alter table fund.fund_profile
    add constraint ck_fund_profile_replication_methodology_first_level
    check (
        replication_methodology_first_level is null
        or replication_methodology_first_level in ('PHYSICAL','SYNTHETICAL','HYBRID','OTHERS')
    );

create table if not exists fund.replication_methodology_detail (
    replication_methodology_detail_id uuid primary key,
    fund_id uuid not null,
    entity_type text not null default 'FUND' check (entity_type = 'FUND'),
    detail_code text not null check (
        detail_code in (
            'FULL',
            'OPTIMIZED_EQUITIES_SAMPLED_BONDS',
            'PHYSICALLY_BACKED',
            'UNFUNDED_SWAP',
            'FUNDED_SWAP',
            'COMBINATION_UNFUNDED_AND_FUNDED_SWAP',
            'FUTURES'
        )
    ),
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
    foreign key (fund_id, entity_type)
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

create unique index if not exists ux_replication_methodology_detail_current
    on fund.replication_methodology_detail (fund_id, detail_code)
    where is_current;

create index if not exists ix_replication_methodology_detail_fund
    on fund.replication_methodology_detail (fund_id);

comment on column fund.fund_profile.replication_methodology_first_level is
'Fund replication methodology first level. Openfunds values are normalized to PHYSICAL, SYNTHETICAL, HYBRID or OTHERS.';

comment on table fund.replication_methodology_detail is
'Versioned normalized second-level replication methodology details. Hybrid Openfunds pipe-separated values become multiple rows; OFST010901 requires OFST010900 source context.';
