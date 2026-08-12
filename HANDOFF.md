# Handoff Loop Engineering

```text
LOOP_ID: OF-LOOP-SOURCE-002
TASK_ID: OF-SOURCE-002
STATUS: EN_COURS
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
CURRENT_HEAD_POLICY: RESOLVE_DYNAMICALLY
LAST_VERIFIED_WAVE: 03
WAVE_03_DATA_HEAD: 5024a9767b1b9aecf8a6cd52d315ccfbf8384389
WAVE_03_CI_RUN: 31595575537
NEXT_WAVE: 04_READ_ONLY_AUDIT
```

## Progression vérifiée

```text
AFRICAN_COUNTRIES: 54
COUNTRY_COVERAGE_BASELINE: 7 / 54
AFTER_WAVE_01: 10 / 54
AFTER_WAVE_02: 14 / 54
AFTER_WAVE_03: 18 / 54
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 36

ORGANIZATIONS: 87 = 67 VALIDATED + 20 PENDING
ORGANIZATION_SCOPE_ROLES: 134 = 90 VALIDATED + 44 PENDING
SOURCE_ENDPOINTS: 43 = 20 VALIDATED + 23 PENDING
```

## Vagues terminées

### Vague 01

```text
BOTSWANA: BOB, NBFIRA, BSE, STATISTICS_BOTSWANA
NAMIBIE: BON, NAMFISA, NSX, NSA_NAMIBIA
ETHIOPIE: NBE, ECMA, ESX, ESS_ETHIOPIA
UEMOA: AMF_UMOA, UMOA_TITRES
CEMAC: COSUMAF
GREEN_RUN: 31592700354
```

### Vague 02

```text
ALGERIE: BANQUE_ALGERIE, COSOB, SGBV, ONS_ALGERIE
MAURICE: BOM, FSC_MAURITIUS, SEM, STATISTICS_MAURITIUS
RWANDA: NBR, CMA_RWANDA, RSE, NISR
TANZANIE: BOT, CMSA_TANZANIA, DSE, NBS_TANZANIA
GREEN_RUN: 31594503714
```

### Vague 03

```text
OUGANDA: BOU, CMA_UGANDA, USE_UGANDA, UBOS
ZAMBIE: BOZ, LUSE, ZAMSTATS, PIA_ZAMBIA
ZIMBABWE: RBZ, SEC_ZIMBABWE, ZSE, ZIMSTAT, IPEC
MALAWI: RBM, MSE_MALAWI, NSO_MALAWI
GREEN_RUN: 31595575537
TESTS: 8 / 8 PASS
```

## Protections actives

```text
FMDQ               REQUIRES_ROLE_MODEL_REVIEW
SEC_ZAMBIA         CURRENT_OFFICIAL_DOMAIN_INTEGRITY_BLOCKER
IRA_URBRA_UGANDA   COMBINED_ROLE_MODEL_MISMATCH
RBM_FUND_REGULATOR PRIMARY_CIS_PROOF_NOT_SUFFICIENT
```

`SEC_ZAMBIA` est explicitement protégé par un test négatif après constat que le domaine historique principal retournait un contenu non institutionnel. `RBM/FUND_REGULATOR` est également protégé contre une promotion sans preuve CIS/OPC explicite.

## Preuve de non-régression la plus récente

```text
WORKFLOW: Institutional Registry
GREEN_RUN: 31595575537
GREEN_HEAD: 5024a9767b1b9aecf8a6cd52d315ccfbf8384389
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
TESTS: 8 / 8 PASS
```

## Fichiers principaux de la boucle

- `docs/00_PROJECT/OF_SOURCE_002_BASELINE_AUDIT_20260812.md` ;
- `docs/00_PROJECT/OF_SOURCE_002_WAVE_01_COMPLETION_20260812.md` ;
- `docs/00_PROJECT/OF_SOURCE_002_WAVE_02_AUDIT_20260812.md` ;
- `docs/00_PROJECT/OF_SOURCE_002_WAVE_02_COMPLETION_20260812.md` ;
- `docs/00_PROJECT/OF_SOURCE_002_WAVE_03_AUDIT_20260812.md` ;
- `docs/00_PROJECT/OF_SOURCE_002_WAVE_03_COMPLETION_20260812.md` ;
- `scripts/validate_institutional_registry.py` ;
- `tests/test_institutional_registry.py` ;
- `.github/workflows/institutional-registry.yml`.

## Limites

Les CSV institutionnels restent des inventaires de découverte/revue conformément à ADR-021. Aucune migration runtime, aucun endpoint spécialisé, aucune provider series, aucune collecte ou série historique n’a été ajoutée par les vagues 01 à 03.

## Point de reprise exact

1. résoudre le HEAD courant ;
2. conserver `OF-SOURCE-002` en `EN_COURS` ;
3. commencer `WAVE_04` uniquement en lecture seule ;
4. sélectionner un lot parmi les 36 pays sans organisation country-scoped ;
5. vérifier des sources officielles primaires actuelles uniquement ;
6. contrôler l'intégrité des domaines ;
7. classifier les rôles sans extrapolation ;
8. vérifier les collisions de codes ;
9. produire une allowlist fermée ;
10. appliquer ensuite TDD RED → organisations → rôles → GREEN.

Ne pas modifier PR nº2, `main`, la cible de PR nº1, créer branche/PR, déployer ou charger des historiques.
