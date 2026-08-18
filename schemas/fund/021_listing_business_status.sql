-- Migration 021: preserve Listing business status separately from bitemporal version state.
-- Forward-only and additive. Absence of source status remains NULL; do not default to ACTIVE.

alter table fund.listing
    add column if not exists listing_status text;

alter table fund.listing
    drop constraint if exists fund_listing_listing_status_check;

alter table fund.listing
    add constraint fund_listing_listing_status_check
    check (
        listing_status is null
        or listing_status in ('PLANNED', 'ACTIVE', 'SUSPENDED', 'DELISTED')
    );

comment on column fund.listing.listing_status is
    'Business status of the listing. Separate from is_current, which represents the current bitemporal assertion version. NULL means status not asserted by the source.';
