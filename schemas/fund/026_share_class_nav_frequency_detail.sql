-- 026 SHARE CLASS NAV FREQUENCY DETAIL
-- PostgreSQL
-- Forward-only extension of the versioned share-class profile.
-- Preserves free-text detail that qualifies nav_frequency without replacing it.

alter table fund.share_class_profile
    add column if not exists nav_frequency_detail text;

comment on column fund.share_class_profile.nav_frequency_detail is
'Optional source-preserving free-text detail qualifying nav_frequency, such as the precise weekday or monthly schedule. It never replaces the governed frequency code.';
