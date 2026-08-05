# AUDIT DU DEPOT OPENFUNDS — 2026-08-03

## 1. OBJET

Ce document établit l'état réel du dépôt `chainsolutions-wealthtech/Openfunds` avant toute nouvelle extension fonctionnelle.

Il distingue explicitement :

- ce qui existe réellement dans les fichiers ;
- ce qui est effectivement exécuté et testé ;
- ce qui est seulement documenté ;
- ce qui est proposé mais non validé ;
- ce qui est partiellement peuplé ;
- ce qui reste absent ;
- ce qui diverge entre les référentiels, les schémas, la documentation et les workflows.

Aucune présence de fichier, de table ou de classe ne vaut preuve d'une fonctionnalité terminée.

## 2. PERIMETRE AUDITE

### Dépôt

```text
chainsolutions-wealthtech/Openfunds
```

### Branche auditée

```text
architecture/africafunds-country-indicators-v0.1
```

### Pull request principale

```text
PR #1
BASE : architecture/canonical-model-v1-bootstrap
HEAD : architecture/africafunds-country-indicators-v0.1
STATUT : DRAFT / OPEN / NON FUSIONNEE
```

### Branche par défaut

```text
main
```

La branche `main` ne contient actuellement qu'un `README.md` minimal. La substance du projet se trouve sur les branches d'architecture et dans la PR #1.

## 3. INVENTAIRE QUANTITATIF

La comparaison entre `main` et la branche auditée montre 94 fichiers ajoutés. Avec le `README.md` déjà présent sur `main`, la branche auditée contient 95 fichiers.

| Famille | Nombre de fichiers | Etat dominant |
|---|---:|---|
| Workflows GitHub Actions | 5 | Implémentés et exécutés |
| Collecteurs Python | 6 | Deux collecteurs FX actifs, primitives communes |
| Référentiels CSV | 22 | Partiellement peuplés, nombreux statuts `PENDING` |
| Documentation | 31 | Riche mais dispersée |
| Chargeurs Python | 2 | Chargeur FX PostgreSQL implémenté |
| Pipelines Python | 2 | Orchestrateur FX quotidien implémenté |
| Dépendances | 1 | `psycopg` uniquement pour les chargeurs |
| Schémas SQL | 12 | Mélange de brouillons, migrations et seeds |
| Tests et fixtures | 13 | Bonne couverture FX et réconciliation d'endpoints |
| README racine | 1 | Incomplet avant consolidation |

## 4. ARBORESCENCE FONCTIONNELLE REELLE

```text
.
├── README.md
├── .github/workflows/
│   ├── bceao-fx-live-smoke.yml
│   ├── beac-fx-live-smoke.yml
│   ├── collector-tests.yml
│   ├── fx-daily-staging.yml
│   └── source-endpoint-schema-tests.yml
├── collectors/
│   ├── bceao_fx.py
│   ├── beac_fx.py
│   ├── common.py
│   ├── fx_canonical.py
│   └── fx_html_common.py
├── loaders/
│   └── fx_postgres.py
├── pipelines/
│   └── fx_daily.py
├── data/reference/
│   ├── référentiels géographiques
│   ├── devises et paires FX
│   ├── organisations et rôles
│   ├── endpoints et mappings
│   ├── séries fournisseurs et spécifications
│   ├── plans de benchmarks et règles qualité
│   └── registres de pilotes et preuves de tests
├── docs/
│   ├── vision et architecture
│   ├── modèles de domaine
│   ├── pilotes Maroc et Tunisie
│   ├── gouvernance des indicateurs D00-D17
│   ├── géographie
│   ├── devises
│   └── sources et collecte
├── schemas/
│   ├── reference/
│   ├── taxonomy/
│   └── market/
├── tests/
│   ├── fixtures/
│   ├── sql/
│   └── tests Python
└── requirements/
    └── collectors-postgres.txt
```

## 5. ETAT PAR COUCHE

### 5.1 Vision et principes architecturaux

**Etat : VALIDE ET DOCUMENTE**

Principes existants :

- PostgreSQL comme source canonique de vérité ;
- architecture API-first ;
- Atomic Design comme architecture de présentation ;
- séparation ingestion, validation, canonique, analytique, API et UI ;
- historisation bitemporelle ;
- conservation des artefacts bruts ;
- provenance complète ;
- projections dérivées reconstructibles ;
- interdiction pour les moteurs dérivés de modifier directement la vérité canonique.

Limite : aucun contrat OpenAPI, serveur API ou composant UI n'est encore implémenté dans ce dépôt.

### 5.2 Géographie et zones de marché

**Etat : REFERENTIEL STRUCTURELLEMENT PEUPLE, VALIDATION OFFICIELLE PARTIELLE**

Données présentes :

- 54 pays africains ;
- 1 continent et 5 régions ;
- UEMOA, CEMAC et CMA ;
- 266 relations pays-vers-région, continent, devise, zone et marché.

Limites :

- les relations sont majoritairement `PENDING` ;
- les dates d'effet historiques ne sont pas renseignées ;
- le fichier legacy `african_countries_v0.1.csv` subsiste comme source de comparaison ;
- la correspondance entre les codes CSV et les identifiants UUID SQL n'est pas encore industrialisée.

### 5.3 Devises et FX

**Etat : REFERENTIEL PEUPLE + PILOTE OPERATIONNEL TESTE**

Référentiels :

- 44 devises ;
- 84 paires requises, soit 42 devises locales vers EUR et USD ;
- convention canonique : `1 SOURCE CURRENCY UNIT = X TARGET CURRENCY UNITS`.

Fonctionnellement implémenté :

- collecte live BCEAO ;
- collecte live BEAC ;
- conservation du buy et du sell observés ;
- calcul du midpoint ;
- inversion vers `XOF_EUR`, `XOF_USD`, `XAF_EUR`, `XAF_USD` ;
- lignée jusqu'au SHA256, au parseur, à la formule et à la date de valeur ;
- chargement PostgreSQL idempotent ;
- orchestration quotidienne en staging.

Limites :

- la base de données persistante de production n'est pas configurée ;
- le stockage brut durable n'est pas configuré ;
- les artefacts GitHub Actions sont temporaires ;
- un seul snapshot économique a été validé pour chaque source ;
- aucun historique complet n'est chargé ;
- le workflow planifié n'est durablement actif qu'après fusion sur la branche par défaut.

### 5.4 Organisations et rôles institutionnels

**Etat : VOCABULAIRE PEUPLE, COUVERTURE PAYS PARTIELLE**

Données présentes :

- 21 types de rôles institutionnels ;
- 40 organisations ;
- 70 affectations organisation × rôle × périmètre ;
- 43 endpoints de travail.

Pays principalement amorcés :

- Maroc ;
- Ghana ;
- Nigeria ;
- Tunisie ;
- Egypte ;
- Kenya ;
- Afrique du Sud ;
- zones UEMOA et CEMAC.

Limites :

- les 54 pays ne disposent pas encore de leur cartographie institutionnelle complète ;
- plusieurs noms de domaines et rôles restent à revérifier ;
- les CSV et les seeds SQL n'ont pas encore des statuts parfaitement synchronisés.

### 5.5 Catalogue pays et indicateurs

**Etat : DOCUMENTE / PROPOSE, NON CHARGE COMME CATALOGUE CANONIQUE COMPLET**

Portée documentée :

- 18 domaines D00-D17 ;
- environ 420 définitions d'indicateurs, métadonnées, événements et produits calculés ;
- matrice logique maximale de 22 680 combinaisons pays × indicateur ;
- modèle relationnel évitant une table de 420 colonnes par pays.

Limites :

- le catalogue est réparti dans plusieurs documents Markdown ;
- il n'existe pas encore de fichier machine-readable unique contenant les 420 définitions complètes ;
- le schéma `country_indicator_information_model_v0.1.sql` est explicitement un brouillon non exécutable en l'état de production ;
- les clés étrangères vers la géographie canonique restent à réconcilier ;
- les 22 680 relations ne sont ni générées ni validées dans une base persistante.

### 5.6 Sources, séries fournisseurs et collecte

**Etat : STRUCTURE PARTIELLEMENT PEUPLEE, DEUX SOURCES LIVE TESTEES**

Données présentes :

- 55 mappings pays/zone × indicateur × source ;
- 50 séries fournisseurs ;
- 17 spécifications de collecte ou templates ;
- 6 lignes de préparation de pilotes ;
- 12 cas de test de collecte ;
- 2 preuves de collecte live.

Implémenté :

- BCEAO FX ;
- BEAC FX.

Documenté mais non implémenté :

- taux directeurs UEMOA/CEMAC ;
- taux interbancaires ;
- indices actions ;
- courbes et adjudications ;
- séries macro ;
- collecte OPCVM par pays.

### 5.7 Modèle fonds, classes, catégories et références

**Etat : MODELE CONCEPTUEL ET SQL DE BROUILLON**

Concepts documentés :

- fonds ;
- classe de parts ;
- classe et sous-classe d'actifs ;
- catégories et sous-catégories nationales, régionales et Afrique ;
- appartenances historisées ;
- blocs de quatre rôles ;
- WTI ;
- WTI Bench ;
- NAV et observations converties.

Limites :

- le modèle ne distingue pas encore complètement `FUND / SUB_FUND / SHARE_CLASS` dans le SQL actuel ;
- aucune migration canonique de production ne crée l'ensemble du domaine fonds ;
- aucune donnée fonds n'est chargée dans le dépôt ;
- aucune catégorie ni sous-catégorie n'est générée ;
- aucun bloc de référence n'est peuplé ;
- aucun WTI ou WTI Bench n'est calculé.

### 5.8 Données OPCVM Tunisie et Nigeria

**Etat : TRAVAUX EXTERNES ANALYSES, NON INTEGRES AU DEPOT**

Le dépôt contient une analyse documentaire de la base tunisienne et des besoins Nigeria. Il ne contient pas les bases SQLite, fichiers Excel sources ni chargeurs pays complets.

La documentation tunisienne décrit un corpus important, mais cette description ne vaut pas intégration canonique dans Openfunds.

### 5.9 API et Atomic Design

**Etat : DECIDE ET DOCUMENTE, NON IMPLEMENTE**

Présent :

- familles de ressources API envisagées ;
- enveloppe canonique conceptuelle ;
- règles Atomic Design ;
- séparation API / view model / présentation.

Absent :

- OpenAPI ;
- GraphQL ;
- serveur API ;
- authentification et autorisation ;
- SDK ;
- composants frontend ;
- tests contractuels.

### 5.10 Mapping Openfunds

**Etat : ABSENT COMME LIVRABLE OPERATIONNEL**

Le projet affirme correctement qu'Openfunds doit être une couche de mapping et non le schéma interne. Cependant :

- aucun catalogue officiel des champs Openfunds n'est versionné dans le dépôt ;
- aucun mapping machine-readable Openfunds → canonique n'est présent ;
- aucune version du standard n'est déclarée ;
- aucune règle de transformation champ par champ n'est implémentée ;
- aucun export Openfunds n'est disponible.

### 5.11 Dictionnaire de données

**Etat : ABSENT COMME REGISTRE UNIFIE**

Les définitions existent de manière fragmentée dans les SQL, CSV et Markdown. Il n'existe pas encore de registre central portant pour chaque champ : type, format, unité, cardinalité, règle qualité, provenance, historisation, mapping externe et version.

## 6. TESTS REELLEMENT EXECUTES

### Tests Python

Les workflows compilent les packages et exécutent :

```bash
python -m compileall -q collectors loaders tests
python -m unittest discover -s tests -p "test_*.py" -v
```

Couverture actuelle :

- parsing BCEAO ;
- parsing BEAC ;
- dates françaises ;
- nombres localisés ;
- transformation canonique XOF/XAF ;
- orchestration quotidienne ;
- statuts de staging et de persistance.

### Tests PostgreSQL

Les workflows utilisent PostgreSQL 16 éphémère et vérifient :

- ordre et réconciliation des schémas d'endpoints ;
- seeds BCEAO et BEAC ;
- lignée des observations FX ;
- insertions déterministes ;
- seconde exécution sans doublon ;
- séparation XOF / XAF ;
- vues des observations courantes.

### Tests live

Les workflows live BCEAO et BEAC ont réussi. Le workflow quotidien double source a également réussi en mode staging.

Limites :

- aucun test d'intégration ne couvre le modèle fonds complet ;
- aucun test ne génère les catégories ou blocs de référence ;
- aucun test ne calcule WTI ou WTI Bench ;
- aucun test ne couvre un mapping Openfunds ;
- aucun test de déploiement en base persistante n'existe.

## 7. DIVERGENCES ET INCOHERENCES IDENTIFIEES

### AUD-001 — README, TODO et SUIVI

- `README.md` ne contenait qu'un titre avant cette consolidation ;
- `TODO.md` était absent ;
- `SUIVI.md` était absent.

Impact : reprise impossible sans relire toute la conversation et l'ensemble des fichiers.

### AUD-002 — Statuts CSV versus seeds SQL

Les CSV présentent encore plusieurs objets BCEAO et BEAC comme `PENDING`, alors que les migrations de seeds et de validation les déclarent `VALIDATED` ou `COLLECTION_TESTED`.

Objets concernés :

- organisations ;
- rôles par périmètre ;
- endpoints ;
- séries fournisseurs ;
- spécifications de collecte ;
- mappings FX.

Action requise : choisir un registre canonique, puis générer les autres représentations depuis celui-ci.

### AUD-003 — Modèles d'endpoints concurrents

Le brouillon pays crée `source.source_endpoint`, tandis que les migrations opérationnelles utilisent `source.endpoint`.

La migration `007_source_endpoint_reconciliation.sql` réconcilie deux variantes de `source.endpoint`, mais pas automatiquement la table séparée `source.source_endpoint` du brouillon pays.

Action requise : remplacer le brouillon parallèle par une référence vers le modèle canonique d'endpoint.

### AUD-004 — Relations pays et `valid_from`

Le CSV canonique autorise des dates d'effet vides lorsque la source historique n'est pas établie. Le schéma `002_country_relationships.sql` impose actuellement `valid_from NOT NULL`.

Action requise : décider entre :

- une date d'effet métier nullable accompagnée d'un statut d'incertitude ;
- une date technique de chargement séparée ;
- une valeur d'effet uniquement après validation documentaire.

Aucune date artificielle ne doit être inventée.

### AUD-005 — Description de la PR devenue obsolète

La description de la PR indique encore qu'aucun `UPDATE` n'existe. Les migrations `010` et `011` contiennent désormais des mises à jour gouvernées de statuts de validation.

Action requise : mettre à jour la description de la PR.

### AUD-006 — Référentiel pays legacy

`african_countries_v0.1.csv` coexiste avec `AFRICA_COUNTRIES.csv`.

Décision existante : `AFRICA_COUNTRIES.csv` est canonique ; le fichier legacy est une source de comparaison uniquement.

Action requise : ajouter un statut explicite `LEGACY_PROPOSAL` ou déplacer le fichier dans un répertoire de sources non canoniques.

### AUD-007 — Catalogue des 420 définitions non centralisé

Les définitions sont documentées, mais aucun artefact machine-readable unique ne les centralise.

Action requise : créer un catalogue canonique versionné avec identifiant, domaine, type, unité, fréquence, devise, source prioritaire, qualité, usage et statut.

### AUD-008 — Absence de migration runner

Les workflows appliquent manuellement une séquence de fichiers SQL. Il n'existe pas encore de registre de migrations ni d'outil unique garantissant l'ordre en production.

Action requise : définir une stratégie de migration versionnée avant tout déploiement persistant.

### AUD-009 — Base persistante et stockage brut absents

Le pipeline quotidien fonctionne mais retourne honnêtement `STAGING_ONLY_DATABASE_NOT_CONFIGURED` lorsque `OPENFUNDS_DATABASE_URL` est absent.

Action requise : configurer une base persistante, un stockage brut immuable et une politique de secrets avant de revendiquer une historisation quotidienne.

### AUD-010 — Openfunds non mappé

Le nom du dépôt ne doit pas masquer l'absence actuelle du mapping champ par champ.

Action requise : obtenir une version officielle du standard, en conserver la provenance, puis créer un mapping humain et machine-readable.

### AUD-011 — Domaine fonds incomplet

Le SQL actuel contient `fund.fund` et `fund.share_class` mais pas un objet `sub_fund` pleinement modélisé, alors que la décision fonctionnelle impose la séparation Fund / SubFund / ShareClass.

Action requise : arbitrage et migration avant chargement de données fonds.

### AUD-012 — PR non fusionnée et `main` minimal

Les workflows planifiés et la documentation ne constituent pas encore la base par défaut du projet.

Action requise : terminer la revue, stabiliser les migrations, mettre la PR à jour puis décider de la fusion.

## 8. MATRICE DE MATURITE

| Composant | Référentiel | Mapping source | Historique réel | Calculs | Tests | Statut consolidé |
|---|---|---|---|---|---|---|
| Pays / régions | Oui | Partiel | N/A | N/A | Validation documentaire | Partiellement validé |
| Zones UEMOA/CEMAC/CMA | Oui | Partiel | N/A | N/A | Partiel | Partiellement validé |
| Devises | Oui | Partiel | Non | Conversion pilote | Oui | Testé sur pilote |
| FX BCEAO | Oui | Oui | Snapshot unique | XOF/EUR/USD | Oui live + PostgreSQL | Collection testée |
| FX BEAC | Oui | Oui | Snapshot unique | XAF/EUR/USD | Oui live + PostgreSQL | Collection testée |
| Organisations | Partiel | Partiel | N/A | N/A | Seeds partiels | En cours |
| Indicateurs D00-D17 | Documentation | Partiel | Non | Non | Non | Proposé / documenté |
| Données macro | Modèle | Partiel | Non | Non | Non | Non commencé |
| Fonds OPCVM | Modèle partiel | Pays pilotes | Non dans le dépôt | Non | Non | A concevoir / intégrer |
| Catégories | Modèle | Non | Non | Non | Non | Proposé |
| WTI | Méthode | Non | Non | Non | Non | Décidé, non implémenté |
| WTI Bench | Méthode | Non | Non | Non | Non | Partiellement décidé |
| API | Ressources proposées | N/A | N/A | N/A | Non | Non implémenté |
| Atomic Design | Principes | N/A | N/A | N/A | Non | Documenté uniquement |
| Mapping Openfunds | Principe | Non | N/A | N/A | Non | Absent |
| Dictionnaire canonique | Fragmenté | N/A | N/A | N/A | Non | A construire |

## 9. RISQUES PRIORITAIRES

1. **Deux sources de vérité** entre CSV et seeds SQL.
2. **Parallélisme de modèles** entre `source.endpoint` et `source.source_endpoint`.
3. **Fausse complétude** si les 420 définitions sont confondues avec 420 séries historiques chargées.
4. **Perte de provenance** si la future base persistante n'archive pas les fichiers bruts.
5. **Dates artificielles** si les contraintes SQL imposent une date métier inconnue.
6. **Conflit Fund/SubFund/ShareClass** avant intégration des fonds Nigeria/Tunisie.
7. **Dérive documentaire** si README, TODO, SUIVI et décisions ne sont pas mis à jour après chaque étape.
8. **Migrations non gouvernées** si l'ordre manuel des scripts est copié en production.
9. **Planification trompeuse** si un workflow de staging est présenté comme historique durable.
10. **Indices non reproductibles** si les sources, univers, calendriers et méthodologies ne sont pas versionnés avant calcul.

## 10. PRIORITES DE CONSOLIDATION

### P0 — Documentation et source de vérité

- compléter `README.md` ;
- créer `TODO.md` ;
- créer `SUIVI.md` ;
- formaliser `DECISIONS.md` ;
- formaliser l'architecture, la gouvernance, les règles qualité et la roadmap ;
- mettre à jour la description de la PR.

### P1 — Réconciliation des modèles

- choisir les tables canoniques d'endpoints ;
- synchroniser CSV et SQL ;
- décider le traitement de `valid_from` inconnu ;
- consolider Fund / SubFund / ShareClass ;
- créer un registre de migrations.

### P2 — Dictionnaire et mapping

- centraliser les 420 définitions ;
- construire le dictionnaire canonique ;
- intégrer le standard Openfunds versionné ;
- produire le mapping machine-readable.

### P3 — Persistance et historiques

- base PostgreSQL persistante ;
- stockage brut immuable ;
- couverture et gaps ;
- backfill FX ;
- collecte des autres indicateurs.

### P4 — Produits analytiques

- catégories et sous-catégories ;
- blocs de quatre références ;
- indices de marché ;
- WTI ;
- WTI Bench ;
- métriques et classements ;
- API et view models.

## 11. DEFINITION DE FIN DE L'AUDIT

L'audit est terminé lorsque :

- l'inventaire est conservé dans le dépôt ;
- les divergences sont identifiées et traçables ;
- aucun composant non implémenté n'est présenté comme terminé ;
- les documents racines reprennent cet état ;
- le point exact de reprise est inscrit dans `SUIVI.md` ;
- les tâches de correction disposent d'identifiants et de critères d'acceptation.
