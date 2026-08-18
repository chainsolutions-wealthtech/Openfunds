-- Migration 023: distinguish identifiers of the listed instrument from identifiers of its iNAV.
-- Existing listing identifiers remain LISTING by default; no historical row is deleted or rewritten destructively.

alter table fund.listing_identifier
    add column if not exists identifier_subject text not null default 'LISTING';

alter table fund.listing_identifier
    drop constraint if exists fund_listing_identifier_subject_check;

alter table fund.listing_identifier
    add constraint fund_listing_identifier_subject_check
    check (identifier_subject in ('LISTING', 'INAV'));

-- Listing-level codes such as generic tickers/local codes are contextual to a listing.
-- Include listing and subject in current-row uniqueness rather than imposing global uniqueness.
drop index if exists fund.ux_fund_listing_identifier_current_scheme_value;

create unique index if not exists ux_fund_listing_identifier_current_subject_scheme_value
    on fund.listing_identifier (
        listing_id,
        identifier_subject,
        identifier_scheme,
        normalized_value
    )
    where is_current;

comment on column fund.listing_identifier.identifier_subject is
    'Subject identified by the listing-level code: LISTING for the listed instrument occurrence, INAV for the intraday-NAV identifier associated with that listing.';
