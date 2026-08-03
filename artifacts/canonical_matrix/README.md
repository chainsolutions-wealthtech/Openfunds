# Export Excel de la matrice canonique AfricaFunds

## Statut

```text
ARTEFACT : MATRICE EXCEL DE REVUE
SOURCE CANONIQUE : data/canonical/ + générateur Python
SOURCE DE VERITE AUTONOME : NON
CHARGEMENT PRODUCTION : INTERDIT
VERSION DU MODELE CANONIQUE : 0.1.0
VERSION DE L’EXPORT EXCEL : 0.4.1
DATE : 2026-08-03
```

Ce répertoire conserve un classeur Excel destiné à la revue fonctionnelle, au contrôle métier et au préremplissage interactif d’un fonds.

Le classeur ne remplace pas les fichiers normalisés de `data/canonical/` et ne doit jamais devenir une seconde source de vérité. Les modifications métier doivent être apportées d’abord aux entrées canoniques, puis régénérées et réexportées.

## Fichier

```text
Matrice_Canonique_AfricaFunds_54_Pays_V4_20260803.xlsx
```

SHA256 :

```text
44e632766b1f43a9b33bab97f4a986d82f17d9b57e55694026c42942c823a9fa
```

## Volumétrie vérifiée

```text
54 pays juridiques
42 périmètres locaux de marché
5 régions africaines
1 continent
9 feuilles de taxonomie
486 règles pays × catégorie
432 catégories canoniques uniques
432 groupes de pairs
432 blocs de référence
```

Les contrôles de cohérence du classeur sont tous à `PASS`.

## Règle de hiérarchie

```text
PAYS JURIDIQUE
→ LOCAL_MARKET
→ REGION
→ AFRICA
```

Le pays juridique reste une donnée d’identité et de réglementation.

Le niveau local est déterminé par le marché de référence :

```text
PAYS BRVM  → UEMOA → AFRICA_OUEST → AFRICA
PAYS BVMAC → CEMAC → AFRICA_CENTRALE → AFRICA
AUTRE PAYS → PAYS → REGION → AFRICA
```

Exemple :

```text
COTE_DIVOIRE + OBLIGATIONS + COURT_TERME
→ UEMOA_OBLIGATIONS_COURT_TERME
→ AFRICA_OUEST_OBLIGATIONS_COURT_TERME
→ AFRICA_OBLIGATIONS_COURT_TERME
```

## Taxonomie

```text
ACTIONS
OBLIGATIONS_COURT_TERME
OBLIGATIONS_MOYEN_TERME
OBLIGATIONS_LONG_TERME
DIVERSIFIE_PRUDENT
DIVERSIFIE_EQUILIBRE
DIVERSIFIE_DYNAMIQUE
DIVERSIFIE_FLEXIBLE
MONETAIRE
```

Règles :

- `ACTIONS` : aucune sous-classe ;
- `MONETAIRE` : aucune sous-classe ;
- `OBLIGATIONS` : sous-classe obligatoire ;
- `DIVERSIFIE` : sous-classe obligatoire.

Les bornes exactes de duration et les seuils des profils diversifiés restent des méthodologies à valider.

## Séparation des références

Le classeur sépare explicitement :

```text
PEER_GROUP
CATEGORY_WTI
PRIMARY_MARKET_BENCHMARK
SECONDARY_MARKET_BENCHMARK
WTI_BENCH
RISK_FREE_RATE
MINIMUM_ACCEPTABLE_RETURN
```

Ces objets n’ont pas la même fonction.

### Groupe de pairs

Utilisé pour :

- rang ;
- percentile ;
- quartile ;
- moyenne et médiane de catégorie ;
- dispersion des fonds comparables.

### WTI de catégorie

Utilisé pour comparer la performance du fonds à la performance observée de sa catégorie.

### Benchmark de marché et WTI Bench

Utilisés pour :

- performance active ;
- tracking error ;
- information ratio ;
- bêta ;
- alpha ;
- R² ;
- capture haussière et baissière.

### Taux sans risque

Utilisé notamment pour :

- Sharpe ;
- Treynor ;
- Jensen ;
- M².

### Rendement minimal acceptable

Utilisé notamment pour le Sortino.

## Onglets du classeur

### `README v4`

Résumé, volumétrie, règles maîtres et graphique des catégories par niveau.

### `Decision Tree v4`

Séquence de décision depuis l’identité du fonds jusqu’aux références de calcul.

### `Scope Routing v4`

54 lignes reliant chaque pays juridique à son périmètre local, sa région et l’Afrique.

### `Taxonomy v4`

Neuf feuilles canoniques de classification.

### `Fund Routing Rules v4`

486 règles déterministes :

```text
54 pays × 9 feuilles de taxonomie
```

Chaque règle produit les catégories, groupes de pairs et blocs de référence local, régional et Afrique.

### `Category Matrix v4`

432 objets catégorie uniques.

### `Reference Matrix v4`

432 blocs de référence comprenant WTI, benchmarks, WTI Bench, taux sans risque, MAR, séries de graphique et dépendances analytiques.

### `Ratio Rules v4`

Dépendances nécessaires à chaque ratio.

### `Fund Prefill v4`

Exemple interactif. Les cellules d’entrée sont :

```text
FUND_ID
LEGAL_COUNTRY_CODE
ASSET_CLASS_CODE
ASSET_SUBCLASS_CODE
```

Le classeur calcule ensuite les trois catégories, les trois groupes de pairs et les trois blocs de référence.

Cet onglet est une vue d’usage, pas une source canonique.

### `Repository Alignment`

Correspondance entre chaque onglet et les fichiers du dépôt.

### `Canonical QA v4`

Contrôles de volumétrie et d’unicité.

### `Changelog v4`

Historique des règles intégrées à l’export.

## Correspondance avec le dépôt

| Classeur | Autorité du dépôt |
|---|---|
| Scope Routing v4 | `data/canonical/FUND_SCOPE_ROUTING_V0_1.csv` |
| Taxonomy v4 | `data/canonical/ASSET_CLASSES_V0_1.csv` et `ASSET_SUBCLASSES_V0_1.csv` |
| Fund Routing Rules v4 | `build/canonical/FUND_CATEGORY_ROUTING_MATRIX_V0_1.csv` |
| Category Matrix v4 | vue de `build/canonical/CATEGORY_REFERENCE_MATRIX_V0_1.csv` |
| Reference Matrix v4 | `build/canonical/CATEGORY_REFERENCE_MATRIX_V0_1.csv` |
| Ratio Rules v4 | `data/canonical/ANALYTICS_REFERENCE_REQUIREMENTS_V0_1.csv` |
| Decision Tree v4 | `docs/02_DOMAIN_MODEL/FUND_CLASSIFICATION_AND_REFERENCE_MATRIX_V0_1.md` |

## Procédure de modification

1. modifier les fichiers normalisés sous `data/canonical/` ;
2. exécuter les tests ;
3. régénérer les vues développées ;
4. contrôler les volumes et l’unicité ;
5. produire un nouvel export Excel ;
6. calculer et enregistrer son SHA256 ;
7. mettre à jour ce README et le manifeste ;
8. ne jamais corriger uniquement le classeur.

Commandes :

```bash
python scripts/generate_fund_category_matrices.py --check
python -m unittest tests/test_fund_category_matrices.py
python scripts/generate_fund_category_matrices.py
```

## Statuts

```text
STRUCTURE_PREFILLED
CANDIDATE_IDENTIFIED
CANDIDATE_TO_VALIDATE
METHODOLOGY_TO_DEFINE
TO_RESEARCH
NOT_ACTIVE
COLLECTION_TESTED
CALCULATION_READY
```

`STRUCTURE_PREFILLED` ne signifie pas que la donnée existe ni que le calcul est activé.

## Limites

- le choix final de certains indices reste à valider ;
- les licences de certaines séries doivent être vérifiées ;
- les taux sans risque ne sont pas tous arrêtés ;
- le MAR du Sortino doit être versionné par catégorie ;
- les méthodologies WTI et WTI Bench restent à approuver ;
- les dates métier inconnues restent vides ;
- l’export n’est pas chargé en production ;
- la source de vérité CSV/SQL globale reste soumise à `ADR-021`.

Aucune valeur manquante n’est remplacée par zéro et aucune date n’est inventée.