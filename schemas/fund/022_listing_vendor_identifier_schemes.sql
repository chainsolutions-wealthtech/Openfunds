-- Migration 022: extend Listing identifier schemes for explicit vendor-specific listing codes.
-- Forward-only: preserve all existing schemes and rows; replace only the scheme CHECK constraint.

alter table fund.listing_identifier
    drop constraint if exists listing_identifier_identifier_scheme_check;

alter table fund.listing_identifier
    add constraint listing_identifier_identifier_scheme_check
    check (
        identifier_scheme in (
            'SEDOL',
            'TICKER',
            'LOCAL_CODE',
            'OTHER',
            'BLOOMBERG',
            'RIC'
        )
    );

comment on column fund.listing_identifier.identifier_scheme is
    'Scheme of a listing-level identifier. BLOOMBERG and RIC remain distinct from generic ticker/local-code semantics.';
