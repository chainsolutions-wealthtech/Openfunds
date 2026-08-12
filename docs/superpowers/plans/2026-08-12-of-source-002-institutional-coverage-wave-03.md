# OF-SOURCE-002 Institutional Coverage Wave 03 Implementation Plan

**Goal:** Ajouter Ouganda, Zambie, Zimbabwe et Malawi au registre institutionnel de découverte/revue en respectant strictement l'allowlist auditée, sans nouvelle branche/PR et sans runtime/historique.

**Authority:** `docs/00_PROJECT/OF_SOURCE_002_WAVE_03_AUDIT_20260812.md`.

## Constraints

- branche unique : `architecture/africafunds-country-indicators-v0.1` ;
- fast-forward uniquement ;
- `main`, PR #1 et PR #2 non modifiées ;
- aucun `SEC_ZAMBIA` dans cette vague ;
- aucun `FUND_REGULATOR` Malawi ;
- aucun rôle combiné inventé pour IRA/URBRA Uganda ;
- aucun endpoint, provider series, collection spec, SQL runtime ou historique ;
- TDD RED → organisations → rôles → GREEN Python 3.11/3.12.

## Task 1 — Contrat RED

- [ ] étendre `tests/test_institutional_registry.py` avec les 16 organisations et 20 relations de vague 03 ;
- [ ] pousser uniquement le test ;
- [ ] vérifier que les 6 tests existants restent verts et que seuls les 2 nouveaux tests échouent pour absence de vague 03.

## Task 2 — Organisations

- [ ] ajouter uniquement les 16 organisations de l'allowlist dans `data/reference/ORGANIZATIONS.csv` ;
- [ ] utiliser seulement les domaines officiels primaires validés par l'audit ;
- [ ] ne pas inscrire `SEC_ZAMBIA` ;
- [ ] vérifier le run intermédiaire : organisations vertes, rôles encore rouges.

## Task 3 — Relations

- [ ] ajouter uniquement les 20 relations de l'allowlist dans `data/reference/ORGANIZATION_SCOPE_ROLES.csv` ;
- [ ] ne pas ajouter `FUND_REGULATOR` pour Malawi ;
- [ ] ne pas fusionner IRA/URBRA dans un rôle non conforme ;
- [ ] vérifier `Institutional Registry` sur Python 3.11/3.12 au HEAD final.

## Task 4 — Clôture

- [ ] recalculer les comptes après vague 03 ;
- [ ] documenter RED/intermédiaire/GREEN ;
- [ ] créer l'attestation de clôture ;
- [ ] réaligner STATUS/LOOP/NEXT/HANDOFF/WORK_LOG/TODO/SUIVI/CHANGELOG ;
- [ ] conserver `OF-SOURCE-002` en `EN_COURS` ;
- [ ] ouvrir la vague 04 en lecture seule sur un nouveau lot contrôlé.
