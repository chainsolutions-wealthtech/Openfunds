create schema if not exists ref;

create table if not exists ref.geographic_entity (
    geographic_entity_id uuid primary key,
    entity_code text not null unique
);

insert into ref.geographic_entity (geographic_entity_id, entity_code)
values ('70000000-0000-0000-0000-000000000001', 'TEST_COUNTRY')
on conflict (entity_code) do nothing;
