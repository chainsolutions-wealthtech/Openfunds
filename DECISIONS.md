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

## ADR-021 — UNE SOURCE D'AUTHORING POUR LES REFERENTIELS

- **Statut :** ACCEPTE
- **Date de validation :** 2026-08-05
- **Problème résolu :** les inventaires CSV et les seeds SQL présentaient des statuts divergents pour BCEAO et BEAC.
- **Décision :**

```text
VALIDATED_FX_REFERENCE_REGISTRY.csv
= SOURCE D'AUTHORING GOUVERNEE DES PILOTES FX VALIDES

SQL GENERE DETERMINISTE
= REPRESENTATION DE SYNCHRONISATION ADDITIVE

POSTGRESQL
= SOURCE DE VERITE RUNTIME APRES APPLICATION
```

- **Règle :** les grands CSV existants restent des inventaires de découverte et de revue. Ils ne concurrencent pas le registre compact des pilotes validés. Les seeds SQL historiques restent rejouables mais ne sont plus une source d'authoring concurrente.
- **Générateur :** `scripts/generate_validated_fx_reference_sql.py`.
- **Sortie générée :** `schemas/reference/012_validated_fx_reference_registry.sql` lors des contrôles et applications.
- **Contrôles :** validation UTF-8/CSV, en-tête exact, complétude, preuves de run, SHA256, dates, génération déterministe et double application PostgreSQL.
- **Portée initiale :** pilotes FX BCEAO/XOF et BEAC/XAF classés `COLLECTION_TESTED`.
- **Limite :** cette décision ne choisit pas le migration runner global de `ADR-023` et ne transforme pas les snapshots en historiques.
- **Options rejetées :**
  1. PostgreSQL comme seule surface d'authoring, car les référentiels doivent rester revus dans Git ;
  2. la réécriture des grands inventaires comme registre de validation, car elle mélangerait découverte et preuve de collecte ;
  3. un manifeste YAML/JSON supplémentaire, qui créerait une autre représentation.

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

---

## RECONCILIATION DES DECISIONS — 2026-08-05

Cette note ne supprime pas les propositions historiques ADR-022 et ADR-023 ; elle enregistre leur supersession par les décisions détaillées acceptées.

- `ADR-026_CANONICAL_ENDPOINT_MODEL.md` : `source.endpoint` est le modèle physique runtime canonique ; la proposition `source.source_endpoint` reste non opérationnelle.
- `ADR-027_EXPLICIT_BUSINESS_DATE_KNOWLEDGE.md` : les dates métier inconnues utilisent un statut explicite et `NULL`, sans date inventée. La proposition ADR-022 est donc `REMPLACEE` pour ce périmètre.
- `ADR-028_GOVERNED_MIGRATION_RUNNER.md` : manifeste de 14 migrations, ledger, SHA-256, modes plan/apply/verify et échec fermé. La proposition ADR-023 est `REMPLACEE` pour l'outil et l'ordre opérationnel.

Statuts vérifiés :

```text
OF-ARCH-001   VERIFIED_COMPLETE
OF-SOURCE-001 VERIFIED_COMPLETE
OF-ARCH-002   VERIFIED_COMPLETE
OF-ARCH-003   VERIFIED_COMPLETE
OF-ARCH-004   IMPLEMENTED_WITH_OPEN_GOVERNANCE_BLOCKER
```

Le statut de `OF-ARCH-004` reste inférieur à `VERIFIED_COMPLETE` : la migration générée `012` peut être rematérialisée avant hashing et n'est pas figée comme artefact historique. Cette décision ne corrige pas ce blocker et n'autorise pas `OF-DATA-001`.

## DECISION DOCUMENTAIRE — OF-DOC-003

- **Statut :** ACCEPTE POUR LA MISSION DOCUMENTAIRE
- **Date :** 2026-08-05
- **Décision :** intégrer le standard Loop Engineering sans remplacer les documents historiques canoniques ; utiliser des index/adaptateurs pour les chemins redondants.
- **Boucle :** `OF-LOOP-DOC-003`.
- **Autorité :** `00_START_HERE.md`, `AGENTS.md`, `SOURCE_OF_TRUTH.md`, `STATUS.md` et `DOCUMENT_INTEGRATION_MATRIX.md` organisent la navigation ; ils ne remplacent pas les ADR, TODO, SUIVI ou rapports datés.
- **Limites :** documentation seulement, aucune modification de migration 012, aucun démarrage de `OF-DATA-001`, aucune opération de branche, PR, fusion ou déploiement.