-- 025 SHARE CLASS TRADING PRICE FREQUENCY
-- PostgreSQL
-- Forward-only extension of the versioned share-class profile.
-- Trading-price publication frequency is intentionally distinct from NAV valuation frequency.

alter table fund.share_class_profile
    add column if not exists trading_price_frequency text;

comment on column fund.share_class_profile.trading_price_frequency is
'Native frequency at which a secondary-market or exchange trading price is published. Distinct from nav_frequency and nullable when not applicable or not evidenced.';
