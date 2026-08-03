# OPENFUNDS — REFERENTIEL CANONIQUE DES FONDS ET DONNEES FINANCIERES AFRICAINES

## 1. PRESENTATION GENERALE

Openfunds est un projet de référentiel canonique destiné à représenter, historiser, contrôler et diffuser les données relatives aux fonds d'investissement, aux marchés, aux pays, aux institutions et aux séries financières nécessaires à leur analyse.

Le projet ne cherche pas à reproduire directement le standard **openfunds** sous la forme d'une table de champs. Il construit une source interne de vérité plus large, puis utilise openfunds et les autres standards comme couches de mapping, d'import et d'export.

Le dépôt doit permettre à terme de représenter :

- les groupes de fonds et structures juridiques ;
- les fonds ;
- les compartiments ;
- les classes de parts ;
- les sociétés de gestion ;
- les dépositaires ;
- les administrateurs, auditeurs et distributeurs ;
- les identifiants et anciennes dénominations ;
- les politiques d'investissement ;
- les classifications ;
- les benchmarks et indices ;
- les frais ;
- les règles opérationnelles ;
- les données réglementaires ;
- les données ESG ;
- les documents ;
- les événements et opérations sur fonds ;
- les valeurs liquidatives ;
- les actifs nets ;
- les dividendes et distributions ;
- les portefeuilles et positions ;
- les performances et risques ;
- les notations ;
- les sources, preuves, extractions et décisions qualité ;
- les données économiques et financières des 54 pays africains ;
- les séries en devise locale, EUR et USD ;
- les catégories nationales, régionales et Afrique ;
- les indices de marché, WTI et WTI Bench.

### Bénéficiaires

Le référentiel cible notamment :

- développeurs et data engineers ;
- analystes financiers et gérants ;
- sociétés de gestion, distributeurs et dépositaires ;
- régulateurs et fournisseurs de données ;
- équipes de contrôle qualité ;
- applications AfricaFunds et ChainSolutions ;
- systèmes de reporting, API, recherche et intelligence artificielle.

### Cas d'usage

- reconstituer l'identité et la trajectoire historique d'un fonds ;
- charger des VL, AUM, dividendes, documents et événements ;
- comparer des fonds dans des univers de pairs cohérents ;
- produire des séries locale/EUR/USD ;
- calculer performances, risques, classements et benchmarks ;
- fournir un historique auditable jusqu'au fichier, à la page ou à la cellule source ;
- alimenter des API, pages fonds, comparateurs, factsheets et outils analytiques ;
- exporter vers openfunds et d'autres standards.

## 2. ETAT REEL DU PROJET

### Branche de travail

```text
architecture/africafunds-country-indicators-v0.1
```

### Pull request

```text
PR #1
BASE : architecture/canonical-model-v1-bootstrap
STATUT : DRAFT / OPEN / NON FUSIONNEE
```

La branche `main` est encore minimale. La documentation, les référentiels, les schémas et les pilotes se trouvent principalement dans la PR #1.

### Inventaire audité au 2026-08-03

La branche contient 95 fichiers :

| Famille | Fichiers |
|---|---:|
| Workflows GitHub Actions | 5 |
| Collecteurs Python | 6 |
| Référentiels CSV | 22 |
| Documentation | 31 |
| Chargeurs Python | 2 |
| Pipelines Python | 2 |
| Fichier de dépendances | 1 |
| Schémas SQL | 12 |
| Tests et fixtures | 13 |
| README racine | 1 |

Voir : [audit complet du dépôt](docs/00_PROJECT/REPOSITORY_AUDIT_2026_08_03.md).

### Ce qui est réellement implémenté et testé

- collecteur FX BCEAO ;
- collecteur FX BEAC ;
- parsing des dates et nombres localisés ;
- conservation des observations buy/sell ;
- calcul des midpoints et inversions ;
- séries `XOF_EUR`, `XOF_USD`, `XAF_EUR`, `XAF_USD` ;
- lignée SHA256, URL, parseur, formule et date de valeur ;
- chargeur PostgreSQL idempotent et versionné ;
- tests PostgreSQL 16 sur base éphémère ;
- orchestration quotidienne BCEAO + BEAC ;
- artefacts GitHub Actions temporaires ;
- tests de réconciliation des modèles d'endpoints.

### Ce qui est structuré mais partiellement peuplé

- 54 pays africains ;
- 1 continent et 5 régions ;
- UEMOA, CEMAC et CMA ;
- 266 relations pays-zone-devise-marché ;
- 44 devises ;
- 84 paires FX requises ;
- 21 rôles institutionnels ;
- 40 organisations ;
- 70 affectations organisation × rôle × périmètre ;
- 43 endpoints ;
- 55 mappings pays/zone × indicateur × source ;
- 50 séries fournisseurs ;
- 17 spécifications ou templates de collecte.

Une grande partie de ces lignes reste `PENDING` ou limitée à quelques pays pilotes.

### Ce qui est documenté mais non implémenté

- catalogue D00-D17 d'environ 420 définitions ;
- modèle complet des indicateurs pays ;
- Fund Relationship Information Model ;
- catégories et sous-catégories nationales, régionales et Afrique ;
- blocs Primary Market Index / Secondary Market Index / WTI / WTI Bench ;
- WTI et WTI Bench ;
- API-first et Atomic Design ;
- pilotes macro, actions, obligations et OPCVM hors FX.

### Ce qui n'est pas encore disponible

- mapping openfunds champ par champ ;
- dictionnaire canonique complet ;
- modèle final Fund / SubFund / ShareClass ;
- base PostgreSQL persistante de production ;
- stockage brut permanent ;
- historique FX multi-dates durable ;
- historiques complets des 54 pays ;
- chargeurs OPCVM Tunisie et Nigeria intégrés à ce dépôt ;
- catégories et blocs de référence générés ;
- indices, WTI, WTI Bench, métriques et classements calculés ;
- API, OpenAPI, SDK ou frontend.

## 3. OBJECTIFS FONCTIONNELS

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
10. gérer les conflits entre sources et les corrections ;
11. conserver les données brutes sans écrasement ;
12. attribuer un statut qualité et un niveau de confiance ;
13. supporter des imports idempotents ;
14. produire des séries locale, EUR et USD ;
15. construire des univers nationaux, régionaux et Afrique ;
16. produire des indices et benchmarks reproductibles ;
17. publier les données par API et exports standardisés.

## 4. OPENFUNDS ET MODELE CANONIQUE

### Ce qu'apporte openfunds

Openfunds fournit un vocabulaire d'échange utile pour de nombreuses données de fonds et classes de parts.

### Pourquoi il ne devient pas directement la base

Un champ externe ne doit pas devenir automatiquement une colonne physique parce que :

- plusieurs champs peuvent décrire le même objet canonique ;
- un champ peut nécessiter une transformation ;
- une valeur peut varier dans le temps ;
- plusieurs standards peuvent viser la même donnée ;
- certaines informations internes ne sont pas couvertes ;
- une source peut fournir des structures imbriquées, répétées ou multilingues.

### Principe de mapping

```text
STANDARD EXTERNE + VERSION + CHAMP
→ REGLE DE NORMALISATION
→ OBJET CANONIQUE CIBLE
→ CHAMP(S) CANONIQUE(S)
→ REGLE DE VALIDATION
→ REGLE D'EXPORT
```

Le futur mapping devra distinguer :

- mapping direct ;
- mapping avec transformation ;
- mapping vers plusieurs champs ;
- mapping depuis plusieurs champs ;
- champ externe non pris en charge ;
- champ canonique sans équivalent ;
- mapping à confirmer ;
- mapping validé.

Voir : [OPENFUNDS_MAPPING.md](OPENFUNDS_MAPPING.md).

## 5. ARCHITECTURE CONCEPTUELLE

### Chaîne principale

```text
REAL_WORLD_DATA
→ RAW_SOURCE
→ NORMALIZED_SOURCE
→ VALIDATION
→ CANONICAL_OBJECTS
→ RELATIONSHIPS_AND_HISTORY
→ CALCULATION_ENGINES
→ API_RESOURCES
→ UI_VIEW_MODELS
→ ATOMIC_DESIGN_PAGES
```

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

Voir : [ARCHITECTURE.md](ARCHITECTURE.md) et [DATA_MODEL.md](DATA_MODEL.md).

## 6. PRINCIPES DE MODELISATION

- séparer statique et dynamique ;
- séparer identité et noms ;
- séparer Fund, SubFund et ShareClass ;
- séparer brut et normalisé ;
- séparer source et valeur consolidée ;
- séparer observation et calcul ;
- conserver les périodes de validité ;
- historiser les relations ;
- tracer jusqu'au document, fichier, page, feuille, ligne, colonne ou cellule ;
- conserver les corrections et conflits ;
- utiliser des identifiants stables ;
- interdire les suppressions destructives d'historique ;
- versionner les référentiels et méthodologies ;
- rendre les imports reproductibles et idempotents ;
- mesurer la qualité ;
- valider progressivement.

Les décisions structurantes sont consolidées dans [DECISIONS.md](DECISIONS.md).

## 7. MODELE TEMPOREL

Les dates ne sont pas interchangeables.

| Champ | Signification |
|---|---|
| `valid_from` | début de validité métier |
| `valid_to` | fin de validité métier |
| `observed_at` / `observation_date` | date économique observée |
| `published_at` / `publication_date` | date de publication |
| `effective_at` | date d'effet juridique ou opérationnel |
| `collected_at` / `retrieved_at` | date de collecte de la source |
| `ingested_at` / `recorded_at` | date d'entrée dans le système |
| `calculated_at` | date d'exécution d'un calcul |
| `corrected_at` | date de correction |
| `superseded_at` | date de remplacement d'une version |

Une date métier inconnue ne doit jamais être remplacée par une date artificielle. Le traitement final de `valid_from` inconnu reste à arbitrer dans `ADR-022`.

## 8. MODELE DE PROVENANCE

Selon la nature de la donnée, la lignée doit permettre de retrouver :

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

## 9. GEOGRAPHIE, TAXONOMIE ET REFERENCES

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

### Catégorie nationale

```text
COUNTRY + ASSET_CLASS
→ NATIONAL_CATEGORY
```

### Sous-catégorie nationale

```text
COUNTRY + ASSET_CLASS + SUB_ASSET_CLASS
→ NATIONAL_SUBCATEGORY
```

Même logique aux niveaux régional et Afrique.

### Bloc de référence

Chaque catégorie et sous-catégorie possède :

```text
PRIMARY_MARKET_INDEX
SECONDARY_MARKET_INDEX
WTI
WTI_BENCH
```

### WTI

Le WTI mesure la performance moyenne observée des fonds éligibles. Il n'utilise pas d'interpolation artificielle de VL.

### WTI Bench

Le WTI Bench est une référence indépendante de marché ou d'allocation. Il doit être transparent, versionné, réplicable, backtesté et auditable.

## 10. DEVISES ET CONVERSIONS

La donnée native n'est jamais écrasée.

```text
NATIVE_OBSERVATION
├── LOCAL
├── EUR
└── USD
```

Chaque conversion conserve :

- l'observation source ;
- la devise source ;
- la devise cible ;
- l'observation FX ;
- le taux ;
- la formule ;
- la date économique ;
- la méthode ;
- le statut qualité.

Les taux, ratios, pourcentages, volatilités et scores ne sont pas convertis comme des montants.

## 11. ORGANISATION DU DEPOT

| Chemin | Rôle | Etat |
|---|---|---|
| `.github/workflows/` | CI, smoke tests live, staging quotidien | Implémenté |
| `collectors/` | téléchargement et parsing des sources | FX BCEAO/BEAC implémenté |
| `loaders/` | chargement canonique en base | FX PostgreSQL implémenté |
| `pipelines/` | orchestration multi-source | FX quotidien implémenté |
| `data/reference/` | référentiels et registres machine-readable | Partiellement peuplé |
| `schemas/reference/` | géographie, organisations, sources, séries et seeds | Mélange migration/brouillon |
| `schemas/taxonomy/` | catégories, fonds, WTI et références | Brouillon non déployé |
| `schemas/market/` | lignée des observations FX | Testé |
| `docs/` | architecture, gouvernance, pilotes et preuves | Documenté |
| `tests/` | fixtures, tests Python et SQL | FX et endpoints couverts |
| `requirements/` | dépendances minimales des collecteurs/chargeurs | Présent |

## 12. INSTALLATION ET COMMANDES VERIFIEES

Les commandes ci-dessous proviennent des workflows existants. Elles supposent un clone local positionné sur la branche de travail.

### Python

Les tests utilisent Python 3.11 et 3.12.

### Installer la dépendance PostgreSQL

```bash
python -m pip install -r requirements/collectors-postgres.txt
```

### Compiler les modules

```bash
python -m compileall -q collectors loaders pipelines tests
```

### Exécuter les tests unitaires

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Collecter le snapshot BCEAO

```bash
python -m collectors.bceao_fx --output-dir artifacts/live/bceao_fx
```

### Collecter le snapshot BEAC

```bash
python -m collectors.beac_fx --output-dir artifacts/live/beac_fx
```

### Lancer le pipeline quotidien en staging

```bash
python -m pipelines.fx_daily \
  --output-dir artifacts/daily/fx \
  --persist-postgres \
  --raw-retention-status LOCAL_PATH_ONLY
```

Sans variable `OPENFUNDS_DATABASE_URL`, le résultat attendu reste :

```text
STAGING_ONLY_DATABASE_NOT_CONFIGURED
```

### Exiger une persistance PostgreSQL

```bash
export OPENFUNDS_DATABASE_URL='postgresql://USER:PASSWORD@HOST:PORT/DATABASE'
python -m pipelines.fx_daily \
  --output-dir artifacts/daily/fx \
  --require-persistence \
  --raw-retention-status PERSISTENT_STORAGE_REQUIRED
```

Ne jamais versionner l'URL de connexion ni les secrets.

### Appliquer les schémas utilisés dans les tests FX

Les workflows utilisent `psql` et appliquent une séquence contrôlée. Cette séquence est destinée aux environnements de test ; elle ne constitue pas encore un migration runner de production.

```bash
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f tests/sql/fx_loader_bootstrap.sql
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f schemas/reference/005_provider_series_and_collection_specifications.sql
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f schemas/market/006_fx_observation_lineage.sql
```

Les seeds BCEAO/BEAC et assertions sont ensuite appliqués par les scripts `tests/sql/fx_loader_seed.sql` et `tests/sql/beac_fx_loader_seed.sql` selon le workflow concerné.

## 13. VARIABLES D'ENVIRONNEMENT

| Variable | Obligatoire | Usage |
|---|---|---|
| `OPENFUNDS_DATABASE_URL` | Non en staging, oui pour persistance | connexion PostgreSQL du pipeline quotidien |
| `DATABASE_URL` | Oui dans les tests SQL | connexion PostgreSQL des workflows |
| `PGPASSWORD` | Selon la configuration psql | mot de passe PostgreSQL de test |

Aucun secret ne doit être ajouté dans un fichier versionné.

## 14. ETAT PAR MODULE

| Module | Statut | Tests | Documentation | Prochaine action |
|---|---|---|---|---|
| Géographie | Partiellement validé | Contrôles documentaires | Oui | vérifier les relations et dates |
| Devises | Référentiel peuplé | Partiel | Oui | vérifier ISO et sources |
| BCEAO FX | Testé live | Oui | Oui | persistance et backfill |
| BEAC FX | Testé live | Oui | Oui | persistance et backfill |
| Organisations | En cours | Seeds partiels | Oui | compléter les 54 pays |
| Endpoints | En cours | Réconciliation testée | Oui | unifier CSV et SQL |
| Catalogue D00-D17 | Documenté | Non | Oui | rendre machine-readable |
| Données macro | Proposé | Non | Oui | implémenter les collecteurs |
| Fonds | Modèle partiel | Non | Oui | arbitrer Fund/SubFund/ShareClass |
| Taxonomie | Proposé | Non | Oui | créer les référentiels et générateur |
| WTI | Décidé | Non | Oui | attendre les séries fonds fiables |
| WTI Bench | Partiellement décidé | Non | Oui | finaliser les méthodologies |
| Mapping Openfunds | A construire | Non | Initial | obtenir et versionner le standard |
| Dictionnaire | A construire | Non | Initial | créer le catalogue canonique |
| API | Non implémenté | Non | Architecture seulement | définir OpenAPI après le modèle |
| Atomic Design | Non implémenté | Non | Architecture seulement | créer les view models après l'API |

## 15. DOCUMENTS DE CONTINUITE

- [TODO.md](TODO.md) — tâches terminées, en cours, restantes et bloquées ;
- [SUIVI.md](SUIVI.md) — journal de continuité et point exact de reprise ;
- [DECISIONS.md](DECISIONS.md) — décisions acceptées et propositions ;
- [ARCHITECTURE.md](ARCHITECTURE.md) — architecture cible et état réel ;
- [DATA_MODEL.md](DATA_MODEL.md) — domaines, entités et relations ;
- [DATA_DICTIONARY.md](DATA_DICTIONARY.md) — gouvernance du dictionnaire ;
- [OPENFUNDS_MAPPING.md](OPENFUNDS_MAPPING.md) — stratégie de mapping ;
- [GOVERNANCE.md](GOVERNANCE.md) — responsabilités et workflow de validation ;
- [QUALITY_RULES.md](QUALITY_RULES.md) — règles qualité ;
- [SOURCE_REGISTRY.md](SOURCE_REGISTRY.md) — sources, endpoints et niveaux de preuve ;
- [ROADMAP.md](ROADMAP.md) — séquence des phases ;
- [CHANGELOG.md](CHANGELOG.md) — historique des changements documentaires et fonctionnels ;
- [audit du dépôt](docs/00_PROJECT/REPOSITORY_AUDIT_2026_08_03.md) ;
- [matrice des écarts](docs/00_PROJECT/CONVERSATION_REPOSITORY_GAP_MATRIX.md).

## 16. ROADMAP RESUMEE

```text
1. CONSOLIDATION DOCUMENTAIRE
2. RECONCILIATION CSV / SQL / SOURCES
3. MODELE FUND / SUBFUND / SHARECLASS
4. DICTIONNAIRE CANONIQUE
5. MAPPING OPENFUNDS
6. PERSISTANCE ET STOCKAGE BRUT
7. HISTORIQUES FX ET COUVERTURE
8. SOURCES MACRO / MARCHE / OPCVM
9. TAXONOMIE ET BLOCS DE REFERENCE
10. INDICES / WTI / WTI BENCH
11. METRIQUES ET CLASSEMENTS
12. API / VIEW MODELS / ATOMIC DESIGN
```

La roadmap détaillée est maintenue dans [ROADMAP.md](ROADMAP.md).

## 17. REGLE DE CONTRIBUTION

Avant toute modification importante :

1. lire `README.md`, `DECISIONS.md`, `TODO.md` et `SUIVI.md` ;
2. identifier la tâche `OF-*` ;
3. vérifier les dépendances et décisions ;
4. éviter toute modification à l'aveugle ;
5. préserver les données brutes et historiques ;
6. ajouter ou mettre à jour les tests ;
7. documenter l'écart entre avant et après ;
8. mettre à jour le point exact de reprise.

## 18. AVERTISSEMENT DE COMPLETUDE

Le dépôt contient une architecture avancée, des référentiels structurés et un pilote FX fonctionnel. Il ne contient pas encore l'ensemble des historiques africains, des fonds, des mappings Openfunds, des indices ou des produits analytiques.

Les termes suivants doivent rester distincts :

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
