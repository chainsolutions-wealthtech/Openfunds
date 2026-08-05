do $$
declare n integer;
begin
 select count(*) into n from source.endpoint where endpoint_code in ('BCEAO_FX_DAILY','BEAC_FX_DAILY') and validation_status='VALIDATED';
 if n<>2 then raise exception 'expected 2 validated endpoints, got %',n; end if;
 select count(*) into n from source.indicator_source_mapping where mapping_code in ('UEMOA_D09_FX_SNAPSHOT','UEMOA_D09_FX_EUR','UEMOA_D09_FX_USD','CEMAC_D09_FX_SNAPSHOT','CEMAC_D09_FX_EUR','CEMAC_D09_FX_USD') and collection_status='COLLECTION_TESTED' and validation_status='VALIDATED';
 if n<>6 then raise exception 'expected 6 validated mappings, got %',n; end if;
 select count(*) into n from source.provider_series where provider_series_code in ('PS_UEMOA_BCEAO_FX_SNAPSHOT','PS_UEMOA_FX_XOF_EUR','PS_UEMOA_FX_XOF_USD','PS_CEMAC_BEAC_FX_SNAPSHOT','PS_CEMAC_FX_XAF_EUR','PS_CEMAC_FX_XAF_USD') and history_status='COLLECTION_TESTED' and validation_status='VALIDATED';
 if n<>6 then raise exception 'expected 6 validated series, got %',n; end if;
 select count(*) into n from source.collection_specification where collection_specification_code in ('CS_UEMOA_BCEAO_FX_SNAPSHOT','CS_UEMOA_FX_XOF_EUR','CS_UEMOA_FX_XOF_USD','CS_CEMAC_BEAC_FX_SNAPSHOT','CS_CEMAC_FX_XAF_EUR','CS_CEMAC_FX_XAF_USD') and implementation_status='COLLECTION_TESTED' and validation_status='VALIDATED';
 if n<>6 then raise exception 'expected 6 validated specifications, got %',n; end if;
 if not exists(select 1 from source.endpoint where endpoint_code='BCEAO_FX_DAILY' and source_note like '%RUN_30777722357%') then raise exception 'BCEAO evidence mismatch'; end if;
 if not exists(select 1 from source.endpoint where endpoint_code='BEAC_FX_DAILY' and source_note like '%RUN_30779605759%') then raise exception 'BEAC evidence mismatch'; end if;
end $$;
