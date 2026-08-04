do $$
declare
    contract_row record;
    fk_count integer;
begin
    if to_regclass('source.endpoint') is null then
        raise exception 'canonical relation source.endpoint is missing';
    end if;

    if to_regclass('source.source_endpoint') is not null then
        raise exception 'parallel relation source.source_endpoint must not exist';
    end if;

    select * into contract_row
    from source.endpoint_model_contract_registry
    where contract_code = 'CANONICAL_ENDPOINT_MODEL';

    if contract_row.canonical_schema <> 'source'
       or contract_row.canonical_relation <> 'endpoint'
       or contract_row.normalized_view <> 'source.endpoint_contract'
       or contract_row.legacy_physical_relation is not null then
        raise exception 'canonical endpoint contract is invalid: %', contract_row;
    end if;

    if to_regclass('source.endpoint_contract') is null then
        raise exception 'normalized endpoint contract view is missing';
    end if;

    select count(*) into fk_count
    from pg_constraint c
    join pg_class child on child.oid = c.conrelid
    join pg_namespace child_ns on child_ns.oid = child.relnamespace
    join pg_class parent on parent.oid = c.confrelid
    join pg_namespace parent_ns on parent_ns.oid = parent.relnamespace
    where c.contype = 'f'
      and parent_ns.nspname = 'source'
      and parent.relname = 'endpoint'
      and child_ns.nspname = 'source'
      and child.relname in ('indicator_source_mapping','provider_series');

    if fk_count <> 2 then
        raise exception 'expected endpoint foreign keys from mapping and provider_series, got %', fk_count;
    end if;

    if exists (
        select 1 from source.endpoint_contract
        where validation_status = 'VALIDATED'
          and canonical_url is null
    ) then
        raise exception 'validated endpoint without canonical URL';
    end if;
end
$$;
