do $$
declare
    n integer;
begin
    if (select valid_from_status from ref.entity_relationship where relationship_id='70000000-0000-0000-0000-000000000002') <> 'KNOWN' then
        raise exception 'existing dated relationship was not classified KNOWN';
    end if;

    insert into ref.entity_relationship (
        relationship_id, source_entity_id, relationship_type, target_entity_code,
        relationship_domain, relationship_role, valid_from, valid_from_status,
        valid_to, valid_to_status, is_primary, validation_status
    ) values
    ('70000000-0000-0000-0000-000000000003','70000000-0000-0000-0000-000000000001','USES_CURRENCY','TST','MONETARY','PRIMARY',null,'UNKNOWN',null,'NOT_APPLICABLE',true,'VALIDATED'),
    ('70000000-0000-0000-0000-000000000004','70000000-0000-0000-0000-000000000001','USES_MARKET_SCOPE','TEST_COUNTRY','MARKET','PRIMARY',null,'NOT_APPLICABLE',null,'NOT_APPLICABLE',true,'VALIDATED'),
    ('70000000-0000-0000-0000-000000000005','70000000-0000-0000-0000-000000000001','BELONGS_TO_REGION','TEST_REGION','GEOGRAPHIC','PRIMARY',date '2020-01-01','APPROXIMATE',null,'NOT_APPLICABLE',true,'VALIDATED')
    on conflict (relationship_id) do nothing;

    select count(*) into n from ref.current_entity_relationship
    where relationship_id='70000000-0000-0000-0000-000000000003';
    if n<>0 then raise exception 'UNKNOWN start date was incorrectly assumed current'; end if;

    select count(*) into n from ref.current_entity_relationship
    where relationship_id in ('70000000-0000-0000-0000-000000000002','70000000-0000-0000-0000-000000000004','70000000-0000-0000-0000-000000000005');
    if n<>3 then raise exception 'expected three current evidenced/not-applicable relationships, got %',n; end if;

    if exists (
        select 1 from ref.entity_relationship
        where (valid_from_status in ('UNKNOWN','NOT_APPLICABLE') and valid_from is not null)
           or (valid_from_status in ('KNOWN','APPROXIMATE') and valid_from is null)
           or (valid_to_status in ('UNKNOWN','NOT_APPLICABLE') and valid_to is not null)
           or (valid_to_status in ('KNOWN','APPROXIMATE') and valid_to is null)
    ) then raise exception 'date value/status mismatch'; end if;

    begin
        insert into ref.entity_relationship (
            relationship_id, source_entity_id, relationship_type, target_entity_code,
            relationship_domain, relationship_role, valid_from, valid_from_status,
            valid_to, valid_to_status, validation_status
        ) values (
            '70000000-0000-0000-0000-000000000006','70000000-0000-0000-0000-000000000001',
            'USES_CENTRAL_BANK','TEST_BANK','INSTITUTIONAL','PRIMARY',null,'KNOWN',null,'NOT_APPLICABLE','PENDING'
        );
        raise exception 'KNOWN without date was accepted';
    exception when check_violation then
        null;
    end;
end
$$;
