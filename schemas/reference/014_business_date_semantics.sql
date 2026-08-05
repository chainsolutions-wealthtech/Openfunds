-- EXPLICIT BUSINESS-DATE KNOWLEDGE SEMANTICS
-- POSTGRESQL
-- Unknown dates remain NULL. No artificial business date is introduced.

create schema if not exists ref;

create table if not exists ref.business_date_status (
    status_code text primary key,
    description text not null,
    requires_date boolean not null,
    is_current_eligible boolean not null
);

insert into ref.business_date_status (status_code, description, requires_date, is_current_eligible)
values
    ('KNOWN', 'Exact business date supported by evidence', true, true),
    ('APPROXIMATE', 'Best supported approximate business date', true, true),
    ('UNKNOWN', 'Business date not known; date value must remain NULL', false, false),
    ('NOT_APPLICABLE', 'Temporal boundary does not apply', false, true)
on conflict (status_code) do update
set description = excluded.description,
    requires_date = excluded.requires_date,
    is_current_eligible = excluded.is_current_eligible;

alter table ref.entity_relationship
    alter column valid_from drop not null,
    add column if not exists valid_from_status text not null default 'UNKNOWN',
    add column if not exists valid_to_status text not null default 'NOT_APPLICABLE';

update ref.entity_relationship
set valid_from_status = case when valid_from is null then 'UNKNOWN' else 'KNOWN' end,
    valid_to_status = case when valid_to is null then 'NOT_APPLICABLE' else 'KNOWN' end
where valid_from_status not in ('KNOWN','APPROXIMATE','UNKNOWN','NOT_APPLICABLE')
   or valid_to_status not in ('KNOWN','APPROXIMATE','UNKNOWN','NOT_APPLICABLE')
   or (valid_from is not null and valid_from_status = 'UNKNOWN')
   or (valid_to is not null and valid_to_status in ('UNKNOWN','NOT_APPLICABLE'));

alter table ref.entity_relationship
    drop constraint if exists entity_relationship_valid_from_status_check,
    drop constraint if exists entity_relationship_valid_to_status_check,
    drop constraint if exists entity_relationship_valid_from_knowledge_check,
    drop constraint if exists entity_relationship_valid_to_knowledge_check,
    drop constraint if exists entity_relationship_temporal_order_check;

alter table ref.entity_relationship
    add constraint entity_relationship_valid_from_status_check
        check (valid_from_status in ('KNOWN','APPROXIMATE','UNKNOWN','NOT_APPLICABLE')),
    add constraint entity_relationship_valid_to_status_check
        check (valid_to_status in ('KNOWN','APPROXIMATE','UNKNOWN','NOT_APPLICABLE')),
    add constraint entity_relationship_valid_from_knowledge_check
        check (
            (valid_from_status in ('KNOWN','APPROXIMATE') and valid_from is not null)
            or (valid_from_status in ('UNKNOWN','NOT_APPLICABLE') and valid_from is null)
        ),
    add constraint entity_relationship_valid_to_knowledge_check
        check (
            (valid_to_status in ('KNOWN','APPROXIMATE') and valid_to is not null)
            or (valid_to_status in ('UNKNOWN','NOT_APPLICABLE') and valid_to is null)
        ),
    add constraint entity_relationship_temporal_order_check
        check (valid_to is null or valid_from is null or valid_to >= valid_from);

create unique index if not exists uq_entity_relationship_temporal_identity
    on ref.entity_relationship (
        source_entity_id,
        relationship_type,
        target_entity_code,
        coalesce(valid_from, date '-infinity'),
        valid_from_status
    );

create or replace view ref.entity_relationship_date_contract as
select
    er.relationship_id,
    er.source_entity_id,
    er.relationship_type,
    er.target_entity_code,
    er.relationship_domain,
    er.relationship_role,
    er.valid_from,
    er.valid_from_status,
    er.valid_to,
    er.valid_to_status,
    er.is_primary,
    er.source_id,
    er.validation_status,
    er.created_at,
    er.updated_at
from ref.entity_relationship er;

-- Preserve the historical output column order of current_entity_relationship.
-- New knowledge-status columns are appended to avoid a destructive view replacement.
create or replace view ref.current_entity_relationship as
select
    relationship_id,
    source_entity_id,
    relationship_type,
    target_entity_code,
    relationship_domain,
    relationship_role,
    valid_from,
    valid_to,
    is_primary,
    source_id,
    validation_status,
    valid_from_status,
    valid_to_status
from ref.entity_relationship
where (
        valid_from_status = 'NOT_APPLICABLE'
        or (valid_from_status in ('KNOWN','APPROXIMATE') and valid_from <= current_date)
    )
  and (
        valid_to_status = 'NOT_APPLICABLE'
        or (valid_to_status in ('KNOWN','APPROXIMATE') and valid_to >= current_date)
    )
  and validation_status = 'VALIDATED';

comment on table ref.business_date_status is
'Governed date-knowledge vocabulary. UNKNOWN and NOT_APPLICABLE require NULL date values.';

comment on view ref.current_entity_relationship is
'Validated relationships whose temporal boundaries are evidenced or explicitly not applicable. UNKNOWN boundaries are never assumed current.';
