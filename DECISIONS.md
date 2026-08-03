# DECISIONS DU PROJET OPENFUNDS

## 1. OBJET

Ce registre consolide les décisions structurantes du projet. Il ne remplace pas les documents détaillés ; il leur attribue des identifiants stables et indique leur statut.

Statuts :

- `ACCEPTE` : décision applicable ;
- `PROPOSE` : proposition à valider ;
- `A_REEXAMINER` : décision ou implémentation présentant un écart ;
- `REMPLACE` : décision remplacée par une autre ;
- `ABANDONNE` : option rejetée.

Toute modification d'une décision `ACCEPTE` doit documenter l'impact, la migration, les alternatives et la validation obtenue.

---

## ADR-001 — MODELE CANONIQUE INTERNE

- **Statut :** ACCEPTE
- **Date :** 2026-07-31
- **Contexte :** Openfunds est utile comme standard d'échange, mais ne couvre pas seul toutes les identités, relations, histoires, sources, événements, documents et calculs nécessaires.
- **Décision :** construire un modèle canonique interne plus riche qu'Openfunds.
- **Justification :** préserver une source de vérité stable, indépendante des versions et limites des standards externes.
- **Conséquences positives :** extension libre, provenance complète, historisation, compatibilité multi-standards.
- **Conséquences négatives :** nécessité d'un dictionnaire et de mappings explicites.
- **Alternative rejetée :** utiliser directement les champs Openfunds comme colonnes physiques uniques.
- **Eléments concernés :** tous les domaines.

## ADR-002 — OPENFUNDS COMME COUCHE DE MAPPING

- **Statut :** ACCEPTE
- **Date :** 2026-07-31
- **Décision :** Openfunds est une couche d'import, d'export et de correspondance ; il n'est pas le schéma canonique.
- **Conséquence :** chaque champ Openfunds devra être relié à un ou plusieurs objets et champs canoniques, avec règle de transformation et version du standard.
- **Limite actuelle :** le mapping opérationnel n'est pas encore présent dans le dépôt.

## ADR-003 — POSTGRESQL COMME SOURCE DE VERITE

- **Statut :** ACCEPTE
- **Date :** 2026-07-31
- **Décision :** PostgreSQL conserve les entités, identifiants, relations, historiques, sources, mappings et décisions qualité faisant autorité.
- **Conséquence :** caches, index de recherche, graphes, projections analytiques et view models sont reconstruits à partir de PostgreSQL et des artefacts bruts.
- **Alternative rejetée :** faire d'un moteur de recherche, d'un fichier CSV ou d'un cache la source canonique.

## ADR-004 — ARCHITECTURE API-FIRST ET ATOMIC DESIGN

- **Statut :** ACCEPTE
- **Date :** 2026-07-31
- **Décision :** les objets canoniques sont exposés par des contrats API stables ; Atomic Design structure la présentation, pas la base de données.
- **Conséquence :** aucune molécule ou composant UI ne lit directement les tables physiques.
- **Limite actuelle :** API, OpenAPI et composants UI non implémentés.

## ADR-005 — SEPARATION DES COUCHES

- **Statut :** ACCEPTE
- **Décision :** séparer :

```text
RAW_SOURCE
→ NORMALIZED_SOURCE
→ VALIDATION
→ CANONICAL_MODEL
→ ANALYTICAL_MODEL
→ API_RESOURCE
→ UI_VIEW_MODEL
```

- **Justification :** empêcher les formats fournisseurs, les besoins UI ou les calculs dérivés de contaminer le modèle canonique.

## ADR-006 — CONSERVATION DES ARTEFACTS BRUTS

- **Statut :** ACCEPTE
- **Décision :** les PDF, Excel, CSV, HTML, images, XML et JSON originaux sont conservés sans modification, avec SHA256 et métadonnées de récupération.
- **Conséquence :** toute donnée publiée doit être reproductible depuis la source.
- **Limite actuelle :** les artefacts FX sont temporaires dans GitHub Actions ; le stockage permanent reste à configurer.

## ADR-007 — HISTORISATION BITEMPORELLE

- **Statut :** ACCEPTE
- **Décision :** distinguer la validité métier de la connaissance système.
- **Champs de référence :** `valid_from`, `valid_to`, `recorded_at`, `superseded_at`.
- **Conséquence :** une correction ne supprime pas silencieusement la version antérieure.
- **Point à réexaminer :** certaines migrations imposent une date métier même lorsqu'elle n'est pas connue.

## ADR-008 — IDENTITE DISTINCTE DE LA DENOMINATION

- **Statut :** ACCEPTE
- **Décision :** l'identifiant canonique d'un fonds ou d'une organisation ne change pas avec son nom ; les noms, alias et anciennes dénominations sont historisés séparément.
- **Conséquence :** un changement de nom ne crée pas automatiquement un nouvel objet économique.
- **Limite actuelle :** tables d'alias fonds non encore implémentées dans la branche.

## ADR-009 — SEPARATION FUND / SUBFUND / SHARECLASS

- **Statut :** ACCEPTE SUR LE PRINCIPE, A_REEXAMINER SUR L'IMPLEMENTATION
- **Décision :** distinguer la structure fonds, le compartiment et la classe de parts.
- **Problème :** le SQL actuel contient `fund.fund` et `fund.share_class` sans modèle `sub_fund` complet.
- **Action :** arbitrer les niveaux juridiques avant toute migration de données fonds.

## ADR-010 — PAYS COMME RACINE NATIONALE

- **Statut :** ACCEPTE
- **Décision :** le pays est la racine de classification nationale ; la région et l'Afrique sont des niveaux d'agrégation.
- **Conséquence :** les catégories nationales sont définies par `COUNTRY + ASSET_CLASS` et les sous-catégories par `COUNTRY + ASSET_CLASS + SUB_ASSET_CLASS`.

## ADR-011 — GEOGRAPHIE ET ZONES DE MARCHE EN PARALLELE

- **Statut :** ACCEPTE
- **Décision :** UEMOA, CEMAC et CMA ne remplacent pas les régions géographiques.
- **Exemple :** un pays UEMOA appartient à une région, au continent, à la zone UEMOA, utilise XOF, BCEAO et BRVM selon le rôle concerné.
- **Conséquence :** les relations sont modélisées explicitement et historisées.

## ADR-012 — CODES TECHNIQUES NORMALISES

- **Statut :** ACCEPTE
- **Décision :** les codes techniques canoniques utilisent :

```text
MAJUSCULES
SANS ACCENT
SANS APOSTROPHE
UNDERSCORE COMME SEPARATEUR
```

- **Conséquence :** les libellés humains accentués restent dans des champs d'affichage séparés.

## ADR-013 — QUATRE ROLES DE REFERENCE

- **Statut :** ACCEPTE
- **Décision :** chaque catégorie ou sous-catégorie possède exactement quatre rôles distincts :

```text
PRIMARY_MARKET_INDEX
SECONDARY_MARKET_INDEX
WTI
WTI_BENCH
```

- **Conséquence :** le nom du rôle est distinct de la série affectée.
- **Interdiction :** ne pas remplacer `WTI - [CATEGORY]` par un code méthodologique de fournisseur.

## ADR-014 — DEFINITION DU WTI

- **Statut :** ACCEPTE
- **Décision :** le WTI représente la performance moyenne observée des fonds éligibles d'une catégorie ou sous-catégorie.
- **Règles :** rendement sur VL ajustées, absence d'interpolation artificielle, univers daté, exclusions tracées, chaînage base 100.
- **Limite actuelle :** aucun moteur WTI n'est encore implémenté.

## ADR-015 — INDEPENDANCE DU WTI BENCH

- **Statut :** ACCEPTE
- **Décision :** le WTI Bench est indépendant de la performance moyenne des fonds ; il représente un benchmark de marché ou d'allocation reproductible.
- **Conséquence :** WTI et WTI Bench ne doivent jamais être confondus.
- **Eléments à valider :** méthodologie monétaire complète et allocation des fonds flexibles.

## ADR-016 — SERIES LOCALE, EUR ET USD

- **Statut :** ACCEPTE
- **Décision :** toute observation monétaire convertible conserve sa valeur native et peut produire des observations EUR et USD explicites avec lignée FX.
- **Conséquence :** les conversions ne remplacent pas la donnée native et ne sont pas seulement du formatage d'affichage.

## ADR-017 — RECONSTRUCTION REGIONALE ET AFRIQUE

- **Statut :** ACCEPTE
- **Décision :** les performances, métriques, classements et WTI régionaux/Afrique sont recalculés depuis les séries fonds converties, et non obtenus par moyenne des classements ou indices nationaux.

## ADR-018 — DONNEE OBSERVEE DISTINCTE DE LA DONNEE CALCULEE

- **Statut :** ACCEPTE
- **Décision :** buy, sell, NAV, AUM, taux et prix publiés restent des observations ; midpoint, inversion FX, rendement, indice et ratio sont des calculs liés aux observations sources.
- **Conséquence :** chaque calcul porte une formule et une version méthodologique.

## ADR-019 — NULL N'EST PAS ZERO

- **Statut :** ACCEPTE
- **Décision :** une valeur absente, inconnue ou non publiée ne devient jamais zéro et ne fait pas l'objet d'un report automatique sans règle approuvée.
- **Conséquence :** les statuts `MISSING`, `NOT_PUBLISHED`, `NOT_APPLICABLE` et `UNKNOWN` doivent rester distincts.

## ADR-020 — VALIDATION PROGRESSIVE

- **Statut :** ACCEPTE
- **Décision :** distinguer les niveaux :

```text
REFERENTIEL_PEUPLE
CATALOGUE_PEUPLE
MAPPING_SOURCE_PEUPLE
COLLECTION_TESTED
PARTIAL_HISTORY_LOADED
COMPLETE_HISTORY_LOADED
CALCULATED_PRODUCTS_AVAILABLE
```

- **Conséquence :** une structure SQL ou un fichier CSV ne prouve pas qu'un historique réel est chargé.

## ADR-021 — UNE SOURCE DE VERITE POUR LES REFERENTIELS

- **Statut :** PROPOSE
- **Problème :** les CSV et seeds SQL présentent actuellement des statuts divergents pour BCEAO et BEAC.
- **Proposition :** désigner un registre canonique machine-readable et générer les autres représentations.
- **Options :**
  1. CSV gouverné → migrations générées ;
  2. PostgreSQL canonique → exports CSV ;
  3. manifeste YAML/JSON → CSV et SQL générés.
- **Validation nécessaire :** choix de la stratégie.

## ADR-022 — DATE METIER INCONNUE

- **Statut :** PROPOSE
- **Problème :** ne pas inventer une date, alors que certaines contraintes imposent `valid_from NOT NULL`.
- **Proposition :** séparer :

```text
EFFECTIVE_DATE
EFFECTIVE_DATE_STATUS
COLLECTED_AT
RECORDED_AT
```

- **Validation nécessaire :** autoriser l'absence de date métier tant qu'une preuve officielle n'existe pas.

## ADR-023 — STRATEGIE DE MIGRATION

- **Statut :** PROPOSE
- **Problème :** l'ordre des fichiers SQL est actuellement appliqué manuellement dans les workflows.
- **Proposition :** adopter un registre de migrations ordonné, vérifiable, idempotent et compatible avec les environnements existants.
- **Validation nécessaire :** outil et politique de déploiement.

## ADR-024 — CATALOGUE CANONIQUE DES CHAMPS

- **Statut :** PROPOSE
- **Décision proposée :** créer un catalogue machine-readable unique pour les champs et indicateurs, avec exports humains.
- **Motif :** éviter la divergence entre Markdown, CSV et SQL.
- **Validation nécessaire :** format maître et cycle de version.

## ADR-025 — STOCKAGE PERSISTANT DES COLLECTES

- **Statut :** PROPOSE
- **Décision proposée :** ne passer à `PARTIAL_HISTORY_LOADED` qu'après stockage durable d'au moins deux dates, des artefacts bruts et des observations PostgreSQL.
- **Précondition :** base persistante, stockage objet, secrets et politique de rétention.

## REGLE DE MISE A JOUR

Après toute décision structurante :

1. mettre à jour ce fichier ;
2. relier la tâche correspondante dans `TODO.md` ;
3. consigner l'intervention dans `SUIVI.md` ;
4. ajouter l'impact à `CHANGELOG.md` ;
5. mettre à jour les schémas, dictionnaires et mappings concernés.
