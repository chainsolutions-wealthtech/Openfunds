# Fund Relationship Information Model — v0.1

## 1. Objet

Ce document matérialise le socle relationnel permettant, à partir d’un fonds, de son pays, de sa classe d’actifs et éventuellement de sa sous-classe d’actifs, de retrouver automatiquement toutes les informations de classification, de regroupement, de référence, de conversion et de comparaison applicables aux niveaux national, régional et Afrique.

Le modèle repose sur des identifiants stables et des relations historisées. Les noms lisibles sont générés par concaténation, mais ils ne remplacent jamais les relations en base.

---

## 2. Variables de départ minimales

```text
fund_id
country_id
asset_class_id
sub_asset_class_id (nullable)
classification_date
```

Exemple :

```text
fund_id = FUND_EXAMPLE_MAR_CT
country = Maroc
asset_class = Obligations
sub_asset_class = Court terme (CT)
```

---

## 3. Référentiels génériques retenus

### 3.1 Classes d’actifs

```text
Actions
Obligations
Diversifié
Monétaire
```

### 3.2 Sous-classes d’actifs

```text
Actions
└── À définir

Obligations
├── Court terme (CT)
├── Moyen terme (MT)
└── Long terme (LT)

Diversifié
├── Prudent
├── Équilibré
├── Dynamique
└── Flexible

Monétaire
└── Monétaire
```

---

## 4. Chaîne géographique

Chaque pays est relié à une région géographique, elle-même reliée au continent Afrique.

Exemple :

```text
Maroc
→ Afrique du Nord
→ Afrique
```

Les unions monétaires ou économiques, telles que l’UEMOA et la CEMAC, constituent une dimension distincte de la région géographique.

---

## 5. Catégorie nationale

### 5.1 Règle

```text
Pays + Classe d’actifs
→ Catégorie nationale
```

### 5.2 Nommage

```text
[Classe d’actifs] + [Nom du pays]
```

Exemples :

```text
Actions Maroc
Obligations Maroc
Diversifié Maroc
Monétaire Maroc
```

### 5.3 Relations obligatoires

```text
national_category.country_id
national_category.asset_class_id
national_category.geographic_level = NATIONAL
```

---

## 6. Sous-catégorie nationale

### 6.1 Règle

```text
Pays + Classe d’actifs + Sous-classe d’actifs
→ Sous-catégorie nationale
```

### 6.2 Nommage

```text
[Classe d’actifs] + [Sous-classe] + [Nom du pays]
```

Exemples :

```text
Obligations CT Maroc
Obligations MT Maroc
Obligations LT Maroc
Diversifié prudent Maroc
Diversifié équilibré Maroc
Diversifié dynamique Maroc
Diversifié flexible Maroc
```

### 6.3 Relation parent-enfant

```text
Obligations CT Maroc
→ parent_category
→ Obligations Maroc
```

La sous-catégorie doit avoir le même pays et la même classe d’actifs que sa catégorie parente.

---

## 7. Appartenance simultanée d’un fonds

Un fonds possédant une sous-classe appartient simultanément à sa catégorie et à sa sous-catégorie.

```text
Fonds obligataire CT marocain
├── Obligations Maroc
└── Obligations CT Maroc
```

La sous-catégorie ne remplace jamais la catégorie parente.

Toutes les appartenances doivent être historisées avec :

```text
valid_from
valid_to
classification_source
classification_method
validation_status
benchmark_eligibility_status
exclusion_reason
```

---

## 8. Regroupements nationaux

### 8.1 Regroupement de catégorie

```text
Obligations Maroc
=
tous les fonds obligataires marocains éligibles
```

Ce regroupement inclut les fonds CT, MT et LT.

### 8.2 Regroupement de sous-catégorie

```text
Obligations CT Maroc
=
tous les fonds marocains classés Obligations / Court terme
```

Ces regroupements servent à construire les univers de pairs, les classements, les métriques, les WTI et les contrôles de couverture.

---

## 9. Bloc des indices de référence

Chaque catégorie et chaque sous-catégorie possède exactement un bloc de quatre références.

```text
1. Indice marché principal
2. Indice marché secondaire
3. WTI
4. WTI Bench
```

### 9.1 Convention de nommage

Pour toute catégorie ou sous-catégorie `X` :

```text
Indice marché principal [X]
Indice marché secondaire [X]
WTI - [X]
WTI Bench - [X]
```

Exemple :

```text
Actions Maroc
├── Indice marché principal Actions Maroc
├── Indice marché secondaire Actions Maroc
├── WTI - Actions Maroc
└── WTI Bench - Actions Maroc
```

Exemple :

```text
Obligations CT Maroc
├── Indice marché principal Obligations CT Maroc
├── Indice marché secondaire Obligations CT Maroc
├── WTI - Obligations CT Maroc
└── WTI Bench - Obligations CT Maroc
```

Le nom du rôle est distinct du nom réel de la série affectée. Exemple :

```text
Rôle : Indice marché principal Actions Maroc
Série affectée : MASI
```

---

## 10. WTI

Le WTI représente la performance moyenne observée des fonds appartenant à une catégorie ou sous-catégorie.

### 10.1 Univers quotidien

Sont retenus les fonds :

- membres de l’univers à la date du calcul ;
- éligibles ;
- disposant d’une nouvelle VL exploitable ;
- disposant d’une précédente VL comparable ;
- non rejetés pour anomalie.

### 10.2 Rendement individuel

```text
fund_return = adjusted_nav_current / adjusted_nav_previous - 1
```

La précédente VL valide peut être quotidienne, hebdomadaire ou irrégulière. Aucune interpolation artificielle des VL n’est autorisée.

### 10.3 Agrégation initiale

```text
WTI_daily_return
= moyenne équipondérée des rendements des fonds contributeurs
```

### 10.4 Chaînage

```text
WTI_level_t = WTI_level_t-1 × (1 + WTI_daily_return_t)
```

Base initiale recommandée : `100`.

### 10.5 WTI de catégorie

`WTI - Obligations Maroc` est calculé directement avec tous les fonds obligataires marocains éligibles. Il n’est pas nécessairement la moyenne des WTI CT, MT et LT.

### 10.6 WTI de sous-catégorie

`WTI - Obligations CT Maroc` est calculé uniquement avec les fonds de la sous-catégorie CT.

---

## 11. WTI Bench

Le WTI Bench représente le benchmark méthodologique indépendant de la catégorie ou sous-catégorie.

```text
WTI
= performance moyenne réelle des fonds

WTI Bench
= référence théorique de marché ou d’allocation
```

Le WTI Bench doit être :

```text
indépendant
représentatif
réplicable
transparent
stable
versionné
backtesté
reconstructible
explicable
auditable
```

### 11.1 Actions

Priorité méthodologique envisagée :

```text
1. indice officiel large Total Return
2. indice officiel Net Total Return
3. indice officiel Price Return
4. second indice approuvé
5. indice reconstruit par la plateforme en dernier recours
```

Deux indices ne sont jamais moyennés automatiquement sans justification économique.

### 11.2 Obligations

Chaîne de construction :

```text
taux et prix officiels
→ instruments admissibles
→ courbe de taux
→ valorisation
→ rendement de prix
→ coupons et intérêts
→ rendement total
→ pondération
→ indice base 100
```

Hiérarchie de données :

```text
transactions représentatives
→ prix officiels
→ cotations fermes
→ prix de référence
→ rendements observés
→ courbe officielle
→ courbe interpolée ou modélisée
→ dernière donnée valide sous limites strictes
```

Pondération cible : encours admissible ou valeur de marché.

### 11.3 Diversifié

Premières allocations à formaliser :

```text
Prudent : 30 % actions / 70 % obligations
Équilibré : 50 % actions / 50 % obligations
Dynamique : 70 % actions / 30 % obligations
Flexible : méthodologie à définir
```

Les composantes doivent être des benchmarks indépendants et versionnés.

### 11.4 Monétaire

Le WTI Bench monétaire doit représenter un placement monétaire réplicable à partir de taux overnight, interbancaires, repos, bons du Trésor courts ou indice monétaire officiel selon le pays.

---

## 12. Niveau régional

Chaque pays est relié à sa région. Le moteur génère :

```text
Région + Classe d’actifs
→ Catégorie régionale

Région + Classe d’actifs + Sous-classe
→ Sous-catégorie régionale
```

Exemple :

```text
Obligations Afrique du Nord
Obligations CT Afrique du Nord
```

Chaque catégorie et sous-catégorie régionale possède également un bloc de quatre références.

---

## 13. Niveau Afrique

Le moteur génère :

```text
Afrique + Classe d’actifs
→ Catégorie Afrique

Afrique + Classe d’actifs + Sous-classe
→ Sous-catégorie Afrique
```

Exemple :

```text
Obligations Afrique
Obligations CT Afrique
```

Chaque catégorie et sous-catégorie Afrique possède également un bloc de quatre références.

---

## 14. Parcours complet d’un fonds obligataire CT marocain

```text
Fonds
├── Pays : Maroc
├── Région : Afrique du Nord
├── Continent : Afrique
├── Classe : Obligations
└── Sous-classe : CT
```

Rattachements :

```text
National
├── Obligations Maroc
└── Obligations CT Maroc

Régional
├── Obligations Afrique du Nord
└── Obligations CT Afrique du Nord

Afrique
├── Obligations Afrique
└── Obligations CT Afrique
```

Le fonds est donc relié à six objets taxonomiques et six blocs de quatre références, soit jusqu’à 24 rôles de référence, auxquels peut s’ajouter le benchmark déclaré dans le prospectus.

---

## 15. Conversion quotidienne locale / EUR / USD

Toute donnée numérique nationale utile doit exister quotidiennement en :

```text
Devise locale
EUR
USD
```

Cela concerne notamment :

```text
VL
AUM
Dividendes
Prix
Coupons
Flux
Encours
Capitalisations
Indices
WTI
WTI Bench
```

Chaque conversion doit conserver :

```text
source_observation_id
source_currency_id
target_currency_id
fx_observation_id
fx_rate
converted_value
conversion_date
conversion_method
quality_status
```

La conversion n’est pas une simple vue d’affichage. Les séries EUR et USD deviennent des séries analytiques complètes.

---

## 16. Reconstruction régionale et Afrique

Les univers régionaux et Afrique sont recalculés à partir des observations converties.

Exemple `Actions Afrique du Nord — EUR` :

```text
VL EUR des fonds Actions Maroc
+ VL EUR des fonds Actions Tunisie
+ VL EUR des fonds Actions Égypte
→ univers régional EUR
→ recalcul des rendements
→ recalcul des métriques
→ recalcul des classements
→ calcul du WTI régional EUR
```

Même logique en USD.

Les niveaux régional et Afrique ne sont donc pas de simples moyennes des indices nationaux locaux.

---

## 17. Informations récupérables à partir d’un fonds

À partir de `fund_id`, le système doit pouvoir retourner :

```text
Identité canonique
Pays
Région
Continent
Devise locale
Classe d’actifs
Sous-classe d’actifs
Catégorie nationale
Sous-catégorie nationale
Catégorie régionale
Sous-catégorie régionale
Catégorie Afrique
Sous-catégorie Afrique
Blocs de références applicables
Indices marché applicables
WTI applicables
WTI Bench applicables
Groupes de pairs
Historique des appartenances
VL locale / EUR / USD
AUM local / EUR / USD
Métriques nationales / régionales / Afrique
Classements nationaux / régionaux / Afrique
Sources et provenance
Statuts qualité
```

---

## 18. Relations essentielles

```text
Country 1 ─── N NationalCategory
Region 1 ─── N RegionalCategory
Continent 1 ─── N AfricaCategory

AssetClass 1 ─── N Category
AssetClass 1 ─── N SubAssetClass

NationalCategory 1 ─── N NationalSubcategory
RegionalCategory 1 ─── N RegionalSubcategory
AfricaCategory 1 ─── N AfricaSubcategory

Category 1 ─── 1 ReferenceBlock
Subcategory 1 ─── 1 ReferenceBlock
ReferenceBlock 1 ─── 4 ReferenceRole

Fund N ─── N CategoryMembership
Fund N ─── N SubcategoryMembership

NativeObservation 1 ─── N ConvertedObservation
FXObservation 1 ─── N ConvertedObservation
```

---

## 19. Principe de stockage

Les noms lisibles sont dérivés. Les relations sont persistées.

À stocker explicitement :

```text
fund_id
country_id
region_id
continent_id
asset_class_id
sub_asset_class_id
national_category_id
national_subcategory_id
regional_category_id
regional_subcategory_id
africa_category_id
africa_subcategory_id
reference_block_id
valid_from
valid_to
```

Le modèle doit permettre une lecture complète à partir du fonds, du fonds et de son pays, ou du fonds et de sa catégorie.