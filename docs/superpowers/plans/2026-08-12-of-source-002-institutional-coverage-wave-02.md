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

- [ ] étendre `tests/test_institutional_registry.py` avec les 16 organisations et 22 relations de rôle de vague 02 ;
- [ ] pousser uniquement le test ;
- [ ] vérifier que les invariants existants restent verts et que les assertions vague 02 échouent pour absence des nouvelles lignes.

## Task 2 — Organisations GREEN

- [ ] ajouter uniquement les 16 organisations de l'allowlist à `data/reference/ORGANIZATIONS.csv` ;
- [ ] `VALIDATED` seulement avec URL officielle primaire et rôle principal prouvé ;
- [ ] aucune date artificielle ;
- [ ] exécuter/observer le workflow.

## Task 3 — Relations GREEN

- [ ] ajouter uniquement les 22 relations de `docs/00_PROJECT/OF_SOURCE_002_WAVE_02_AUDIT_20260812.md` ;
- [ ] ne pas ajouter de rôle assurance/pension pour Algérie/Tanzanie dans cette vague ;
- [ ] vérifier le workflow Python 3.11/3.12 au HEAD de données.

## Task 4 — Clôture de vague

- [ ] recalculer organisations, validations, pays country-scoped et relations ;
- [ ] écrire une attestation de clôture datée ;
- [ ] mettre à jour STATUS, LOOP_STATE, CURRENT_ITERATION, NEXT_ACTION, HANDOFF, WORK_LOG, TODO, SUIVI et CHANGELOG ;
- [ ] conserver `OF-SOURCE-002` en `EN_COURS` ;
- [ ] ouvrir la vague 03 en read-only audit sur un nouveau lot contrôlé de pays.
