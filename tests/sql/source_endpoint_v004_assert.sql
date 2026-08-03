do $$
declare
    endpoint_row record;
    pending_row record;
    current_count integer;
    pending_current_count integer;
begin
    select *
    into endpoint_row
    from source.endpoint
    where endpoint_code = 'ENDPOINT_V004';

    if endpoint_row.url <> 'https://relational.example.test/data' then
        raise exception 'compatibility URL was not derived: %', endpoint_row.url;
    end if;
    if endpoint_row.data_portal_url <> 'https://relational.example.test/data' then
        raise exception 'data_portal_url was not preserved: %', endpoint_row.data_portal_url;
    end if;
    if endpoint_row.file_format <> 'HTML,CSV' then
        raise exception 'legacy file_format was not derived: %', endpoint_row.file_format;
    end if;
    if endpoint_row.publication_frequency <> 'DAILY' then
        raise exception 'publication_frequency was not derived: %', endpoint_row.publication_frequency;
    end if;
    if endpoint_row.expected_history_start <> date '2018-01-01' then
        raise exception 'expected_history_start was not derived: %', endpoint_row.expected_history_start;
    end if;
    if endpoint_row.scope_type <> 'ZONE' or endpoint_row.scope_code <> 'UEMOA' then
        raise exception 'scope fields were not preserved: % / %', endpoint_row.scope_type, endpoint_row.scope_code;
    end if;

    select *
    into pending_row
    from source.endpoint
    where endpoint_code = 'ENDPOINT_PENDING_NO_URL';

    if pending_row.validation_status <> 'PENDING' then
        raise exception 'pending endpoint status changed unexpectedly';
    end if;
    if pending_row.url is not null
       or pending_row.official_url is not null
       or pending_row.data_portal_url is not null
       or pending_row.api_base_url is not null then
        raise exception 'pending endpoint received an invented URL';
    end if;

    select count(*)
    into current_count
    from source.current_endpoint
    where endpoint_code = 'ENDPOINT_V004'
      and canonical_url = 'https://relational.example.test/data';

    select count(*)
    into pending_current_count
    from source.current_endpoint
    where endpoint_code = 'ENDPOINT_PENDING_NO_URL';

    if current_count <> 1 then
        raise exception 'current_endpoint view did not expose reconciled relational row';
    end if;
    if pending_current_count <> 0 then
        raise exception 'pending endpoint must not appear in current_endpoint view';
    end if;
end
$$;
