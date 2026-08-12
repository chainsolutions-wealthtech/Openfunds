# État vérifié du projet

```text
STATUS_DATE: 2026-08-12
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
CURRENT_HEAD_POLICY: RESOLVE_DYNAMICALLY
TASK_ID: OF-SOURCE-002
LOOP_ID: OF-LOOP-SOURCE-002
LOOP_STATUS: EN_COURS
LAST_VERIFIED_WAVE: 01
WAVE_01_DATA_HEAD: 1f85c0df1878743f4a2ac322c2087b0b1a549641
WAVE_01_CI_RUN: 31592700354
PRODUCTION_DEPLOYED: NO
RUNTIME_DATABASE_CHANGED_BY_WAVE_01: NO
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

## OF-SOURCE-002 — état réel

```text
AFRICAN_COUNTRIES: 54
ORGANIZATIONS: 55 = 35 VALIDATED + 20 PENDING
COUNTRIES_WITH_COUNTRY_SCOPED_ORGANIZATION: 10
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 44
ORGANIZATION_SCOPE_ROLES: 92 = 48 VALIDATED + 44 PENDING
SOURCE_ENDPOINTS: 43 = 20 VALIDATED + 23 PENDING
GLOBAL_TASK_STATUS: EN_COURS
```

Vague 01 vérifiée : Botswana, Namibie et Éthiopie ont été ajoutés au niveau pays ; AMF-UMOA et UMOA-Titres au niveau UEMOA ; COSUMAF au niveau CEMAC. Quinze organisations et vingt-deux relations de rôle ont été ajoutées sans inventer de date, de collecte ou d’historique.

`FMDQ` reste hors allowlist jusqu’à revue du rôle canonique exact.

## Contrôle institutionnel exécutable

```text
WORKFLOW: Institutional Registry
RUN: 31592700354
CONCLUSION: SUCCESS
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
TESTS: 4 / 4 PASS
```

Le contrôle couvre unicité et syntaxe des codes, références organisation/rôle/scope, pays/zones canoniques, statuts, présence d’URL pour les objets validés et contrat de la vague 01.

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

Aucun historique pays/fonds, NAV, AUM, dividende ou portefeuille n’est chargé. Aucun PostgreSQL persistant, stockage objet permanent, catalogue officiel Openfunds, mapping officiel, API, UI, merge ou déploiement n’est réalisé par `OF-SOURCE-002/WAVE_01`.

Conformément à ADR-021, les grands CSV institutionnels restent des inventaires de découverte/revue ; ils ne deviennent pas automatiquement la vérité runtime PostgreSQL.

## Prochaine action

```text
NEXT: OF-SOURCE-002 / WAVE_02
INITIAL_MODE: READ_ONLY_AUDIT
OBJECTIVE: couvrir les rôles manquants des 10 pays présents et rechercher les institutions officielles des 44 pays sans organisation nationale
WRITE_GATE: OFFICIAL_PRIMARY_EVIDENCE + COLLISION_REVIEW + ALLOWLIST
OF-MAP-001: BLOCKED_OFFICIAL_OPENFUNDS_CATALOGUE_UNAVAILABLE
```
