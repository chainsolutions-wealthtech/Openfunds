# TODO — REGISTRE DES TACHES OPENFUNDS

Dernière mise à jour : `2026-09-10`.

## Réconciliation courante — 2026-09-10

Cette section supersède uniquement les statuts courants obsolètes ; toutes les sections historiques ci-dessous sont conservées.

```text
OF-DOC-003: VERIFIED_COMPLETE_DOCUMENTARY_SOCLE
OF-MAP-002: EN_COURS / CI_FAILURE_KNOWN
CURRENT_GATE: RESTORE_BATCH_07_NO_PARENT_CURRENCY_INFERENCE_CONTRACT
NEXT_AFTER_GREEN: TASK_4_REVIEW_OUTCOMES
GITHUB_RULESETS: NONE_OBSERVED
PRODUCTION_DEPLOYED: NO
```

### OF-DOC-003 — résultat de la réconciliation

Le socle de gouvernance de type Regulatory a été transposé **comme mécanisme**, sans copier le métier Regulatory :

- `00_START_HERE.md` réconcilié avec contrôle Git avant écriture ;
- `SOURCE_OF_TRUTH.md` renforcé avec hiérarchie des autorités et mémoire canonique dans Git ;
- `LOOP_ENGINEERING.md` complété avec la boucle `DISCOVER → ... → VERIFY_REMOTE_STATE → SELECT_NEXT` ;
- `DEFINITION_OF_DONE.md` ajouté ;
- `STATUS.md`, `NEXT_ACTION.md`, `LOOP_STATE.md`, `CURRENT_ITERATION.md` et `HANDOFF.md` réconciliés ;
- preuve : `docs/00_PROJECT/OF_DOC_003_GOVERNANCE_RECONCILIATION_20260910.md` ;
- aucun code métier, migration, mapping, test, branche, PR, `main`, production ou donnée réelle modifié par cette tranche.

Le gap GitHub natif reste ouvert : aucun Ruleset n'est observé. Il ne bloque pas la clôture **documentaire** de `OF-DOC-003`, mais empêche de qualifier le dépôt de gouvernance entièrement enforced par GitHub.

### OF-MAP-002 — gate CI avant Task 4

Le run `OF-MAP-002 Mapping Registry` `32541124896` observé sur `275ec7a10658cfc5a9f5822eb2315bf01138fc10` est rouge : l'intégration officielle/canonique passe, mais les jobs unitaires Python 3.11 et 3.12 échouent parce que le contrat Batch 07 attend `NO_PARENT_CURRENCY_INFERENCE` dans `NOTES`.

La prochaine action est de réconcilier cette incohérence **sans supprimer ni affaiblir le test**, puis de reprendre Task 4.

---

## 1. REGLES

Chaque tâche possède un identifiant stable et reste conservée après sa clôture.

Statuts :

```text
A_ANALYSER
PROPOSE
A_ARBITRER
DECIDE
EN_COURS
PARTIELLEMENT_IMPLEMENTE
IMPLEMENTE
TESTE
DOCUMENTE
BLOQUE
A_CORRIGER
TERMINE
```

Priorités : `P0_CRITIQUE`, `P1_HAUTE`, `P2_MOYENNE`, `P3_BASSE`.

## Synchronisation des statuts — 2026-08-11

Les statuts de `OF-ARCH-001`, `OF-SOURCE-001`, `OF-ARCH-002`, `OF-ARCH-003`, `OF-ARCH-004`, `OF-DATA-001`, `OF-DATA-002` et `OF-DATA-003` sont alignés sur les boucles vérifiées et les preuves CI. Les descriptions historiques restent conservées ; le statut `TERMINE` n’implique ni déploiement de production ni chargement d’historiques réels.

Une tâche ne passe à `TERMINE` qu'après vérification de ses critères d'acceptation. La création d'un fichier ou d'une table vide ne suffit pas.

---

# A. PROCHAINE ETAPE IMMEDIATE

## OF-ARCH-001 — Choisir la source de vérité des référentiels

- **Statut :** TERMINE
- **Priorité :** P0_CRITIQUE
- **Domaine :** Architecture / Gouvernance
- **Dépendances :** `ADR-021`
- **Description :** éliminer la double saisie entre CSV gouvernés et seeds SQL.
- **Options :**
  1. CSV maître générant les migrations ;
  2. PostgreSQL maître générant les CSV ;
  3. manifeste YAML/JSON maître générant les deux.
- **Critères d'acceptation :**
  - une représentation maître est déclarée ;
  - les autres sont générées ou automatiquement contrôlées ;
  - les statuts BCEAO/BEAC concordent ;
  - un test bloque toute divergence ;
  - la méthode de modification et de revue est documentée.
- **Livrables :** ADR accepté, générateur/synchroniseur, contrôle CI.
- **Fichiers :** `data/reference/`, `schemas/reference/`, `DECISIONS.md`.
- **Risques :** corrections contradictoires et états de production incohérents.

## OF-SOURCE-001 — Synchroniser BCEAO/BEAC entre CSV et SQL

- **Statut :** TERMINE
- **Priorité :** P0_CRITIQUE
- **Domaine :** Sources / Référentiels
- **Dépendances :** OF-ARCH-001
- **Description :** aligner organisations, rôles, endpoints, mappings, séries et spécifications avec les validations live.
- **Critères d'acceptation :**
  - aucun objet générique/spécifique en double sans statut explicite ;
  - IDs et lignée existants préservés ;
  - statuts `VALIDATED` et `COLLECTION_TESTED` cohérents ;
  - preuves de run reliées ;
  - migration ou génération additive et idempotente ;
  - test de divergence vert.
- **Livrables :** référentiels corrigés, migration/générateur, tests.

---

# B. ARCHITECTURE ET MODELE DE DONNEES

## OF-ARCH-002 — Unifier le modèle des endpoints

- **Statut :** TERMINE
- **Priorité :** P0_CRITIQUE
- **Dépendances :** OF-ARCH-001
- **Problème :** coexistence conceptuelle de `source.endpoint` et `source.source_endpoint`.
- **Critères d'acceptation :** modèle unique, FK réconciliées, migration additive, tests des ordres 003/004 toujours verts.
- **Livrables :** ADR, SQL, tests et documentation.

## OF-ARCH-003 — Définir les dates métier inconnues

- **Statut :** TERMINE
- **Priorité :** P0_CRITIQUE
- **Dépendances :** `ADR-022`
- **Critères d'acceptation :**
  - date métier séparée de collecte/enregistrement ;
  - statut `KNOWN`, `APPROXIMATE`, `UNKNOWN` ou `NOT_APPLICABLE` ;
  - aucune date artificielle ;
  - sémantique CSV/SQL identique ;
  - vues courantes déterministes.
- **Livrables :** décision, migration, règles qualité, tests.

## OF-ARCH-004 — Adopter une stratégie de migrations

- **Statut :** TERMINE
- **Priorité :** P0_CRITIQUE
- **Dépendances :** OF-ARCH-001/002, `ADR-023`
- **Critères d'acceptation :** ordre unique, registre des migrations, tests base vide/existante, procédure de réparation, aucune destruction de données.
- **Livrables :** migration runner, documentation de déploiement, CI.

## OF-DATA-001 — Stabiliser Fund / SubFund / ShareClass

- **Statut :** TERMINE
- **Priorité :** P0_CRITIQUE
- **Dépendances :** `ADR-009`, exemples Maroc/Tunisie/Nigeria
- **Critères d'acceptation :**
  - entités et cardinalités approuvées ;
  - SICAV, FCP, umbrella et fonds sans compartiment couverts ;
  - identités, noms et alias séparés ;
  - événements de fusion/transfert modélisables ;
  - migration compatible avec les données existantes ;
  - tests de non-duplication.
- **Livrables :** ADR, diagramme, SQL et tests.

## OF-DATA-002 — Peupler le dictionnaire canonique

- **Statut :** TERMINE
- **Priorité :** P0_CRITIQUE
- **Dépendances :** OF-DATA-001, `ADR-024`
- **Etat actuel :** `OF-DATA-002` vérifié complet : paquet JSON gouverné `data/dictionary/spec_v1/`, 10 tables, 143 champs, 36 attributs par champ et CI Python 3.11/3.12 verte.
- **Critères d'acceptation :** chaque champ possède ID, définition, domaine, entité, type, unité, devise, cardinalité, contraintes, validation, normalisation, historique, provenance, sensibilité, confiance, mapping et version.
- **Livrables :** format maître machine-readable, vues humaines et tests.

## OF-DATA-003 — Centraliser les définitions D00-D17

- **Statut :** TERMINE
- **Priorité :** P0_CRITIQUE
- **Dépendances :** OF-DATA-002
- **Critères d'acceptation :** compte vérifié, codes uniques, nature RAW/METADATA/EVENT/CALCULATED, unité, fréquence, source, usages, statut et génération des Markdown.
- **Livrables :** catalogue structuré, import SQL et tests d'unicité.
- **Date de fin :** 2026-08-11
- **Résultat vérifié :** 18 domaines, 420 codes uniques, paquet d’authoring JSON v1, classification gouvernée 298 `RAW` / 85 `METADATA` / 7 `EVENT` / 30 `CALCULATED`, vues JSON/CSV `;`/Markdown/SQL déterministes, migration `016` et double application PostgreSQL 16 en CI.
- **Preuve :** `docs/00_PROJECT/OF_DATA_003_COMPLETION_20260811.md`.

---

# C. MAPPING OPENFUNDS

## OF-MAP-001 — Intégrer le catalogue officiel openfunds

- **Statut :** TERMINE
- **Priorité :** P0_CRITIQUE
- **Dépendances :** OF-DATA-002
- **Critères d'acceptation :** version, source, date, identifiants, descriptions, types et cardinalités sourcés ; aucun contenu officiel inventé.
- **Livrables :** source officielle archivée sans modification, checksum gouverné, parser déterministe et inventaire structurel vérifié.
- **Résultat vérifié 2026-08-17 :** Field List officiel `2.13.0` (`FINAL`, `2026-03-23`) archivé byte-identical ; SHA256 `40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4` ; parser checksum-gated vérifié sur Python 3.11/3.12 et sur le PDF officiel de 745 pages ; inventaire exact de 1 869 OF-ID uniques = 1 849 IDs concrets + 20 templates pays `XX`.
- **Preuves :** `docs/00_PROJECT/OF_MAP_001_OPENFUNDS_V2_13_0_OFFICIAL_ARCHIVE_COMPLETION_20260817.md`, `docs/00_PROJECT/OF_MAP_001_DETERMINISTIC_PARSE_COMPLETION_20260817.md`, `scripts/parse_openfunds_v2_13_0.py`, run GREEN `32061806859`.

## OF-MAP-002 — Construire le mapping openfunds → canonique

- **Statut :** EN_COURS
- **Priorité :** P0_CRITIQUE
- **Dépendances :** OF-MAP-001, OF-DATA-001/002
- **Critères d'acceptation :** statut par champ, cible canonique, transformations, pertes, champs sans équivalent, mapping humain/machine et tests aller-retour.
- **Livrables :** `OPENFUNDS_MAPPING.md` enrichi, registre structuré et fixtures.
- **Progression vérifiée 2026-08-17 :** registre gouverné `data/openfunds/mapping/v2.13.0/MAPPING_REGISTRY.csv`, manifeste et validator checksum-gated opérationnels. Baseline vide GREEN (`32064814922`), validator durci contre doublons `(OF-ID, FIELD_ID)` et incohérences d'entité GREEN (`32065124602`). Batch 01 GREEN (`32065216172`) : 4 lignes validées couvrant 2 OF-ID (`OFST010010`, `OFST020000`) vers 4 cibles canoniques ; 1 867 OF-ID restent non revus et sont calculés, jamais matérialisés artificiellement.

---

# D. SOURCES, IMPORTS ET HISTORIQUES

## OF-SOURCE-002 — Compléter les institutions des 54 pays

- **Statut :** EN_COURS
- **Priorité :** P1_HAUTE
- **Dépendances :** OF-ARCH-001
- **Critères d'acceptation :** statut pour banque centrale, statistiques, finances, dette, bourse, régulateurs fonds et assurance/pension ; URL et preuve vérifiées ; non-applicabilité explicite.
- **Livrables :** organisations, rôles et endpoints complets.
- **Progression vérifiée au 2026-08-17 :** Waves 01 à 13 exécutées sous contrats TDD ; 141 organisations dont 121 `VALIDATED`, 199 relations organisation-rôle = 187 `VALIDATED` + 12 `PENDING`, 53/54 pays avec au moins une organisation country-scoped ; `ERYTHREE` reste volontairement non peuplée faute de source primaire officielle actuelle vérifiée. Wave 13 a fermé les 9 `FX_REFERENCE_RATE_PROVIDER` sous preuves primaires officielles ; résiduel exact : 5 index providers, 3 monetary unions, 2 supranational authorities et 2 interbank market operators.
- **Preuves :** rapports `OF_SOURCE_002_*`, tests `tests/test_institutional_registry*.py`, workflow `Institutional Registry`, audits post-Wave 10/11/12 et `scripts/audit_institutional_role_coverage.py`.
- **Prochaine unité :** poursuivre séparément les 5 `INDEX_PROVIDER` ambigus et la revue sémantique des 7 rôles zonaux ; ne pas confondre validation institutionnelle avec validation endpoint/série `OF-SOURCE-003`, et conserver les cas non applicables ou insuffisamment prouvés explicites.
- **Limite :** couverture 53/54 ne signifie pas complétude de tous les rôles ; les CSV restent des surfaces gouvernées de découverte/revue et la production persistante reste séparée.

## OF-SOURCE-003 — Vérifier les 55 mappings initiaux

- **Statut :** EN_COURS
- **Priorité :** P1_HAUTE
- **Critères d'acceptation :** endpoint, série, fréquence, unité, historique, priorité, méthode, rupture et statut vérifiés.
- **Livrables :** mappings et provider series corrigés.

## OF-IMPORT-001 — Configurer PostgreSQL persistant

- **Statut :** BLOQUE
- **Priorité :** P1_HAUTE
- **Dépendances :** OF-ARCH-004, environnement durable, `OPENFUNDS_DATABASE_URL`
- **Critères d'acceptation :** migrations gouvernées, secret hors dépôt, double run idempotent, métriques, sauvegarde/restauration.

## OF-IMPORT-002 — Configurer le stockage brut immuable

- **Statut :** BLOQUE
- **Priorité :** P1_HAUTE
- **Critères d'acceptation :** URI durable par SHA256, append-only/versionné, intégrité, rétention, restauration et lien dans `source.raw_artifact`.

## OF-HIST-001 — Construire la couverture historique FX

- **Statut :** PROPOSE
- **Priorité :** P1_HAUTE
- **Dépendances :** OF-IMPORT-001/002
- **Critères d'acceptation :** dates distinctes, première/dernière date, calendrier, gaps classés, révisions, statut historique fondé sur des données durables.

## OF-HIST-002 — Backfiller les archives BCEAO/BEAC

- **Statut :** A_ANALYSER
- **Priorité :** P1_HAUTE
- **Dépendances :** OF-HIST-001
- **Critères d'acceptation :** inventaire officiel, début vérifié, ruptures, collecteur reproductible, couverture et preuve de complétude.

## OF-IMPORT-003 — Intégrer la base OPCVM Tunisie

- **Statut :** A_ANALYSER
- **Priorité :** P1_HAUTE
- **Dépendances :** OF-DATA-001, provenance commune, accès au fichier
- **Critères d'acceptation :** source hashée, schéma audité, fonds/alias/gestionnaires/NAV/dividendes/documents/événements mappés, conflits conservés, null jamais zéro, import idempotent.

## OF-IMPORT-004 — Intégrer les archives OPCVM Nigeria

- **Statut :** A_ANALYSER
- **Priorité :** P1_HAUTE
- **Dépendances :** OF-DATA-001, accès SEC
- **Critères d'acceptation :** archives depuis 2011, feuilles/dates contrôlées, NAV/Unit/Bid/Offer séparés, NGN/USD, entités harmonisées avec preuve, provenance cellule, événements, doublons et corruptions conservés.

---

# E. TAXONOMIE, BENCHMARKS ET CALCULS

## OF-TAX-001 — Peupler les classes et sous-classes

- **Statut :** TERMINE
- **Priorité :** P1_HAUTE
- **Dépendances :** OF-ARCH-004
- **Critères d'acceptation :** Actions, Obligations CT/MT/LT, Diversifié Prudent/Equilibré/Dynamique/Flexible, Monétaire, seeds idempotents et tests.
- **Résultat vérifié 2026-08-17 :** 4 classes, 7 sous-classes, snapshot source figé, générateur SQL déterministe, migration gouvernée `017_CANONICAL_FUND_TAXONOMY_V0_1` ordre 170, PostgreSQL 16 GREEN et seconde application 100 % idempotente.
- **Preuve :** `docs/00_PROJECT/OF_TAX_001_002_RUNTIME_PERSISTENCE_COMPLETION_20260817.md`.

## OF-TAX-002 — Générer catégories et sous-catégories

- **Statut :** TERMINE
- **Priorité :** P2_MOYENNE
- **Dépendances :** OF-TAX-001 et géographie validée
- **Critères d'acceptation :** national/régional/Afrique, codes déterministes, parentés, historisation et absence de doublon.
- **Résultat vérifié 2026-08-17 :** structure V0.1 déterministe déjà testée à 486 routages et 432 catégories/blocs de référence ; persistance PostgreSQL gouvernée par migration 017. Les objets restent `STRUCTURE_PREFILLED` / `NOT_ACTIVE` : activation, séries et méthodologies demeurent hors de cette clôture.

## OF-BENCH-001 — Générer les blocs de quatre références

- **Statut :** PROPOSE
- **Priorité :** P2_MOYENNE
- **Dépendances :** OF-TAX-002
- **Critères d'acceptation :** un bloc par catégorie, quatre rôles et affectations historisées.

## OF-BENCH-002 — Finaliser les méthodologies WTI Bench

- **Statut :** EN_COURS
- **Priorité :** P2_MOYENNE
- **Dépendances :** sources de marché validées
- **Critères d'acceptation :** méthodes actions, obligations, diversifié, monétaire et flexible ; version, rebalancement, backtest et gouvernance.

## OF-CALC-001 — Implémenter le WTI

- **Statut :** BLOQUE
- **Priorité :** P2_MOYENNE
- **Dépendances :** NAV fiables, OF-TAX-002, OF-BENCH-001
- **Critères d'acceptation :** univers daté, VL ajustées, aucune interpolation, contributions, exclusions, couverture, chaînage et reproductibilité.

## OF-CALC-002 — Implémenter métriques et classements

- **Statut :** BLOQUE
- **Priorité :** P2_MOYENNE
- **Dépendances :** séries fonds et benchmarks
- **Critères d'acceptation :** performances, volatilité, drawdown, Sharpe, Sortino, alpha, beta, R², VaR, percentiles, quartiles et rangs versionnés.

---

# F. API, UI, QUALITE, SECURITE ET DEPLOIEMENT

## OF-QA-001 — Rendre les règles qualité exécutables

- **Statut :** EN_COURS
- **Priorité :** P1_HAUTE
- **Critères d'acceptation :** unicité, FK, dates, devises, nombres, URLs, ISIN, LEI, doublons, conflits, fraîcheur, provenance et corrections contrôlés.

## OF-SEC-001 — Définir la politique de sécurité

- **Statut :** PROPOSE
- **Priorité :** P2_MOYENNE
- **Critères d'acceptation :** secrets, rôles base, accès, chiffrement, logs, sensibilité et incidents documentés et testés.

## OF-API-001 — Définir les contrats API

- **Statut :** BLOQUE
- **Priorité :** P3_BASSE
- **Dépendances :** OF-DATA-001/002
- **Critères d'acceptation :** OpenAPI versionné, ressources, erreurs, pagination, temporalité, provenance, qualité et sécurité.

## OF-UI-001 — Définir les view models Atomic Design

- **Statut :** BLOQUE
- **Priorité :** P3_BASSE
- **Dépendances :** OF-API-001
- **Critères d'acceptation :** contrats atoms/molecules/organisms/templates, états loading/empty/error/stale/restricted, localisation et accessibilité.

## OF-DEPLOY-001 — Préparer la fusion de la PR #1

- **Statut :** EN_COURS
- **Priorité :** P1_HAUTE
- **Dépendances :** décisions critiques, CI verte, revue
- **Critères d'acceptation :** PR exacte, workflows verts, 104 fichiers revus, décisions ouvertes listées, stratégie de fusion validée.

---

# G. TACHES TERMINEES

## OF-DOC-001 — Consolider la documentation racine

- **Statut :** TERMINE
- **Date de fin :** 2026-08-03
- **Résultat :**
  - README complet ;
  - TODO exploitable ;
  - SUIVI avec point exact de reprise ;
  - ADR-001 à ADR-025 ;
  - architecture, modèle, dictionnaire, mapping, gouvernance, qualité, sources, roadmap et changelog ;
  - audit du dépôt et matrice de 45 écarts ;
  - description PR #1 corrigée ;
  - inventaire post-consolidation de 104 fichiers ;
  - cinq workflows verts.
- **Livrables :** documents racines et `docs/00_PROJECT/`.

## OF-AUDIT-001 — Inventorier le dépôt

- **Statut :** TERMINE
- **Date de fin :** 2026-08-03
- **Résultat :** audit initial de 95 fichiers, maturité par couche et 45 écarts. Après consolidation, la branche contient 104 fichiers.

## OF-GEO-001 — Référentiel pays et régions

- **Statut :** TERMINE_STRUCTUREL
- **Résultat :** 54 pays, 1 continent et 5 régions.
- **Limite :** validation officielle et dates historiques partielles.

## OF-GEO-002 — Relations pays

- **Statut :** TERMINE_STRUCTUREL
- **Résultat :** 266 relations.
- **Limite :** statuts `PENDING` et question `valid_from`.

## OF-FX-001 — Référentiels devises et paires

- **Statut :** TERMINE_STRUCTUREL
- **Résultat :** 44 devises, 84 paires locale→EUR/USD et règles de conversion.

## OF-FX-002 — BCEAO FX

- **Statut :** TERMINE_COLLECTION_TESTED
- **Résultat :** live, SHA256, date, XOF/EUR/USD et chargement idempotent.
- **Limite :** snapshot unique.

## OF-FX-003 — BEAC FX

- **Statut :** TERMINE_COLLECTION_TESTED
- **Résultat :** 13 paires live, SHA256, date, XAF/EUR/USD et chargement idempotent.
- **Limite :** snapshot unique.

## OF-FX-004 — Orchestrateur quotidien FX

- **Statut :** TERMINE_STAGING
- **Résultat :** pipeline double source et manifeste de couverture.
- **Limite :** stockage durable non configuré.

## OF-TEST-001 — Réconciliation des endpoints

- **Statut :** TERMINE
- **Résultat :** tests des ordres 003/004 et migration 007 idempotente.

---

# H. BLOCAGES PRINCIPAUX

| Tâche | Blocage |
|---|---|
| OF-MAP-001 | version officielle openfunds absente |
| OF-MAP-002 | catalogue externe et modèle fonds non stabilisés |
| OF-IMPORT-001 | base persistante et migration runner absents |
| OF-IMPORT-002 | stockage immuable absent |
| OF-CALC-001/002 | historiques fonds, taxonomie et benchmarks absents |
| OF-API-001 | modèle canonique non stabilisé |
| OF-UI-001 | API absente |


---

# I. MISE A JOUR DOCUMENTAIRE — 2026-08-04

Cette section complète le registre sans modifier les résultats historiques du 3 août 2026.

## Correction de volumétrie courante

La PR nº 1 contient actuellement **122 fichiers modifiés** selon les métadonnées GitHub. Les nombres 95 et 104 restent conservés ci-dessus comme états historiques de l'audit initial et de la première consolidation.

Pour `OF-DEPLOY-001`, le critère courant devient : revue des 122 fichiers au HEAD audité, sans considérer ce volume comme figé si la branche évolue.

## Correction de statut — Taxonomie et matrices

| Tâche | Statut courant au 2026-08-04 | Limite |
|---|---|---|
| `OF-TAX-001` | `STRUCTURE_PRESENT / TESTED` | référentiels et tests présents ; aucune activation ou migration de production revendiquée |
| `OF-TAX-002` | `STRUCTURE_PRESENT / IMPLEMENTED / TESTED / NOT_ACTIVE` | générateur déterministe, 486 règles ; membres fonds et historique non disponibles |
| `OF-BENCH-001` | `STRUCTURE_PRESENT / IMPLEMENTED / TESTED / NOT_ACTIVE` | 432 blocs structurels ; séries, licences et méthodologies non validées |
| `OF-BENCH-002` | `EN_COURS` | WTI Bench non calculé et non actif |
| `OF-CALC-001` | `BLOQUE` | aucun WTI calculé |
| `OF-CALC-002` | `BLOQUE` | aucun moteur actif de ratios ou classements |

Cette correction de statut ne transforme jamais une structure générée en produit analytique actif.

## Sujets proposés — sans réordonner les tâches existantes

L'ordre immédiat reste :

```text
OF-ARCH-001
→ OF-SOURCE-001
→ OF-ARCH-002
→ OF-ARCH-003
→ OF-ARCH-004
```

### Collision d'identifiant géographique

Le nouvel intitulé proposé « Réconcilier NATIONAL et LOCAL_MARKET » ne peut pas utiliser `OF-GEO-001`, car cet identifiant est déjà attribué à « Référentiel pays et régions ».

```text
STATUT                  PROPOSE
IDENTIFIANT DEMANDE     OF-GEO-001
COLLISION               OUI
IDENTIFIANT FINAL       A ARBITRER
CANDIDATS NON VALIDES   OF-GEO-003 / OF-MARKET-001
```

Aucune nouvelle tâche avec un identifiant collisionné n'est créée dans ce registre.

### OF-SCOPE-001 — Introduire INVESTMENT_SCOPE

- **Statut :** PROPOSE
- **Priorité proposée :** P0
- **Dépendances :** OF-DATA-001, classification et benchmarks
- **Objet :** séparer domicile juridique, périmètre réglementaire, géographie d'investissement, marché principal, benchmark déclaré et devise de référence.
- **Interdiction :** ne pas déduire automatiquement le mandat d'investissement du seul pays juridique.

### OF-EXPORT-001 — Rendre le classeur reproductible

- **Statut :** PROPOSE
- **Priorité proposée :** P1
- **Dépendances :** entrées canoniques et générateur
- **Objet :** prouver que le classeur de revue peut être régénéré de manière déterministe depuis le dépôt.
- **Interdiction :** le classeur reste un export dérivé et ne devient pas une source canonique.

### OF-DOC-002 — Réaligner les statuts documentaires

- **Statut :** PROPOSE
- **Priorité proposée :** P1
- **Objet :** maintenir l'alignement entre documentation, matrices, SQL, code et statuts GitHub.
- **Etat apporté par cette intervention :** baseline et rapports préparés ; la gouvernance documentaire reste une obligation continue.

## Point d’entrée permanent et rapports de préparation

- `docs/00_PROJECT/BRANCH_INVENTORY_AND_EXPLOITATION_PLAN.md`
- `docs/00_PROJECT/GITHUB_BASELINE_AUDIT_20260804.md`
- `docs/00_PROJECT/BRANCH_INVENTORY_20260804.csv`
- `docs/00_PROJECT/BOOTSTRAP_INTEGRATION_ASSESSMENT_20260804.md`
- `docs/00_PROJECT/PR_CONTENT_RECONCILIATION_20260804.csv`
- `docs/00_PROJECT/CANONICAL_PROJECT_STATE_20260804.md`
- `docs/00_PROJECT/OPEN_DECISIONS_AND_EXECUTION_GATES_20260804.md`
- `docs/00_PROJECT/ISSUE_MIGRATION_DRAFT_20260804.csv`
- `docs/00_PROJECT/HANDOFF_TO_NEXT_AGENT_20260804.md`

Aucune issue GitHub n'a été créée par cette intervention.

---

# J. RECONCILIATION ET LOOP ENGINEERING — 2026-08-05

Cette section supersède les statuts courants obsolètes sans supprimer les sections historiques.

## Statuts vérifiés

```text
OF-ARCH-001   VERIFIED_COMPLETE
OF-SOURCE-001 VERIFIED_COMPLETE
OF-ARCH-002   VERIFIED_COMPLETE
OF-ARCH-003   VERIFIED_COMPLETE
OF-ARCH-004   IMPLEMENTED_WITH_OPEN_GOVERNANCE_BLOCKER
OF-DATA-001   NOT_STARTED
```

Le blocker de `OF-ARCH-004` concerne l'immuabilité historique de la migration générée `012`. Le runner est implémenté et testé dans ses scénarios documentés, mais la migration historique peut être rematérialisée depuis le CSV avant hashing. Aucune correction technique n'est apportée dans `OF-DOC-003`.

## OF-DOC-003 — Intégrer le standard Loop Engineering complet

- **Statut :** EN_COURS
- **Priorité :** P0_DOCUMENTATION
- **Boucle :** `OF-LOOP-DOC-003`
- **Branche :** `architecture/africafunds-country-indicators-v0.1`
- **Objet :** réconcilier la mémoire permanente, créer la matrice de correspondance et tous les chemins Markdown du kit, initialiser les règles communes IA/humains, les catalogues, manifestes et handoffs.
- **Critères d'acceptation :** 176 chemins du kit présents ; aucun document vide ; canoniques historiques conservés ; zéro modification technique ; contrôles et CI rapportés honnêtement ; aucune opération Git/PR interdite ; `OF-DATA-001` non commencé.
- **Livrables :** `00_START_HERE.md`, `AGENTS.md`, `SOURCE_OF_TRUTH.md`, `STATUS.md`, `LOOP_STATE.md`, `DOCUMENT_INTEGRATION_MATRIX.md`, `FILES_CATALOG.md`, `MANIFEST.md`, documents sous `docs/01-governance/` à `docs/12-optional/`, réconciliation permanente et rapport final.

## Prochaine action autorisée

```text
CLOTURER OF-DOC-003
→ VERIFIER LE HEAD ET LA CI
→ AUTORISER SEPAREMENT LA RESOLUTION DU BLOCKER 012
```

Ne pas retargeter ou fusionner la PR nº 1, ne pas modifier la PR nº 2 et ne pas commencer `OF-DATA-001`.

---

# K. OF-SOURCE-002 — VAGUE 01 VERIFIEE / VAGUE 02 OUVERTE — 2026-08-12

```text
TASK_ID: OF-SOURCE-002
GLOBAL_STATUS: EN_COURS
WAVE_01: VERIFIED_COMPLETE
WAVE_01_CI_RUN: 31592700354
WAVE_02: READ_ONLY_AUDIT
```

### Résultat de la vague 01

- baseline lue avant écriture : 40 organisations, 70 relations de rôles, 43 endpoints ;
- 15 organisations officiellement vérifiées ajoutées ;
- 22 relations organisation-rôle officiellement vérifiées ajoutées ;
- couverture country-scoped passée de 7/54 à 10/54 pays ;
- 44 pays restent sans organisation nationale ;
- `Institutional Registry` ajouté comme contrôle exécutable ;
- TDD RED puis GREEN vérifié sur Python 3.11/3.12 ;
- `FMDQ` exclu de l’allowlist dans l’attente d’une revue sémantique du rôle ;
- aucun endpoint, SQL runtime, historique, branche, PR ou déploiement ajouté.

### Vague 02 — gate

La prochaine action est un audit read-only des 44 pays non couverts et des rôles manquants des 10 pays déjà représentés. Une nouvelle écriture n’est autorisée qu’après preuve officielle primaire, revue des collisions de code et allowlist explicite.
