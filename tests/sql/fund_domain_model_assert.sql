-- OF-DATA-001 PostgreSQL integration and non-duplication assertions
-- Idempotent fixture covering Morocco, Tunisia and Nigeria structures.

insert into ref.geographic_entity (
    geographic_entity_id, entity_type, code, name_fr, name_en, valid_from, is_active
) values
    ('10000000-0000-0000-0000-000000000001','COUNTRY','MAR','Maroc','Morocco','2026-01-01',true),
    ('10000000-0000-0000-0000-000000000002','COUNTRY','TUN','Tunisie','Tunisia','2026-01-01',true),
    ('10000000-0000-0000-0000-000000000003','COUNTRY','NGA','Nigeria','Nigeria','2026-01-01',true)
on conflict (geographic_entity_id) do nothing;

insert into ref.currency (
    currency_id, iso_code, name_fr, name_en, decimal_places, is_active
) values
    ('20000000-0000-0000-0000-000000000001','MAD','Dirham marocain','Moroccan dirham',2,true),
    ('20000000-0000-0000-0000-000000000002','TND','Dinar tunisien','Tunisian dinar',3,true),
    ('20000000-0000-0000-0000-000000000003','NGN','Naira nigérian','Nigerian naira',2,true)
on conflict (currency_id) do nothing;

insert into ref.organization (
    organization_id, organization_code, organization_type,
    name_fr_canonical, name_en, primary_country_code,
    validation_status, source_note
) values
    ('30000000-0000-0000-0000-000000000001','TEST_MANAGER_A','MANAGEMENT_COMPANY',
     'Gestionnaire test A','Test Manager A','TUN','VALIDATED','OF-DATA-001 fixture'),
    ('30000000-0000-0000-0000-000000000002','TEST_MANAGER_B','MANAGEMENT_COMPANY',
     'Gestionnaire test B','Test Manager B','TUN','VALIDATED','OF-DATA-001 fixture')
on conflict (organization_id) do nothing;

insert into fund.entity (entity_id, entity_type, canonical_code) values
    ('40000000-0000-0000-0000-000000000001','FUND','FUND_MAR_STANDALONE_TEST'),
    ('40000000-0000-0000-0000-000000000002','SHARE_CLASS','SHARE_MAR_A_TEST'),
    ('40000000-0000-0000-0000-000000000003','FUND','FUND_TUN_UMBRELLA_TEST'),
    ('40000000-0000-0000-0000-000000000004','SUBFUND','SUBFUND_TUN_BOND_TEST'),
    ('40000000-0000-0000-0000-000000000005','SHARE_CLASS','SHARE_TUN_BOND_A_TEST'),
    ('40000000-0000-0000-0000-000000000006','FUND','FUND_NGA_STANDALONE_TEST'),
    ('40000000-0000-0000-0000-000000000007','SHARE_CLASS','SHARE_NGA_ACC_TEST'),
    ('40000000-0000-0000-0000-000000000008','SHARE_CLASS','SHARE_NGA_DIST_TEST'),
    ('40000000-0000-0000-0000-000000000009','SHARE_CLASS','SHARE_INVALID_PARENT_TEST')
on conflict (entity_id) do nothing;

insert into fund.entity_state (
    entity_state_id, entity_id, lifecycle_status, domicile_country_id,
    effective_from, effective_from_status, effective_to_status,
    validation_status, source_note
) values
    ('60000000-0000-0000-0000-000000000001','40000000-0000-0000-0000-000000000001','ACTIVE','10000000-0000-0000-0000-000000000001','2020-01-01','KNOWN','NOT_APPLICABLE','VALIDATED','Morocco standalone fixture'),
    ('60000000-0000-0000-0000-000000000002','40000000-0000-0000-0000-000000000002','ACTIVE','10000000-0000-0000-0000-000000000001','2020-01-01','KNOWN','NOT_APPLICABLE','VALIDATED','Morocco share fixture'),
    ('60000000-0000-0000-0000-000000000003','40000000-0000-0000-0000-000000000003','ACTIVE','10000000-0000-0000-0000-000000000002',null,'UNKNOWN','NOT_APPLICABLE','VALIDATED','Tunisia umbrella fixture'),
    ('60000000-0000-0000-0000-000000000004','40000000-0000-0000-0000-000000000004','ACTIVE','10000000-0000-0000-0000-000000000002',null,'UNKNOWN','NOT_APPLICABLE','VALIDATED','Tunisia subfund fixture'),
    ('60000000-0000-0000-0000-000000000005','40000000-0000-0000-0000-000000000005','ACTIVE','10000000-0000-0000-0000-000000000002',null,'UNKNOWN','NOT_APPLICABLE','VALIDATED','Tunisia share fixture'),
    ('60000000-0000-0000-0000-000000000006','40000000-0000-0000-0000-000000000006','ACTIVE','10000000-0000-0000-0000-000000000003','2018-05-01','APPROXIMATE','NOT_APPLICABLE','VALIDATED','Nigeria standalone fixture'),
    ('60000000-0000-0000-0000-000000000007','40000000-0000-0000-0000-000000000007','ACTIVE','10000000-0000-0000-0000-000000000003','2018-05-01','APPROXIMATE','NOT_APPLICABLE','VALIDATED','Nigeria accumulating class fixture'),
    ('60000000-0000-0000-0000-000000000008','40000000-0000-0000-0000-000000000008','ACTIVE','10000000-0000-0000-0000-000000000003','2021-02-01','APPROXIMATE','NOT_APPLICABLE','VALIDATED','Nigeria distributing class fixture')
on conflict (entity_state_id) do nothing;

insert into fund.fund_profile (
    fund_profile_id, fund_id, structure_type, legal_form_code,
    has_legal_personality, base_currency_id,
    effective_from, effective_from_status, effective_to_status,
    validation_status, source_note
) values
    ('70000000-0000-0000-0000-000000000001','40000000-0000-0000-0000-000000000001','STANDALONE','SICAV',true,'20000000-0000-0000-0000-000000000001','2020-01-01','KNOWN','NOT_APPLICABLE','VALIDATED','Morocco SICAV without compartment'),
    ('70000000-0000-0000-0000-000000000002','40000000-0000-0000-0000-000000000003','UMBRELLA','FCP',false,'20000000-0000-0000-0000-000000000002',null,'UNKNOWN','NOT_APPLICABLE','VALIDATED','Tunisia umbrella FCP'),
    ('70000000-0000-0000-0000-000000000003','40000000-0000-0000-0000-000000000006','STANDALONE','UNIT_TRUST',false,'20000000-0000-0000-0000-000000000003','2018-05-01','APPROXIMATE','NOT_APPLICABLE','VALIDATED','Nigeria standalone unit trust')
on conflict (fund_profile_id) do nothing;

insert into fund.subfund_profile (
    subfund_profile_id, subfund_id, compartment_type, base_currency_id,
    effective_from, effective_from_status, effective_to_status,
    validation_status, source_note
) values
    ('71000000-0000-0000-0000-000000000001','40000000-0000-0000-0000-000000000004','COMPARTMENT','20000000-0000-0000-0000-000000000002',null,'UNKNOWN','NOT_APPLICABLE','VALIDATED','Tunisia legal compartment')
on conflict (subfund_profile_id) do nothing;

insert into fund.share_class_profile (
    share_class_profile_id, share_class_id, currency_id,
    distribution_policy, hedging_policy, nav_frequency, is_representative,
    effective_from, effective_from_status, effective_to_status,
    validation_status, source_note
) values
    ('72000000-0000-0000-0000-000000000001','40000000-0000-0000-0000-000000000002','20000000-0000-0000-0000-000000000001','ACCUMULATING','UNHEDGED','DAILY',true,'2020-01-01','KNOWN','NOT_APPLICABLE','VALIDATED','Morocco class A'),
    ('72000000-0000-0000-0000-000000000002','40000000-0000-0000-0000-000000000005','20000000-0000-0000-0000-000000000002','ACCUMULATING','UNHEDGED','DAILY',true,null,'UNKNOWN','NOT_APPLICABLE','VALIDATED','Tunisia subfund class'),
    ('72000000-0000-0000-0000-000000000003','40000000-0000-0000-0000-000000000007','20000000-0000-0000-0000-000000000003','ACCUMULATING','UNHEDGED','WEEKLY',true,'2018-05-01','APPROXIMATE','NOT_APPLICABLE','VALIDATED','Nigeria accumulating class'),
    ('72000000-0000-0000-0000-000000000004','40000000-0000-0000-0000-000000000008','20000000-0000-0000-0000-000000000003','DISTRIBUTING','UNHEDGED','WEEKLY',false,'2021-02-01','APPROXIMATE','NOT_APPLICABLE','VALIDATED','Nigeria distributing class')
on conflict (share_class_profile_id) do nothing;

insert into fund.structure_relationship (
    structure_relationship_id, parent_entity_id, parent_entity_type,
    child_entity_id, child_entity_type, relationship_type,
    effective_from, effective_from_status, effective_to_status,
    validation_status, source_note
) values
    ('80000000-0000-0000-0000-000000000001','40000000-0000-0000-0000-000000000001','FUND','40000000-0000-0000-0000-000000000002','SHARE_CLASS','FUND_HAS_SHARE_CLASS','2020-01-01','KNOWN','NOT_APPLICABLE','VALIDATED','Standalone direct path'),
    ('80000000-0000-0000-0000-000000000002','40000000-0000-0000-0000-000000000003','FUND','40000000-0000-0000-0000-000000000004','SUBFUND','FUND_HAS_SUBFUND',null,'UNKNOWN','NOT_APPLICABLE','VALIDATED','Umbrella to compartment'),
    ('80000000-0000-0000-0000-000000000003','40000000-0000-0000-0000-000000000004','SUBFUND','40000000-0000-0000-0000-000000000005','SHARE_CLASS','SUBFUND_HAS_SHARE_CLASS',null,'UNKNOWN','NOT_APPLICABLE','VALIDATED','Compartment to class'),
    ('80000000-0000-0000-0000-000000000004','40000000-0000-0000-0000-000000000006','FUND','40000000-0000-0000-0000-000000000007','SHARE_CLASS','FUND_HAS_SHARE_CLASS','2018-05-01','APPROXIMATE','NOT_APPLICABLE','VALIDATED','Nigeria accumulating class path'),
    ('80000000-0000-0000-0000-000000000005','40000000-0000-0000-0000-000000000006','FUND','40000000-0000-0000-0000-000000000008','SHARE_CLASS','FUND_HAS_SHARE_CLASS','2021-02-01','APPROXIMATE','NOT_APPLICABLE','VALIDATED','Nigeria distributing class path')
on conflict (structure_relationship_id) do nothing;

insert into fund.entity_event (
    event_id, event_type, effective_date, effective_date_status,
    publication_date, event_summary, validation_status, source_note
) values
    ('50000000-0000-0000-0000-000000000001','MERGER','2024-06-30','KNOWN','2024-05-31','Fixture merger with predecessor and successor','VALIDATED','OF-DATA-001 merger fixture'),
    ('50000000-0000-0000-0000-000000000002','MANAGEMENT_TRANSFER',null,'UNKNOWN','2025-01-15','Fixture transfer between management companies','VALIDATED','OF-DATA-001 transfer fixture'),
    ('50000000-0000-0000-0000-000000000003','RENAME','2023-01-01','APPROXIMATE','2023-02-01','Fixture historical rename','VALIDATED','OF-DATA-001 rename fixture')
on conflict (event_id) do nothing;

insert into fund.event_participant (
    event_participant_id, event_id, entity_id, organization_id,
    participant_role, note
) values
    ('b0000000-0000-0000-0000-000000000001','50000000-0000-0000-0000-000000000001','40000000-0000-0000-0000-000000000001',null,'PREDECESSOR','Predecessor role fixture'),
    ('b0000000-0000-0000-0000-000000000002','50000000-0000-0000-0000-000000000001','40000000-0000-0000-0000-000000000006',null,'SUCCESSOR','Successor role fixture'),
    ('b0000000-0000-0000-0000-000000000003','50000000-0000-0000-0000-000000000002','40000000-0000-0000-0000-000000000004',null,'TRANSFERRED_ENTITY','Transferred subfund fixture'),
    ('b0000000-0000-0000-0000-000000000004','50000000-0000-0000-0000-000000000002',null,'30000000-0000-0000-0000-000000000001','FROM_MANAGER','Former manager fixture'),
    ('b0000000-0000-0000-0000-000000000005','50000000-0000-0000-0000-000000000002',null,'30000000-0000-0000-0000-000000000002','TO_MANAGER','New manager fixture'),
    ('b0000000-0000-0000-0000-000000000006','50000000-0000-0000-0000-000000000003','40000000-0000-0000-0000-000000000004',null,'SUBJECT','Renamed subfund fixture')
on conflict (event_participant_id) do nothing;

insert into fund.entity_name (
    entity_name_id, entity_id, event_id, name_role, name_text,
    normalized_name, language_code, effective_from, effective_from_status,
    effective_to, effective_to_status, is_current, validation_status, source_note
) values
    ('90000000-0000-0000-0000-000000000001','40000000-0000-0000-0000-000000000001',null,'LEGAL_NAME','SICAV Maroc Test','SICAV MAROC TEST','fr','2020-01-01','KNOWN',null,'NOT_APPLICABLE',true,'VALIDATED','Current legal name'),
    ('90000000-0000-0000-0000-000000000002','40000000-0000-0000-0000-000000000003',null,'LEGAL_NAME','FCP Tunisien Ombrelle Test','FCP TUNISIEN OMBRELLE TEST','fr',null,'UNKNOWN',null,'NOT_APPLICABLE',true,'VALIDATED','Current umbrella name'),
    ('90000000-0000-0000-0000-000000000003','40000000-0000-0000-0000-000000000004',null,'LEGAL_NAME','Compartiment Obligataire Tunisie Test','COMPARTIMENT OBLIGATAIRE TUNISIE TEST','fr','2023-01-01','APPROXIMATE',null,'NOT_APPLICABLE',true,'VALIDATED','Current subfund name'),
    ('90000000-0000-0000-0000-000000000004','40000000-0000-0000-0000-000000000004','50000000-0000-0000-0000-000000000003','FORMER_NAME','Ancien Compartiment Taux Test','ANCIEN COMPARTIMENT TAUX TEST','fr',null,'UNKNOWN','2022-12-31','APPROXIMATE',true,'VALIDATED','Former name preserved separately'),
    ('90000000-0000-0000-0000-000000000005','40000000-0000-0000-0000-000000000004',null,'ALIAS','Tunisia Bond Sleeve','TUNISIA BOND SLEEVE','en',null,'UNKNOWN',null,'NOT_APPLICABLE',true,'VALIDATED','Alias preserved separately'),
    ('90000000-0000-0000-0000-000000000006','40000000-0000-0000-0000-000000000006',null,'LEGAL_NAME','Nigeria Unit Trust Test','NIGERIA UNIT TRUST TEST','en','2018-05-01','APPROXIMATE',null,'NOT_APPLICABLE',true,'VALIDATED','Current Nigeria legal name')
on conflict (entity_name_id) do nothing;

insert into fund.entity_identifier (
    entity_identifier_id, entity_id, identifier_scheme,
    identifier_value, normalized_value,
    effective_from, effective_from_status, effective_to_status,
    validation_status, source_note
) values
    ('a0000000-0000-0000-0000-000000000001','40000000-0000-0000-0000-000000000002','ISIN','MA0000000001','MA0000000001','2020-01-01','KNOWN','NOT_APPLICABLE','VALIDATED','Morocco test ISIN'),
    ('a0000000-0000-0000-0000-000000000002','40000000-0000-0000-0000-000000000005','REGULATOR_ID','CMF-TUN-TEST-001','CMF-TUN-TEST-001',null,'UNKNOWN','NOT_APPLICABLE','VALIDATED','Tunisia regulator identifier'),
    ('a0000000-0000-0000-0000-000000000003','40000000-0000-0000-0000-000000000007','LOCAL_CODE','SEC-NGA-TEST-ACC','SEC-NGA-TEST-ACC',null,'UNKNOWN','NOT_APPLICABLE','VALIDATED','Nigeria accumulating class code'),
    ('a0000000-0000-0000-0000-000000000004','40000000-0000-0000-0000-000000000008','LOCAL_CODE','SEC-NGA-TEST-DIST','SEC-NGA-TEST-DIST',null,'UNKNOWN','NOT_APPLICABLE','VALIDATED','Nigeria distributing class code')
on conflict (entity_identifier_id) do nothing;

do $$
begin
    if to_regclass('fund.entity') is null
       or to_regclass('fund.structure_relationship') is null
       or to_regclass('fund.current_share_class_path') is null then
        raise exception 'canonical fund runtime objects are missing';
    end if;

    if to_regclass('fund.fund') is not null
       or to_regclass('fund.share_class') is not null then
        raise exception 'legacy draft fund tables were activated';
    end if;

    if not exists (
        select 1 from fund.current_share_class_path
        where share_class_id = '40000000-0000-0000-0000-000000000002'
          and fund_id = '40000000-0000-0000-0000-000000000001'
          and subfund_id is null
    ) then
        raise exception 'standalone fund path is incorrect';
    end if;

    if not exists (
        select 1 from fund.current_share_class_path
        where share_class_id = '40000000-0000-0000-0000-000000000005'
          and fund_id = '40000000-0000-0000-0000-000000000003'
          and subfund_id = '40000000-0000-0000-0000-000000000004'
    ) then
        raise exception 'umbrella/subfund/share-class path is incorrect';
    end if;

    if (
        select count(*) from fund.current_share_class_path
        where fund_id = '40000000-0000-0000-0000-000000000006'
    ) <> 2 then
        raise exception 'Nigeria standalone fund must expose two direct share classes';
    end if;

    if exists (
        select 1 from fund.structure_quality_issue
        where entity_id in (
            '40000000-0000-0000-0000-000000000004',
            '40000000-0000-0000-0000-000000000002',
            '40000000-0000-0000-0000-000000000005',
            '40000000-0000-0000-0000-000000000007',
            '40000000-0000-0000-0000-000000000008'
        )
    ) then
        raise exception 'validated fixture contains a structural quality issue';
    end if;

    if (
        select count(*) from fund.entity_name
        where entity_id = '40000000-0000-0000-0000-000000000004'
          and name_role in ('LEGAL_NAME','FORMER_NAME','ALIAS')
    ) <> 3 then
        raise exception 'identity, former name and alias are not separated';
    end if;

    if (
        select count(*) from fund.event_participant
        where event_id = '50000000-0000-0000-0000-000000000002'
    ) <> 3 then
        raise exception 'management transfer participants are incomplete';
    end if;
end
$$;

do $$
begin
    begin
        insert into fund.entity_identifier (
            entity_identifier_id, entity_id, identifier_scheme,
            identifier_value, normalized_value,
            effective_from, effective_from_status, effective_to_status,
            validation_status, source_note
        ) values (
            'afffffff-0000-0000-0000-000000000001',
            '40000000-0000-0000-0000-000000000007',
            'ISIN','MA0000000001','MA0000000001',
            null,'UNKNOWN','NOT_APPLICABLE','VALIDATED','must fail'
        );
        raise exception 'duplicate current ISIN was accepted';
    exception
        when unique_violation then null;
    end;
end
$$;

do $$
begin
    begin
        insert into fund.structure_relationship (
            structure_relationship_id, parent_entity_id, parent_entity_type,
            child_entity_id, child_entity_type, relationship_type,
            effective_from, effective_from_status, effective_to_status,
            validation_status, source_note
        ) values (
            '8fffffff-0000-0000-0000-000000000001',
            '40000000-0000-0000-0000-000000000006','FUND',
            '40000000-0000-0000-0000-000000000002','SHARE_CLASS',
            'FUND_HAS_SHARE_CLASS',null,'UNKNOWN','NOT_APPLICABLE',
            'VALIDATED','must fail second parent'
        );
        raise exception 'a share class received two current structural parents';
    exception
        when unique_violation then null;
    end;
end
$$;

do $$
begin
    begin
        insert into fund.structure_relationship (
            structure_relationship_id, parent_entity_id, parent_entity_type,
            child_entity_id, child_entity_type, relationship_type,
            effective_from, effective_from_status, effective_to_status,
            validation_status, source_note
        ) values (
            '8fffffff-0000-0000-0000-000000000002',
            '40000000-0000-0000-0000-000000000003','FUND',
            '40000000-0000-0000-0000-000000000009','SHARE_CLASS',
            'FUND_HAS_SHARE_CLASS',null,'UNKNOWN','NOT_APPLICABLE',
            'VALIDATED','must fail direct class under umbrella'
        );
        raise exception 'an umbrella fund accepted a direct share-class edge';
    exception
        when raise_exception then
            if position('STANDALONE' in sqlerrm) = 0 then
                raise;
            end if;
    end;
end
$$;
