# SUIVI — JOURNAL DE CONTINUITE DU PROJET OPENFUNDS

Dernière mise à jour : `2026-08-03`  
Branche de travail : `architecture/africafunds-country-indicators-v0.1`  
Pull request principale : `#1` — brouillon, ouverte, non fusionnée.

---

## 1. ETAT GENERAL DU PROJET

### Objectif actuel

Construire un référentiel canonique des fonds d'investissement et des données financières africaines, plus riche qu'openfunds, tout en conservant un mapping explicite vers openfunds et d'autres standards.

Le projet doit réunir dans une architecture auditée :

```text
SOURCES BRUTES
→ NORMALISATION
→ VALIDATION
→ OBJETS CANONIQUES
→ HISTORISATION ET PROVENANCE
→ CALCULS
→ API
→ VIEW MODELS
→ INTERFACES ATOMIC DESIGN
```

### Périmètre actuel

Le dépôt couvre aujourd'hui principalement :

- la vision canonique et API-first ;
- la géographie africaine et les zones de marché ;
- les devises et les paires FX nécessaires ;
- les organisations, rôles et endpoints de quelques pays pilotes ;
- le cadre D00-D17 des indicateurs pays ;
- un modèle relationnel fonds/taxonomie encore en brouillon ;
- deux collecteurs FX opérationnels, BCEAO et BEAC ;
- une transformation canonique XOF/XAF vers EUR/USD ;
- un chargeur PostgreSQL idempotent ;
- un orchestrateur quotidien de staging ;
- des tests Python, PostgreSQL et live.

### Niveau d'avancement

```text
ARCHITECTURE ET PRINCIPES                  AVANCES ET DOCUMENTES
REFERENTIELS GEOGRAPHIQUES                 STRUCTURELLEMENT PEUPLES
CATALOGUE D00-D17                          DOCUMENTE, NON CENTRALISE
ORGANISATIONS ET SOURCES                   PARTIELLEMENT PEUPLEES
BCEAO FX / BEAC FX                         COLLECTION_TESTED
HISTORIQUE FX MULTI-DATES DURABLE           NON
MODELE FONDS FINAL                          NON STABILISE
MAPPING OPENFUNDS                           ABSENT
DICTIONNAIRE CANONIQUE COMPLET              ABSENT
CATEGORIES / BLOCS DE REFERENCE             NON GENERES
WTI / WTI BENCH / METRIQUES                 NON CALCULES
API / ATOMIC DESIGN                         NON IMPLEMENTES
PRODUCTION PERSISTANTE                      NON CONFIGUREE
```

### Dernier point de travail

La dernière phase fonctionnelle avant cette consolidation a créé et testé un pipeline quotidien commun BCEAO/BEAC. Le premier run réel a correctement produit un statut :

```text
STAGING_ONLY_DATABASE_NOT_CONFIGURED
```

Ce statut prouve la collecte et la transformation, mais pas la persistance ni l'historique complet.

### Phase actuellement menée

Consolidation documentaire et gouvernance du dépôt avant toute nouvelle extension fonctionnelle :

- audit intégral ;
- matrice des écarts ;
- README complet ;
- TODO traçable ;
- décisions formalisées ;
- journal de continuité ;
- documents transversaux de référence.

---

## 2. REALISATIONS

### 2.1 Fondation architecturale

- **Période :** 2026-07-31 au 2026-08-03
- **Composant :** vision et architecture
- **Nature :** décision d'une architecture hybride, PostgreSQL canonique, API-first et Atomic Design.
- **Fichiers :**
  - `docs/00_VISION/Architecture_Decision_Hybrid_API_Atomic_Design.md`
  - `docs/01_ARCHITECTURE/Fund_Relationship_Information_Model_v0.1.md`
  - `schemas/taxonomy/fund_relationship_information_model_v0.1.sql`
- **Résultat :** séparation des couches raw, validation, canonique, analytique, API et UI ; principes bitemporels et de provenance.
- **Tests :** aucun test global du modèle fonds.
- **Limites :** SQL de domaine encore en brouillon ; Fund/SubFund/ShareClass incomplet.

### 2.2 Référentiels géographiques

- **Date :** 2026-08-03
- **Composant :** pays, régions et zones
- **Fichiers :**
  - `data/reference/AFRICA_COUNTRIES.csv`
  - `data/reference/AFRICA_REGIONS.csv`
  - `data/reference/MARKET_ZONES.csv`
  - `data/reference/COUNTRY_RELATIONSHIPS.csv`
  - `schemas/reference/002_country_relationships.sql`
- **Résultat :** 54 pays, 1 continent, 5 régions, UEMOA/CEMAC/CMA et 266 relations.
- **Tests :** contrôles de volumétrie et validation documentaire.
- **Limites :** relations majoritairement `PENDING`, dates historiques non attestées, conflit de nullabilité de `valid_from`.

### 2.3 Devises et règles de conversion

- **Date :** 2026-08-03
- **Composant :** devises et FX
- **Fichiers :**
  - `data/reference/CURRENCIES.csv`
  - `data/reference/FX_PAIRS.csv`
  - `docs/05_CURRENCIES/DAILY_CONVERSION_RULES.md`
- **Résultat :** 44 devises et 84 paires locale vers EUR/USD.
- **Tests :** transformations XOF et XAF couvertes par les tests Python.
- **Limites :** sources officielles et routes de conversion non définies pour la majorité des devises.

### 2.4 Organisations, rôles et sources

- **Date :** 2026-08-03
- **Composant :** institutions et endpoints
- **Fichiers :**
  - `data/reference/ORGANIZATION_ROLES.csv`
  - `data/reference/ORGANIZATIONS.csv`
  - `data/reference/ORGANIZATION_SCOPE_ROLES.csv`
  - `data/reference/SOURCE_ENDPOINTS.csv`
  - `data/reference/COUNTRY_OR_ZONE_INDICATOR_SOURCE_MAPPING.csv`
  - `data/reference/PROVIDER_SERIES.csv`
  - `data/reference/COLLECTION_SPECIFICATIONS.csv`
  - `schemas/reference/003_organizations_and_roles.sql`
  - `schemas/reference/004_source_endpoints_and_indicator_mapping.sql`
  - `schemas/reference/005_provider_series_and_collection_specifications.sql`
  - `schemas/reference/007_source_endpoint_reconciliation.sql`
- **Résultat :** vocabulaire institutionnel, premières organisations et chaîne source complète.
- **Tests :** réconciliation des endpoints dans les deux ordres de création et seconde application idempotente.
- **Limites :** couverture limitée à quelques pays ; statuts CSV/SQL divergents.

### 2.5 Collecteur BCEAO FX

- **Date :** 2026-08-03
- **Composant :** UEMOA / XOF
- **Fichiers :**
  - `collectors/bceao_fx.py`
  - `collectors/fx_html_common.py`
  - `collectors/fx_canonical.py`
  - `schemas/reference/008_bceao_fx_collection_seed.sql`
  - `.github/workflows/bceao-fx-live-smoke.yml`
  - `docs/06_SOURCES/BCEAO_FX_COLLECTION_TEST_EVIDENCE.md`
- **Résultat :** téléchargement live, SHA256, date de valeur, buy/sell observés, XOF_EUR et XOF_USD calculés.
- **Tests :** fixture, live smoke, chargement PostgreSQL, double chargement sans doublon.
- **Limites :** snapshot unique ; base du workflow éphémère.

### 2.6 Collecteur BEAC FX

- **Date :** 2026-08-03
- **Composant :** CEMAC / XAF
- **Fichiers :**
  - `collectors/beac_fx.py`
  - `collectors/fx_html_common.py`
  - `collectors/fx_canonical.py`
  - `schemas/reference/009_beac_fx_collection_seed.sql`
  - `schemas/reference/010_beac_fx_parser_v0_2.sql`
  - `schemas/reference/011_beac_fx_collection_validation.sql`
  - `.github/workflows/beac-fx-live-smoke.yml`
  - `docs/06_SOURCES/BEAC_FX_COLLECTION_TEST_EVIDENCE.md`
- **Résultat :** adaptation au HTML réel en blocs `div.taux_de_change`, 13 paires observées, XAF_EUR et XAF_USD calculés.
- **Tests :** fixture réaliste, live smoke, PostgreSQL, séparation XAF/XOF, idempotence.
- **Limites :** snapshot unique ; base du workflow éphémère.

### 2.7 Chargeur PostgreSQL FX

- **Date :** 2026-08-03
- **Composant :** persistance et lignée
- **Fichiers :**
  - `loaders/fx_postgres.py`
  - `schemas/market/006_fx_observation_lineage.sql`
  - `tests/sql/fx_loader_bootstrap.sql`
  - `tests/sql/fx_loader_seed.sql`
  - `tests/sql/beac_fx_loader_seed.sql`
- **Résultat :** identifiants déterministes, transaction, `INSERTED`, `SKIPPED_IDENTICAL`, supersession de versions.
- **Tests :** PostgreSQL 16 réel dans GitHub Actions.
- **Limites :** aucun déploiement permanent.

### 2.8 Pipeline quotidien commun

- **Date :** 2026-08-03
- **Composant :** orchestration FX
- **Fichiers :**
  - `pipelines/fx_daily.py`
  - `tests/test_fx_daily_pipeline.py`
  - `.github/workflows/fx-daily-staging.yml`
  - `docs/06_SOURCES/FX_DAILY_STAGING_AND_PERSISTENCE_POLICY.md`
- **Résultat :** collecte BCEAO + BEAC, staging canonique, manifeste de couverture, persistance optionnelle.
- **Tests :** tests unitaires et premier run double source réussi.
- **Limites :** secret `OPENFUNDS_DATABASE_URL` absent ; artefacts GitHub Actions temporaires ; schedule durable uniquement après fusion sur la branche par défaut.

### 2.9 Cadre pays D00-D17

- **Période :** 2026-08-03
- **Composant :** données pays
- **Fichiers :**
  - `docs/04_DATA_GOVERNANCE/indicator_catalog/`
  - `docs/04_DATA_GOVERNANCE/Africa_Country_Indicator_Framework_v0.1.md`
  - `schemas/reference/country_indicator_information_model_v0.1.sql`
- **Résultat :** environ 420 définitions réparties en 18 domaines et modèle relationnel proposé.
- **Tests :** aucun import complet du catalogue.
- **Limites :** absence d'un catalogue machine-readable unique et de 22 680 relations matérialisées.

### 2.10 Consolidation documentaire

- **Date :** 2026-08-03
- **Composant :** gouvernance du projet
- **Fichiers créés ou refondus :**
  - `README.md`
  - `TODO.md`
  - `SUIVI.md`
  - `DECISIONS.md`
  - `docs/00_PROJECT/REPOSITORY_AUDIT_2026_08_03.md`
  - `docs/00_PROJECT/CONVERSATION_REPOSITORY_GAP_MATRIX.md`
- **Résultat :** inventaire des 95 fichiers, 45 écarts, 25 ADR, tâches `OF-*`, commandes vérifiées et point de reprise.
- **Tests :** relecture croisée encore en cours pendant cette consolidation.
- **Limites :** documents complémentaires et cohérence finale à achever avant clôture de `OF-DOC-001`.

---

## 3. DECISIONS VALIDEES

Le détail complet est dans `DECISIONS.md`.

| ID | Décision | Statut | Conséquence principale |
|---|---|---|---|
| ADR-001 | Modèle canonique interne | ACCEPTE | openfunds ne devient pas le schéma physique unique |
| ADR-002 | Openfunds comme mapping | ACCEPTE | import/export versionné vers le canonique |
| ADR-003 | PostgreSQL source de vérité | ACCEPTE | projections dérivées reconstructibles |
| ADR-004 | API-first et Atomic Design | ACCEPTE | la présentation ne modèle pas la base |
| ADR-005 | Séparation des couches | ACCEPTE | raw, validation, canonique, calcul et UI distincts |
| ADR-006 | Conservation des artefacts bruts | ACCEPTE | source hashée et reproductible |
| ADR-007 | Historisation bitemporelle | ACCEPTE | validité métier distincte de la connaissance système |
| ADR-008 | Identité distincte des noms | ACCEPTE | alias et anciens noms historisés |
| ADR-009 | Fund/SubFund/ShareClass | PRINCIPE ACCEPTE | implémentation à réexaminer |
| ADR-010 | Pays racine nationale | ACCEPTE | catégories nationales par pays |
| ADR-011 | Zones de marché parallèles | ACCEPTE | UEMOA/CEMAC ne remplacent pas les régions |
| ADR-012 | Codes techniques normalisés | ACCEPTE | majuscules, sans accent, underscore |
| ADR-013 | Quatre rôles de référence | ACCEPTE | Primary, Secondary, WTI, WTI Bench distincts |
| ADR-014 | WTI = pairs observés | ACCEPTE | moyenne de fonds éligibles et datés |
| ADR-015 | WTI Bench indépendant | ACCEPTE | benchmark de marché/allocation séparé |
| ADR-016 | Local, EUR et USD | ACCEPTE | valeur native toujours conservée |
| ADR-017 | Recalcul régional/Afrique | ACCEPTE | calcul depuis les séries fonds converties |
| ADR-018 | Observé distinct de calculé | ACCEPTE | formule et méthodologie liées à la source |
| ADR-019 | Null différent de zéro | ACCEPTE | aucune fabrication des absences |
| ADR-020 | Validation progressive | ACCEPTE | structure, mapping, historique et calcul sont distincts |

---

## 4. POINTS PROPOSES MAIS NON ENCORE VALIDES

| ID | Proposition | Raison | Impact | Validation nécessaire |
|---|---|---|---|---|
| ADR-021 | Une source de vérité pour CSV/SQL | statuts BCEAO/BEAC divergents | gouvernance des référentiels | choisir CSV, base ou manifeste maître |
| ADR-022 | Date métier inconnue explicite | ne pas inventer de date | schémas temporels et relations | approuver nullabilité/statut de date |
| ADR-023 | Migration runner gouverné | ordre SQL manuel | déploiement et non-régression | choisir outil et politique |
| ADR-024 | Catalogue canonique machine-readable | définitions dispersées | dictionnaire et mappings | choisir format maître |
| ADR-025 | Persistance avant statut historique | staging non durable | couverture et statut | configurer DB et stockage brut |
| PROP-WTI-FLEX | Allocation flexible | aucune allocation fixe approuvée | WTI Bench diversifié flexible | méthodologie à valider |
| PROP-MONEY-BENCH | Benchmark monétaire complet | sources différentes par pays | WTI Bench monétaire | hiérarchie de taux/instruments |

Aucune de ces propositions ne doit être transformée silencieusement en décision.

---

## 5. AMELIORATIONS APPORTEES

### Architecture

- distinction entre organisation, rôle, périmètre et endpoint ;
- modèle de source jusqu'à la série fournisseur et la spécification de collecte ;
- lignée FX avec observations brutes et calculées ;
- profils séparés BCEAO_XOF et BEAC_XAF.

### Nommage

- codes canoniques en majuscules sans accent ;
- noms d'affichage séparés ;
- convention FX unique ;
- noms WTI et WTI Bench préservés.

### Historisation

- identifiants déterministes ;
- seconde ingestion identique ignorée ;
- version modifiée capable de superséder l'ancienne ;
- source value date conservée séparément du run date.

### Qualité

- absence de valeur jamais transformée en zéro ;
- buy et sell conservés séparément ;
- SHA256 vérifié ;
- assertions sur la devise locale ;
- interdiction de mélanger XOF et XAF ;
- statut de staging distinct de la production.

### Tests

- tests Python 3.11 et 3.12 ;
- PostgreSQL 16 éphémère ;
- tests de migration dans deux ordres ;
- smoke tests live BCEAO et BEAC ;
- double téléchargement et double chargement ;
- workflow quotidien double source.

### Documentation

- audit du dépôt ;
- matrice de 45 écarts ;
- registre des décisions ;
- registre des tâches ;
- README d'entrée complet ;
- preuve de collecte par source ;
- politique de staging et persistance.

---

## 6. ECARTS ENTRE LA CONVERSATION ET LE DEPOT

| Sujet | Demande ou décision | Etat dans le dépôt | Ecart | Action | Priorité |
|---|---|---|---|---|---|
| Openfunds | mapping complet vers le canonique | principe seulement | catalogue et mapping absents | OF-MAP-001/002 | P0 |
| Fund/SubFund/ShareClass | séparation stricte | Fund + ShareClass en brouillon | SubFund incomplet | OF-DATA-001 | P0 |
| Dictionnaire | tous les champs documentés | définitions dispersées | pas de registre unique | OF-DATA-002 | P0 |
| 420 définitions | catalogue complet exploitable | Markdown réparti | pas de fichier maître | OF-DATA-003 | P0 |
| Sources 54 pays | cartographie institutionnelle complète | quelques pays pilotes | couverture incomplète | OF-SOURCE-002 | P1 |
| Données historiques | séries réelles par pays | snapshots FX et analyse Tunisie | pas de couverture générale | OF-HIST/IMPORT | P1 |
| Tunisie | base OPCVM complète reliée au canonique | analyse documentaire seulement | fichier/chargeur absents | OF-IMPORT-003 | P1 |
| Nigeria | archives SEC auditées depuis 2011 | mappings et besoin documentés | pipeline absent | OF-IMPORT-004 | P1 |
| Catégories | génération national/régional/Afrique | modèle seulement | aucune ligne générée | OF-TAX-001/002 | P1/P2 |
| Références | quatre rôles par catégorie | schéma seulement | aucun bloc peuplé | OF-BENCH-001 | P2 |
| WTI | calcul de performance des pairs | méthode documentée | moteur absent | OF-CALC-001 | P2 |
| WTI Bench | benchmark indépendant | méthode partielle | moteur absent | OF-BENCH-002 | P2 |
| API | ressources versionnées | liste conceptuelle | aucun OpenAPI/serveur | OF-API-001 | P3 |
| Atomic Design | pages et composants réutilisables | règles conceptuelles | aucun view model | OF-UI-001 | P3 |
| Persistance | collecte quotidienne durable | workflow staging | DB et objet storage absents | OF-IMPORT-001/002 | P1 |

La matrice exhaustive est maintenue dans `docs/00_PROJECT/CONVERSATION_REPOSITORY_GAP_MATRIX.md`.

---

## 7. RISQUES ET BLOCAGES

### Risques critiques

1. **Double source de vérité :** CSV et seeds SQL peuvent diverger.
2. **Modèles parallèles :** `source.endpoint` et `source.source_endpoint` peuvent coexister.
3. **Date métier artificielle :** certaines contraintes imposent `valid_from` alors que la date est inconnue.
4. **Mauvaise identité fonds :** chargement prématuré avant décision Fund/SubFund/ShareClass.
5. **Fausse complétude :** 420 définitions ne signifient pas 420 historiques collectés par pays.
6. **Perte de source :** artefacts GitHub temporaires sans stockage immuable.
7. **Déploiement non gouverné :** ordre des migrations appliqué manuellement.
8. **PR non fusionnée :** le `main` reste minimal et les schedules ne constituent pas encore une production durable.

### Blocages externes

- version officielle du standard openfunds non présente dans le dépôt ;
- base PostgreSQL persistante non configurée ;
- stockage brut permanent non configuré ;
- accès gouverné aux sources OPCVM Tunisie/Nigeria à organiser ;
- décisions méthodologiques WTI Bench encore ouvertes.

### Incident de gouvernance pendant l'audit

Une PR de comparaison vers `main` a été créée par erreur lors de l'inventaire :

```text
PR #3 — CLOSED — accidental comparison PR
```

Elle a été immédiatement fermée, n'a pas été fusionnée et n'a modifié aucun fichier ni aucune branche. L'incident est conservé ici par transparence.

---

## 8. PRIORITES IMMEDIATES

```text
P0
├── terminer la consolidation documentaire
├── choisir la source de vérité CSV/SQL
├── unifier le modèle d'endpoint
├── résoudre valid_from inconnu
├── définir la stratégie de migration
├── stabiliser Fund/SubFund/ShareClass
├── construire le dictionnaire
└── préparer le mapping Openfunds

P1
├── synchroniser BCEAO/BEAC dans les référentiels
├── compléter les institutions des 54 pays
├── configurer DB et stockage brut
├── construire la couverture FX
├── intégrer Tunisie/Nigeria
└── rendre les règles qualité exécutables
```

---

## 9. POINT EXACT DE REPRISE

### Dernière tâche terminée

```text
OF-AUDIT-001 — INVENTORIER LE DEPOT
```

Résultat :

- 95 fichiers inventoriés ;
- états réel/documenté/proposé/absent séparés ;
- 45 écarts identifiés ;
- 25 décisions formalisées ;
- README remplacé ;
- TODO créé ;
- SUIVI créé.

### Tâche actuellement en cours

```text
OF-DOC-001 — CONSOLIDER LA DOCUMENTATION RACINE
```

Il reste à :

1. créer ou compléter les documents transversaux liés depuis le README ;
2. vérifier tous les liens relatifs ;
3. relire README/TODO/SUIVI/DECISIONS ensemble ;
4. mettre à jour la description de la PR #1 devenue obsolète ;
5. vérifier que la CI reste verte ;
6. marquer `OF-DOC-001` comme terminée seulement après ces contrôles.

### Fichiers à ouvrir en priorité

```text
README.md
TODO.md
SUIVI.md
DECISIONS.md
docs/00_PROJECT/REPOSITORY_AUDIT_2026_08_03.md
docs/00_PROJECT/CONVERSATION_REPOSITORY_GAP_MATRIX.md
```

Puis :

```text
ARCHITECTURE.md
DATA_MODEL.md
DATA_DICTIONARY.md
OPENFUNDS_MAPPING.md
GOVERNANCE.md
QUALITY_RULES.md
SOURCE_REGISTRY.md
ROADMAP.md
CHANGELOG.md
```

### Vérifications à effectuer

- aucun lien relatif cassé ;
- aucune commande inventée ;
- aucun secret présent ;
- nombre de fichiers et compteurs cohérents ;
- statuts cohérents entre README, TODO, SUIVI et référentiels ;
- distinction constante entre structure, mapping, collecte, historique et calcul ;
- PR #1 toujours en brouillon et non fusionnée ;
- workflows documentaires ou techniques toujours verts.

### Prochaine modification fonctionnelle attendue après la consolidation

Ne pas commencer directement la couverture historique persistante.

La prochaine intervention technique doit être :

```text
OF-ARCH-001 + OF-SOURCE-001
CHOISIR LA SOURCE DE VERITE DES REFERENTIELS
ET SYNCHRONISER BCEAO/BEAC ENTRE CSV ET SQL
```

Ordre attendu :

```text
1. comparer les codes génériques et spécifiques BCEAO/BEAC
2. choisir le registre maître
3. produire une migration ou un générateur non destructif
4. mettre à jour les statuts CSV/SQL
5. ajouter un test de divergence
6. relire les preuves de collecte
7. mettre à jour TODO, SUIVI, DECISIONS et CHANGELOG
```

### Critères de fin de l'étape suivante

- une seule source de vérité est déclarée ;
- BCEAO et BEAC ont les mêmes statuts dans toutes les représentations ;
- aucun endpoint, mapping, provider series ou collection spec en double ;
- les IDs existants et la lignée sont préservés ;
- les migrations sont additives et idempotentes ;
- les tests Python et PostgreSQL sont verts ;
- aucune nouvelle collecte historique n'est engagée avant cette réconciliation.
