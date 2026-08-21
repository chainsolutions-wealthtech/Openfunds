-- 037 SHARE CLASS TRACKED INDEX
-- PostgreSQL
-- Forward-only extension for the index tracked by an ETF Share Class.
-- Index currency is deliberately not inferred from Share Class currency when
-- Openfunds leaves OFST023805 empty to indicate a local-currency index.

create table if not exists fund.share_class_tracked_index (
    share_class_tracked_index_id uuid primary key,
    share_class_id uuid not null,
    entity_type text not null default 'SHARE_CLASS' check (entity_type = 'SHARE_CLASS'),
    index_name text not null,
    index_currency_id uuid references ref.currency(currency_id),
    index_currency_mode text not null default 'UNKNOWN' check (
        index_currency_mode in ('EXPLICIT_ISO4217','LOCAL_CURRENCY','UNKNOWN')
    ),
    index_type text check (
        index_type is null or index_type in (
            'PRICE',
            'PERFORMANCE',
            'PERFORMANCE_NET_DIVIDENDS',
            'PERFORMANCE_GROSS_DIVIDENDS'
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
    foreign key (share_class_id, entity_type)
        references fund.entity(entity_id, entity_type),
    check (length(btrim(index_name)) > 0),
    check (
        (index_currency_mode = 'EXPLICIT_ISO4217' and index_currency_id is not null)
        or
        (index_currency_mode in ('LOCAL_CURRENCY','UNKNOWN') and index_currency_id is null)
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

create unique index if not exists ux_share_class_tracked_index_current
    on fund.share_class_tracked_index (share_class_id)
    where is_current;

create index if not exists ix_share_class_tracked_index_currency
    on fund.share_class_tracked_index (index_currency_id)
    where index_currency_id is not null;

comment on table fund.share_class_tracked_index is
'Versioned index tracked by an ETF Share Class. Benchmark equivalence is validated separately and is not inferred by this table.';

comment on column fund.share_class_tracked_index.index_currency_mode is
'EXPLICIT_ISO4217 when OFST023805 supplies a currency; LOCAL_CURRENCY when the source explicitly leaves the field empty for a local-currency index; UNKNOWN when no assertion is available. No Share Class currency inference is permitted.';
