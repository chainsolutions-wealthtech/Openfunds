# Handoff Loop Engineering

```text
LOOP_ID: OF-LOOP-SOURCE-002
TASK_ID: OF-SOURCE-002
STATUS: EN_COURS
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
CURRENT_HEAD_POLICY: RESOLVE_DYNAMICALLY
LAST_VERIFIED_WAVE: 01
WAVE_01_DATA_HEAD: 1f85c0df1878743f4a2ac322c2087b0b1a549641
WAVE_01_CI_RUN: 31592700354
NEXT_WAVE: 02_READ_ONLY_AUDIT
```

## Vague 01 — résultat vérifié

```text
AFRICAN_COUNTRIES: 54
ORGANIZATIONS_BEFORE: 40
ORGANIZATIONS_AFTER: 55
VALIDATED_ORGANIZATIONS_AFTER: 35
COUNTRY_COVERAGE_BEFORE: 7 / 54
COUNTRY_COVERAGE_AFTER: 10 / 54
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 44
SCOPE_ROLES_BEFORE: 70
SCOPE_ROLES_AFTER: 92
VALIDATED_SCOPE_ROLES_AFTER: 48
SOURCE_ENDPOINTS: 43 UNCHANGED
```

Organisations intégrées :

```text
BOTSWANA: BOB, NBFIRA, BSE, STATISTICS_BOTSWANA
NAMIBIE: BON, NAMFISA, NSX, NSA_NAMIBIA
ETHIOPIE: NBE, ECMA, ESX, ESS_ETHIOPIA
UEMOA: AMF_UMOA, UMOA_TITRES
CEMAC: COSUMAF
```

Vingt-deux relations de rôles officiellement prouvées ont été ajoutées. `FMDQ` reste hors allowlist en attente de revue du rôle canonique exact.

## Preuve de non-régression

```text
WORKFLOW: Institutional Registry
RED_RUN: 31592435103
INTERMEDIATE_RUN: 31592516832
GREEN_RUN: 31592700354
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
TESTS: 4 / 4 PASS
```

## Fichiers principaux de la boucle

- `docs/00_PROJECT/OF_SOURCE_002_BASELINE_AUDIT_20260812.md` ;
- `docs/00_PROJECT/OF_SOURCE_002_WAVE_01_COMPLETION_20260812.md` ;
- `docs/superpowers/plans/2026-08-12-of-source-002-institutional-coverage-wave-01.md` ;
- `data/reference/ORGANIZATIONS.csv` ;
- `data/reference/ORGANIZATION_SCOPE_ROLES.csv` ;
- `scripts/validate_institutional_registry.py` ;
- `tests/test_institutional_registry.py` ;
- `.github/workflows/institutional-registry.yml`.

## Limites

Les CSV institutionnels restent des inventaires de découverte/revue conformément à ADR-021. Aucune migration runtime, aucun endpoint spécialisé, aucune provider series, aucune collecte ou série historique n’a été ajouté par la vague 01.

## Point de reprise exact

1. résoudre le HEAD courant ;
2. conserver `OF-SOURCE-002` en `EN_COURS` ;
3. lister les 44 pays sans organisation country-scoped ;
4. mesurer les rôles manquants des 10 pays présents ;
5. vérifier des sources officielles primaires uniquement ;
6. classifier `VERIFIED`, `SOURCE_IDENTIFIED`, `PENDING`, `NOT_PUBLISHED`, `NOT_APPLICABLE` ;
7. vérifier les collisions de codes ;
8. produire l’allowlist vague 02 avant toute écriture.

Ne pas modifier PR nº2, `main`, la cible de PR nº1, créer branche/PR, déployer ou charger des historiques.
