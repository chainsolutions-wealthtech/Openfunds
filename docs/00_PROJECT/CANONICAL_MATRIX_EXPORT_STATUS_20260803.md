# Statut de l’export Excel de la matrice canonique — 2026-08-03

## Résultat

Un classeur de revue a été produit à partir des règles validées de classification des fonds.

```text
ARTEFACT
artifacts/canonical_matrix/Matrice_Canonique_AfricaFunds_54_Pays_V4_20260803.xlsx

EXPORT_VERSION
0.4.1

CANONICAL_MODEL_VERSION
0.1.0

STATUS
NON_CANONICAL_DERIVED_EXPORT
```

## Ce qui est couvert

- 54 pays juridiques ;
- routage UEMOA et CEMAC vers leur marché commun ;
- cinq régions et le niveau Afrique ;
- neuf feuilles de taxonomie ;
- 486 règles pays × catégorie ;
- 432 catégories uniques ;
- 432 groupes de pairs ;
- 432 blocs de référence ;
- WTI natif, EUR et USD ;
- WTI Bench natif, EUR et USD ;
- benchmark principal et secondaire ;
- taux sans risque et rendement minimal acceptable ;
- séries à afficher ;
- dépendances de calcul des ratios ;
- exemple de préremplissage automatique d’un fonds.

## Règle validée

```text
PAYS JURIDIQUE
→ LOCAL_MARKET
→ REGION
→ AFRICA
```

Cas particuliers :

```text
PAYS BRVM  → UEMOA → AFRICA_OUEST → AFRICA
PAYS BVMAC → CEMAC → AFRICA_CENTRALE → AFRICA
```

Le pays juridique reste conservé séparément.

## Source de vérité

Le classeur n’est pas la source canonique.

Autorité :

```text
data/canonical/
scripts/generate_fund_category_matrices.py
tests/test_fund_category_matrices.py
build/canonical/
```

Toute modification doit être faite dans les entrées normalisées, testée et régénérée avant de produire un nouvel export Excel.

## Contrôles

```text
54 pays                         PASS
42 périmètres locaux           PASS
8 pays UEMOA                    PASS
6 pays CEMAC                    PASS
9 feuilles de taxonomie        PASS
486 règles de routage          PASS
432 catégories                 PASS
432 blocs de référence         PASS
432 codes catégorie uniques    PASS
432 groupes de pairs uniques   PASS
432 blocs uniques              PASS
FORMULA ERROR SCAN             NO MATCH
```

## Limites

L’export préremplit la structure et les rôles. Il ne prouve pas que :

- l’historique d’un indice est disponible ;
- la licence est acquise ;
- le benchmark est officiellement validé ;
- la méthodologie WTI ou WTI Bench est approuvée ;
- le taux sans risque est définitivement choisi ;
- les calculs sont actifs en production.

Les objets concernés conservent des statuts comme `TO_RESEARCH`, `CANDIDATE_TO_VALIDATE` ou `METHODOLOGY_TO_DEFINE`.

## Point de reprise

Le prochain travail sur cette matrice doit porter sur :

1. validation des bornes CT/MT/LT ;
2. validation des profils prudent/équilibré/dynamique/flexible ;
3. méthodologie de pondération du WTI ;
4. méthodologie WTI Bench par classe ;
5. sélection des taux sans risque et MAR ;
6. validation des indices et licences ;
7. rattachement au modèle final Fund/SubFund/ShareClass ;
8. persistance après les décisions `OF-ARCH-001` à `OF-ARCH-004`.

Aucune date métier inconnue n’a été inventée et aucune valeur manquante n’a été convertie en zéro.