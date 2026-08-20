-- 029 ENTITY LIFECYCLE PHASE
-- PostgreSQL
-- Forward-only extension preserving precise Openfunds Share Class lifecycle semantics
-- without replacing the broader canonical lifecycle_status.

alter table fund.entity_state
    add column if not exists lifecycle_phase text;

do $$
begin
    if not exists (
        select 1
        from pg_constraint
        where conname = 'ck_fund_entity_state_lifecycle_phase'
          and conrelid = 'fund.entity_state'::regclass
    ) then
        alter table fund.entity_state
            add constraint ck_fund_entity_state_lifecycle_phase
            check (
                lifecycle_phase is null
                or lifecycle_phase in (
                    'PROJECTED',
                    'TO_BE_LAUNCHED',
                    'OFFERING_PERIOD',
                    'ACTIVE',
                    'DORMANT',
                    'IN_LIQUIDATION',
                    'TERMINATED'
                )
            );
    end if;
end
$$;

comment on column fund.entity_state.lifecycle_phase is
'Precise lifecycle phase when explicitly evidenced. Additive to broad lifecycle_status; Openfunds Share Class values map without collapsing projected, offering-period, dormant, liquidation or terminated semantics.';
