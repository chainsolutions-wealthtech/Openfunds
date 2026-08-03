# SUIVI — JOURNAL DE CONTINUITE DU PROJET OPENFUNDS

Dernière mise à jour : `2026-08-03`  
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
CATALOGUE D00-D17                        DOCUMENTE, NON CENTRALISE
BCEAO FX / BEAC FX                       COLLECTION_TESTED
HISTORIQUE DURABLE MULTI-DATES           NON
MODELE FUND/SUBFUND/SHARECLASS           A ARBITRER
DICTIONNAIRE MACHINE-READABLE            NON PEUPLE
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
