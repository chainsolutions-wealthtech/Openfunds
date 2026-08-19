-- 024 LISTING INCEPTION PRICE
-- PostgreSQL
-- Forward-only extension of fund.listing.
-- Stores the price observed at the first listing on the relevant venue.
-- Currency / quote-unit semantics remain governed independently by migration 020.

alter table fund.listing
    add column if not exists inception_price numeric;

alter table fund.listing
    drop constraint if exists listing_inception_price_positive_check;

alter table fund.listing
    add constraint listing_inception_price_positive_check
    check (inception_price is null or inception_price > 0);

comment on column fund.listing.inception_price is
'Price at first listing on this venue. Unit/currency is carried by the listing quote-unit and trading-currency semantics; no currency or factor is inferred from the numeric value.';
