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

- [x] étendre `tests/test_institutional_registry.py` avec les 16 organisations et 20 relations de vague 03 ;
- [x] pousser uniquement le test ;
- [x] vérifier que les 6 tests existants restent verts et que seuls les 2 nouveaux tests échouent pour absence de vague 03.

## Task 2 — Organisations

- [x] ajouter uniquement les 16 organisations de l'allowlist dans `data/reference/ORGANIZATIONS.csv` ;
- [x] utiliser seulement les domaines officiels primaires validés par l'audit ;
- [x] ne pas inscrire `SEC_ZAMBIA` ;
- [x] vérifier le run intermédiaire : organisations vertes, rôles encore rouges.

## Task 3 — Relations

- [x] ajouter uniquement les 20 relations de l'allowlist dans `data/reference/ORGANIZATION_SCOPE_ROLES.csv` ;
- [x] ne pas ajouter `FUND_REGULATOR` pour Malawi ;
- [x] ne pas fusionner IRA/URBRA dans un rôle non conforme ;
- [x] vérifier `Institutional Registry` sur Python 3.11/3.12 au HEAD final.

## Task 4 — Clôture

- [x] recalculer les comptes après vague 03 ;
- [x] documenter RED/intermédiaire/GREEN ;
- [x] créer l'attestation de clôture ;
- [x] réaligner STATUS/LOOP/NEXT/HANDOFF/WORK_LOG/TODO/SUIVI/CHANGELOG ;
- [x] conserver `OF-SOURCE-002` en `EN_COURS` ;
- [x] ouvrir la vague 04 en lecture seule sur un nouveau lot contrôlé.

## Closure evidence

```text
RED_HEAD: c7169584b582760a26c708c701c63e77799ff3d8
RED_RUN: 31595214746
INTERMEDIATE_HEAD: f74a482eb375e819419c77697d89c9d74676da2f
INTERMEDIATE_RUN: 31595412831
GREEN_HEAD: 5024a9767b1b9aecf8a6cd52d315ccfbf8384389
GREEN_RUN: 31595575537
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
TESTS: 8 / 8 PASS
COUNTRY_COVERAGE_AFTER: 18 / 54
SEC_ZAMBIA: BLOCKED / ABSENT
RBM_FUND_REGULATOR: NOT_PROVEN / ABSENT
GLOBAL_TASK: OF-SOURCE-002 EN_COURS
NEXT: WAVE_04 READ_ONLY_AUDIT
```
