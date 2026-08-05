insert into ref.organization (
    organization_id,
    organization_code,
    organization_type,
    name_fr_canonical,
    validation_status
)
values (
    '30000000-0000-0000-0000-000000000001',
    'ORG_V003',
    'CENTRAL_BANK',
    'ORGANISATION TEST V003',
    'VALIDATED'
);

insert into source.endpoint (
    endpoint_id,
    organization_id,
    endpoint_code,
    endpoint_type,
    url,
    access_method,
    file_format,
    authentication_type,
    publication_frequency,
    expected_history_start,
    validation_status
)
values (
    '30000000-0000-0000-0000-000000000002',
    '30000000-0000-0000-0000-000000000001',
    'ENDPOINT_V003',
    'OFFICIAL_WEBSITE',
    'https://legacy.example.test/',
    'PUBLIC_WEB',
    'HTML,PDF',
    'NONE',
    'DAILY',
    '2020-01-01',
    'VALIDATED'
);
