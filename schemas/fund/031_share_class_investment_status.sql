-- 031 SHARE CLASS INVESTMENT STATUS
-- PostgreSQL
-- Forward-only Share Class dealing-access semantics, distinct from lifecycle phase.

alter table fund.share_class_profile
    add column if not exists investment_status text,
    add column if not exists investment_status_description text,
    add column if not exists investment_status_date date,
    add column if not exists investment_status_date_status text not null default 'UNKNOWN';

do $$
begin
    if not exists (
        select 1 from pg_constraint
        where conname = 'ck_share_class_profile_investment_status'
          and conrelid = 'fund.share_class_profile'::regclass
    ) then
        alter table fund.share_class_profile
            add constraint ck_share_class_profile_investment_status
            check (
                investment_status is null
                or investment_status in (
                    'OPEN',
                    'SOFT_CLOSED',
                    'HARD_CLOSED',
                    'CLOSED_FOR_REDEMPTION',
                    'CLOSED_FOR_SUBSCRIPTION_AND_REDEMPTION'
                )
            );
    end if;

    if not exists (
        select 1 from pg_constraint
        where conname = 'ck_share_class_profile_investment_status_date_status'
          and conrelid = 'fund.share_class_profile'::regclass
    ) then
        alter table fund.share_class_profile
            add constraint ck_share_class_profile_investment_status_date_status
            check (investment_status_date_status in ('KNOWN','UNKNOWN'));
    end if;

    if not exists (
        select 1 from pg_constraint
        where conname = 'ck_share_class_profile_investment_status_date_coupling'
          and conrelid = 'fund.share_class_profile'::regclass
    ) then
        alter table fund.share_class_profile
            add constraint ck_share_class_profile_investment_status_date_coupling
            check (
                (investment_status_date_status = 'KNOWN' and investment_status_date is not null)
                or
                (investment_status_date_status = 'UNKNOWN' and investment_status_date is null)
            );
    end if;
end
$$;

comment on column fund.share_class_profile.investment_status is
'Current Share Class dealing-access status for investors; distinct from lifecycle_phase.';
comment on column fund.share_class_profile.investment_status_description is
'Optional source-preserving detail qualifying investment_status.';
comment on column fund.share_class_profile.investment_status_date is
'Explicit reference date of the investment status when supplied by the source.';
comment on column fund.share_class_profile.investment_status_date_status is
'Knowledge status coupled to investment_status_date; UNKNOWN prevents synthetic dates.';
