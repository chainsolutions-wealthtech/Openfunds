# Matrice canonique préremplie de classification des fonds

## Statut

```text
VERSION : 0.1.0
CANONICAL_STATUS : STRUCTURE_PREFILLED
PRODUCTION_STATUS : NOT_ACTIVE
PERSISTANCE RUNTIME : MIGRATION 017 GOUVERNEE / POSTGRESQL 16 VERIFIE
```

Ce répertoire contient la première matrice canonique normalisée permettant de router automatiquement un fonds à partir de son pays juridique, de sa classe d’actifs et de sa sous-classe éventuelle.

La matrice maîtresse reste compacte et révisable. Le générateur produit ensuite les vues développées complètes :

```text
486 REGLES DE ROUTAGE
432 CATEGORIES ET BLOCS DE REFERENCES
```

Les objets sont préremplis sur le plan structurel. Cela ne signifie pas que toutes les séries de marché, tous les taux sans risque ou toutes les méthodologies de benchmark sont déjà validés.

Depuis le 2026-08-17, cette structure est persistée de manière gouvernée par `017_CANONICAL_FUND_TAXONOMY_V0_1`. Les fichiers de ce répertoire restent la surface d'authoring/revue ; un snapshot immuable alimente le générateur SQL et PostgreSQL devient la vérité runtime après application. Cette persistance **n'active pas** les templates : `CANONICAL_STATUS=STRUCTURE_PREFILLED` et `PRODUCTION_STATUS=NOT_ACTIVE` restent obligatoires.

## Hiérarchie

```text
PAYS JURIDIQUE DU FONDS
→ NIVEAU LOCAL DE MARCHE
→ REGION GEOGRAPHIQUE
→ AFRICA
```

Règle locale :

```text
SI LE PAYS APPARTIENT A UNE BOURSE COMMUNE REGIONALE
    LOCAL_SCOPE = ZONE DE MARCHE
SINON
    LOCAL_SCOPE = PAYS
```

Conséquences :

```text
PAYS UEMOA → UEMOA → AFRICA_OUEST → AFRICA
PAYS CEMAC → CEMAC → AFRICA_CENTRALE → AFRICA
NIGERIA    → NIGERIA → AFRICA_OUEST → AFRICA
MAROC      → MAROC → AFRICA_NORD → AFRICA
```

Le pays juridique n’est jamais supprimé.

## Taxonomie V0.1

Neuf feuilles de classification :

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
- `OBLIGATIONS` : sous-classe obligatoire parmi court, moyen et long terme ;
- `DIVERSIFIE` : sous-classe obligatoire parmi prudent, équilibré, dynamique et flexible ;
- `MONETAIRE` : aucune sous-classe.

## Fichiers maîtres

### `ASSET_CLASSES_V0_1.csv`

Quatre classes d’actifs et leur règle de sous-classe.

### `ASSET_SUBCLASSES_V0_1.csv`

Sept sous-classes :

- trois `DURATION_BUCKET` obligataires ;
- quatre `RISK_PROFILE` diversifiés.

### `FUND_SCOPE_ROUTING_V0_1.csv`

54 lignes, une par pays juridique.

Chaque ligne fixe :

- le niveau local de marché ;
- la bourse commune éventuelle ;
- la devise locale ;
- la région géographique ;
- le continent ;
- la raison du routage.

### `CATEGORY_TEMPLATE_MATRIX_V0_1.csv`

Neuf modèles préremplis, un par feuille de taxonomie.

Chaque modèle définit déjà :

- le code de catégorie ;
- le groupe de pairs ;
- le WTI de catégorie ;
- la moyenne et la médiane ;
- le benchmark principal ;
- le benchmark secondaire ;
- le WTI Bench ;
- le taux sans risque ;
- le rendement minimal acceptable ;
- les séries du graphique ;
- la méthode de classement ;
- la politique de conversion ;
- les statuts de validation et de production.

Les modèles utilisent `{SCOPE}`. Le générateur le remplace par le pays, la zone, la région ou `AFRICA`.

### `SCOPE_REFERENCE_OVERRIDES_V0_1.csv`

Exceptions et candidats propres à certains marchés.

Exemples :

```text
UEMOA_ACTIONS  → BRVM_COMPOSITE
CEMAC_ACTIONS  → BVMAC_ALL_SHARE
MAROC_ACTIONS  → MASI
NIGERIA_ACTIONS → NGX_ALL_SHARE
```

Ces codes sont des candidats à valider, pas des séries déjà collectées.

### `ANALYTICS_REFERENCE_REQUIREMENTS_V0_1.csv`

La matrice indique quelle référence est nécessaire pour chaque métrique.

```text
RANG / QUARTILE / PERCENTILE
→ GROUPE DE PAIRS

SURPERFORMANCE FACE A LA CATEGORIE
→ WTI DE CATEGORIE

BETA / R² / INFORMATION RATIO
→ BENCHMARK PRINCIPAL

SHARPE
→ TAUX SANS RISQUE

JENSEN / TREYNOR
→ BENCHMARK PRINCIPAL + TAUX SANS RISQUE

SORTINO
→ RENDEMENT MINIMAL ACCEPTABLE
```

### `MATRIX_MANIFEST_V0_1.json`

Décrit les règles, les volumes attendus et les sorties développées.

## Génération des vues complètes

```bash
python scripts/generate_fund_category_matrices.py
```

Sortie par défaut :

```text
build/canonical/FUND_CATEGORY_ROUTING_MATRIX_V0_1.csv
build/canonical/CATEGORY_REFERENCE_MATRIX_V0_1.csv
build/canonical/ANALYTICS_REFERENCE_REQUIREMENTS_V0_1.csv
build/canonical/MATRIX_MANIFEST_V0_1.json
```

Contrôle sans écriture :

```bash
python scripts/generate_fund_category_matrices.py --check
```

Répertoire personnalisé :

```bash
python scripts/generate_fund_category_matrices.py \
  --output-dir /tmp/openfunds-canonical
```

Tests :

```bash
python -m unittest tests/test_fund_category_matrices.py
```

## Volumétrie développée

```text
54 pays × 9 feuilles = 486 règles de routage
```

```text
42 périmètres locaux × 9 = 378
5 régions × 9             = 45
AFRICA × 9                = 9
TOTAL                     = 432 blocs de références
```

## Affichage graphique

Chaque bloc prévoit :

```text
SERIE 1 : FONDS BASE 100
SERIE 2 : WTI DE CATEGORIE
SERIE 3 : BENCHMARK PRINCIPAL OU WTI BENCH
SERIE 4 : REFERENCE OPTIONNELLE
```

Deux références sont affichées par défaut. Une troisième peut être activée en plus du fonds.

## Limites explicites

- les codes de benchmark sont d’abord des rôles canoniques ;
- les provider series candidates ne sont pas toutes validées ;
- `WTI_BENCH_STATUS=METHODOLOGY_TO_VALIDATE` ne signifie pas que l’indice est calculable ;
- `RISK_FREE_STATUS=SERIES_TO_VALIDATE` ne signifie pas qu’un taux sans risque officiel est choisi ;
- les dates restent vides tant qu’elles ne sont pas connues ;
- aucune matrice n’est chargée en production ;
- l’intégration PostgreSQL dépend de `ADR-021` et de la stratégie de migrations.

Aucune valeur manquante n’est remplacée par zéro et aucune date artificielle n’est inventée.
