-- REFERENCE ROWS REQUIRED BY THE BCEAO FX LOADER INTEGRATION TEST.

-- The bitemporal migration must remove the original four-column UNIQUE
-- constraint. The current-version partial index replaces it.
do $$
begin
    if exists (
        select 1
        from pg_constraint constraint_row
        where constraint_row.conrelid = 'market.fx_observation'::regclass
          and constraint_row.contype = 'u'
          and (
              select array_agg(attribute_row.attname order by key_row.ordinality)
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
end
$$;

insert into source.provider_series (
    provider_series_id,
    provider_series_code,
    mapping_code,
    organization_id,
    endpoint_id,
    canonical_indicator_code,
    native_series_code,
    native_series_name,
    native_series_url,
    native_frequency,
    native_unit,
    native_currency_code,
    revision_policy,
    history_status,
    validation_status
)
values
    (
        '10000000-0000-0000-0000-000000000001',
        'PS_UEMOA_BCEAO_FX_SNAPSHOT',
        'UEMOA_D09_FX_SNAPSHOT',
        '00000000-0000-0000-0000-000000000010',
        '00000000-0000-0000-0000-000000000020',
        'FX_XOF_EUR_USD_RAW',
        'BCEAO_FX_DAILY_TABLE',
        'COURS DES DEVISES BCEAO',
        'https://www.bceao.int/fr',
        'DAILY',
        'FX_RATE',
        'XOF',
        'KEEP_ALL_REVISIONS',
        'COLLECTION_TESTED',
        'VALIDATED'
    ),
    (
        '10000000-0000-0000-0000-000000000002',
        'PS_UEMOA_FX_XOF_EUR',
        'UEMOA_D09_FX_EUR',
        '00000000-0000-0000-0000-000000000010',
        '00000000-0000-0000-0000-000000000020',
        'FX_XOF_EUR',
        null,
        'XOF VERS EUR CALCULE DEPUIS LE MIDPOINT BCEAO',
        null,
        'DAILY',
        'FX_RATE',
        'XOF',
        'KEEP_ALL_REVISIONS',
        'COLLECTION_TESTED',
        'VALIDATED'
    ),
    (
        '10000000-0000-0000-0000-000000000003',
        'PS_UEMOA_FX_XOF_USD',
        'UEMOA_D09_FX_USD',
        '00000000-0000-0000-0000-000000000010',
        '00000000-0000-0000-0000-000000000020',
        'FX_XOF_USD',
        null,
        'XOF VERS USD CALCULE DEPUIS LE MIDPOINT BCEAO',
        null,
        'DAILY',
        'FX_RATE',
        'XOF',
        'KEEP_ALL_REVISIONS',
        'COLLECTION_TESTED',
        'VALIDATED'
    )
on conflict (provider_series_code) do nothing;

insert into source.collection_specification (
    collection_specification_id,
    collection_specification_code,
    provider_series_id,
    collection_method,
    request_method,
    discovery_rule,
    table_or_selector,
    date_extraction_rule,
    value_extraction_rule,
    number_parsing_rule,
    currency_rule,
    frequency_check,
    deduplication_key,
    revision_handling,
    raw_artifact_required,
    hash_required,
    parser_version,
    retry_policy,
    quality_check_profile,
    implementation_status,
    validation_status
)
values (
    '20000000-0000-0000-0000-000000000001',
    'CS_UEMOA_BCEAO_FX_SNAPSHOT',
    '10000000-0000-0000-0000-000000000001',
    'HTML_SNAPSHOT',
    'GET',
    'DOWNLOAD_BCEAO_HOME_PAGE_AND_PARSE_FX_TABLE',
    'COURS_DES_DEVISES_TABLE',
    'FRENCH_TEXT_DATE_OR_NUMERIC_DATE',
    'PROVIDER_BUY_AND_SELL_RATES',
    'LOCALE_AWARE_DECIMAL',
    'PRESERVE_PROVIDER_QUOTE_THEN_INVERT_MIDPOINT',
    'DAILY_BUSINESS_DAY_CHECK',
    'RAW_SHA256|VALUE_DATE|CURRENCY|RATE_TYPE',
    'KEEP_ALL_REVISIONS',
    true,
    true,
    '0.2.0',
    'STANDARD_BACKOFF',
    'FX_BUY_SELL_DATE_AND_LINEAGE_CHECKS',
    'COLLECTION_TESTED',
    'VALIDATED'
)
on conflict (collection_specification_code) do nothing;
