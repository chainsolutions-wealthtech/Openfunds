# OPENFUNDS — REFERENTIEL CANONIQUE DES FONDS ET DONNEES FINANCIERES AFRICAINES

## 1. PRESENTATION GENERALE

Openfunds est un projet de référentiel canonique destiné à représenter, historiser, contrôler et diffuser les données relatives aux fonds d'investissement, aux marchés, aux pays, aux institutions et aux séries financières nécessaires à leur analyse.

Le projet ne cherche pas à reproduire directement le standard **openfunds** sous la forme d'une table de champs. Il construit une source interne de vérité plus large, puis utilise openfunds et les autres standards comme couches de mapping, d'import et d'export.

Le dépôt doit permettre à terme de représenter :

- groupes, structures juridiques, fonds, compartiments et classes de parts ;
- sociétés de gestion, dépositaires, administrateurs, auditeurs et distributeurs ;
- identifiants, noms actuels, anciens noms et alias ;
- politiques d'investissement, classifications, benchmarks et frais ;
- règles opérationnelles, réglementaires et ESG ;
- documents, événements et opérations sur fonds ;
- valeurs liquidatives, actifs nets, dividendes et flux ;
- portefeuilles, performances, risques, notations et classements ;
- sources, fichiers, extractions, preuves et décisions qualité ;
- données économiques et financières des 54 pays africains ;
- séries en devise locale, EUR et USD ;
- catégories nationales, régionales et Afrique ;
- indices de marché, WTI et WTI Bench.

### Bénéficiaires

- développeurs et data engineers ;
- analystes financiers et gérants ;
- sociétés de gestion, distributeurs et dépositaires ;
- régulateurs et fournisseurs de données ;
- équipes de contrôle et gouvernance ;
- applications AfricaFunds et ChainSolutions ;
- API, reportings et systèmes d'intelligence artificielle.

### Cas d'usage

- reconstituer l'identité et la trajectoire historique d'un fonds ;
- charger des VL, AUM, dividendes, documents et événements ;
- comparer des fonds dans des univers de pairs cohérents ;
- produire des séries locale, EUR et USD ;
- calculer performances, risques, classements et benchmarks ;
- tracer une donnée jusqu'au fichier, à la page ou à la cellule source ;
- alimenter pages fonds, comparateurs, factsheets et outils analytiques ;
- importer et exporter vers openfunds et d'autres standards.

## 2. OBJECTIFS FONCTIONNELS

Le modèle cible doit :

1. attribuer un identifiant canonique stable à chaque objet ;
2. séparer identité, dénomination et alias ;
3. distinguer Fund, SubFund et ShareClass ;
4. gérer lancements, changements de nom et changements de gestionnaire ;
5. gérer fusions, absorptions, scissions, transferts, liquidations et clôtures ;
6. historiser classifications, benchmarks, frais et statuts réglementaires ;
7. historiser NAV, AUM, dividendes, performances et risques ;
8. conserver les documents et leurs versions ;
9. relier chaque valeur à sa source et à sa preuve ;
10. gérer conflits, corrections et niveaux de confiance ;
11. conserver les données brutes sans écrasement ;
12. supporter des imports reproductibles et idempotents ;
13. produire des séries locale, EUR et USD ;
14. construire des univers nationaux, régionaux et Afrique ;
15. produire indices et benchmarks reproductibles ;
16. publier les données par API et exports standardisés.

## 3. OPENFUNDS ET MODELE CANONIQUE

### Rôle d'openfunds

Openfunds fournit un vocabulaire d'échange utile pour les données de fonds et de classes de parts. Il n'est pas le schéma interne unique.

Un champ externe ne devient pas automatiquement une colonne physique parce que :

- plusieurs champs peuvent décrire le même objet canonique ;
- un champ peut nécessiter une transformation ;
- une valeur peut évoluer dans le temps ;
- plusieurs standards peuvent viser la même donnée ;
- certaines informations internes ne sont pas couvertes ;
- une source peut être imbriquée, répétée ou multilingue.

### Chaîne de mapping

```text
STANDARD + VERSION + FIELD
→ NORMALIZATION_RULE
→ CANONICAL_ENTITY
→ CANONICAL_FIELD_OR_RELATION
→ VALIDATION_RULE
→ EXPORT_RULE
```

Le mapping devra distinguer :

```text
DIRECT
TRANSFORMED
ONE_TO_MANY
MANY_TO_ONE
UNSUPPORTED_EXTERNAL_FIELD
CANONICAL_ONLY
TO_CONFIRM
VALIDATED
```

Etat actuel : le principe est accepté, mais le catalogue officiel et le mapping champ par champ ne sont pas encore présents. Voir `OPENFUNDS_MAPPING.md`.

## 4. ARCHITECTURE CONCEPTUELLE

```text
REAL_WORLD_DATA
→ RAW_SOURCE
→ NORMALIZED_SOURCE
→ VALIDATION
→ CANONICAL_MODEL
→ ANALYTICAL_MODEL
→ API_RESOURCE
→ UI_VIEW_MODEL
→ ATOMIC_DESIGN
```

PostgreSQL est la source canonique de vérité. Les fichiers originaux doivent être conservés dans un stockage immuable. Les index de recherche, caches, graphes et vues analytiques sont dérivés et reconstruisibles.

### Familles de domaine

1. identité ;
2. structure juridique ;
3. fonds ;
4. compartiments ;
5. classes de parts ;
6. sociétés de gestion ;
7. fournisseurs de services ;
8. politique d'investissement ;
9. classifications ;
10. benchmarks ;
11. frais ;
12. éligibilité ;
13. distribution ;
14. règles opérationnelles ;
15. données réglementaires ;
16. ESG ;
17. documents ;
18. opérations et événements ;
19. historique des changements ;
20. métadonnées ;
21. données dynamiques ;
22. valeurs liquidatives ;
23. actifs nets ;
24. distributions et dividendes ;
25. portefeuilles ;
26. performances ;
27. risques ;
28. notations ;
29. sources ;
30. provenance ;
31. qualité ;
32. gouvernance.

Voir `ARCHITECTURE.md` et `DATA_MODEL.md`.

## 5. PRINCIPES DE MODELISATION

- séparer statique et dynamique ;
- séparer identité et noms ;
- séparer Fund, SubFund et ShareClass ;
- séparer brut et normalisé ;
- séparer source et valeur consolidée ;
- séparer observation et calcul ;
- conserver les périodes de validité ;
- historiser les relations ;
- tracer jusqu'au document, fichier, page, feuille, ligne, colonne ou cellule ;
- conserver corrections et conflits ;
- utiliser des identifiants stables ;
- interdire les suppressions destructives d'historique ;
- versionner référentiels et méthodologies ;
- mesurer la qualité ;
- valider progressivement.

Les décisions structurantes sont dans `DECISIONS.md`.

## 6. MODELE TEMPOREL

| Champ | Signification |
|---|---|
| `valid_from` | début de validité métier |
| `valid_to` | fin de validité métier |
| `observation_date` | date économique observée |
| `publication_date` | date de publication |
| `effective_at` | date d'effet juridique ou opérationnel |
| `retrieved_at` | date de collecte |
| `recorded_at` | date d'entrée dans le système |
| `calculated_at` | date d'exécution d'un calcul |
| `corrected_at` | date de correction |
| `superseded_at` | date de remplacement d'une version |

Une date métier inconnue ne doit jamais être remplacée par une date artificielle. Le traitement final relève de `ADR-022`.

## 7. MODELE DE PROVENANCE

Selon la donnée, la lignée doit retrouver :

```text
COUNTRY_OR_ZONE
ORGANIZATION
SOURCE_ENDPOINT
URL
SOURCE_DOCUMENT
ORIGINAL_FILENAME
MIME_TYPE
SHA256
PUBLICATION_DATE
RETRIEVED_AT
WORKSHEET
TABLE
PAGE
ROW
COLUMN
CELL
RAW_LABEL
RAW_VALUE
PARSER_VERSION
TRANSFORMATION_RULE
METHODOLOGY_VERSION
VALIDATION_DECISION
CONFIDENCE_SCORE
```

Les sources brutes restent distinctes des valeurs normalisées et canoniques.

## 8. GEOGRAPHIE, TAXONOMIE ET REFERENCES

### Géographie

```text
COUNTRY
→ REGION
→ AFRICA
```

Les zones de marché restent parallèles :

```text
COUNTRY
→ MARKET_SCOPE
→ CENTRAL_BANK / EXCHANGE / REGULATOR / SOURCE
```

### Catégories

```text
COUNTRY + ASSET_CLASS
→ NATIONAL_CATEGORY

COUNTRY + ASSET_CLASS + SUB_ASSET_CLASS
→ NATIONAL_SUBCATEGORY
```

La même logique est reconstruite aux niveaux régional et Afrique.

### Bloc de référence

Chaque catégorie et sous-catégorie possède :

```text
PRIMARY_MARKET_INDEX
SECONDARY_MARKET_INDEX
WTI
WTI_BENCH
```

Le WTI mesure la performance observée des fonds éligibles. Le WTI Bench est une référence indépendante de marché ou d'allocation.

## 9. DEVISES ET CONVERSIONS

La donnée native n'est jamais écrasée :

```text
NATIVE_OBSERVATION
├── LOCAL
├── EUR
└── USD
```

Chaque conversion conserve l'observation source, la paire FX, la date, le taux, la formule, la méthode et le statut qualité. Les taux, ratios, pourcentages, volatilités et scores ne sont pas convertis comme des montants.

## 10. ETAT REEL DU DEPOT

### Branche et PR

```text
BRANCH : architecture/africafunds-country-indicators-v0.1
PR     : #1
BASE   : architecture/canonical-model-v1-bootstrap
STATUS : DRAFT / OPEN / NOT_MERGED
```

La branche `main` reste minimale.

### Inventaire

L'audit initial précédant la consolidation recensait 95 fichiers. Après création des neuf documents transversaux supplémentaires, la comparaison actuelle avec `main` contient **104 fichiers** : 103 ajouts et le README remplacé.

| Famille | Nombre actuel |
|---|---:|
| Workflows GitHub Actions | 5 |
| Collecteurs Python | 6 |
| Référentiels CSV | 22 |
| Chargeurs Python | 2 |
| Pipelines Python | 2 |
| Dépendances | 1 |
| Schémas SQL | 12 |
| Tests et fixtures | 13 |
| Documentation et fichiers de gouvernance | 41 |

L'audit historique reste dans `docs/00_PROJECT/REPOSITORY_AUDIT_2026_08_03.md`. La matrice des 45 écarts est dans `docs/00_PROJECT/CONVERSATION_REPOSITORY_GAP_MATRIX.md`.

### Réellement implémenté et testé

- collecteur live BCEAO FX ;
- collecteur live BEAC FX ;
- parsing dates et nombres localisés ;
- buy/sell observés conservés ;
- `XOF_EUR`, `XOF_USD`, `XAF_EUR`, `XAF_USD` ;
- SHA256, URL, parseur, formule et date de valeur ;
- chargeur PostgreSQL idempotent ;
- tests PostgreSQL 16 ;
- réconciliation des schémas d'endpoints ;
- orchestrateur quotidien BCEAO + BEAC ;
- staging et artefacts GitHub Actions temporaires.

### Structurellement peuplé

- 54 pays ;
- 1 continent et 5 régions ;
- UEMOA, CEMAC et CMA ;
- 266 relations ;
- 44 devises ;
- 84 paires FX ;
- 21 rôles institutionnels ;
- 40 organisations ;
- 70 affectations de rôles ;
- 43 endpoints ;
- 55 mappings indicateur-source ;
- 50 séries fournisseurs ;
- 17 spécifications/templates.

Une grande partie reste `PENDING` ou limitée à quelques pays pilotes.

### Documenté mais non implémenté

- environ 420 définitions D00-D17 ;
- modèle complet des indicateurs pays ;
- modèle fonds et taxonomie ;
- catégories et sous-catégories ;
- blocs de quatre références ;
- WTI et WTI Bench ;
- API-first et Atomic Design.

### Absent ou incomplet

- mapping openfunds opérationnel ;
- dictionnaire canonique machine-readable complet ;
- modèle final Fund/SubFund/ShareClass ;
- PostgreSQL persistant de production ;
- stockage brut permanent ;
- historique FX multi-dates durable ;
- historiques complets des 54 pays ;
- chargeurs OPCVM Tunisie/Nigeria intégrés ;
- catégories et blocs générés ;
- indices, WTI, WTI Bench, métriques et classements ;
- API, OpenAPI, SDK et frontend.

## 11. ORGANISATION DU DEPOT

| Chemin | Rôle | Etat |
|---|---|---|
| `.github/workflows/` | CI, smoke tests et staging quotidien | implémenté |
| `collectors/` | téléchargement et parsing | BCEAO/BEAC FX implémentés |
| `loaders/` | chargement canonique | FX PostgreSQL implémenté |
| `pipelines/` | orchestration multi-source | FX quotidien implémenté |
| `data/reference/` | référentiels machine-readable | partiellement peuplé |
| `schemas/reference/` | géographie, organisations, sources et seeds | mélange de migrations et propositions |
| `schemas/taxonomy/` | fonds, catégories et références | brouillon |
| `schemas/market/` | observations FX | testé |
| `docs/` | architecture, pilotes, sources et preuves | riche et consolidé |
| `tests/` | fixtures, tests Python et SQL | FX/endpoints couverts |
| `requirements/` | dépendances minimales | présent |

## 12. COMMANDES VERIFIEES

Les commandes ci-dessous proviennent des workflows existants.

### Dépendance PostgreSQL

```bash
python -m pip install -r requirements/collectors-postgres.txt
```

### Compilation et tests

```bash
python -m compileall -q collectors loaders pipelines tests
python -m unittest discover -s tests -p "test_*.py" -v
```

### Collectes live

```bash
python -m collectors.bceao_fx --output-dir artifacts/live/bceao_fx
python -m collectors.beac_fx --output-dir artifacts/live/beac_fx
```

### Pipeline quotidien en staging

```bash
python -m pipelines.fx_daily \
  --output-dir artifacts/daily/fx \
  --persist-postgres \
  --raw-retention-status LOCAL_PATH_ONLY
```

Sans `OPENFUNDS_DATABASE_URL`, le statut attendu est :

```text
STAGING_ONLY_DATABASE_NOT_CONFIGURED
```

### Persistance exigée

```bash
export OPENFUNDS_DATABASE_URL='postgresql://USER:PASSWORD@HOST:PORT/DATABASE'
python -m pipelines.fx_daily \
  --output-dir artifacts/daily/fx \
  --require-persistence \
  --raw-retention-status PERSISTENT_STORAGE_REQUIRED
```

Ne jamais versionner l'URL de connexion ni les secrets.

### Schémas utilisés dans les tests FX

```bash
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f tests/sql/fx_loader_bootstrap.sql
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f schemas/reference/005_provider_series_and_collection_specifications.sql
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f schemas/market/006_fx_observation_lineage.sql
```

Cette séquence est vérifiée pour les tests ; elle n'est pas encore un migration runner de production.

## 13. VARIABLES D'ENVIRONNEMENT

| Variable | Usage |
|---|---|
| `OPENFUNDS_DATABASE_URL` | PostgreSQL persistant du pipeline quotidien |
| `DATABASE_URL` | PostgreSQL des tests et scripts SQL |
| `PGPASSWORD` | authentification `psql` selon environnement |

Aucun secret ne doit être ajouté au dépôt.

## 14. ETAT PAR MODULE

| Module | Statut | Tests | Prochaine action |
|---|---|---|---|
| Géographie | partiellement validé | contrôles documentaires | vérifier relations et dates |
| Devises | référentiel peuplé | partiel | vérifier ISO et sources |
| BCEAO FX | collection testée | live + PostgreSQL | persistance et backfill |
| BEAC FX | collection testée | live + PostgreSQL | persistance et backfill |
| Organisations | en cours | seeds partiels | compléter les 54 pays |
| Endpoints | en cours | réconciliation testée | unifier CSV et SQL |
| Catalogue D00-D17 | documenté | non | rendre machine-readable |
| Fonds | modèle partiel | non | arbitrer Fund/SubFund/ShareClass |
| Taxonomie | proposé | non | créer référentiels et générateur |
| WTI | décidé, non implémenté | non | attendre les séries fonds |
| WTI Bench | partiellement décidé | non | finaliser méthodologies |
| Mapping openfunds | absent | non | obtenir/versionner le standard |
| Dictionnaire | spécification créée | non | peupler le catalogue maître |
| API | non implémenté | non | définir OpenAPI après le modèle |
| Atomic Design | non implémenté | non | définir view models après API |

## 15. DOCUMENTS DE CONTINUITE

- `TODO.md` — tâches et critères d'acceptation ;
- `SUIVI.md` — historique et point exact de reprise ;
- `DECISIONS.md` — décisions et propositions ;
- `ARCHITECTURE.md` — architecture cible et actuelle ;
- `DATA_MODEL.md` — domaines, entités et relations ;
- `DATA_DICTIONARY.md` — structure du dictionnaire ;
- `OPENFUNDS_MAPPING.md` — stratégie de mapping ;
- `GOVERNANCE.md` — workflow de validation ;
- `QUALITY_RULES.md` — règles qualité ;
- `SOURCE_REGISTRY.md` — chaîne des sources ;
- `ROADMAP.md` — phases et portes de sortie ;
- `CHANGELOG.md` — changements ;
- `docs/00_PROJECT/REPOSITORY_AUDIT_2026_08_03.md` — audit ;
- `docs/00_PROJECT/CONVERSATION_REPOSITORY_GAP_MATRIX.md` — écarts.

## 16. ROADMAP RESUMEE

```text
1. CONSOLIDATION DOCUMENTAIRE
2. RECONCILIATION CSV / SQL / SOURCES
3. MODELE FUND / SUBFUND / SHARECLASS
4. DICTIONNAIRE CANONIQUE
5. MAPPING OPENFUNDS
6. PERSISTANCE ET STOCKAGE BRUT
7. HISTORIQUES ET COUVERTURE
8. SOURCES MACRO / MARCHE / OPCVM
9. TAXONOMIE ET BLOCS DE REFERENCE
10. INDICES / WTI / WTI BENCH
11. METRIQUES ET CLASSEMENTS
12. API / VIEW MODELS / ATOMIC DESIGN
```

Le détail est dans `ROADMAP.md`.

## 17. REGLE DE CONTRIBUTION

Avant toute modification importante :

1. lire README, DECISIONS, TODO et SUIVI ;
2. identifier la tâche `OF-*` ;
3. vérifier les dépendances et décisions ;
4. éviter toute modification à l'aveugle ;
5. préserver données brutes et historiques ;
6. ajouter ou mettre à jour les tests ;
7. documenter l'avant et l'après ;
8. mettre à jour le point exact de reprise.

## 18. AVERTISSEMENT DE COMPLETUDE

Le dépôt contient une architecture avancée, des référentiels structurés et un pilote FX fonctionnel. Il ne contient pas encore tous les historiques africains, fonds, mappings openfunds, indices ou produits analytiques.

Les niveaux suivants restent distincts :

```text
ARCHITECTURE_PRESENTE
REFERENTIEL_PEUPLE
SOURCE_MAPPEE
COLLECTION_TESTED
PARTIAL_HISTORY_LOADED
COMPLETE_HISTORY_LOADED
INDEX_CALCULATED
PRODUCTION_DEPLOYED
```

---

## 19. POINT D'ENTREE LOOP ENGINEERING — 2026-08-05

Les sections précédentes restent l'historique canonique du projet. Pour l'état vivant et l'ordre de reprise, lire désormais :

1. `00_START_HERE.md` ;
2. `AGENTS.md` ;
3. `SOURCE_OF_TRUTH.md` ;
4. `STATUS.md` ;
5. `NEXT_ACTION.md` ;
6. `LOOP_STATE.md` et `CURRENT_ITERATION.md` ;
7. `DOCUMENT_INTEGRATION_MATRIX.md`.

Statuts vérifiés :

```text
OF-ARCH-001   VERIFIED_COMPLETE
OF-SOURCE-001 VERIFIED_COMPLETE
OF-ARCH-002   VERIFIED_COMPLETE
OF-ARCH-003   VERIFIED_COMPLETE
OF-ARCH-004   IMPLEMENTED_WITH_OPEN_GOVERNANCE_BLOCKER
OF-DATA-001   NOT_STARTED
```

Le blocker de `OF-ARCH-004` est l'immuabilité historique de la migration générée `012`. La boucle `OF-LOOP-DOC-003` n'apporte aucune modification technique, ne rend pas la PR nº 1 fusionnable et ne modifie pas la PR nº 2.

Les volumes 95 et 104 et les comptes de workflows ci-dessus sont historiques. L'état GitHub doit toujours être résolu dynamiquement ; l'observation initiale de cette boucle est le HEAD `3c54c54733e116f35ff63a0759c921afd58c57a6`, avec une PR nº 1 à 184 commits et 162 fichiers modifiés avant l'intégration documentaire.