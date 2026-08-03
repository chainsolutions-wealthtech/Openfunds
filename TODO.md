# TODO — REGISTRE DES TACHES OPENFUNDS

## 1. REGLES

Chaque tâche possède un identifiant stable. Une tâche terminée n'est jamais supprimée : elle reste dans la section des réalisations achevées.

Statuts :

- `A_ANALYSER`
- `PROPOSE`
- `DECIDE`
- `EN_COURS`
- `PARTIELLEMENT_IMPLEMENTE`
- `IMPLEMENTE`
- `TESTE`
- `DOCUMENTE`
- `BLOQUE`
- `A_CORRIGER`
- `TERMINE`

Priorités :

- `P0_CRITIQUE`
- `P1_HAUTE`
- `P2_MOYENNE`
- `P3_BASSE`

Dernière mise à jour : `2026-08-03`.

---

# A. TACHES EN COURS OU PRIORITAIRES

## OF-DOC-001 — Consolider la documentation racine

- **Statut :** EN_COURS
- **Priorité :** P0_CRITIQUE
- **Domaine :** Documentation
- **Ajoutée :** 2026-08-03
- **Dernière mise à jour :** 2026-08-03
- **Description :** transformer le dépôt en projet reprenable sans relire la conversation.
- **Dépendances :** audit complet du dépôt.
- **Critères d'acceptation :**
  - `README.md` explique le projet, l'architecture, l'état réel et les commandes vérifiées ;
  - `TODO.md` contient les tâches terminées, en cours et restantes ;
  - `SUIVI.md` contient les réalisations, décisions, écarts, risques et point exact de reprise ;
  - les documents complémentaires sont cohérents ;
  - aucun module non implémenté n'est présenté comme terminé ;
  - les liens relatifs sont valides.
- **Livrables :** `README.md`, `TODO.md`, `SUIVI.md`, documents de gouvernance.
- **Fichiers concernés :** racine du dépôt, `docs/00_PROJECT/`.
- **Risques :** divergence future si les fichiers ne sont pas entretenus.

## OF-ARCH-001 — Choisir la source de vérité des référentiels

- **Statut :** A_ARBITRER
- **Priorité :** P0_CRITIQUE
- **Domaine :** Architecture / Gouvernance
- **Description :** éliminer la double saisie entre CSV gouvernés et seeds SQL.
- **Dépendances :** `ADR-021`.
- **Options :**
  1. CSV maître générant les migrations ;
  2. PostgreSQL maître générant les CSV ;
  3. manifeste YAML/JSON générant les deux.
- **Critères d'acceptation :**
  - une seule représentation est déclarée canonique ;
  - les autres sont générées ou contrôlées automatiquement ;
  - les statuts BCEAO/BEAC concordent partout ;
  - un test bloque toute divergence.
- **Livrables :** décision ADR, générateur/synchroniseur, test de cohérence.
- **Fichiers concernés :** `data/reference/`, `schemas/reference/`.
- **Risques :** incohérences de production, corrections contradictoires.

## OF-ARCH-002 — Unifier le modèle des endpoints

- **Statut :** A_CORRIGER
- **Priorité :** P0_CRITIQUE
- **Domaine :** Architecture / Sources
- **Description :** supprimer le parallélisme conceptuel entre `source.endpoint` et `source.source_endpoint` sans perte de données.
- **Dépendances :** OF-ARCH-001, audit `AUD-003`.
- **Critères d'acceptation :**
  - un modèle canonique unique d'endpoint est retenu ;
  - le modèle pays référence ce modèle ;
  - aucune table concurrente n'est créée ;
  - les migrations fonctionnent depuis les états 003 et 004 ;
  - les tests d'ordre restent verts.
- **Livrables :** migration additive, modèle mis à jour, tests SQL.
- **Fichiers concernés :** `schemas/reference/country_indicator_information_model_v0.1.sql`, `003`, `004`, `007`.
- **Risques :** perte de FK ou duplication de sources.

## OF-ARCH-003 — Définir le traitement des dates métier inconnues

- **Statut :** A_ARBITRER
- **Priorité :** P0_CRITIQUE
- **Domaine :** Modèle temporel
- **Description :** résoudre l'écart entre l'interdiction d'inventer une date et les colonnes `valid_from NOT NULL`.
- **Dépendances :** `ADR-022`.
- **Critères d'acceptation :**
  - date métier, date de collecte et date d'enregistrement sont distinctes ;
  - un statut indique `KNOWN`, `APPROXIMATE`, `UNKNOWN` ou `NOT_APPLICABLE` ;
  - aucun `1900-01-01` ou équivalent artificiel ;
  - le CSV et le SQL portent la même sémantique ;
  - les vues courantes restent déterministes.
- **Livrables :** décision, migration, règles qualité, tests.
- **Risques :** fausse histoire juridique ou relations impossibles à charger.

## OF-ARCH-004 — Adopter une stratégie de migrations

- **Statut :** PROPOSE
- **Priorité :** P0_CRITIQUE
- **Domaine :** Migrations / Déploiement
- **Description :** remplacer l'ordre manuel des fichiers SQL par une stratégie de migration gouvernée.
- **Dépendances :** `ADR-023`, OF-ARCH-001 et OF-ARCH-002.
- **Critères d'acceptation :**
  - ordre de migration unique et versionné ;
  - registre des migrations appliquées ;
  - migrations idempotentes ou explicitement non rejouables ;
  - rollback ou procédure de réparation documentée ;
  - tests depuis une base vide et une base partiellement initialisée ;
  - aucune donnée existante détruite.
- **Livrables :** outil/configuration de migration, documentation, CI.
- **Risques :** schémas divergents entre environnements.

## OF-DATA-001 — Stabiliser Fund / SubFund / ShareClass

- **Statut :** A_ARBITRER
- **Priorité :** P0_CRITIQUE
- **Domaine :** Modèle de données Fonds
- **Description :** définir les niveaux juridiques et investissables sans fusionner fonds, compartiment et classe de parts.
- **Dépendances :** `ADR-009`, analyse des structures Maroc/Tunisie/Nigeria.
- **Critères d'acceptation :**
  - entités et cardinalités approuvées ;
  - exemples SICAV, FCP, umbrella et fonds sans compartiment couverts ;
  - identifiants stables ;
  - noms et alias séparés ;
  - événements de fusion/transfert modélisables ;
  - migration compatible avec les données existantes.
- **Livrables :** ADR, diagramme, SQL, tests.
- **Fichiers concernés :** `schemas/taxonomy/fund_relationship_information_model_v0.1.sql`, `DATA_MODEL.md`.
- **Risques :** mauvaise résolution d'entité et doublons fonds.

## OF-DATA-002 — Construire le dictionnaire canonique machine-readable

- **Statut :** EN_COURS
- **Priorité :** P0_CRITIQUE
- **Domaine :** Dictionnaire de données
- **Description :** centraliser les champs dispersés dans les SQL, CSV et Markdown.
- **Dépendances :** OF-DATA-001, `ADR-024`.
- **Critères d'acceptation :** chaque champ possède :
  - identifiant canonique ;
  - nom technique et fonctionnel ;
  - définition ;
  - domaine et entité ;
  - type, format, unité et devise ;
  - cardinalité et nullabilité ;
  - contraintes et valeurs autorisées ;
  - validation, normalisation et calcul ;
  - source et priorité ;
  - historisation ;
  - niveau de sensibilité et confiance ;
  - mapping externe ;
  - version et statut.
- **Livrables :** `DATA_DICTIONARY.md`, CSV/JSON/YAML ou tables canoniques.
- **Risques :** mappings incohérents et schémas non gouvernés.

## OF-DATA-003 — Centraliser les 420 définitions D00-D17

- **Statut :** EN_COURS
- **Priorité :** P0_CRITIQUE
- **Domaine :** Catalogue des indicateurs
- **Description :** convertir les définitions Markdown en catalogue machine-readable unique.
- **Dépendances :** OF-DATA-002.
- **Critères d'acceptation :**
  - compte de définitions vérifié ;
  - code unique en majuscules sans accent ;
  - domaine D00-D17 ;
  - nature RAW/METADATA/EVENT/CALCULATED ;
  - unité, fréquence et traitement devise ;
  - source privilégiée ;
  - usages et dépendances ;
  - statut de validation ;
  - génération des vues Markdown.
- **Livrables :** catalogue structuré, import SQL, tests d'unicité.
- **Risques :** divergence entre documentation et base.

## OF-MAP-001 — Intégrer le catalogue officiel Openfunds

- **Statut :** BLOQUE
- **Priorité :** P0_CRITIQUE
- **Domaine :** Mapping Openfunds
- **Description :** versionner les champs officiels openfunds avec leur provenance et leur version.
- **Dépendances :** accès à une version officielle exploitable, règles de licence, OF-DATA-002.
- **Critères d'acceptation :**
  - version du standard identifiée ;
  - source et date de récupération conservées ;
  - identifiant, nom, description, type, cardinalité et obligation chargés ;
  - aucun contenu officiel inventé ;
  - différences de versions traçables.
- **Livrables :** registre officiel source + catalogue structuré.
- **Blocage :** le standard officiel n'est pas encore présent dans le dépôt.

## OF-MAP-002 — Construire le mapping Openfunds vers le canonique

- **Statut :** BLOQUE
- **Priorité :** P0_CRITIQUE
- **Domaine :** Mapping
- **Dépendances :** OF-MAP-001, OF-DATA-001, OF-DATA-002.
- **Critères d'acceptation :**
  - chaque champ openfunds possède un statut de mapping ;
  - objet canonique cible identifié ;
  - transformations et normalisations documentées ;
  - pertes d'information signalées ;
  - champs canoniques sans équivalent listés ;
  - mapping humain et machine-readable ;
  - tests aller/retour sur fixtures.
- **Livrables :** `OPENFUNDS_MAPPING.md`, fichier structuré, tests.

## OF-SOURCE-001 — Synchroniser les objets BCEAO/BEAC entre CSV et SQL

- **Statut :** A_CORRIGER
- **Priorité :** P0_CRITIQUE
- **Domaine :** Sources / Référentiels
- **Description :** répercuter les validations live dans les registres canoniques sans créer de doublons génériques/spécifiques.
- **Dépendances :** OF-ARCH-001.
- **Critères d'acceptation :**
  - organisations, rôles, endpoints, mappings, séries et spécifications concordent ;
  - codes génériques obsolètes remplacés ou marqués ;
  - les preuves de run sont reliées ;
  - test automatique de cohérence.
- **Livrables :** référentiels corrigés, migration, test.

## OF-SOURCE-002 — Compléter les institutions des 54 pays

- **Statut :** EN_COURS
- **Priorité :** P1_HAUTE
- **Domaine :** Sources
- **Description :** identifier banques centrales, statistiques, finances, dette, bourses, régulateurs fonds et régulateurs assurance/pension.
- **Dépendances :** OF-ARCH-001.
- **Critères d'acceptation :**
  - chaque pays possède un statut par rôle ;
  - organisation et rôle sont séparés ;
  - URLs officielles vérifiées ;
  - dates d'effet et preuves lorsque disponibles ;
  - absence documentée lorsque non applicable.
- **Livrables :** `ORGANIZATIONS.csv`, `ORGANIZATION_SCOPE_ROLES.csv`, `SOURCE_ENDPOINTS.csv`.

## OF-SOURCE-003 — Vérifier les 55 mappings initiaux

- **Statut :** EN_COURS
- **Priorité :** P1_HAUTE
- **Domaine :** Sources / Indicateurs
- **Critères d'acceptation :**
  - endpoint exact ;
  - série exacte ;
  - fréquence et unité réelles ;
  - historique disponible ;
  - priorité de source ;
  - méthode de collecte ;
  - statut de validation ;
  - rupture méthodologique documentée.
- **Livrables :** mappings et séries fournisseurs corrigés.

## OF-IMPORT-001 — Configurer PostgreSQL persistant pour le pipeline FX

- **Statut :** BLOQUE
- **Priorité :** P1_HAUTE
- **Domaine :** Import / Déploiement
- **Dépendances :** OF-ARCH-004, environnement PostgreSQL durable, secret `OPENFUNDS_DATABASE_URL`.
- **Critères d'acceptation :**
  - migrations déployées de manière gouvernée ;
  - secret configuré hors dépôt ;
  - run quotidien charge BCEAO et BEAC ;
  - seconde exécution idempotente ;
  - métriques de run disponibles ;
  - sauvegarde et restauration testées.
- **Livrables :** configuration d'environnement, procédure et preuve de run.

## OF-IMPORT-002 — Configurer le stockage brut immuable

- **Statut :** BLOQUE
- **Priorité :** P1_HAUTE
- **Domaine :** Provenance / Stockage
- **Dépendances :** environnement de stockage, politique d'accès.
- **Critères d'acceptation :**
  - URI durable par SHA256 ;
  - écriture append-only ou versionnée ;
  - vérification d'intégrité ;
  - rétention documentée ;
  - restauration testée ;
  - URI écrite dans `source.raw_artifact`.
- **Livrables :** stockage, politique, tests.

## OF-HIST-001 — Construire la couverture historique FX

- **Statut :** PROPOSE
- **Priorité :** P1_HAUTE
- **Domaine :** Historique
- **Dépendances :** OF-IMPORT-001, OF-IMPORT-002.
- **Critères d'acceptation :**
  - nombre de dates distinctes ;
  - première et dernière date ;
  - calendrier de publication ;
  - gaps classés ;
  - jours sans publication distingués des erreurs ;
  - révisions conservées ;
  - statut `PARTIAL_HISTORY_LOADED` uniquement après preuve durable.
- **Livrables :** vues de couverture, rapport, règles qualité.

## OF-HIST-002 — Inventorier et backfiller les archives BCEAO/BEAC FX

- **Statut :** A_ANALYSER
- **Priorité :** P1_HAUTE
- **Domaine :** Historique / FX
- **Dépendances :** OF-HIST-001.
- **Critères d'acceptation :**
  - archives officielles inventoriées ;
  - début vérifié ;
  - fichiers et ruptures recensés ;
  - backfill reproductible ;
  - couverture calculée ;
  - historique complet déclaré uniquement après contrôle.
- **Livrables :** inventaire, collecteur historique, preuve de couverture.

## OF-IMPORT-003 — Intégrer la base OPCVM Tunisie

- **Statut :** A_ANALYSER
- **Priorité :** P1_HAUTE
- **Domaine :** Import OPCVM
- **Dépendances :** OF-DATA-001, modèle provenance commun, accès au fichier source.
- **Critères d'acceptation :**
  - fichier original conservé et hashé ;
  - schéma SQLite inventorié ;
  - fonds, alias, gestionnaires, NAV, dividendes, documents et événements mappés ;
  - conflits conservés ;
  - TND non inventé lorsqu'il n'est pas attesté par la source ;
  - aucune valeur manquante transformée en zéro ;
  - import idempotent.
- **Livrables :** spécification, chargeur, contrôles et rapport.

## OF-IMPORT-004 — Intégrer les archives OPCVM Nigeria

- **Statut :** A_ANALYSER
- **Priorité :** P1_HAUTE
- **Domaine :** Import OPCVM
- **Dépendances :** OF-DATA-001, accès aux archives SEC.
- **Critères d'acceptation :**
  - fichiers XLS/XLSX inventoriés depuis 2011 ;
  - feuilles et dates réelles contrôlées ;
  - NAV, Unit Price, Bid et Offer séparés ;
  - NGN et USD distingués ;
  - fonds/gestionnaires harmonisés sans fusion aveugle ;
  - provenance jusqu'à la cellule ;
  - trajectoires, alias et événements reconstitués ;
  - doublons, corruptions et conflits conservés.
- **Livrables :** référentiel Nigeria, import, rapports et tests.

## OF-TAX-001 — Peupler les classes et sous-classes d'actifs

- **Statut :** DECIDE / NON_IMPLEMENTE
- **Priorité :** P1_HAUTE
- **Domaine :** Taxonomie
- **Dépendances :** OF-ARCH-004.
- **Critères d'acceptation :**
  - `ACTIONS`, `OBLIGATIONS`, `DIVERSIFIE`, `MONETAIRE` ;
  - sous-classes CT/MT/LT, PRUDENT/EQUILIBRE/DYNAMIQUE/FLEXIBLE ;
  - règles d'éligibilité ;
  - seeds idempotents ;
  - tests d'unicité et hiérarchie.
- **Livrables :** référentiels et migration.

## OF-TAX-002 — Générer catégories et sous-catégories

- **Statut :** PROPOSE
- **Priorité :** P2_MOYENNE
- **Domaine :** Taxonomie
- **Dépendances :** OF-TAX-001, géographie validée.
- **Critères d'acceptation :**
  - génération nationale, régionale et Afrique ;
  - relation parent-enfant correcte ;
  - codes déterministes ;
  - aucune duplication ;
  - historisation ;
  - tests de recomposition.
- **Livrables :** générateur, migration/seeds et tests.

## OF-BENCH-001 — Générer les blocs de quatre références

- **Statut :** PROPOSE
- **Priorité :** P2_MOYENNE
- **Domaine :** Benchmarks
- **Dépendances :** OF-TAX-002.
- **Critères d'acceptation :** un bloc unique par catégorie avec les quatre rôles, noms canoniques et affectations historisées.
- **Livrables :** générateur, tables, tests.

## OF-BENCH-002 — Finaliser les méthodologies WTI Bench

- **Statut :** EN_COURS
- **Priorité :** P2_MOYENNE
- **Domaine :** Benchmarks
- **Dépendances :** sources de marché validées.
- **Critères d'acceptation :**
  - actions : hiérarchie TR/NTR/PR ;
  - obligations : univers, courbe, coupons, total return et pondération ;
  - diversifié : allocations et rebalancement ;
  - monétaire : taux et instruments admissibles ;
  - flexible : méthode validée ;
  - version, backtest et gouvernance.
- **Livrables :** méthodologies versionnées.

## OF-CALC-001 — Implémenter le moteur WTI

- **Statut :** BLOQUE
- **Priorité :** P2_MOYENNE
- **Domaine :** Calcul
- **Dépendances :** historiques NAV fiables, OF-TAX-002, OF-BENCH-001.
- **Critères d'acceptation :** univers daté, VL ajustées, absence d'interpolation, contributions, exclusions, couverture, chaînage et reproductibilité.
- **Livrables :** moteur, tables de contribution, tests et documentation.

## OF-CALC-002 — Implémenter métriques et classements

- **Statut :** BLOQUE
- **Priorité :** P2_MOYENNE
- **Domaine :** Calcul analytique
- **Dépendances :** séries fonds historiques et benchmarks.
- **Critères d'acceptation :** performances, volatilité, drawdown, Sharpe, Sortino, alpha, beta, R², VaR, percentiles, quartiles et rangs versionnés.
- **Livrables :** moteur, dictionnaire de calcul, tests.

## OF-API-001 — Définir les contrats API

- **Statut :** BLOQUE
- **Priorité :** P3_BASSE
- **Domaine :** API
- **Dépendances :** OF-DATA-001 et OF-DATA-002.
- **Critères d'acceptation :** OpenAPI versionné, ressources, enveloppe, erreurs, pagination, temporalité, provenance, qualité et sécurité.
- **Livrables :** OpenAPI, fixtures contractuelles, tests.

## OF-UI-001 — Définir les view models Atomic Design

- **Statut :** BLOQUE
- **Priorité :** P3_BASSE
- **Domaine :** UI
- **Dépendances :** OF-API-001.
- **Critères d'acceptation :** contrats atoms/molecules/organisms/templates, états loading/empty/error/stale/restricted, localisation et accessibilité.
- **Livrables :** view models et documentation composants.

## OF-QA-001 — Rendre les règles qualité exécutables

- **Statut :** EN_COURS
- **Priorité :** P1_HAUTE
- **Domaine :** Qualité
- **Description :** transformer les règles CSV/Markdown en validations réutilisables.
- **Critères d'acceptation :** unicité, FK, dates, devises, nombres, URLs, ISIN, LEI, doublons, conflits, fraîcheur, provenance et corrections contrôlés.
- **Livrables :** moteur/règles, rapports, tests.

## OF-SEC-001 — Définir la politique de sécurité

- **Statut :** PROPOSE
- **Priorité :** P2_MOYENNE
- **Domaine :** Sécurité
- **Critères d'acceptation :** gestion des secrets, rôles base, accès aux sources, chiffrement, logs, données sensibles et procédures d'incident documentés.
- **Livrables :** politique, configuration et tests de non-exposition.

## OF-DEPLOY-001 — Préparer la fusion de la PR #1

- **Statut :** EN_COURS
- **Priorité :** P1_HAUTE
- **Domaine :** Déploiement / Gouvernance Git
- **Dépendances :** OF-DOC-001, correction de la description PR, CI verte, arbitrage des divergences critiques.
- **Critères d'acceptation :**
  - PR à jour avec le scope réel ;
  - tous les workflows verts ;
  - aucune affirmation obsolète ;
  - revue des 95 fichiers ;
  - décisions ouvertes clairement listées ;
  - stratégie de fusion validée.
- **Livrables :** PR prête à revue, rapport de contrôle.

---

# B. TACHES TERMINEES

## OF-AUDIT-001 — Inventorier le dépôt

- **Statut :** TERMINE
- **Priorité :** P0_CRITIQUE
- **Date de fin :** 2026-08-03
- **Résultat :** 95 fichiers inventoriés, 45 écarts documentés, maturité par couche établie.
- **Livrables :**
  - `docs/00_PROJECT/REPOSITORY_AUDIT_2026_08_03.md` ;
  - `docs/00_PROJECT/CONVERSATION_REPOSITORY_GAP_MATRIX.md`.

## OF-GEO-001 — Créer le référentiel des pays et régions

- **Statut :** TERMINE SUR LE PLAN STRUCTUREL
- **Date de fin :** 2026-08-03
- **Résultat :** 54 pays, 1 continent et 5 régions.
- **Limite :** validation officielle et dates historiques encore partielles.

## OF-GEO-002 — Créer les relations pays

- **Statut :** TERMINE SUR LE PLAN STRUCTUREL
- **Date de fin :** 2026-08-03
- **Résultat :** 266 relations normalisées.
- **Limite :** statuts `PENDING` et question `valid_from`.

## OF-FX-001 — Créer les référentiels devises et paires

- **Statut :** TERMINE SUR LE PLAN STRUCTUREL
- **Date de fin :** 2026-08-03
- **Résultat :** 44 devises, 84 paires locale→EUR/USD et règles de conversion.
- **Limite :** sources officielles manquantes pour la majorité des devises.

## OF-FX-002 — Implémenter et tester BCEAO FX

- **Statut :** TERMINE AU NIVEAU COLLECTION_TESTED
- **Date de fin :** 2026-08-03
- **Résultat :** collecte live, SHA256, date de valeur, XOF/EUR/USD, chargement PostgreSQL idempotent.
- **Limite :** snapshot unique, pas d'historique durable.

## OF-FX-003 — Implémenter et tester BEAC FX

- **Statut :** TERMINE AU NIVEAU COLLECTION_TESTED
- **Date de fin :** 2026-08-03
- **Résultat :** collecte live de 13 paires, SHA256, date de valeur, XAF/EUR/USD, chargement idempotent.
- **Limite :** snapshot unique, pas d'historique durable.

## OF-FX-004 — Créer l'orchestrateur quotidien FX

- **Statut :** TERMINE AU NIVEAU STAGING
- **Date de fin :** 2026-08-03
- **Résultat :** pipeline BCEAO + BEAC, manifeste de couverture et workflow planifié.
- **Limite :** base persistante et stockage permanent non configurés.

## OF-TEST-001 — Tester la réconciliation des endpoints

- **Statut :** TERMINE
- **Date de fin :** 2026-08-03
- **Résultat :** tests dans les deux ordres 003/004 et migration 007 idempotente.

---

# C. TACHES BLOQUEES PAR DECISION OU ENVIRONNEMENT

| Tâche | Blocage | Décision / ressource attendue |
|---|---|---|
| OF-MAP-001 | Standard officiel absent | version et droits d'utilisation |
| OF-MAP-002 | catalogue et modèle fonds non stabilisés | OF-MAP-001, OF-DATA-001/002 |
| OF-IMPORT-001 | base persistante absente | environnement + migration runner |
| OF-IMPORT-002 | stockage immuable absent | environnement + politique |
| OF-CALC-001 | historiques NAV et catégories absents | ingestion fonds + taxonomie |
| OF-CALC-002 | séries et benchmarks absents | moteurs amont |
| OF-API-001 | modèle canonique non stabilisé | dictionnaire et entités |
| OF-UI-001 | API absente | contrats API |

## REGLE DE CLOTURE

Une tâche ne passe à `TERMINE` que lorsque ses critères d'acceptation sont vérifiés par un test, une preuve documentaire ou une revue explicite. Un fichier créé sans données réelles ni validation ne suffit pas.
