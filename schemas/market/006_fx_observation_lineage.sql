-- FX OBSERVATION LINEAGE AND BITEMPORAL EXTENSION
-- POSTGRESQL
-- Extends the existing market.fx_observation table without creating a parallel FX model.

create schema if not exists market;

alter table market.fx_observation
    alter column fx_rate type numeric(38,18) using fx_rate::numeric(38,18);

alter table market.fx_observation
    add column if not exists observation_kind text not null default 'OBSERVED',
    add column if not exists rate_type text not null default 'MIDPOINT',
    add column if not exists provider_series_id uuid references source.provider_series(provider_series_id),
    add column if not exists collection_run_id uuid references source.collection_run(collection_run_id),
    add column if not exists raw_artifact_id uuid references source.raw_artifact(raw_artifact_id),
    add column if not exists source_buy_rate numeric(38,18),
    add column if not exists source_sell_rate numeric(38,18),
    add column if not exists source_midpoint numeric(38,18),
    add column if not exists source_quote_convention text,
    add column if not exists transformation_formula text,
    add column if not exists methodology_version text,
    add column if not exists source_parser_version text,
    add column if not exists source_raw_sha256 text,
    add column if not exists collected_at timestamptz,
    add column if not exists system_from timestamptz not null default now(),
    add column if not exists system_to timestamptz,
    add column if not exists is_current boolean not null default true,
    add column if not exists validation_status text not null default 'PENDING';

-- Replace the original non-vintage uniqueness rule with a current-version rule.
-- PostgreSQL truncates identifiers longer than 63 bytes, so the legacy constraint
-- must be found by its column definition rather than by a hard-coded name.
do $$
declare
    legacy_constraint_name text;
begin
    select constraint_row.conname
    into legacy_constraint_name
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
    limit 1;

    if legacy_constraint_name is not null then
        execute format(
            'alter table market.fx_observation drop constraint %I',
            legacy_constraint_name
        );
    end if;
end
$$;

alter table market.fx_observation
    drop constraint if exists fx_observation_observation_kind_check,
    drop constraint if exists fx_observation_rate_type_check,
    drop constraint if exists fx_observation_validation_status_check,
    drop constraint if exists fx_observation_positive_rate_check,
    drop constraint if exists fx_observation_source_buy_positive_check,
    drop constraint if exists fx_observation_source_sell_positive_check,
    drop constraint if exists fx_observation_source_midpoint_positive_check,
    drop constraint if exists fx_observation_temporal_check,
    drop constraint if exists fx_observation_calculated_lineage_check;

alter table market.fx_observation
    add constraint fx_observation_observation_kind_check
        check (observation_kind in ('OBSERVED','CALCULATED')),
    add constraint fx_observation_rate_type_check
        check (rate_type in ('BUY','SELL','MIDPOINT','MIDPOINT_INVERTED','REFERENCE','CLOSE')),
    add constraint fx_observation_validation_status_check
        check (validation_status in ('PENDING','VALIDATED','REJECTED','SUPERSEDED')),
    add constraint fx_observation_positive_rate_check
        check (fx_rate > 0),
    add constraint fx_observation_source_buy_positive_check
        check (source_buy_rate is null or source_buy_rate > 0),
    add constraint fx_observation_source_sell_positive_check
        check (source_sell_rate is null or source_sell_rate > 0),
    add constraint fx_observation_source_midpoint_positive_check
        check (source_midpoint is null or source_midpoint > 0),
    add constraint fx_observation_temporal_check
        check (system_to is null or system_to >= system_from),
    add constraint fx_observation_calculated_lineage_check
        check (
            observation_kind <> 'CALCULATED'
            or (
                transformation_formula is not null
                and methodology_version is not null
                and source_quote_convention is not null
                and source_raw_sha256 is not null
            )
        );

create unique index if not exists ux_fx_observation_current_series
    on market.fx_observation (
        observation_date,
        source_currency_id,
        target_currency_id,
        rate_type,
        coalesce(provider_series_id, '00000000-0000-0000-0000-000000000000'::uuid)
    )
    where is_current;

create index if not exists idx_fx_observation_pair_date
    on market.fx_observation (
        source_currency_id,
        target_currency_id,
        observation_date desc
    );

create index if not exists idx_fx_observation_raw_artifact
    on market.fx_observation (raw_artifact_id);

create index if not exists idx_fx_observation_collection_run
    on market.fx_observation (collection_run_id);

create or replace view market.current_fx_observation as
select *
from market.fx_observation
where is_current
  and system_to is null
  and validation_status = 'VALIDATED';

comment on table market.fx_observation is
'Canonical FX observations. Observed provider values and calculated canonical rates preserve collection, artifact, quote-convention and methodology lineage.';

comment on column market.fx_observation.observation_kind is
'OBSERVED for a directly published rate; CALCULATED for an inversion, midpoint, triangulation or other versioned transformation.';

comment on column market.fx_observation.fx_rate is
'Canonical rule: one unit of source currency equals fx_rate units of target currency.';

comment on column market.fx_observation.source_quote_convention is
'Exact quote direction of the source observation before canonical normalization.';

comment on column market.fx_observation.transformation_formula is
'Explicit formula used to derive a calculated canonical observation.';
