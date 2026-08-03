-- BEAC FX PARSER VERSION 0.2.0
-- The official page renders FX rows as repeated DIV.taux_de_change blocks.
-- This migration records the implemented parser revision while live validation
-- remains pending.

update source.collection_specification
set parser_version = '0.2.0',
    table_or_selector = 'DIV.taux_de_change|TABLE_FALLBACK',
    value_extraction_rule = 'PROVIDER_PAIR_BUY_AND_SELL_FROM_TEXT_BLOCKS',
    quality_check_profile = 'FX_DIV_BLOCK_BUY_SELL_DATE_AND_LINEAGE_CHECKS',
    implementation_status = 'COLLECTOR_IMPLEMENTED',
    validation_status = 'PENDING',
    updated_at = now()
where collection_specification_code = 'CS_CEMAC_BEAC_FX_SNAPSHOT';

update source.provider_series
set history_status = 'COLLECTOR_IMPLEMENTED',
    validation_status = 'PENDING',
    updated_at = now()
where provider_series_code in (
    'PS_CEMAC_BEAC_FX_SNAPSHOT',
    'PS_CEMAC_FX_XAF_EUR',
    'PS_CEMAC_FX_XAF_USD'
);
