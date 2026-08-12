# OF-SOURCE-002 Institutional Coverage Wave 04 Implementation Plan

**Goal:** Ajouter Angola, Mozambique, Cabo Verde et Seychelles au registre institutionnel de découverte/revue, uniquement à partir de l'allowlist auditée et sans nouvelle branche/PR, runtime ou historique.

**Authority:** `docs/00_PROJECT/OF_SOURCE_002_WAVE_04_AUDIT_20260812.md`.

## Constraints

- branche unique : `architecture/africafunds-country-indicators-v0.1` ;
- fast-forward uniquement ;
- `main`, PR #1 et PR #2 non modifiées ;
- aucun rôle hors allowlist ;
- Banco de Moçambique ne reçoit aucun `INSURANCE_PENSION_REGULATOR` ;
- AGMVM est documentée comme service sous le Gouverneur du BCV ;
- MERJ est admise sur preuve du répertoire officiel FSA ;
- aucun endpoint, provider series, collection spec, SQL runtime ou historique ;
- TDD RED → organisations → rôles → GREEN Python 3.11/3.12.

## Task 1 — Contrat RED

- [ ] étendre `tests/test_institutional_registry.py` avec les 15 organisations et 21 relations de vague 04 ;
- [ ] ajouter des protections négatives pour le rôle assurance/pension de Banco de Moçambique ;
- [ ] pousser uniquement le test ;
- [ ] vérifier que les 8 tests existants restent verts et que seuls les 2 nouveaux tests de vague 04 échouent.

## Task 2 — Organisations

- [ ] ajouter uniquement les 15 organisations de l'allowlist dans `data/reference/ORGANIZATIONS.csv` ;
- [ ] conserver les domaines officiels actuels documentés dans l'audit ;
- [ ] documenter `AGMVM` comme service sous BCV ;
- [ ] vérifier le run intermédiaire : organisations vertes, rôles encore rouges.

## Task 3 — Relations

- [ ] ajouter uniquement les 21 relations de l'allowlist dans `data/reference/ORGANIZATION_SCOPE_ROLES.csv` ;
- [ ] ne pas ajouter assurance/pension à Banco de Moçambique ;
- [ ] vérifier `Institutional Registry` sur Python 3.11/3.12 au HEAD final.

## Task 4 — Clôture

- [ ] recalculer les comptes après vague 04 ;
- [ ] documenter RED/intermédiaire/GREEN ;
- [ ] créer l'attestation de clôture ;
- [ ] réaligner la mémoire vivante courte sans écraser les journaux tronqués ;
- [ ] conserver `OF-SOURCE-002` en `EN_COURS` ;
- [ ] ouvrir vague 05 en lecture seule sur un nouveau lot contrôlé.
