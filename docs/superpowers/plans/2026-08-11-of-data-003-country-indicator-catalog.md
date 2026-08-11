# OF-DATA-003 Country Indicator Catalogue Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Centraliser exactement les 420 définitions D00–D17 dans un catalogue machine-readable gouverné, sans inventer les champs absents ni confondre définition, source, collecte, historique chargé et produit calculé.

**Architecture:** Migration mirror-first en deux temps. Les sept Markdown historiques sont des sources de bootstrap/fidélité figées ; un paquet JSON versionné devient ensuite la source d’authoring unique. Les vues JSON expansée, CSV `;`, Markdown exhaustive et SQL seed sont générées de façon déterministe et vérifiées contre les sources historiques.

**Tech Stack:** Python 3.11/3.12 standard library, JSON, CSV UTF-8 `;`, Markdown, PostgreSQL seed SQL, GitHub Actions.

## Global Constraints

- Branche unique autorisée : `architecture/africafunds-country-indicators-v0.1`.
- Ne pas créer de branche ou de PR ; ne pas merger, retargeter ou modifier `main`.
- Baseline autorisée au démarrage : `145461e04ba9affd2b11fedaf56ed4ad49171b5d` ; tout nouveau HEAD doit être un descendant fast-forward de cette baseline.
- Option A validée : mirror-first, zéro invention, valeur absente = `null` + statut explicite.
- Le catalogue doit contenir exactement 18 domaines et 420 définitions ; les codes canoniques doivent être uniques.
- `RAW`, `METADATA`, `EVENT`, `CALCULATED` est une classification gouvernée séparée ; elle ne doit pas réécrire la nature source.
- `target_history` exprime une exigence de couverture, jamais une preuve d’historique chargé.
- `CANONICAL_INDICATOR_CODE`, code de mapping métier et `PROVIDER_SERIES_CODE` restent distincts.
- Aucune donnée réelle, observation, historique, secret ou configuration de production n’est importé.
- Le SQL produit est un seed gouverné et testé ; aucune application PostgreSQL de production n’est autorisée dans cette boucle.
- `NULL`, `UNKNOWN`, `NOT_AUTHORED`, `NOT_APPLICABLE` et zéro restent distincts.

---

### Task 1: Freeze the legacy contract and bootstrap parser

**Files:**
- Create: `scripts/country_indicator_catalog.py`
- Create: `tests/test_country_indicator_catalog.py`

**Interfaces:**
- Consumes: les sept fichiers sous `docs/04_DATA_GOVERNANCE/indicator_catalog/`.
- Produces: `parse_legacy_catalog(root) -> list[dict]`, `validate_catalog(catalog)`, `render_authoring_package(catalog)`.

- [ ] **Step 1: Write failing tests** vérifiant les sept sources, 18 domaines, le décompte exact par domaine, 420 lignes et l’unicité de tous les codes.
- [ ] **Step 2: Verify tests fail** avant création du parseur.
- [ ] **Step 3: Implement strict Markdown parsing** sans traduction ni normalisation destructive ; conserver texte, fréquence, unité, source préférée, usages, benchmark, priorité, historique et colonnes D00 supplémentaires.
- [ ] **Step 4: Encode absence explicitly** : valeurs non présentes = `null`, accompagnées de statuts `NOT_AUTHORED` lorsque requis.
- [ ] **Step 5: Verify tests pass** et que toute variation de compte/colonne/source échoue.

### Task 2: Create the governed machine-readable authoring package

**Files:**
- Create: `data/indicator_catalog/v1/00_metadata.json`
- Create: `data/indicator_catalog/v1/catalog.json`
- Create: `data/indicator_catalog/country-indicator-catalog-v1.schema.json`

**Interfaces:**
- Consumes: sortie bootstrap validée de Task 1.
- Produces: source d’authoring unique version `1.0.0`, 18 domaines / 420 objets.

- [ ] **Step 1: Bootstrap exactly from legacy sources** ; aucune définition ou traduction nouvelle.
- [ ] **Step 2: Store provenance per object** : fichier source, domaine, code et hash/source locator déterministe.
- [ ] **Step 3: Separate source and governed semantics** avec `source_nature` et `canonical_nature` ; lorsqu’une classification gouvernée n’est pas explicitement décidée, utiliser `null` + `NOT_AUTHORED`.
- [ ] **Step 4: Store independent evidence states** : `definition_status`, `source_mapping_status`, `collection_spec_status`, `collection_test_status`, `history_status`, `calculation_status`.
- [ ] **Step 5: Validate JSON package** contre le schéma logique et le snapshot legacy.

### Task 3: Deterministic generated views and SQL seed

**Files:**
- Create: `scripts/generate_country_indicator_catalog.py`
- Generated only: `build/indicator_catalog/COUNTRY_INDICATOR_CATALOG_V1.json`
- Generated only: `build/indicator_catalog/COUNTRY_INDICATOR_CATALOG_V1.csv`
- Generated only: `build/indicator_catalog/COUNTRY_INDICATOR_CATALOG_V1.md`
- Generated only: `build/indicator_catalog/COUNTRY_INDICATOR_CATALOG_V1.sql`
- Create: `data/indicator_catalog/COUNTRY_INDICATOR_CATALOG_MANIFEST_V1.json`

**Interfaces:**
- Consumes: `data/indicator_catalog/v1/`.
- Produces: quatre vues reproductibles et leurs SHA-256.

- [ ] **Step 1: Write tests for deterministic ordering and CSV delimiter `;`.**
- [ ] **Step 2: Generate exhaustive Markdown** par D00–D17 depuis le JSON master.
- [ ] **Step 3: Generate SQL seed** créant/peuplant uniquement les objets catalogue requis de manière additive/idempotente, sans observations ni données pays.
- [ ] **Step 4: Generate manifest checksums** et faire échouer `--check-manifest` sur toute dérive.
- [ ] **Step 5: Verify two consecutive generations are byte-identical.**

### Task 4: PostgreSQL governance without deployment

**Files:**
- Create: `schemas/reference/016_country_indicator_catalog.sql`
- Modify: `migrations/manifest.json`
- Test: `tests/test_country_indicator_catalog.py`

**Interfaces:**
- Consumes: seed généré depuis le master.
- Produces: migration gouvernée additive `016_COUNTRY_INDICATOR_CATALOG` avec tables de définition uniquement.

- [ ] **Step 1: Test migration shape first** : aucune commande destructive, aucune observation, aucune donnée pays, aucune transaction embarquée.
- [ ] **Step 2: Define `ref.indicator_domain` and `ref.indicator_definition`** avec code stable, sémantique source, statuts et contraintes d’unicité.
- [ ] **Step 3: Seed exactly 18 domains and 420 definitions** depuis le générateur ; `ON CONFLICT` ne doit jamais masquer une collision sémantique.
- [ ] **Step 4: Add migration to governed manifest at order 160** avec mode généré/frozen selon la politique existante.
- [ ] **Step 5: Verify migration materialization and runner plan** sans connexion production.

### Task 5: CI, documentation and handoff

**Files:**
- Create: `.github/workflows/country-indicator-catalog.yml`
- Create: `docs/01_ARCHITECTURE/ADR-032_COUNTRY_INDICATOR_CATALOG_MIRROR_FIRST.md`
- Create: `docs/04_DATA_GOVERNANCE/COUNTRY_INDICATOR_CATALOG_V1.md`
- Modify: `docs/04_DATA_GOVERNANCE/Africa_Country_Indicator_Framework_v0.1.md`
- Modify: `TODO.md`
- Modify: `SUIVI.md`
- Modify: `NEXT_ACTION.md`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: package, generator, tests and migration.
- Produces: workflow Python 3.11/3.12, artefacts de revue et point de reprise exact.

- [ ] **Step 1: CI runs generation + manifest check + unit tests on Python 3.11 and 3.12.**
- [ ] **Step 2: CI uploads JSON/CSV/Markdown/SQL build views** for review.
- [ ] **Step 3: Document source-of-truth transition** : Markdown historiques = bootstrap/audit ; JSON v1 = authoring authority ; build = derived.
- [ ] **Step 4: Mark `OF-DATA-003` complete only after CI success** et ne démarrer aucune tâche suivante automatiquement dans la même clôture.
- [ ] **Step 5: Record dynamic HEAD policy and exact restart gate** pour la prochaine boucle.

## Self-review

- Spec coverage: 420 objets, unicité, nature séparée, unité/fréquence/source/usages/statuts, Markdown, SQL, tests et CI sont couverts.
- No placeholders: aucune étape ne dépend d’un contenu `TBD` ou d’une invention métier.
- Type consistency: `catalog.json` est l’unique authoring authority après bootstrap ; toutes les sorties et le SQL dérivent de ce fichier.
- Safety: aucune observation réelle ni production n’est touchée ; `main`, PR2 et les branches sont hors scope.
