# OF-SOURCE-002 — Wave 09 zone-role validation audit — 2026-08-17

```text
TASK_ID: OF-SOURCE-002
LOOP_ID: OF-LOOP-SOURCE-002
WAVE: 09
MODE: READ_ONLY_AUDIT
MUTATION_TYPE: STATUS_PROMOTION_OF_EXISTING_ROWS_ONLY
WRITE_GATE: PRIMARY_OFFICIAL_EVIDENCE + EXACT_TUPLE_MATCH + TDD_RED
```

## Objective

Promote four already-existing zone-scoped relationships from `PENDING` to `VALIDATED` without adding, renaming or duplicating organizations or role relationships.

## Official evidence

### UEMOA

- BCEAO official presentation: https://www.bceao.int/content/presentation-de-la-bceao
  - BCEAO is the common issuing institution for the eight UMOA member states and exercises the exclusive monetary-issuance function for the Union.
- BCEAO official home: https://www.bceao.int/fr
  - identifies BCEAO as the common issuing institution of UMOA member states.
- BRVM official: https://www.brvm.org/
  - BRVM is the regional securities exchange for the eight UEMOA countries and operates a market extended across the Union.

### CEMAC

- BEAC official presentation: https://www.beac.int/beac/la-beac/
  - BEAC is the common central bank of the six CEMAC states and conducts CEMAC monetary policy.
- BVMAC official presentation: https://www.bvm-ac.org/presentation-de-la-bvmac/
  - BVMAC is the regional market operator charged exclusively with organization, operation and management of the Central African financial market.

## Exact existing rows allowed for promotion

```text
BCEAO;CENTRAL_BANK;UEMOA;MONETARY_ZONE
BEAC;CENTRAL_BANK;CEMAC;MONETARY_ZONE
BRVM;COMMON_STOCK_EXCHANGE;UEMOA;MONETARY_ZONE
BVMAC;COMMON_STOCK_EXCHANGE;CEMAC;MONETARY_ZONE
```

## Non-regression rules

- no new organization;
- no new role relationship;
- no code change;
- no scope change;
- no historical date invented;
- only `VALIDATION_STATUS` and `SOURCE_NOTE` may change for the four exact rows;
- all other rows must remain byte-for-byte semantically unchanged;
- UEMOA/CEMAC competence remains zone-scoped, never duplicated country-by-country.

## Expected registry state after GREEN

```text
ORGANIZATIONS: unchanged at 141
COUNTRY_COVERAGE: unchanged at 53 / 54
ORGANIZATION_SCOPE_ROLES: unchanged at 199
VALIDATED_RELATIONSHIPS: 159
PENDING_RELATIONSHIPS: 40
```

The role-coverage audit should then inherit central-bank and common-exchange coverage for UEMOA/CEMAC member countries.
