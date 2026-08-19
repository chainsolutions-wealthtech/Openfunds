-- 028 SHARE CLASS MULTICURRENCY DEALING
-- PostgreSQL
-- Forward-only extension: preserve the single Share Class reference currency
-- while modelling additional subscription/redemption currencies separately.

alter table fund.share_class_profile
    add column if not exists is_multicurrency boolean;

create table if not exists fund.share_class_dealing_currency (
    share_class_dealing_currency_id uuid primary key,
    share_class_id uuid not null,
    entity_type text not null default 'SHARE_CLASS' check (entity_type = 'SHARE_CLASS'),
    currency_id uuid not null references ref.currency(currency_id),
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

create unique index if not exists ux_share_class_dealing_currency_current
    on fund.share_class_dealing_currency (share_class_id, currency_id)
    where is_current;

create index if not exists ix_share_class_dealing_currency_share_class
    on fund.share_class_dealing_currency (share_class_id);

comment on column fund.share_class_profile.is_multicurrency is
'Explicit source assertion that the Share Class can be subscribed/redeemed in additional currencies beyond its reference currency.';

comment on table fund.share_class_dealing_currency is
'Versioned additional dealing currencies accepted for a Share Class. The reference/NAV currency remains fund.share_class_profile.currency_id.';
