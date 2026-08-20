-- 032 SHARE CLASS ETF FLAG
-- PostgreSQL
-- Forward-only Share Class-level ETF classification.

alter table fund.share_class_profile
    add column if not exists is_etf boolean;

comment on column fund.share_class_profile.is_etf is
'Explicit Share Class-level Exchange Traded Fund flag. Nullable when not evidenced; intentionally not a Fund-level attribute.';
