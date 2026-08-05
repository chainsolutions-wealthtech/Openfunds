-- BEAC FX LIVE COLLECTION VALIDATION
-- Controlled workflow run: 30779605759
-- Parser: 0.2.0
-- Value date: 2026-07-31
-- Raw SHA256: C93BE111A3997C913917B5AAE425A02FB575FE0B39BFDA67953E237E0A11C23C
-- This validates one current snapshot and the executable pipeline.
-- It does not claim partial or complete historical coverage.

update source.endpoint
set last_verified_at = '2026-08-03T02:34:40Z'::timestamptz,
    validation_status = 'VALIDATED',
    source_note = 'LIVE_RUN_30779605759_SHA256_C93BE111A3997C913917B5AAE425A02FB575FE0B39BFDA67953E237E0A11C23C_VALUE_DATE_2026_07_31_13_OBSERVATIONS_NO_WARNINGS_IDEMPOTENT',
    updated_at = now()
where endpoint_code = 'BEAC_FX_DAILY';

update source.indicator_source_mapping
set collection_status = 'COLLECTION_TESTED',
    validation_status = 'VALIDATED',
    source_note = case mapping_code
        when 'CEMAC_D09_FX_EUR'
            then 'LIVE_OBSERVED_EUR_XAF_BUY_SELL_THEN_INVERTED_MIDPOINT_RUN_30779605759'
        when 'CEMAC_D09_FX_USD'
            then 'LIVE_OBSERVED_USD_XAF_BUY_SELL_THEN_INVERTED_MIDPOINT_RUN_30779605759'
        else source_note
    end,
    updated_at = now()
where mapping_code in ('CEMAC_D09_FX_EUR','CEMAC_D09_FX_USD');

update source.provider_series
set history_status = 'COLLECTION_TESTED',
    validation_status = 'VALIDATED',
    updated_at = now()
where provider_series_code in (
    'PS_CEMAC_BEAC_FX_SNAPSHOT',
    'PS_CEMAC_FX_XAF_EUR',
    'PS_CEMAC_FX_XAF_USD'
);

update source.collection_specification
set parser_version = '0.2.0',
    table_or_selector = 'DIV.taux_de_change|TABLE_FALLBACK',
    value_extraction_rule = 'PROVIDER_PAIR_BUY_AND_SELL_FROM_TEXT_BLOCKS',
    quality_check_profile = 'FX_DIV_BLOCK_BUY_SELL_DATE_SHA256_IDEMPOTENCE_AND_POSTGRES_LINEAGE_CHECKS',
    implementation_status = 'COLLECTION_TESTED',
    validation_status = 'VALIDATED',
    updated_at = now()
where collection_specification_code = 'CS_CEMAC_BEAC_FX_SNAPSHOT';
