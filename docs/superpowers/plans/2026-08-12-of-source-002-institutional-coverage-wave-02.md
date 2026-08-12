# OF-SOURCE-002 Institutional Coverage Wave 02 Implementation Plan

**Goal:** Ajouter Algérie, Maurice, Rwanda et Tanzanie au registre institutionnel de découverte/revue, uniquement sur preuves officielles primaires et sans créer de branche, PR, endpoint, migration runtime ou historique.

**Authority:** `docs/00_PROJECT/OF_SOURCE_002_WAVE_02_AUDIT_20260812.md` contient l'allowlist fermée de la vague.

## Constraints

- branche unique : `architecture/africafunds-country-indicators-v0.1` ;
- fast-forward uniquement ;
- PR #2 lecture seule ;
- `main` intouchée ;
- CSV institutionnels = discovery/review, pas runtime PostgreSQL ;
- aucun rôle hors allowlist ;
- aucun statut de collecte/historique ;
- TDD RED → GREEN avec `Institutional Registry` Python 3.11/3.12.

## Task 1 — Contrat RED

- [x] étendre `tests/test_institutional_registry.py` avec les 16 organisations et 22 relations de rôle de vague 02 ;
- [x] pousser uniquement le test ;
- [x] vérifier que les invariants existants restent verts et que les assertions vague 02 échouent pour absence des nouvelles lignes.

## Task 2 — Organisations GREEN

- [x] ajouter uniquement les 16 organisations de l'allowlist à `data/reference/ORGANIZATIONS.csv` ;
- [x] `VALIDATED` seulement avec URL officielle primaire et rôle principal prouvé ;
- [x] aucune date artificielle ;
- [x] exécuter/observer le workflow.

## Task 3 — Relations GREEN

- [x] ajouter uniquement les 22 relations de `docs/00_PROJECT/OF_SOURCE_002_WAVE_02_AUDIT_20260812.md` ;
- [x] ne pas ajouter de rôle assurance/pension pour Algérie/Tanzanie dans cette vague ;
- [x] vérifier le workflow Python 3.11/3.12 au HEAD de données.

## Task 4 — Clôture de vague

- [x] recalculer organisations, validations, pays country-scoped et relations ;
- [x] écrire une attestation de clôture datée ;
- [x] mettre à jour la mémoire vivante lors de la consolidation cumulative après vague 03 ;
- [x] conserver `OF-SOURCE-002` en `EN_COURS` ;
- [x] ouvrir la vague 03 en read-only audit sur un nouveau lot contrôlé de pays.

## Closure evidence

```text
RED_HEAD: 39b5f3a04df4c5f69d9ac4300c5a21e4f5728749
RED_RUN: 31594066287
INTERMEDIATE_HEAD: 8a057200682773b09f61e898e55ca2f3537422f2
INTERMEDIATE_RUN: 31594256827
GREEN_HEAD: 2216ff00406e3ee40b0f8ef70ff8710f5c928d34
GREEN_RUN: 31594503714
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
TESTS: 6 / 6 PASS
COUNTRY_COVERAGE_AFTER: 14 / 54
GLOBAL_TASK: OF-SOURCE-002 EN_COURS
```
