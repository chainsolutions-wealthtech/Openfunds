-- Migration 033: Fund passive flag
-- Forward-only, additive. No historical data backfill or inference.

alter table fund.fund_profile
    add column if not exists is_passive boolean;
