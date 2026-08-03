-- APPLY AND ASSERT THE BEAC FX PRODUCTION SEED BEFORE LIVE VALIDATION.

\ir ../../schemas/reference/009_beac_fx_collection_seed.sql

do $$
declare
    organization_count integer;
    role_count integer;
    endpoint_count integer;
    mapping_count integer;
    provider_series_count integer;
    specification_count integer;
begin
    select count(*)
    into organization_count
    from ref.organization
    where organization_id = 'af6d3e9d-95fd-50ca-8880-6f58f564bdd4'
      and organization_code = 'BEAC'
      and primary_zone_code = 'CEMAC'
      and validation_status = 'VALIDATED';

    select count(*)
    into role_count
    from ref.organization_scope_role
    where organization_id = 'af6d3e9d-95fd-50ca-8880-6f58f564bdd4'
      and scope_entity_code = 'CEMAC'
      and role_code in ('CENTRAL_BANK','FX_REFERENCE_RATE_PROVIDER')
      and validation_status = 'VALIDATED';

    select count(*)
    into endpoint_count
    from source.current_endpoint
    where endpoint_id = 'cb5518cd-236c-5ded-8941-56f09eb74bdc'
      and endpoint_code = 'BEAC_FX_DAILY'
      and scope_type = 'ZONE'
      and scope_code = 'CEMAC'
      and canonical_url = 'https://www.beac.int/index.php/accueil'
      and expected_frequency = 'DAILY';

    select count(*)
    into mapping_count
    from source.indicator_source_mapping
    where mapping_code in ('CEMAC_D09_FX_EUR','CEMAC_D09_FX_USD')
      and endpoint_id = 'cb5518cd-236c-5ded-8941-56f09eb74bdc'
      and collection_status = 'URL_LINKED'
      and validation_status = 'VALIDATED';

    select count(*)
    into provider_series_count
    from source.provider_series
    where provider_series_code in (
        'PS_CEMAC_BEAC_FX_SNAPSHOT',
        'PS_CEMAC_FX_XAF_EUR',
        'PS_CEMAC_FX_XAF_USD'
    )
      and endpoint_id = 'cb5518cd-236c-5ded-8941-56f09eb74bdc'
      and history_status = 'COLLECTOR_IMPLEMENTED'
      and validation_status = 'PENDING';

    select count(*)
    into specification_count
    from source.collection_specification
    where collection_specification_id = '128bb2f4-ff2d-5633-8e13-b5e1cb72c88d'
      and collection_specification_code = 'CS_CEMAC_BEAC_FX_SNAPSHOT'
      and parser_version = '0.1.0'
      and raw_artifact_required
      and hash_required
      and implementation_status = 'COLLECTOR_IMPLEMENTED'
      and validation_status = 'PENDING';

    if organization_count <> 1 then
        raise exception 'canonical BEAC organization seed is missing or invalid';
    end if;
    if role_count <> 2 then
        raise exception 'expected two validated BEAC CEMAC role assignments, got %', role_count;
    end if;
    if endpoint_count <> 1 then
        raise exception 'validated BEAC FX endpoint seed is missing or invalid';
    end if;
    if mapping_count <> 2 then
        raise exception 'expected two BEAC FX URL-linked mappings, got %', mapping_count;
    end if;
    if provider_series_count <> 3 then
        raise exception 'expected three pending BEAC provider series, got %', provider_series_count;
    end if;
    if specification_count <> 1 then
        raise exception 'pending BEAC collection specification is missing or invalid';
    end if;
end
$$;
