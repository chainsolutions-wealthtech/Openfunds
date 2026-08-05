do $$
declare
    endpoint_row record;
    current_count integer;
begin
    select *
    into endpoint_row
    from source.endpoint
    where endpoint_code = 'ENDPOINT_V003';

    if endpoint_row.url <> 'https://legacy.example.test/' then
        raise exception 'legacy URL was not preserved: %', endpoint_row.url;
    end if;
    if endpoint_row.official_url <> 'https://legacy.example.test/' then
        raise exception 'official_url was not derived: %', endpoint_row.official_url;
    end if;
    if endpoint_row.file_formats <> array['HTML','PDF']::text[] then
        raise exception 'file_formats were not derived: %', endpoint_row.file_formats;
    end if;
    if endpoint_row.expected_frequency <> 'DAILY' then
        raise exception 'expected_frequency was not derived: %', endpoint_row.expected_frequency;
    end if;
    if endpoint_row.history_start <> date '2020-01-01' then
        raise exception 'history_start was not derived: %', endpoint_row.history_start;
    end if;
    if endpoint_row.auth_required then
        raise exception 'public legacy endpoint incorrectly requires authentication';
    end if;

    select count(*)
    into current_count
    from source.current_endpoint
    where endpoint_code = 'ENDPOINT_V003'
      and canonical_url = 'https://legacy.example.test/';

    if current_count <> 1 then
        raise exception 'current_endpoint view did not expose reconciled legacy row';
    end if;
end
$$;
