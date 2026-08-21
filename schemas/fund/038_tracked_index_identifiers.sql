-- 038 TRACKED INDEX IDENTIFIERS
-- PostgreSQL
-- Forward-only vendor identifier relation for ETF tracked indexes.
-- Vendor-significant identifier content/case is preserved; no destructive case normalization.

create table if not exists fund.tracked_index_identifier (
    tracked_index_identifier_id uuid primary key,
    share_class_tracked_index_id uuid not null references fund.share_class_tracked_index(share_class_tracked_index_id),
    identifier_scheme text not null check (identifier_scheme in ('BLOOMBERG','RIC')),
    identifier_value text not null,
    normalized_value text not null,
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
    check (length(btrim(identifier_value)) > 0),
    check (length(btrim(normalized_value)) > 0),
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

create unique index if not exists ux_tracked_index_identifier_current_scheme
    on fund.tracked_index_identifier (share_class_tracked_index_id, identifier_scheme)
    where is_current;

create index if not exists ix_tracked_index_identifier_value
    on fund.tracked_index_identifier (identifier_scheme, normalized_value);

comment on table fund.tracked_index_identifier is
'Versioned Bloomberg/RIC identifiers for a Share Class tracked index. Runtime proprietary-identifier use remains subject to explicit project usage review.';

comment on column fund.tracked_index_identifier.normalized_value is
'Outer-whitespace-normalized matching value only. Vendor-significant content and case, especially Reuters/RIC case, must be preserved.';
