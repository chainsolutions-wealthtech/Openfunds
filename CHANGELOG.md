# CHANGELOG OPENFUNDS

Toutes les modifications importantes du projet sont consignées ici. Les commits Git restent la source détaillée des changements fichier par fichier.

## [UNRELEASED]

### A décider

- mapping champ-par-champ Openfunds v2.13.0 → modèle canonique (`OF-MAP-002`) sur l'inventaire officiel désormais verrouillé ;
- PostgreSQL persistant et stockage brut immuable ;
- complétude des institutions et mappings sources des 54 pays ;
- méthodologies WTI Bench, risque sans risque et MAR encore ouvertes.

### Limites connues

- PR #1 non fusionnée ;
- branche `main` minimale ;
- PostgreSQL persistant non configuré ;
- stockage brut permanent absent ;
- historique FX limité à un snapshot validé par zone ;
- mapping Openfunds champ-par-champ encore incomplet (`OF-MAP-001` terminé, `OF-MAP-002` en cours) ;
- API et produits analytiques actifs non implémentés.

## [2026-08-17] — TAXONOMIE POSTGRESQL, OPENFUNDS ET COUVERTURE INSTITUTIONNELLE

### Taxonomie

- générateur SQL déterministe et migration `017_CANONICAL_FUND_TAXONOMY_V0_1` ordre 170 ;
- snapshot source V0.1 immuable avec SHA-256 ;
- 4 classes, 7 sous-classes, 54 routages, 9 templates, 11 overrides, 25 exigences analytiques ;
- Python 3.11/3.12 GREEN ;
- PostgreSQL 16 : chaîne 001→017, ledger, contrat runtime et seconde application idempotente GREEN ;
- run `Canonical Taxonomy Migration` `32058160324` SUCCESS ;
- ADR-029 et rapport de clôture ajoutés ;
- statuts fonctionnels conservés : `STRUCTURE_PREFILLED` / `NOT_ACTIVE`.

### OF-SOURCE-002

- Waves 02 à 12 poursuivies sous TDD ;
- 53/54 pays country-scoped, 141 organisations, 199 relations organisation-rôle = 178 `VALIDATED` + 21 `PENDING` ;
- Waves 10–12 : 12 rôles institutionnels, 3 bourses et 4 fournisseurs d'indices promus sans création ni retargeting ;
- résiduel exact : 9 FX, 5 index providers, 3 monetary unions, 2 supranational authorities, 2 interbank operators ;
- Érythrée volontairement non peuplée sans preuve primaire officielle actuelle.

### Openfunds

- v2.13.0 et licence `CC BY-ND 4.0` vérifiées ;
- Field List officiel FINAL de 745 pages archivé byte-identical (2 957 096 octets) ;
- SHA256 verrouillé : `40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4` ;
- parser checksum-gated `scripts/parse_openfunds_v2_13_0.py` vérifié Python 3.11/3.12 et sur le document réel ;
- inventaire exact : 1 869 OF-ID uniques = 1 849 concrets + 20 templates pays `XX` ;
- `OF-MAP-001` terminé ; `OF-MAP-002` devient le chantier actif.

### Non activé

- aucun WTI/WTI Bench live, aucun benchmark/RFR/MAR promu, aucune production persistante, aucun merge/retargeting/déploiement/main mutation.

## [2026-08-12] — OF-SOURCE-002 VAGUE 01 — COUVERTURE INSTITUTIONNELLE

### Audité

- les 54 pays canoniques et les registres `ORGANIZATIONS`, `ORGANIZATION_ROLES`, `ORGANIZATION_SCOPE_ROLES` et `SOURCE_ENDPOINTS` ;
- baseline : 40 organisations, 70 relations organisation-rôle, 43 endpoints et 7/54 pays avec au moins une organisation country-scoped ;
- les actifs de recherche de la PR nº2 ont été relus sans la modifier ;
- les candidats ont été réconciliés avec les codes existants puis vérifiés sur des sources institutionnelles officielles primaires.

### Ajouté

- `docs/superpowers/plans/2026-08-12-of-source-002-institutional-coverage-wave-01.md` ;
- `docs/00_PROJECT/OF_SOURCE_002_BASELINE_AUDIT_20260812.md` ;
- `docs/00_PROJECT/OF_SOURCE_002_WAVE_01_COMPLETION_20260812.md` ;
- `scripts/validate_institutional_registry.py` ;
- `tests/test_institutional_registry.py` ;
- workflow `.github/workflows/institutional-registry.yml` ;
- 15 organisations vérifiées : BOB, NBFIRA, BSE, STATISTICS_BOTSWANA, BON, NAMFISA, NSX, NSA_NAMIBIA, NBE, ECMA, ESX, ESS_ETHIOPIA, AMF_UMOA, UMOA_TITRES et COSUMAF ;
- 22 relations organisation-rôle vérifiées pour banque centrale, régulation marché/fonds, assurance/pension, bourse, statistiques et titres publics.

### TDD et vérification

```text
RED_INITIAL_RUN: 31592435103 — FAILURE attendu
INTERMEDIATE_RUN: 31592516832 — VALIDATOR PASS / ALLOWLIST FAIL attendu
GREEN_FINAL_RUN: 31592700354 — SUCCESS
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
TESTS: 4 / 4 PASS
```

### État après vague 01

```text
ORGANIZATIONS: 55 = 35 VALIDATED + 20 PENDING
COUNTRIES_WITH_COUNTRY_SCOPED_ORGANIZATION: 10 / 54
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 44
ORGANIZATION_SCOPE_ROLES: 92 = 48 VALIDATED + 44 PENDING
SOURCE_ENDPOINTS: 43 UNCHANGED
```

### Gouvernance et limites

- `OF-SOURCE-002` reste `EN_COURS` ;
- `FMDQ` reste hors allowlist jusqu'à arbitrage de son rôle canonique ;
- les grands CSV institutionnels restent des inventaires de découverte/revue conformément à ADR-021 ;
- aucune migration runtime, aucun endpoint spécialisé, provider series, collection specification, historique, base persistante, branche, PR, merge, retargeting ou déploiement n'a été créé ;
- la vague 02 est ouverte en `READ_ONLY_AUDIT` sur les 44 pays non couverts et les rôles manquants des 10 pays présents.

## [2026-08-11] — OF-DATA-003 CATALOGUE D00-D17 GOUVERNE

### Décidé

- Option A `MIRROR_FIRST` : les sept Markdown historiques restent des sources de bootstrap/audit et le paquet JSON `data/indicator_catalog/v1/` devient l’autorité d’authoring ;
- les valeurs absentes restent `null` avec statut explicite ;
- `source_nature` et `canonical_nature` sont séparés ;
- la classification `RAW / METADATA / EVENT / CALCULATED` est une décision de gouvernance versionnée, pas une assertion fournisseur ;
- `target_history` ne prouve jamais qu’un historique est chargé.

### Ajouté

- 19 fichiers d’authoring (`00_metadata.json` + D00 à D17) ;
- JSON Schema du catalogue ;
- générateur déterministe JSON/CSV `;`/Markdown/SQL ;
- manifeste SHA-256 ;
- migration gouvernée `016_COUNTRY_INDICATOR_CATALOG` ;
- tests contractuels et workflow Python 3.11/3.12 ;
- ADR-032, documentation de gouvernance et rapport de clôture.

### Vérifié

- 18 domaines / 420 codes uniques ;
- 298 `RAW`, 85 `METADATA`, 7 `EVENT`, 30 `CALCULATED` ;
- aucun historique chargé revendiqué ;
- run catalogue `31484468846` : `SUCCESS` ;
- run migrations `31484586710` : `SUCCESS` ;
- double application PostgreSQL 16, vérification runtime et scénario d’adoption sans ledger : `SUCCESS`.

### Corrigé

- suppression d’une mutation CI du paquet d’authoring avant génération du manifeste ;
- découplage du test Fund/SubFund/ShareClass de la position globale de la migration `015`.

### Non réalisé

- aucune production persistante ;
- aucune observation ou histoire pays chargée ;
- aucun mapping officiel Openfunds inventé ;
- aucun merge, retargeting, nouvelle branche, nouvelle PR ou déploiement.

## [2026-08-03] — CONSOLIDATION DOCUMENTAIRE

### Ajouté

- audit complet des 95 fichiers de la branche ;
- matrice de 45 écarts entre conversation, décisions et dépôt ;
- `TODO.md` avec tâches `OF-*`, dépendances et critères d'acceptation ;
- `SUIVI.md` avec réalisations, décisions, risques et point exact de reprise ;
- `DECISIONS.md` avec ADR-001 à ADR-025 ;
- `ARCHITECTURE.md` ;
- `DATA_MODEL.md` ;
- `DATA_DICTIONARY.md` ;
- `OPENFUNDS_MAPPING.md` ;
- `GOVERNANCE.md` ;
- `QUALITY_RULES.md` ;
- `SOURCE_REGISTRY.md` ;
- `ROADMAP.md` ;
- `CHANGELOG.md`.

### Modifié

- remplacement du README minimal par un guide complet ;
- documentation des commandes réellement utilisées par les workflows ;
- distinction explicite entre architecture, référentiel, mapping, collecte, historique, calcul et production.

### Corrigé

- clarification que les 420 définitions ne sont pas 420 séries historiques par pays ;
- clarification que les pilotes FX sont `COLLECTION_TESTED` et non des historiques complets ;
- identification des divergences CSV/SQL et des modèles d'endpoints concurrents ;
- documentation transparente de la PR #3 accidentelle, immédiatement fermée sans fusion ni modification de fichier.

## [2026-08-03] — PIPELINE QUOTIDIEN FX

### Ajouté

- `pipelines/fx_daily.py` ;
- orchestration BCEAO_XOF et BEAC_XAF ;
- manifeste de couverture par source ;
- persistance PostgreSQL optionnelle ;
- workflow `Daily Africa FX Staging` ;
- politique de staging et persistance ;
- tests unitaires de l'orchestrateur.

### Validé

- collecte double source ;
- quatre paires canoniques : XOF_EUR, XOF_USD, XAF_EUR, XAF_USD ;
- statut honnête `STAGING_ONLY_DATABASE_NOT_CONFIGURED` sans secret de production ;
- artefacts temporaires GitHub Actions.

## [2026-08-03] — BEAC FX

### Ajouté

- collecteur BEAC ;
- parsing des blocs `div.taux_de_change` ;
- fallback tableau ;
- profil de chargement `BEAC_XAF` ;
- seed CEMAC/BEAC ;
- migration parseur 0.2.0 ;
- migration de validation live ;
- workflow live et fixture réaliste.

### Validé

- 13 paires observées ;
- date de valeur ;
- SHA256 ;
- buy et sell distincts ;
- XAF_EUR et XAF_USD calculés ;
- six observations PostgreSQL ;
- double chargement idempotent ;
- absence de mélange XOF/XAF.

### Corrigé

- adaptation du parseur après inspection de l'artefact réel ;
- correction documentaire du taux XAF_USD.

## [2026-08-03] — BCEAO FX

### Ajouté

- collecteur BCEAO ;
- parsing HTML, dates françaises et nombres localisés ;
- transformation canonique XOF ;
- seed UEMOA/BCEAO ;
- workflow live ;
- preuve de collecte.

### Validé

- date de valeur ;
- SHA256 ;
- EUR/USD présents ;
- XOF_EUR et XOF_USD ;
- chargement PostgreSQL idempotent.

## [2026-08-03] — CHARGEUR ET SCHEMAS DE SOURCES

### Ajouté

- chargeur PostgreSQL multi-profils ;
- tables de runs, artefacts, séries et spécifications ;
- lignée FX observée/calculée ;
- vues d'observations courantes ;
- tests PostgreSQL 16 ;
- migration de réconciliation des endpoints.

### Corrigé

- suppression robuste d'une ancienne contrainte unique tronquée par PostgreSQL ;
- compatibilité des deux ordres de création 003/004 ;
- endpoint `PENDING` autorisé sans URL vérifiée ;
- conflits de types et de colonnes détectés par les tests.

## [2026-08-03] — REFERENTIELS AFRICAINS

### Ajouté

- 54 pays ;
- 1 continent et 5 régions ;
- UEMOA, CEMAC et CMA ;
- 266 relations pays ;
- 44 devises ;
- 84 paires locale→EUR/USD ;
- organisations, rôles et périmètres initiaux ;
- endpoints, mappings, séries et spécifications initiaux ;
- cadre D00-D17 ;
- pilotes Maroc et Tunisie ;
- modèle relationnel pays-indicateur.

### Documentation

- règles de conversion quotidienne ;
- modèles organisations/sources ;
- workflow de collecte ;
- plans de benchmarks et règles qualité.

## [2026-07-31] — FONDATION ARCHITECTURALE

### Décidé

- modèle canonique interne plus riche qu'openfunds ;
- PostgreSQL comme source de vérité ;
- API-first ;
- Atomic Design comme présentation ;
- historisation bitemporelle ;
- provenance complète ;
- séparation raw/validation/canonique/calcul/API/UI ;
- quatre rôles de référence ;
- WTI distinct du WTI Bench ;
- niveaux national, régional et Afrique.

## [2026-08-04] — BASELINE GITHUB ET HANDOFF DOCUMENTAIRE

### Ajouté

- `docs/00_PROJECT/BRANCH_INVENTORY_AND_EXPLOITATION_PLAN.md` ;
- `docs/00_PROJECT/GITHUB_BASELINE_AUDIT_20260804.md` ;
- `docs/00_PROJECT/BRANCH_INVENTORY_20260804.csv` ;
- `docs/00_PROJECT/BOOTSTRAP_INTEGRATION_ASSESSMENT_20260804.md` ;
- `docs/00_PROJECT/PR_CONTENT_RECONCILIATION_20260804.csv` ;
- `docs/00_PROJECT/CANONICAL_PROJECT_STATE_20260804.md` ;
- `docs/00_PROJECT/OPEN_DECISIONS_AND_EXECUTION_GATES_20260804.md` ;
- `docs/00_PROJECT/ISSUE_MIGRATION_DRAFT_20260804.csv` ;
- `docs/00_PROJECT/HANDOFF_TO_NEXT_AGENT_20260804.md`.

### Vérifié

- le HEAD de la branche de travail correspondait au SHA de contrôle `cce82f3276d408ddb71366f5236c10282f0b6614` ;
- les douze branches ont été inventoriées sans modification ;
- les treize actifs du bootstrap ont le même SHA de blob dans la branche complète ;
- la PR nº 1 reste ouverte, en brouillon et non fusionnée ;
- la PR nº 2 reste ouverte, en brouillon et non fusionnée ;
- les deux CSV de la PR nº 2 sont préservés exactement dans `research_queue` ;
- trois documents Markdown détaillés de la PR nº 2 restent uniques ou seulement résumés.

### Statuts corrigés

- la PR nº 1 comptait alors 122 fichiers modifiés ; les chiffres 95 et 104 restent conservés comme états historiques ;
- la taxonomie, les 486 règles de routage et les 432 catégories/blocs sont `STRUCTURE_PRESENT / TESTED / NOT_ACTIVE` ;
- WTI, WTI Bench, ratios, classements et historiques complets restent non actifs ;
- le classeur Excel reste un export dérivé non canonique dont la reproductibilité complète demeure une porte ouverte.

### Non modifié

- aucune branche ou PR ;
- aucune issue ;
- aucun workflow ;
- aucun code, SQL, donnée canonique/de référence, générateur ou test ;
- aucun environnement, secret ou déploiement.

## [2026-08-05] — ARCHITECTURE GATES ET LOOP ENGINEERING

### Vérifié

```text
OF-ARCH-001   VERIFIED_COMPLETE
OF-SOURCE-001 VERIFIED_COMPLETE
OF-ARCH-002   VERIFIED_COMPLETE
OF-ARCH-003   VERIFIED_COMPLETE
OF-ARCH-004   IMPLEMENTED_WITH_OPEN_GOVERNANCE_BLOCKER
```

- source d'authoring compacte des pilotes FX, endpoint runtime canonique et dates métier explicites ;
- runner de 14 migrations et run PostgreSQL 16 réussi ;
- blocker de gouvernance maintenu pour l'immuabilité de la migration générée `012` ;
- PR nº 1 toujours draft, non fusionnée et non fusionnable dans sa base observée ;
- PR nº 2 non modifiée, trois Markdown uniques toujours à décider.

### Ajouté — OF-DOC-003

- standard Loop Engineering complet et 176 chemins Markdown ;
- `00_START_HERE.md`, `AGENTS.md`, `SOURCE_OF_TRUTH.md`, mémoire de boucle et handoff ;
- `DOCUMENT_INTEGRATION_MATRIX.md` ;
- catalogue, manifest, politiques, registres, modèles et fichiers conditionnels ;
- `docs/00_PROJECT/PERMANENT_DOCUMENT_RECONCILIATION_20260805.md`.

### Limites

Cette intégration est documentaire. Elle ne modifie pas la migration `012`, ne commence pas `OF-DATA-001`, ne rend pas la PR nº 1 fusionnable et n'effectue aucun déploiement.
