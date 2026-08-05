insert into ref.entity_relationship (
    relationship_id,
    source_entity_id,
    relationship_type,
    target_entity_code,
    relationship_domain,
    relationship_role,
    valid_from,
    valid_to,
    is_primary,
    validation_status
)
values (
    '70000000-0000-0000-0000-000000000002',
    '70000000-0000-0000-0000-000000000001',
    'BELONGS_TO_CONTINENT',
    'AFRICA',
    'GEOGRAPHIC',
    'PRIMARY',
    date '2020-01-01',
    null,
    true,
    'VALIDATED'
)
on conflict (relationship_id) do nothing;
