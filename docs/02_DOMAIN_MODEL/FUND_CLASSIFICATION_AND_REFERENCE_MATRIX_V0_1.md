# Arbre de décision et matrice canonique de classification des fonds — V0.1

## 1. Objet

Le système doit pouvoir recevoir un fonds avec un minimum d’informations et produire automatiquement son environnement de classification, de comparaison, de benchmark et d’analyse.

Entrée minimale :

```text
LEGAL_COUNTRY_CODE
ASSET_CLASS_CODE
ASSET_SUBCLASS_CODE éventuel
```

Sortie attendue :

```text
LOCAL_CATEGORY
REGIONAL_CATEGORY
AFRICA_CATEGORY

LOCAL_PEER_GROUP
REGIONAL_PEER_GROUP
AFRICA_PEER_GROUP

LOCAL_REFERENCE_BLOCK
REGIONAL_REFERENCE_BLOCK
AFRICA_REFERENCE_BLOCK
```

Chaque bloc de références contient les objets nécessaires aux graphiques, aux classements et aux ratios.

## 2. Séparation des responsabilités

Quatre objets ne doivent jamais être confondus.

### 2.1 Catégorie et groupe de pairs

Ils servent à répondre à la question :

> Avec quels fonds ce fonds doit-il être classé ?

Ils permettent de calculer :

- rang ;
- percentile ;
- quartile ;
- moyenne ;
- médiane ;
- écart à la moyenne ;
- statistiques de dispersion de la catégorie.

### 2.2 WTI de catégorie

Le WTI représente une série temporelle construite à partir des fonds éligibles de la catégorie.

Il sert à répondre à la question :

> Comment l’ensemble des fonds comparables a-t-il réellement performé ?

Il permet notamment :

- comparaison en base 100 ;
- surperformance face aux pairs ;
- corrélation avec la catégorie ;
- tracking error face à la catégorie.

### 2.3 Benchmark de marché et WTI Bench

Le benchmark de marché est indépendant du groupe de fonds.

Il sert à répondre à la question :

> Comment le fonds s’est-il comporté face au marché ou au portefeuille théorique correspondant à son mandat ?

Il permet notamment :

- performance active ;
- tracking error de marché ;
- information ratio ;
- bêta ;
- alpha ;
- R² ;
- capture haussière et baissière.

Le WTI Bench est le benchmark canonique calculé lorsque l’indice officiel unique n’est pas suffisant ou n’existe pas.

### 2.4 Taux sans risque et rendement minimal acceptable

Le taux sans risque sert notamment au calcul de :

- Sharpe ;
- Treynor ;
- alpha de Jensen ;
- M².

Le rendement minimal acceptable sert notamment au Sortino.

Un indice actions ou obligataire ne doit jamais être utilisé comme remplacement silencieux du taux sans risque.

## 3. Hiérarchie géographique et de marché

La hiérarchie retenue est :

```text
IDENTITE JURIDIQUE : PAYS REEL DU FONDS

NIVEAU 1 : LOCAL DE MARCHE
NIVEAU 2 : REGION GEOGRAPHIQUE
NIVEAU 3 : AFRICA
```

### 3.1 UEMOA

Pour tout pays membre du marché commun BRVM :

```text
BENIN
BURKINA_FASO
COTE_DIVOIRE
GUINEE_BISSAU
MALI
NIGER
SENEGAL
TOGO
```

La hiérarchie est :

```text
UEMOA
→ AFRICA_OUEST
→ AFRICA
```

Exemple :

```text
LEGAL_COUNTRY_CODE = COTE_DIVOIRE
LOCAL_SCOPE_CODE   = UEMOA
REGIONAL_SCOPE     = AFRICA_OUEST
CONTINENT_SCOPE    = AFRICA
```

### 3.2 CEMAC

Pour tout pays membre du marché commun BVMAC :

```text
CAMEROUN
GABON
REPUBLIQUE_CENTRAFRICAINE
REPUBLIQUE_DU_CONGO
GUINEE_EQUATORIALE
TCHAD
```

La hiérarchie est :

```text
CEMAC
→ AFRICA_CENTRALE
→ AFRICA
```

### 3.3 Pays avec marché individuel

Exemple Nigeria :

```text
NIGERIA
→ AFRICA_OUEST
→ AFRICA
```

Le pays juridique reste toujours conservé, y compris lorsque la catégorie locale utilise UEMOA ou CEMAC.

## 4. Taxonomie

### 4.1 Actions

```text
ACTIONS
```

Aucune sous-classe canonique dans la V0.1.

### 4.2 Obligations

```text
OBLIGATIONS_COURT_TERME
OBLIGATIONS_MOYEN_TERME
OBLIGATIONS_LONG_TERME
```

La sous-classe représente une dimension de maturité ou de duration. Les bornes exactes devront être versionnées dans une méthodologie dédiée.

### 4.3 Diversifié

```text
DIVERSIFIE_PRUDENT
DIVERSIFIE_EQUILIBRE
DIVERSIFIE_DYNAMIQUE
DIVERSIFIE_FLEXIBLE
```

La sous-classe représente un profil de risque ou d’allocation. Les seuils exacts devront être versionnés.

### 4.4 Monétaire

```text
MONETAIRE
```

Aucune sous-classe canonique dans la V0.1.

## 5. Arbre de décision

```text
UN FONDS
│
├── Lire le pays juridique
│
├── Lire la classe d’actifs
│
├── La classe exige-t-elle une sous-classe ?
│   ├── ACTIONS       → non
│   ├── MONETAIRE     → non
│   ├── OBLIGATIONS   → oui : CT / MT / LT
│   └── DIVERSIFIE    → oui : prudent / équilibré / dynamique / flexible
│
├── Le pays relève-t-il d’une bourse commune ?
│   ├── BRVM  → LOCAL_SCOPE = UEMOA
│   ├── BVMAC → LOCAL_SCOPE = CEMAC
│   └── non   → LOCAL_SCOPE = PAYS
│
├── Déterminer la région géographique
│
├── Construire les trois catégories
│   ├── LOCAL_SCOPE + FEUILLE DE TAXONOMIE
│   ├── REGION + FEUILLE DE TAXONOMIE
│   └── AFRICA + FEUILLE DE TAXONOMIE
│
├── Affecter les trois groupes de pairs
│
├── Affecter les trois blocs de références
│
└── Résoudre, pour chaque bloc :
    ├── WTI de catégorie
    ├── benchmark principal
    ├── benchmark secondaire
    ├── WTI Bench
    ├── taux sans risque
    ├── rendement minimal acceptable
    ├── séries du graphique
    ├── méthode de classement
    └── méthode de conversion
```

## 6. Matrice normalisée et volumétrie développée

La source canonique V0.1 reste normalisée :

```text
54 ROUTES PAYS
9 MODELES DE CATEGORIE
11 SURCHARGES DE REFERENCES
25 REGLES DE DEPENDANCE ANALYTIQUE
```

Le générateur produit ensuite les vues complètes.

### 6.1 Règles de routage développées

```text
54 pays × 9 feuilles = 486 règles
```

### 6.2 Catégories et blocs uniques développés

```text
42 périmètres locaux × 9 = 378
5 régions × 9             = 45
AFRICA × 9                = 9
TOTAL                     = 432
```

Les 42 périmètres locaux résultent de la substitution des huit pays UEMOA par un périmètre UEMOA et des six pays CEMAC par un périmètre CEMAC. Les vues développées sont régénérées, non saisies manuellement.

## 7. Contenu d’un bloc de références

Exemple :

```text
REFERENCE_BLOCK_CODE
RB_UEMOA_OBLIGATIONS_COURT_TERME

CATEGORY_CODE
UEMOA_OBLIGATIONS_COURT_TERME

PEER_GROUP_CODE
PG_UEMOA_OBLIGATIONS_COURT_TERME

CATEGORY_WTI_CODE
WTI_UEMOA_OBLIGATIONS_COURT_TERME

PRIMARY_BENCHMARK_CODE
BM_UEMOA_SOV_SHORT_TR

SECONDARY_BENCHMARK_CODE
BM_UEMOA_SOV_ALL_TR

WTI_BENCH_CODE
WTIB_UEMOA_OBLIGATIONS_COURT_TERME

RISK_FREE_RATE_CODE
RFR_UEMOA_DEFAULT

MINIMUM_ACCEPTABLE_RETURN_CODE
MAR_UEMOA_OBLIGATIONS_COURT_TERME
```

## 8. Organisation des graphiques

Chaque graphique peut afficher le fonds et jusqu’à trois références.

### 8.1 Actions

Par défaut :

```text
FONDS BASE 100
WTI DE CATEGORIE
BENCHMARK ACTIONS PRINCIPAL
```

Option :

```text
WTI BENCH
```

### 8.2 Obligations

Par défaut :

```text
FONDS BASE 100
WTI DE CATEGORIE
WTI BENCH OBLIGATAIRE
```

Option :

```text
BENCHMARK SOUVERAIN DE MATURITE
```

### 8.3 Diversifié

Par défaut :

```text
FONDS BASE 100
WTI DE CATEGORIE
WTI BENCH COMPOSITE
```

Option :

```text
BENCHMARK COMPOSITE PRINCIPAL
```

### 8.4 Monétaire

Par défaut :

```text
FONDS BASE 100
WTI DE CATEGORIE
BENCHMARK MONETAIRE PRINCIPAL
```

Option :

```text
WTI BENCH MONETAIRE
```

## 9. Exemple complet

Entrée :

```text
LEGAL_COUNTRY_CODE = COTE_DIVOIRE
ASSET_CLASS_CODE = OBLIGATIONS
ASSET_SUBCLASS_CODE = COURT_TERME
```

Résultat :

```text
LOCAL_CATEGORY
UEMOA_OBLIGATIONS_COURT_TERME

REGIONAL_CATEGORY
AFRICA_OUEST_OBLIGATIONS_COURT_TERME

CONTINENT_CATEGORY
AFRICA_OBLIGATIONS_COURT_TERME
```

Groupes :

```text
PG_UEMOA_OBLIGATIONS_COURT_TERME
PG_AFRICA_OUEST_OBLIGATIONS_COURT_TERME
PG_AFRICA_OBLIGATIONS_COURT_TERME
```

Blocs :

```text
RB_UEMOA_OBLIGATIONS_COURT_TERME
RB_AFRICA_OUEST_OBLIGATIONS_COURT_TERME
RB_AFRICA_OBLIGATIONS_COURT_TERME
```

## 10. Statuts et gouvernance

`STRUCTURE_PREFILLED` signifie que l’objet, son code et son rôle sont précréés.

Il ne signifie pas :

- que l’historique est chargé ;
- que le fournisseur est validé ;
- que la licence est acquise ;
- que la méthodologie WTI ou WTI Bench est approuvée ;
- que le taux sans risque a été choisi ;
- que le calcul est actif en production.

Les statuts de données et de méthodologie restent séparés.

## 11. Artefacts

Sources canoniques normalisées :

```text
data/canonical/ASSET_CLASSES_V0_1.csv
data/canonical/ASSET_SUBCLASSES_V0_1.csv
data/canonical/FUND_SCOPE_ROUTING_V0_1.csv
data/canonical/CATEGORY_TEMPLATE_MATRIX_V0_1.csv
data/canonical/SCOPE_REFERENCE_OVERRIDES_V0_1.csv
data/canonical/ANALYTICS_REFERENCE_REQUIREMENTS_V0_1.csv
data/canonical/MATRIX_MANIFEST_V0_1.json
```

Générateur et tests :

```text
scripts/generate_fund_category_matrices.py
tests/test_fund_category_matrices.py
```

Vues développées générées :

```text
build/canonical/FUND_CATEGORY_ROUTING_MATRIX_V0_1.csv
build/canonical/CATEGORY_REFERENCE_MATRIX_V0_1.csv
build/canonical/ANALYTICS_REFERENCE_REQUIREMENTS_V0_1.csv
build/canonical/MATRIX_MANIFEST_V0_1.json
```

## 12. Prochaines décisions

La structure est désormais déterministe. Les décisions restantes portent principalement sur :

1. la source de vérité technique CSV/SQL ;
2. les bornes exactes des sous-classes obligataires ;
3. les seuils des profils diversifiés ;
4. la pondération du WTI ;
5. la méthodologie du WTI Bench ;
6. le choix du taux sans risque par périmètre ;
7. le choix du MAR pour le Sortino ;
8. la validation et la licence des séries de benchmark ;
9. l’activation en production et les dates métier.
