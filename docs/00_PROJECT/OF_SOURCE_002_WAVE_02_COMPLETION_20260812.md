# OF-SOURCE-002 — Wave 02 completion attestation — 2026-08-12

```text
TASK_ID: OF-SOURCE-002
LOOP_ID: OF-LOOP-SOURCE-002
WAVE: 02
STATUS: VERIFIED_COMPLETE_WAVE / GLOBAL_TASK_EN_COURS
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
WAVE_DATA_HEAD: 2216ff00406e3ee40b0f8ef70ff8710f5c928d34
GREEN_RUN: 31594503714
PRODUCTION_DEPLOYED: NO
RUNTIME_DATABASE_CHANGED: NO
HISTORY_LOADED: NO
NEW_BRANCH_CREATED: NO
NEW_PR_CREATED: NO
PR2_MODIFIED: NO
```

## Résultat

La vague 02 a ajouté uniquement les organisations et relations explicitement autorisées par `docs/00_PROJECT/OF_SOURCE_002_WAVE_02_AUDIT_20260812.md`.

### Organisations ajoutées — 16

```text
ALGERIE: BANQUE_ALGERIE, COSOB, SGBV, ONS_ALGERIE
MAURICE: BOM, FSC_MAURITIUS, SEM, STATISTICS_MAURITIUS
RWANDA: NBR, CMA_RWANDA, RSE, NISR
TANZANIE: BOT, CMSA_TANZANIA, DSE, NBS_TANZANIA
```

### Relations ajoutées — 22

Rôles prouvés uniquement :

```text
CENTRAL_BANK
CAPITAL_MARKET_REGULATOR
FUND_REGULATOR
INSURANCE_PENSION_REGULATOR   # Maurice et Rwanda seulement
STOCK_EXCHANGE
STATISTICS_OFFICE
```

Aucun rôle assurance/pension n’a été attribué à l’Algérie ou la Tanzanie dans cette vague faute de preuve suffisante qu’une même organisation corresponde exactement au rôle canonique combiné.

## TDD

```text
RED_RUN: 31594066287
RED_HEAD: 39b5f3a04df4c5f69d9ac4300c5a21e4f5728749
RESULT: 4 existing tests PASS / 2 wave-02 tests FAIL as expected

INTERMEDIATE_RUN: 31594256827
INTERMEDIATE_HEAD: 8a057200682773b09f61e898e55ca2f3537422f2
RESULT: 5 / 6 PASS; organizations GREEN; scope roles still RED as expected

GREEN_RUN: 31594503714
GREEN_HEAD: 2216ff00406e3ee40b0f8ef70ff8710f5c928d34
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
TESTS: 6 / 6 PASS
```

Le workflow général `Collector Tests` a également été déclenché au commit RED et a échoué parce qu’il exécutait le contrat de vague 02 avant présence des données. Il n’a pas été relancé automatiquement sur le HEAD de données final ; cette absence de run courant n’est pas présentée comme un succès. Le workflow gouvernant directement les registres institutionnels, `Institutional Registry`, est quant à lui vert au HEAD final.

## État après vague 02

```text
AFRICAN_COUNTRIES: 54
ORGANIZATIONS: 71 = 51 VALIDATED + 20 PENDING
COUNTRIES_WITH_COUNTRY_SCOPED_ORGANIZATION: 14
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 40
ORGANIZATION_SCOPE_ROLES: 114 = 70 VALIDATED + 44 PENDING
SOURCE_ENDPOINTS: 43 = 20 VALIDATED + 23 PENDING
```

## Limites conservées

- aucun endpoint spécialisé ;
- aucune provider series ;
- aucune collection specification ;
- aucune preuve de collecte ;
- aucune migration SQL runtime ;
- aucun historique réel ;
- aucune base PostgreSQL persistante ;
- aucune nouvelle branche ou PR ;
- aucune modification de `main`, PR nº1 ou PR nº2.

Les CSV institutionnels restent des inventaires de découverte/revue conformément à ADR-021.

## Point de reprise

`OF-SOURCE-002` reste `EN_COURS`.

La vague 03 commence en lecture seule. Lot de recherche prioritaire : `OUGANDA`, `ZAMBIE`, `ZIMBABWE`, `MALAWI`. Les mêmes gates restent obligatoires : sources officielles primaires, revue de collisions, allowlist fermée, RED contractuel puis GREEN, aucune extension implicite du périmètre.
