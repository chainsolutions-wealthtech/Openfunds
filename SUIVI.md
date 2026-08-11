# SUIVI — JOURNAL DE CONTINUITE DU PROJET OPENFUNDS

Dernière mise à jour : `2026-08-11`  
Branche : `architecture/africafunds-country-indicators-v0.1`  
PR principale : `#1` — brouillon, ouverte, fusionnable, non fusionnée.

## 1. ETAT GENERAL DU PROJET

### Objectif

Construire un référentiel canonique des fonds d'investissement et des données financières africaines, plus riche qu'openfunds, avec mapping explicite vers les standards externes.

```text
SOURCES BRUTES
→ NORMALISATION
→ VALIDATION
→ OBJETS CANONIQUES
→ HISTORISATION ET PROVENANCE
→ CALCULS
→ API
→ VIEW MODELS
→ ATOMIC DESIGN
```

### Périmètre réel actuel

- géographie africaine, devises et zones de marché ;
- cadre D00-D17 des indicateurs pays ;
- organisations, rôles, endpoints, mappings et séries initiales ;
- modèle fonds/taxonomie encore en brouillon ;
- collecteurs BCEAO et BEAC FX ;
- transformations XOF/XAF vers EUR/USD ;
- lignée et chargeur PostgreSQL idempotent ;
- workflow quotidien double source en staging ;
- documentation permanente et gouvernance consolidées.

### Etat synthétique

```text
DOCUMENTATION PERMANENTE                 TERMINEE
ARCHITECTURE ET PRINCIPES                DOCUMENTES
REFERENTIELS GEOGRAPHIQUES               STRUCTURELLEMENT PEUPLES
ORGANISATIONS ET SOURCES                 PARTIELLEMENT PEUPLEES
CATALOGUE D00-D17                        CENTRALISE JSON / TESTE / MIGRATION 016
BCEAO FX / BEAC FX                       COLLECTION_TESTED
HISTORIQUE DURABLE MULTI-DATES           NON
MODELE FUND/SUBFUND/SHARECLASS           VERIFIED_COMPLETE
DICTIONNAIRE MACHINE-READABLE            FUND CORE + D00-D17 GOUVERNES
MAPPING OPENFUNDS                        ABSENT
CATEGORIES / BLOCS DE REFERENCE          NON GENERES
WTI / WTI BENCH / METRIQUES              NON CALCULES
API / FRONTEND                           NON IMPLEMENTES
PRODUCTION PERSISTANTE                   NON CONFIGUREE
```

### Niveau d'inventaire

- audit initial avant consolidation : 95 fichiers ;
- état post-consolidation : 104 fichiers dans la comparaison avec `main` ;
- PR #1 : 104 fichiers modifiés, dont 103 ajouts et le README remplacé.

## 2. REALISATIONS

### 2.1 Architecture canonique

- **Période :** 2026-07-31 au 2026-08-03
- **Résultat :** PostgreSQL source de vérité, architecture API-first, Atomic Design de présentation, séparation raw/validation/canonique/calcul/API/UI, bitemporalité et provenance.
- **Fichiers :** `ARCHITECTURE.md`, `DATA_MODEL.md`, ADR historique et modèles SQL.
- **Limite :** modèle fonds final non stabilisé.

### 2.2 Géographie et devises

- **Résultat :** 54 pays, 1 continent, 5 régions, UEMOA/CEMAC/CMA, 266 relations, 44 devises et 84 paires locale→EUR/USD.
- **Fichiers :** `data/reference/AFRICA_*`, `MARKET_ZONES.csv`, `COUNTRY_RELATIONSHIPS.csv`, `CURRENCIES.csv`, `FX_PAIRS.csv`.
- **Limite :** validation officielle et dates historiques partielles.

### 2.3 Organisations et sources

- **Résultat :** 21 rôles, 40 organisations, 70 affectations de rôle, 43 endpoints, 55 mappings, 50 séries et 17 spécifications/templates.
- **Tests :** modèle d'endpoint testé dans les ordres 003/004 et migration 007 rejouable.
- **Limite :** couverture pays partielle et divergence CSV/SQL.

### 2.4 BCEAO FX

- **Résultat :** source live, artefact SHA256, date de valeur, buy/sell, XOF_EUR et XOF_USD, chargement idempotent.
- **Tests :** fixture, live smoke, PostgreSQL 16, double chargement.
- **Limite :** snapshot unique et stockage éphémère du workflow.

### 2.5 BEAC FX

- **Résultat :** parsing de 13 blocs de change, date de valeur, buy/sell, XAF_EUR et XAF_USD, séparation XOF/XAF.
- **Tests :** fixture réaliste, live smoke, PostgreSQL 16, idempotence.
- **Limite :** snapshot unique et stockage éphémère.

### 2.6 Pipeline quotidien FX

- **Résultat :** orchestration BCEAO + BEAC, quatre taux canoniques, manifeste de couverture, persistance optionnelle.
- **Premier statut sans base persistante :** `STAGING_ONLY_DATABASE_NOT_CONFIGURED`.
- **Limite :** artefacts Actions temporaires et schedule durable uniquement après fusion sur la branche par défaut.

### 2.7 Cadre pays D00-D17

- **Résultat :** 18 domaines et environ 420 définitions documentées ; modèle relationnel évitant une table pays de 420 colonnes.
- **Limite :** aucun catalogue machine-readable unique ni matrice 54×420 chargée en base.

### 2.8 Consolidation documentaire

- **Tâche :** `OF-DOC-001`
- **Statut :** TERMINE
- **Livrables :**
  - `README.md` ;
  - `TODO.md` ;
  - `SUIVI.md` ;
  - `DECISIONS.md` ;
  - `ARCHITECTURE.md` ;
  - `DATA_MODEL.md` ;
  - `DATA_DICTIONARY.md` ;
  - `OPENFUNDS_MAPPING.md` ;
  - `GOVERNANCE.md` ;
  - `QUALITY_RULES.md` ;
  - `SOURCE_REGISTRY.md` ;
  - `ROADMAP.md` ;
  - `CHANGELOG.md` ;
  - audit du dépôt ;
  - matrice de 45 écarts.
- **Contrôles :** description PR corrigée, inventaire recalculé, cinq workflows verts.

## 3. DECISIONS VALIDEES

Le détail est dans `DECISIONS.md`.

| ID | Décision | Statut |
|---|---|---|
| ADR-001 | modèle canonique interne | ACCEPTE |
| ADR-002 | openfunds comme couche de mapping | ACCEPTE |
| ADR-003 | PostgreSQL source de vérité | ACCEPTE |
| ADR-004 | API-first et Atomic Design | ACCEPTE |
| ADR-005 | séparation des couches | ACCEPTE |
| ADR-006 | conservation des artefacts bruts | ACCEPTE |
| ADR-007 | historisation bitemporelle | ACCEPTE |
| ADR-008 | identité distincte des noms | ACCEPTE |
| ADR-009 | séparation Fund/SubFund/ShareClass | PRINCIPE ACCEPTE, IMPLEMENTATION A REVOIR |
| ADR-010 | pays comme racine nationale | ACCEPTE |
| ADR-011 | géographie et zones de marché en parallèle | ACCEPTE |
| ADR-012 | codes techniques normalisés | ACCEPTE |
| ADR-013 | quatre rôles de référence | ACCEPTE |
| ADR-014 | WTI fondé sur les pairs observés | ACCEPTE |
| ADR-015 | WTI Bench indépendant | ACCEPTE |
| ADR-016 | observations locale/EUR/USD | ACCEPTE |
| ADR-017 | recalcul régional/Afrique | ACCEPTE |
| ADR-018 | observé distinct de calculé | ACCEPTE |
| ADR-019 | null différent de zéro | ACCEPTE |
| ADR-020 | validation progressive | ACCEPTE |

## 4. PROPOSITIONS NON ENCORE VALIDEES

| ID | Proposition | Validation attendue |
|---|---|---|
| ADR-021 | source de vérité unique CSV/SQL | choisir CSV, PostgreSQL ou manifeste maître |
| ADR-022 | date métier inconnue explicite | approuver nullabilité et statut de connaissance |
| ADR-023 | migration runner gouverné | choisir outil et politique |
| ADR-024 | catalogue canonique machine-readable | choisir format maître |
| ADR-025 | persistance avant statut historique | configurer DB et stockage immuable |
| PROP-WTI-FLEX | méthode pour fonds flexibles | allocation/règle à valider |
| PROP-MONEY-BENCH | benchmark monétaire | hiérarchie des sources et instruments |

Ces propositions ne doivent pas être implémentées comme décisions acquises sans validation.

## 5. AMELIORATIONS APPORTEES

- séparation organisation/rôle/périmètre/endpoint ;
- chaîne endpoint→mapping→série→spécification→run→artefact→observation ;
- profils distincts BCEAO_XOF et BEAC_XAF ;
- identifiants déterministes et chargement idempotent ;
- correction versionnée au lieu de l'écrasement ;
- source value date distincte de la date du run ;
- SHA256, parseur et formule de transformation ;
- tests Python 3.11/3.12 et PostgreSQL 16 ;
- smoke tests live et pipeline quotidien ;
- distinction stricte entre référentiel, mapping, collecte, historique, calcul et production ;
- documents permanents avec tâches et décisions stables.

## 6. ECARTS ENTRE CONVERSATION ET DEPOT

| Sujet | Attendu | Etat réel | Action |
|---|---|---|---|
| Mapping openfunds | mapping complet | absent | OF-MAP-001/002 |
| Fund/SubFund/ShareClass | séparation stricte | modèle incomplet | OF-DATA-001 |
| Dictionnaire | catalogue complet | structure seulement | OF-DATA-002 |
| 420 définitions | machine-readable | Markdown dispersé | OF-DATA-003 |
| Institutions 54 pays | couverture complète | quelques pilotes | OF-SOURCE-002 |
| Historique | séries durables | snapshots FX | OF-IMPORT/HIST |
| Tunisie | base canonique intégrée | analyse seulement | OF-IMPORT-003 |
| Nigeria | archives depuis 2011 | besoin documenté | OF-IMPORT-004 |
| Catégories | national/régional/Afrique | modèle seulement | OF-TAX-001/002 |
| Références | quatre rôles peuplés | schéma seulement | OF-BENCH-001 |
| WTI/WTI Bench | calculs disponibles | méthodologies seulement | OF-CALC/BENCH |
| API/UI | ressources et pages | architecture seulement | OF-API/UI |
| Persistance | quotidien durable | staging temporaire | OF-IMPORT-001/002 |

La matrice exhaustive est dans `docs/00_PROJECT/CONVERSATION_REPOSITORY_GAP_MATRIX.md`.

## 7. RISQUES ET BLOCAGES

### Risques critiques

1. double source de vérité entre CSV et seeds SQL ;
2. modèles parallèles `source.endpoint` / `source.source_endpoint` ;
3. dates métier artificielles imposées par certaines contraintes ;
4. mauvaise résolution Fund/SubFund/ShareClass ;
5. confusion entre 420 définitions et 420 historiques par pays ;
6. perte de provenance sans stockage brut permanent ;
7. ordre de migrations manuel ;
8. PR non fusionnée et branche `main` minimale.

### Blocages externes

- catalogue officiel openfunds non présent ;
- PostgreSQL persistant non configuré ;
- stockage immuable non configuré ;
- intégration des fichiers Tunisie/Nigeria à organiser ;
- méthodologies WTI Bench incomplètes.

### Incident transparent

Une PR de comparaison accidentelle a été créée puis immédiatement fermée :

```text
PR #3 — CLOSED — accidental comparison PR
```

Elle n'a pas été fusionnée et n'a modifié aucun fichier ni branche.

## 8. CONTROLES DE LA CONSOLIDATION

Etat des workflows sur le commit de contrôle documentaire :

```text
Collector Tests                  SUCCESS
Source Endpoint Schema Tests     SUCCESS
BCEAO FX Live Smoke              SUCCESS
BEAC FX Live Smoke               SUCCESS
Daily Africa FX Staging          SUCCESS
```

La PR #1 reste en brouillon, ouverte, fusionnable et non fusionnée. Sa description distingue désormais structure, implémentation testée, limites et décisions ouvertes.

## POINT EXACT DE REPRISE

### Dernière tâche terminée

```text
OF-DOC-001 — CONSOLIDER LA DOCUMENTATION RACINE
```

La consolidation est terminée : documents obligatoires et complémentaires présents, PR corrigée, 104 fichiers inventoriés et cinq workflows verts.

### Tâche à commencer

```text
OF-ARCH-001 — CHOISIR LA SOURCE DE VERITE DES REFERENTIELS
OF-SOURCE-001 — SYNCHRONISER BCEAO/BEAC ENTRE CSV ET SQL
```

### Fichiers à ouvrir

```text
DECISIONS.md
TODO.md
SOURCE_REGISTRY.md
data/reference/ORGANIZATIONS.csv
data/reference/ORGANIZATION_SCOPE_ROLES.csv
data/reference/SOURCE_ENDPOINTS.csv
data/reference/COUNTRY_OR_ZONE_INDICATOR_SOURCE_MAPPING.csv
data/reference/PROVIDER_SERIES.csv
data/reference/COLLECTION_SPECIFICATIONS.csv
schemas/reference/003_organizations_and_roles.sql
schemas/reference/004_source_endpoints_and_indicator_mapping.sql
schemas/reference/005_provider_series_and_collection_specifications.sql
schemas/reference/007_source_endpoint_reconciliation.sql
schemas/reference/008_bceao_fx_collection_seed.sql
schemas/reference/009_beac_fx_collection_seed.sql
schemas/reference/010_beac_fx_parser_v0_2.sql
schemas/reference/011_beac_fx_collection_validation.sql
```

### Vérifications à effectuer

1. lister les codes BCEAO/BEAC génériques et spécifiques ;
2. comparer IDs, URLs, rôles, statuts et versions ;
3. identifier les doublons réels et les objets complémentaires ;
4. vérifier les FK utilisées par le chargeur ;
5. choisir le registre maître selon `ADR-021` ;
6. documenter l'impact avant modification ;
7. préserver tous les IDs et observations existants.

### Prochaine modification attendue

```text
REGISTRE MAITRE CHOISI
→ GENERATION OU SYNCHRONISATION NON DESTRUCTIVE
→ STATUTS BCEAO/BEAC ALIGNES
→ TEST AUTOMATIQUE DE DIVERGENCE
```

### Critères de fin

- une source de vérité déclarée ;
- aucune double saisie non contrôlée ;
- BCEAO/BEAC cohérents dans CSV et SQL ;
- aucun endpoint, mapping, provider series ou spec en double sans justification ;
- migrations additives et idempotentes ;
- tests Python/PostgreSQL/live verts ;
- README, TODO, SUIVI, ADR et CHANGELOG mis à jour.

Ne pas commencer la couverture historique persistante avant cette réconciliation.


---

## MISE A JOUR DU 4 AOUT 2026 — BASELINE GITHUB IMMUTABLE

### Périmètre

Intervention documentaire uniquement sur :

```text
architecture/africafunds-country-indicators-v0.1
```

SHA de départ vérifié :

```text
cce82f3276d408ddb71366f5236c10282f0b6614
```

Le SHA correspondait exactement au dernier point connu avant toute écriture.

### Actions réalisées

- inventaire des douze branches ;
- audit des trois branches significatives ;
- comparaison du bootstrap et de la branche complète ;
- audit de la PR nº 1 et de la PR nº 2 ;
- réconciliation du contenu de la PR nº 2 ;
- état canonique par niveau de maturité ;
- préparation des décisions ouvertes et portes d'exécution ;
- préparation d'une migration progressive des tâches P0/P1 vers GitHub Issues, sans créer d'issue ;
- préparation du handoff pour la prochaine intervention.

### Etat GitHub vérifié avant commit

```text
MAIN_HEAD_SHA
946145e4b33a6289eb340a16bf5c651cb9bbee7c

WORK_BRANCH_START_HEAD_SHA
cce82f3276d408ddb71366f5236c10282f0b6614

BOOTSTRAP_HEAD_SHA
136abf71f0825075361f8c7446e19c6f6476a3a5

PR2_HEAD_SHA
81d32b83e6a87d01c4e66c2c2db00199b4553d70
```

PR nº 1 :

```text
OPEN
DRAFT
NOT_MERGED
MERGEABLE
173 COMMITS
122 CHANGED FILES
0 FORMAL REVIEWS
```

PR nº 2 :

```text
OPEN
DRAFT
NOT_MERGED
MERGEABLE
5 COMMITS
5 CHANGED FILES
0 FORMAL REVIEWS
```

### Workflows

Les cinq derniers runs observés au HEAD audité de la PR nº 1 étaient `SUCCESS` :

```text
Collector Tests
Source Endpoint Schema Tests
Daily Africa FX Staging
BCEAO FX Live Smoke
BEAC FX Live Smoke
```

Aucun workflow n'a été modifié par cette intervention.

### Bootstrap

Le bootstrap et la branche complète sont historiquement divergents. Toutefois, les treize actifs du bootstrap ont été comparés par SHA de blob et sont tous identiques dans la branche complète.

Recommandation documentaire :

```text
STRATEGY_B
BRANCHE COMPLETE → MAIN DIRECTEMENT
```

Cette recommandation reste soumise à revue et ne constitue ni retargeting ni autorisation de fusion.

### Etat canonique corrigé

```text
TAXONOMIE                         STRUCTURE_PRESENT / TESTED
486 REGLES DE ROUTAGE             IMPLEMENTED / TESTED / NOT_ACTIVE
432 CATEGORIES ET PEER GROUPS     STRUCTURE_PRESENT / TESTED / NOT_ACTIVE
432 BLOCS DE REFERENCE            STRUCTURE_PRESENT / TESTED / NOT_ACTIVE
WTI                               NOT_IMPLEMENTED / NOT_ACTIVE
WTI BENCH                         NOT_CALCULATED / NOT_ACTIVE
RATIOS ET CLASSEMENTS             NOT_IMPLEMENTED
HISTORIQUES FX COMPLETS           NON
PRODUCTION PERSISTANTE            NON
```

Les nombres 95 et 104 restent des états historiques. Le volume courant de la PR nº 1 est 122 fichiers modifiés.

### PR nº 2

Préservés exactement dans `research_queue` :

- `OFFICIAL_SOURCE_INVENTORY_20260803.csv` ;
- `CANONICAL_INTEGRATION_MATRIX_20260803.csv`.

Restent uniques ou seulement résumés :

- `AFRICA_MARKET_RATES_MACRO_SOURCE_HANDOFF_20260803.md` ;
- `NON_REGRESSION_AND_STATUS_RULES_20260803.md` ;
- `PR1_RESEARCH_ASSET_EXPLOITATION_GUIDE_20260803.md`.

La PR nº 2 ne doit pas être fermée avant préservation ou décision explicite sur ces trois documents.

### Identifiants proposés

- `OF-SCOPE-001` : aucune collision observée ;
- `OF-EXPORT-001` : aucune collision observée ;
- `OF-DOC-002` : aucune collision observée ;
- le nouvel usage proposé de `OF-GEO-001` entre en collision avec la tâche existante « Référentiel pays et régions ». Aucun nouvel identifiant géographique n'a été décidé.

### Rapports ajoutés

```text
docs/00_PROJECT/BRANCH_INVENTORY_AND_EXPLOITATION_PLAN.md
docs/00_PROJECT/GITHUB_BASELINE_AUDIT_20260804.md
docs/00_PROJECT/BRANCH_INVENTORY_20260804.csv
docs/00_PROJECT/BOOTSTRAP_INTEGRATION_ASSESSMENT_20260804.md
docs/00_PROJECT/PR_CONTENT_RECONCILIATION_20260804.csv
docs/00_PROJECT/CANONICAL_PROJECT_STATE_20260804.md
docs/00_PROJECT/OPEN_DECISIONS_AND_EXECUTION_GATES_20260804.md
docs/00_PROJECT/ISSUE_MIGRATION_DRAFT_20260804.csv
docs/00_PROJECT/HANDOFF_TO_NEXT_AGENT_20260804.md
```

## POINT EXACT DE REPRISE APRES CETTE BASELINE

Lire d'abord le document maître vivant et les huit rapports datés du 4 août 2026.

L'ordre fonctionnel reste :

```text
OF-ARCH-001
→ OF-SOURCE-001
→ OF-ARCH-002
→ OF-ARCH-003
→ OF-ARCH-004
```

Ne pas commencer :

- l'historique persistant ;
- l'import massif de fonds ;
- un migration runner choisi implicitement ;
- l'activation WTI/WTI Bench ;
- un déploiement ;
- un retargeting ou une fusion ;

avant validation explicite des portes correspondantes.

---

## MISE A JOUR DU 5 AOUT 2026 — AUDIT FINAL ET LOOP ENGINEERING

### État dynamique avant la boucle

```text
CONTROL_BRANCH
architecture/africafunds-country-indicators-v0.1

OBSERVED_HEAD
3c54c54733e116f35ff63a0759c921afd58c57a6

DOCUMENTARY_BASELINE_END
59f6475102b8a0c5b1274060afc412db787f2caf

RELATION
10 commits ahead / 0 behind

MAIN_HEAD
946145e4b33a6289eb340a16bf5c651cb9bbee7c
```

Douze branches, PR nº 1 ouverte/draft/non fusionnée/non fusionnable à l'observation et PR nº 2 ouverte/draft/non fusionnée ont été vérifiées. Aucun changement de PR ou de branche n'a été réalisé.

### Gates vérifiés

```text
OF-ARCH-001   VERIFIED_COMPLETE
OF-SOURCE-001 VERIFIED_COMPLETE
OF-ARCH-002   VERIFIED_COMPLETE
OF-ARCH-003   VERIFIED_COMPLETE
OF-ARCH-004   IMPLEMENTED_WITH_OPEN_GOVERNANCE_BLOCKER
```

Le blocker maintenu est l'immuabilité de la migration générée `012`. La concurrence du runner et les scénarios d'adoption partielle restent également seulement partiellement couverts. `OF-DATA-001` n'est pas commencé.

### Boucle documentaire

```text
TASK_ID
OF-DOC-003

LOOP_ID
OF-LOOP-DOC-003

OBJECTIF
Intégrer le standard Loop Engineering complet sans remplacer les sources canoniques historiques.
```

Livrables principaux : réconciliation permanente, matrice des 176 fichiers, `00_START_HERE.md`, `AGENTS.md`, `SOURCE_OF_TRUTH.md`, mémoire de boucle, catalogues, manifestes, politiques, modèles et adaptateurs IA.

### Nouveau point exact de reprise

1. lire `00_START_HERE.md` et `AGENTS.md` ;
2. résoudre le HEAD courant et comparer à la baseline ;
3. lire `STATUS.md`, `LOOP_STATE.md`, `CURRENT_ITERATION.md`, `WORK_LOG.md`, `NEXT_ACTION.md` et `HANDOFF.md` ;
4. terminer et vérifier `OF-DOC-003` ;
5. n'autoriser qu'ensuite une phase séparée pour le blocker de migration `012` ;
6. ne pas commencer `OF-DATA-001`, fusionner ou retargeter une PR, modifier `main` ou déployer.

## MISE A JOUR DU 11 AOUT 2026 — OF-DATA-003 VERIFIED COMPLETE

```text
TASK_ID: OF-DATA-003
LOOP_ID: OF-LOOP-DATA-003
LOOP_START_HEAD: 145461e04ba9affd2b11fedaf56ed4ad49171b5d
VALIDATED_TECHNICAL_HEAD: 0777afffad950e779234ef09f3f2b9031ec41ce7
CURRENT_HEAD_POLICY: RESOLVE_DYNAMICALLY
PRODUCTION_DEPLOYED: NO
REAL_COUNTRY_HISTORY_LOADED: NO
```

### Résultat

- les sept Markdown D00–D17 historiques ont été figés comme sources de bootstrap et de fidélité ;
- `data/indicator_catalog/v1/` est la source d’authoring logique gouvernée ;
- 18 domaines et exactement 420 codes canoniques uniques sont présents ;
- les absences restent `null` / `NOT_AUTHORED` au lieu d’être inventées ;
- `source_nature` reste distinct de `canonical_nature` ;
- la classification gouvernée `OF-DATA-003-A` compte 298 `RAW`, 85 `METADATA`, 7 `EVENT` et 30 `CALCULATED` ;
- `target_history` reste une exigence et tous les `history_status` restent `NOT_ASSERTED_BY_DEFINITION_CATALOGUE` ;
- JSON expansé, CSV UTF-8 `;`, Markdown et SQL sont générés déterministement ;
- la migration `016_COUNTRY_INDICATOR_CATALOG` crée uniquement `ref.indicator_domain` et `ref.indicator_definition` ;
- aucune observation, série pays, historique réel, secret, base persistante ou production n’a été chargé.

### Preuves

```text
COUNTRY_INDICATOR_CATALOG_RUN: 31484468846 — SUCCESS
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
MIGRATION_RUNNER_RUN: 31484586710 — SUCCESS
POSTGRESQL_16_DOUBLE_APPLY: SUCCESS
POSTGRESQL_16_VERIFY: SUCCESS
RUNTIME_COUNTS: 18 DOMAINS / 420 DEFINITIONS
```

Le run de migrations valide aussi les fixtures Fund/SubFund/ShareClass et le scénario d’adoption d’une base déjà initialisée sans ledger.

### Correction transparente de boucle

La CI a révélé qu’une étape réappliquait la classification dans son workspace avant de figer le manifeste. Le SQL était identique, mais la phrase de métadonnées rendait le hash JSON différent. La cause a été corrigée au commit `d8b3a2d697e9bfdad9a022ba8379494fcaa17608` : le paquet JSON commité est désormais strictement autoritaire et la CI le vérifie sans le réécrire. Un test fonds supposait ensuite à tort que la migration `015` devait rester la dernière migration globale ; le commit `0777afffad950e779234ef09f3f2b9031ec41ce7` a recentré l’invariant sur l’unicité de la migration canonique du domaine `fund`.

### Prochaine porte

`OF-MAP-001` reste bloqué tant qu’un catalogue Openfunds officiel, versionné et licencié n’est pas archivé. La prochaine tâche non bloquée de priorité haute est `OF-SOURCE-002` : compléter les institutions des 54 pays. La reprise doit commencer en lecture seule par un audit de couverture et de preuve ; aucune donnée réelle ne doit être inventée ou déclarée complète sans source vérifiée.
