# OF-SOURCE-002 Institutional Coverage Wave 01 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Commencer `OF-SOURCE-002` sans nouvelle branche en mesurant la couverture institutionnelle réelle puis en intégrant uniquement une première vague d’organisations et de rôles prouvés par des sources officielles.

**Architecture:** Les grands CSV `data/reference/*.csv` restent des inventaires de découverte/revue conformément à ADR-021 ; PostgreSQL reste la vérité runtime après migration gouvernée. Cette vague ne charge aucune donnée historique, ne crée aucun endpoint collecté, ne modifie aucun SQL runtime et ne transforme jamais une recherche web en statut `COLLECTION_TESTED`.

**Tech Stack:** CSV UTF-8 séparateur `;`, Python 3.11/3.12 pour les contrôles, GitHub Actions, PostgreSQL 16 uniquement pour les tests existants qui le nécessitent.

## Global Constraints

- Branche unique autorisée : `architecture/africafunds-country-indicators-v0.1`.
- Ne pas créer de branche ou PR, ne pas travailler sur `main`, ne pas fusionner/retargeter PR #1 ou PR #2.
- Commits fast-forward uniquement.
- `research_queue` et PR #2 sont des preuves/candidats, jamais une source canonique.
- Codes techniques en majuscules, sans accent, underscore comme séparateur.
- `NULL != 0`; aucune date, URL, institution, rôle, série ou statut de collecte inventé.
- `SOURCE_IDENTIFIED/URL_LINKED/VALIDATED` ne signifie jamais `COLLECTION_TESTED` ni `HISTORY_LOADED`.
- Préserver UEMOA/CEMAC au niveau zone et le pays émetteur au niveau souverain.

---

### Task 1: Geler la baseline de couverture institutionnelle

**Files:**
- Read: `data/reference/AFRICA_COUNTRIES.csv`
- Read: `data/reference/ORGANIZATIONS.csv`
- Read: `data/reference/ORGANIZATION_ROLES.csv`
- Read: `data/reference/ORGANIZATION_SCOPE_ROLES.csv`
- Read: `data/reference/SOURCE_ENDPOINTS.csv`
- Create: `docs/00_PROJECT/OF_SOURCE_002_BASELINE_AUDIT_20260812.md`

**Interfaces:**
- Consumes: les 54 pays canoniques et les registres institutionnels existants.
- Produces: une baseline chiffrée, une matrice de lacunes et une allowlist de vague 01.

- [x] **Step 1:** Résoudre le HEAD courant et vérifier qu’il descend sans divergence de la baseline documentaire.
- [x] **Step 2:** Compter les pays ayant au moins une organisation country-scoped, les rôles couverts, les statuts `VALIDATED/PENDING`, et les pays sans organisation propre.
- [x] **Step 3:** Réconcilier les candidats de la PR #2 avec les codes existants et classifier les collisions.
- [x] **Step 4:** Vérifier chaque organisation de l’allowlist sur une source officielle primaire actuelle.
- [x] **Step 5:** Écrire le rapport daté sans modifier les registres canoniques.

### Task 2: Ajouter un validateur exécutable des registres institutionnels

**Files:**
- Create: `scripts/validate_institutional_registry.py`
- Create: `tests/test_institutional_registry.py`
- Create: `.github/workflows/institutional-registry.yml`

**Interfaces:**
- Consumes: `AFRICA_COUNTRIES.csv`, `ORGANIZATIONS.csv`, `ORGANIZATION_ROLES.csv`, `ORGANIZATION_SCOPE_ROLES.csv`, `SOURCE_ENDPOINTS.csv`.
- Produces: contrôle déterministe des codes, doublons, FK logiques, scopes, statuts et URLs requises pour les objets validés.

- [x] **Step 1: RED:** ajouter les tests d’unicité, uppercase/no-accent, FK organisation→rôle/scope, scope country/zone et présence d’URL pour les organisations/endpoints `VALIDATED`.
- [x] **Step 2:** Exécuter la CI et confirmer que le test de couverture de l’allowlist échoue tant que les nouvelles organisations ne sont pas intégrées.
- [x] **Step 3: GREEN:** implémenter le validateur minimal et son workflow Python 3.11/3.12.
- [x] **Step 4:** Confirmer que les invariants existants passent et que seule l’absence attendue de la vague 01 reste rouge.

### Task 3: Intégrer les organisations vérifiées de la vague 01

**Files:**
- Modify: `data/reference/ORGANIZATIONS.csv`
- Test: `tests/test_institutional_registry.py`

**Interfaces:**
- Consumes: allowlist du rapport de Task 1 et preuves officielles.
- Produces: organisations de découverte/revue sans prétention de persistance runtime.

- [x] **Step 1:** Ajouter seulement les codes absents et prouvés : Botswana, Namibie, Éthiopie, AMF-UMOA, UMOA-Titres, COSUMAF selon l’allowlist finale.
- [x] **Step 2:** Conserver `VALIDATED` uniquement quand identité + rôle principal + domaine officiel sont prouvés ; sinon `PENDING`.
- [x] **Step 3:** Vérifier absence de doublon/code collision et exécuter le validateur.

### Task 4: Intégrer les relations organisation-rôle-périmètre prouvées

**Files:**
- Modify: `data/reference/ORGANIZATION_SCOPE_ROLES.csv`
- Test: `tests/test_institutional_registry.py`

**Interfaces:**
- Consumes: organisations de Task 3 et rôles existants de `ORGANIZATION_ROLES.csv`.
- Produces: relations explicites pays/zone sans inventer de rôle.

- [x] **Step 1:** Ajouter les relations prouvées `CENTRAL_BANK`, `STOCK_EXCHANGE`, `CAPITAL_MARKET_REGULATOR`, `FUND_REGULATOR`, `INSURANCE_PENSION_REGULATOR`, `STATISTICS_OFFICE`, `GOVERNMENT_SECURITIES_AGENCY` selon les sources officielles.
- [x] **Step 2:** Ne pas ajouter `INDEX_PROVIDER`, `FX_REFERENCE_RATE_PROVIDER`, ministère/dette/assurance ou autre rôle non prouvé par la source contrôlée.
- [x] **Step 3:** Exécuter le validateur et vérifier toutes les FK/scopes.

### Task 5: Clôturer la vague et préparer la suivante

**Files:**
- Modify: `TODO.md`
- Modify: `SUIVI.md`
- Modify: `STATUS.md`
- Modify: `LOOP_STATE.md`
- Modify: `CURRENT_ITERATION.md`
- Modify: `WORK_LOG.md`
- Modify: `NEXT_ACTION.md`
- Modify: `HANDOFF.md`
- Modify: `CHANGELOG.md`
- Create: `docs/00_PROJECT/OF_SOURCE_002_WAVE_01_COMPLETION_20260812.md`

**Interfaces:**
- Consumes: CI de la vague 01 et inventaire restant.
- Produces: statut exact `OF-SOURCE-002` (qui reste `EN_COURS` tant que les 54 pays ne satisfont pas les critères), preuve de ce qui a été ajouté, liste des pays/rôles restant à rechercher.

- [x] **Step 1:** Revalider le HEAD et les workflows déclenchés.
- [x] **Step 2:** Documenter faits, preuves, limites, risques et couverture restante.
- [x] **Step 3:** Laisser `OF-SOURCE-002` en `EN_COURS` sauf si les 54 pays et tous les rôles exigés sont réellement couverts.
- [x] **Step 4:** Fixer la prochaine vague en lecture seule avant toute nouvelle écriture.

## Closure evidence

```text
WAVE_01_DATA_HEAD: 1f85c0df1878743f4a2ac322c2087b0b1a549641
GREEN_RUN: 31592700354
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
TESTS: 4 / 4 PASS
GLOBAL_TASK: OF-SOURCE-002 EN_COURS
NEXT: WAVE_02 READ_ONLY_AUDIT
```
