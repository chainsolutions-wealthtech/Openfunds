# État vérifié du projet

```text
STATUS_DATE: 2026-08-12
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
CURRENT_HEAD_POLICY: RESOLVE_DYNAMICALLY
TASK_ID: OF-SOURCE-002
LOOP_ID: OF-LOOP-SOURCE-002
LOOP_STATUS: EN_COURS
LAST_VERIFIED_WAVE: 03
WAVE_03_DATA_HEAD: 5024a9767b1b9aecf8a6cd52d315ccfbf8384389
WAVE_03_CI_RUN: 31595575537
PRODUCTION_DEPLOYED: NO
RUNTIME_DATABASE_CHANGED_BY_OF_SOURCE_002: NO
REAL_COUNTRY_HISTORY_LOADED: NO
```

## Gates achevés

```text
OF-ARCH-001   VERIFIED_COMPLETE
OF-SOURCE-001 VERIFIED_COMPLETE
OF-ARCH-002   VERIFIED_COMPLETE
OF-ARCH-003   VERIFIED_COMPLETE
OF-ARCH-004   VERIFIED_COMPLETE
OF-DATA-001   VERIFIED_COMPLETE
OF-DATA-002   VERIFIED_COMPLETE
OF-DATA-003   VERIFIED_COMPLETE
```

## OF-SOURCE-002 — état réel après vague 03

```text
AFRICAN_COUNTRIES: 54
ORGANIZATIONS: 87 = 67 VALIDATED + 20 PENDING
COUNTRIES_WITH_COUNTRY_SCOPED_ORGANIZATION: 18
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 36
ORGANIZATION_SCOPE_ROLES: 134 = 90 VALIDATED + 44 PENDING
SOURCE_ENDPOINTS: 43 = 20 VALIDATED + 23 PENDING
GLOBAL_TASK_STATUS: EN_COURS
```

### Vagues vérifiées

```text
WAVE_01: VERIFIED_COMPLETE — Botswana, Namibie, Éthiopie + UEMOA/CEMAC
WAVE_02: VERIFIED_COMPLETE — Algérie, Maurice, Rwanda, Tanzanie
WAVE_03: VERIFIED_COMPLETE — Ouganda, Zambie, Zimbabwe, Malawi
```

Les vagues 01 à 03 n'ont ajouté aucun endpoint spécialisé, aucune provider series, aucune collection specification, aucune migration SQL runtime et aucun historique réel.

## Contrôle institutionnel exécutable

```text
WORKFLOW: Institutional Registry
LAST_GREEN_RUN: 31595575537
HEAD: 5024a9767b1b9aecf8a6cd52d315ccfbf8384389
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
TESTS: 8 / 8 PASS
```

Le contrôle couvre les invariants historiques, les allowlists vagues 01 à 03 et des protections négatives explicites.

## Protections et blockers de preuve

```text
FMDQ: REQUIRES_ROLE_MODEL_REVIEW
SEC_ZAMBIA: CURRENT_OFFICIAL_DOMAIN_INTEGRITY_BLOCKER
UGANDA_IRA_URBRA: COMBINED_ROLE_MODEL_MISMATCH
RBM_FUND_REGULATOR: PRIMARY_CIS_PROOF_NOT_SUFFICIENT
```

Aucune de ces situations ne doit être résolue par supposition.

## Catalogue D00–D17 conservé

```text
AUTHORITATIVE_PACKAGE: data/indicator_catalog/v1/
DOMAIN_COUNT: 18
INDICATOR_COUNT: 420
RAW: 298
METADATA: 85
EVENT: 7
CALCULATED: 30
MIGRATION: 016_COUNTRY_INDICATOR_CATALOG
STATUS: VERIFIED_COMPLETE
```

## Limites conservées

Aucun historique pays/fonds, NAV, AUM, dividende ou portefeuille n’est chargé. Aucun PostgreSQL persistant, stockage objet permanent, catalogue officiel Openfunds, mapping officiel, API, UI, merge ou déploiement n’est réalisé par `OF-SOURCE-002`.

Conformément à ADR-021, les grands CSV institutionnels restent des inventaires de découverte/revue ; ils ne deviennent pas automatiquement la vérité runtime PostgreSQL.

## Prochaine action

```text
NEXT: OF-SOURCE-002 / WAVE_04
INITIAL_MODE: READ_ONLY_AUDIT
OBJECTIVE: sélectionner un nouveau lot contrôlé parmi les 36 pays sans organisation nationale
WRITE_GATE: CURRENT_OFFICIAL_PRIMARY_EVIDENCE + COLLISION_REVIEW + CLOSED_ALLOWLIST
OF-MAP-001: BLOCKED_OFFICIAL_OPENFUNDS_CATALOGUE_UNAVAILABLE
```
