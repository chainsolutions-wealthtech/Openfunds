-- Migration 020: preserve listing quote-unit semantics separately from economic currency.
-- fund.listing.trading_currency_id remains the canonical parent economic currency.
-- trading_quote_unit_code preserves an exact three-character listing quote-unit code
-- when the listing is expressed in a distinct unit (for example a verified minor unit).
-- trading_quote_unit_factor converts one quote unit into the parent trading currency
-- only when that factor is explicitly known; NULL is preferred to an invented factor.

alter table fund.listing
    add column if not exists trading_quote_unit_code text,
    add column if not exists trading_quote_unit_factor numeric(20, 10);

do $$
begin
    if not exists (
        select 1
        from pg_constraint
        where conname = 'listing_quote_unit_code_format_ck'
          and conrelid = 'fund.listing'::regclass
    ) then
        alter table fund.listing
            add constraint listing_quote_unit_code_format_ck
            check (
                trading_quote_unit_code is null
                or (
                    char_length(trading_quote_unit_code) = 3
                    and trading_quote_unit_code = upper(trading_quote_unit_code)
                    and trading_quote_unit_code ~ '^[A-Z]{3}$'
                )
            );
    end if;

    if not exists (
        select 1
        from pg_constraint
        where conname = 'listing_quote_unit_factor_positive_ck'
          and conrelid = 'fund.listing'::regclass
    ) then
        alter table fund.listing
            add constraint listing_quote_unit_factor_positive_ck
            check (
                trading_quote_unit_factor is null
                or trading_quote_unit_factor > 0
            );
    end if;

    if not exists (
        select 1
        from pg_constraint
        where conname = 'listing_quote_unit_factor_requires_code_ck'
          and conrelid = 'fund.listing'::regclass
    ) then
        alter table fund.listing
            add constraint listing_quote_unit_factor_requires_code_ck
            check (
                trading_quote_unit_factor is null
                or trading_quote_unit_code is not null
            );
    end if;
end
$$;
