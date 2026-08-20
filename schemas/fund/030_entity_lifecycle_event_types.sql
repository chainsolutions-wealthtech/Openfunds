-- 030 ENTITY LIFECYCLE EVENT TYPES
-- PostgreSQL
-- Forward-only semantic extension of fund.entity_event.event_type.
-- Existing event rows are not rewritten. The former inline check constraint is replaced
-- by an explicit superset so recurring lifecycle events can be represented historically.

alter table fund.entity_event
    drop constraint if exists entity_event_event_type_check;

alter table fund.entity_event
    drop constraint if exists ck_fund_entity_event_event_type;

alter table fund.entity_event
    add constraint ck_fund_entity_event_event_type
    check (
        event_type in (
            'LAUNCH',
            'RENAME',
            'MERGER',
            'ABSORPTION',
            'SPLIT',
            'MANAGEMENT_TRANSFER',
            'DOMICILE_TRANSFER',
            'LEGAL_FORM_CHANGE',
            'SUSPENSION',
            'REACTIVATION',
            'CLOSURE',
            'LIQUIDATION',
            'OTHER',
            'SUBSCRIPTION_PERIOD_START',
            'SUBSCRIPTION_PERIOD_END',
            'DORMANCY_START',
            'DORMANCY_END',
            'LIQUIDATION_START',
            'TERMINATION'
        )
    );

comment on column fund.entity_event.event_type is
'Canonical event type. Lifecycle-specific additions preserve subscription-period, dormancy, liquidation-start and termination events without rewriting prior event semantics.';
