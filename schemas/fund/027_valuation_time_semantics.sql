-- 027 VALUATION TIME SEMANTICS
-- PostgreSQL
-- Forward-only extension for Fund valuation-point time and Share Class NAV publication time.
-- The abbreviated timezone label is source-preserving only and MUST NOT be treated as an automation-safe IANA timezone.

alter table fund.fund_profile
    add column if not exists valuation_point_time time,
    add column if not exists valuation_timezone_label text,
    add column if not exists valuation_timezone_iana text;

alter table fund.share_class_profile
    add column if not exists nav_publication_time time;

comment on column fund.fund_profile.valuation_point_time is
'Fund valuation point local wall-clock time. Requires timezone context for automatic instant conversion.';

comment on column fund.fund_profile.valuation_timezone_label is
'Source-preserving timezone abbreviation or label. Ambiguous abbreviations are not automation-safe and must never be silently converted to an IANA timezone.';

comment on column fund.fund_profile.valuation_timezone_iana is
'IANA/tz-database timezone identifier when explicitly supplied by the source, e.g. Europe/Paris. Preferred for automated temporal interpretation.';

comment on column fund.share_class_profile.nav_publication_time is
'Local wall-clock time when the Share Class NAV is published. Openfunds semantics inherit the Fund valuation-point timezone; this field must not be interpreted as an absolute instant without governed timezone context.';
