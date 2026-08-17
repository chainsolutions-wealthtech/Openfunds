-- 019 SHARE CLASS LISTING CORE
-- PostgreSQL
-- Forward-only extension of the canonical Fund/SubFund/ShareClass domain.
-- A listing is a market occurrence of a SHARE_CLASS and is deliberately
-- separated from fund.entity_identifier, which stores entity-level identity.

create table if not exists fund.listing (
    listing_id uuid primary key,
    share_class_id uuid not null,
    entity_type text not null default 'SHARE_CLASS' check (entity_type = 'SHARE_CLASS'),
    exchange_organization_id uuid references ref.organization(organization_id),
    venue_mic text,
    trading_currency_id uuid references ref.currency(currency_id),
    is_primary boolean not null default false,
    valid_from date,
    valid_from_status text not null default 'UNKNOWN' check (
        valid_from_status in ('KNOWN','APPROXIMATE','UNKNOWN','NOT_APPLICABLE')
    ),
    valid_to date,
    valid_to_status text not null default 'NOT_APPLICABLE' check (
        valid_to_status in ('KNOWN','APPROXIMATE','UNKNOWN','NOT_APPLICABLE')
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
    check (exchange_organization_id is not null or venue_mic is not null),
    check (venue_mic is null or venue_mic ~ '^[A-Z0-9]{4}$'),
    check (
        (valid_from_status in ('KNOWN','APPROXIMATE') and valid_from is not null)
        or
        (valid_from_status in ('UNKNOWN','NOT_APPLICABLE') and valid_from is null)
    ),
    check (
        (valid_to_status in ('KNOWN','APPROXIMATE') and valid_to is not null)
        or
        (valid_to_status in ('UNKNOWN','NOT_APPLICABLE') and valid_to is null)
    ),
    check (valid_to is null or valid_from is null or valid_to >= valid_from),
    check (
        (is_current and superseded_at is null)
        or
        (not is_current and superseded_at is not null)
    )
);

create unique index if not exists ux_fund_listing_current_venue
    on fund.listing (share_class_id, coalesce(venue_mic, ''), coalesce(exchange_organization_id::text, ''))
    where is_current;

create table if not exists fund.listing_identifier (
    listing_identifier_id uuid primary key,
    listing_id uuid not null references fund.listing(listing_id),
    identifier_scheme text not null check (
        identifier_scheme in ('SEDOL','TICKER','LOCAL_CODE','OTHER')
    ),
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

create unique index if not exists ux_fund_listing_identifier_current_scheme_value
    on fund.listing_identifier (identifier_scheme, normalized_value)
    where is_current;

create index if not exists ix_fund_listing_share_class
    on fund.listing (share_class_id);

create index if not exists ix_fund_listing_identifier_listing
    on fund.listing_identifier (listing_id);

comment on table fund.listing is
'Market listing occurrence of a canonical SHARE_CLASS. Venue identity is not collapsed into the share-class entity.';

comment on table fund.listing_identifier is
'Identifiers attached to a specific listing, including SEDOL, rather than to the legal/economic share-class identity.';
