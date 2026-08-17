-- 018 EXTENDED SECURITY IDENTIFIER SCHEMES
-- PostgreSQL
-- OF-DATA-001 / OF-MAP-002
--
-- Forward-only widening of the canonical identifier-scheme vocabulary.
-- Migration 015 remains immutable. Existing rows are neither rewritten nor deleted.

alter table fund.entity_identifier
    drop constraint if exists entity_identifier_identifier_scheme_check;

alter table fund.entity_identifier
    add constraint entity_identifier_identifier_scheme_check
    check (
        identifier_scheme in (
            'ISIN','LEI','WKN','SEDOL','VALOR',
            'REGULATOR_ID','LOCAL_CODE','OPENFUNDS_ID',
            'INTERNAL_LEGACY_ID','OTHER'
        )
    );
