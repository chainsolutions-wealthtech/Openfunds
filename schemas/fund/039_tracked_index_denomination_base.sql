-- 039 TRACKED INDEX DENOMINATION BASE
-- PostgreSQL
-- Forward-only Share Class tracked-index ratio attribute.
-- This field preserves the supplied Fund Price / Index multiplier only;
-- it does not synthesize either fund price or index level.

alter table fund.share_class_tracked_index
    add column if not exists denomination_base numeric(20,10);

alter table fund.share_class_tracked_index
    drop constraint if exists ck_share_class_tracked_index_denomination_base_positive;

alter table fund.share_class_tracked_index
    add constraint ck_share_class_tracked_index_denomination_base_positive
    check (denomination_base is null or denomination_base > 0);

comment on column fund.share_class_tracked_index.denomination_base is
'Explicit source multiplier defined as Fund Price divided by tracked Index. Positive when supplied; no fund-price or index-level value is inferred.';
