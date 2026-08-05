-- APPLY AND ASSERT THE CANONICAL BCEAO FX SEED AND FX LINEAGE MIGRATION.

\ir ../../schemas/reference/008_bceao_fx_collection_seed.sql

do $$
declare
    organization_count integer;
    role_count integer;
    endpoint_count integer;
    mapping_count integer;
    provider_series_count integer;
    specification_count integer;
begin
    -- The bitemporal migration must remove the original four-column UNIQUE
    -- constraint. The current-version partial index replaces it.
    if exists (
        select 1
        from pg_constraint constraint_row
        where constraint_row.conrelid = 'market.fx_observation'::regclass
          and constraint_row.contype = 'u'
          and (
              select array_agg(attribute_row.attname::text order by key_row.ordinality)
              from unnest(constraint_row.conkey) with ordinality as key_row(attnum, ordinality)
              join pg_attribute attribute_row
                on attribute_row.attrelid = constraint_row.conrelid
               and attribute_row.attnum = key_row.attnum
          ) = array[
              'observation_date',
              'source_currency_id',
              'target_currency_id',
              'source_id'
          ]::text[]
    ) then
        raise exception 'legacy FX uniqueness constraint was not removed';
    end if;

    select count(*)
    into organization_count
    from ref.organization
    where organization_id = '302dbf2d-4a75-5e9f-84eb-d6b5368cf4ab'
      and organization_code = 'BCEAO'
      and primary_zone_code = 'UEMOA'
      and validation_status = 'VALIDATED';

    select count(*)
    into role_count
    from ref.organization_scope_role
    where organization_id = '302dbf2d-4a75-5e9f-84eb-d6b5368cf4ab'
      and scope_entity_code = 'UEMOA'
      and role_code in ('CENTRAL_BANK','FX_REFERENCE_RATE_PROVIDER')
      and validation_status = 'VALIDATED';

    select count(*)
    into endpoint_count
    from source.current_endpoint
    where endpoint_id = '857a19f9-8c29-5dff-a84c-c0c93a540bf8'
      and endpoint_code = 'BCEAO_FX_DAILY'
      and scope_type = 'ZONE'
      and scope_code = 'UEMOA'
      and canonical_url = 'https://www.bceao.int/fr'
      and expected_frequency = 'DAILY';

    select count(*)
    into mapping_count
    from source.indicator_source_mapping
    where mapping_code in ('UEMOA_D09_FX_EUR','UEMOA_D09_FX_USD')
      and endpoint_id = '857a19f9-8c29-5dff-a84c-c0c93a540bf8'
      and collection_status = 'COLLECTION_TESTED'
      and validation_status = 'VALIDATED';

    select count(*)
    into provider_series_count
    from source.provider_series
    where provider_series_code in (
        'PS_UEMOA_BCEAO_FX_SNAPSHOT',
        'PS_UEMOA_FX_XOF_EUR',
        'PS_UEMOA_FX_XOF_USD'
    )
      and endpoint_id = '857a19f9-8c29-5dff-a84c-c0c93a540bf8'
      and history_status = 'COLLECTION_TESTED'
      and validation_status = 'VALIDATED';

    select count(*)
    into specification_count
    from source.collection_specification
    where collection_specification_id = '11464493-a058-5ff6-98ad-4f0a3ba8d82b'
      and collection_specification_code = 'CS_UEMOA_BCEAO_FX_SNAPSHOT'
      and parser_version = '0.2.0'
      and raw_artifact_required
      and hash_required
      and implementation_status = 'COLLECTION_TESTED'
      and validation_status = 'VALIDATED';

    if organization_count <> 1 then
        raise exception 'canonical BCEAO organization seed is missing or invalid';
    end if;
    if role_count <> 2 then
        raise exception 'expected two validated BCEAO UEMOA role assignments, got %', role_count;
    end if;
    if endpoint_count <> 1 then
        raise exception 'validated BCEAO FX endpoint seed is missing or invalid';
    end if;
    if mapping_count <> 2 then
        raise exception 'expected two validated BCEAO FX mappings, got %', mapping_count;
    end if;
    if provider_series_count <> 3 then
        raise exception 'expected three validated BCEAO provider series, got %', provider_series_count;
    end if;
    if specification_count <> 1 then
        raise exception 'validated BCEAO collection specification is missing or invalid';
    end if;
end
$$;
