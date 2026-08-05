# ROADMAP OPENFUNDS

## PRINCIPE

Chaque phase possède une porte de sortie. Une phase aval ne doit pas être présentée comme terminée tant que ses dépendances ne sont pas vérifiées.

## PHASE 0 — CONSOLIDATION ET GOUVERNANCE

**Statut : EN COURS**

Livrables :

- README, TODO, SUIVI ;
- audit et matrice des écarts ;
- décisions ;
- architecture, modèle, dictionnaire, mapping, qualité, sources et changelog ;
- description PR exacte.

Porte de sortie : documents cohérents, liens valides, point de reprise et CI verte.

Tâches : `OF-DOC-001`, `OF-DEPLOY-001`.

## PHASE 1 — RECONCILIATION DES REFERENTIELS

**Statut : A ARBITRER**

Travaux :

- choisir la source de vérité CSV/SQL ;
- synchroniser BCEAO/BEAC ;
- unifier les endpoints ;
- résoudre les dates métier inconnues ;
- marquer les fichiers legacy ;
- adopter un migration runner.

Porte de sortie : une seule représentation maître, migrations testées et aucune divergence de statut.

Tâches : `OF-ARCH-001` à `004`, `OF-SOURCE-001`.

## PHASE 2 — MODELE FONDS ET DICTIONNAIRE

**Statut : NON COMMENCE**

Travaux :

- Fund/SubFund/ShareClass ;
- identités, noms et alias ;
- organisations de service ;
- documents et événements ;
- dictionnaire canonique ;
- catalogue D00-D17 machine-readable.

Porte de sortie : modèle approuvé, migrations non destructives, champs versionnés et tests.

Tâches : `OF-DATA-001` à `003`.

## PHASE 3 — MAPPING OPENFUNDS

**Statut : BLOQUE**

Travaux :

- obtenir et versionner le standard officiel ;
- charger le catalogue ;
- mapper chaque champ ;
- documenter transformations et pertes ;
- tester import/export.

Porte de sortie : rapport de couverture et mapping humain/machine validé.

Tâches : `OF-MAP-001`, `OF-MAP-002`.

## PHASE 4 — PERSISTANCE ET PROVENANCE DURABLES

**Statut : BLOQUE PAR ENVIRONNEMENT**

Travaux :

- PostgreSQL persistant ;
- stockage brut immuable ;
- secrets et accès ;
- sauvegarde/restauration ;
- métriques et alertes de run.

Porte de sortie : un run quotidien durable charge les deux zones et conserve les artefacts.

Tâches : `OF-IMPORT-001`, `OF-IMPORT-002`, `OF-SEC-001`.

## PHASE 5 — HISTORIQUES FX ET COUVERTURE

**Statut : NON COMMENCE**

Travaux :

- plusieurs dates persistées ;
- vues de couverture ;
- calendrier et gaps ;
- inventaire des archives ;
- backfill BCEAO/BEAC ;
- révisions et ruptures.

Porte de sortie : statut `PARTIAL_HISTORY_LOADED`, puis `COMPLETE_HISTORY_LOADED` uniquement après preuve.

Tâches : `OF-HIST-001`, `OF-HIST-002`.

## PHASE 6 — INSTITUTIONS ET SOURCES DES 54 PAYS

**Statut : EN COURS PARTIEL**

Travaux :

- compléter les rôles institutionnels ;
- vérifier endpoints et séries ;
- renseigner fréquences, unités et historiques ;
- déclarer les données non publiées/non applicables.

Porte de sortie : couverture institutionnelle auditée pour chaque pays et zone.

Tâches : `OF-SOURCE-002`, `OF-SOURCE-003`.

## PHASE 7 — INGESTION OPCVM TUNISIE ET NIGERIA

**Statut : A ANALYSER**

Travaux :

- intégrer la base CMF Tunisie ;
- auditer les archives SEC Nigeria depuis 2011 ;
- harmoniser identités et événements ;
- conserver NAV, AUM, dividendes, documents et conflits ;
- provenance cellule/page.

Porte de sortie : imports idempotents, rapports de couverture et données reliées au modèle fonds.

Tâches : `OF-IMPORT-003`, `OF-IMPORT-004`.

## PHASE 8 — AUTRES DONNEES PAYS ET MARCHE

**Statut : PROPOSE**

Ordre indicatif :

1. taux directeurs ;
2. taux interbancaires ;
3. adjudications et courbes ;
4. indices actions ;
5. inflation, PIB, dette et réserves ;
6. autres fonds et institutionnels.

Porte de sortie : chaque série possède source, spécification, historique, qualité et provenance.

## PHASE 9 — TAXONOMIE ET GROUPES DE PAIRS

**Statut : NON COMMENCE**

Travaux :

- classes et sous-classes ;
- catégories nationales, régionales et Afrique ;
- appartenances historisées ;
- univers éligibles ;
- groupes de pairs.

Porte de sortie : générateur déterministe et couverture fonds suffisante.

Tâches : `OF-TAX-001`, `OF-TAX-002`.

## PHASE 10 — BLOCS DE REFERENCE ET BENCHMARKS

**Statut : NON COMMENCE**

Travaux :

- générer les quatre rôles ;
- affecter indices officiels ;
- finaliser WTI Bench actions, obligations, diversifié et monétaire ;
- versionner les méthodologies.

Porte de sortie : affectations auditées et méthodologies approuvées.

Tâches : `OF-BENCH-001`, `OF-BENCH-002`.

## PHASE 11 — WTI, INDICES, METRIQUES ET CLASSEMENTS

**Statut : BLOQUE PAR LES SERIES AMONT**

Travaux :

- calcul WTI ;
- indices obligataires/monétaires ;
- performances et risques ;
- rangs, quartiles et percentiles ;
- versions locale/EUR/USD ;
- contributions et exclusions.

Porte de sortie : reconstruction exacte depuis les entrées et méthodologies.

Tâches : `OF-CALC-001`, `OF-CALC-002`.

## PHASE 12 — API ET ATOMIC DESIGN

**Statut : NON COMMENCE**

Travaux :

- OpenAPI ;
- ressources temporelles avec provenance ;
- clients typés ;
- view models ;
- atoms, molecules, organisms, templates et pages ;
- sécurité et contrôle d'accès.

Porte de sortie : API contractuellement testée et pages alimentées exclusivement par les ressources canoniques.

Tâches : `OF-API-001`, `OF-UI-001`.

## ORDRE IMMEDIAT APRES CONSOLIDATION

```text
OF-ARCH-001
→ OF-SOURCE-001
→ OF-ARCH-002
→ OF-ARCH-003
→ OF-ARCH-004
→ OF-DATA-001
→ OF-DATA-002
→ OF-DATA-003
```

La couverture historique persistante ne doit pas précéder la réconciliation des référentiels et migrations.


---

## MISE A JOUR DOCUMENTAIRE — 2026-08-04

Cette section corrige l'état courant sans réécrire les états historiques du 3 août 2026.

### Phase 0

**Statut courant : BASELINE DOCUMENTAIRE ETABLIE / REVUE ET INTEGRATION ENCORE OUVERTES**

Le point d’entrée permanent est :

- `docs/00_PROJECT/BRANCH_INVENTORY_AND_EXPLOITATION_PLAN.md`.

Les rapports de contrôle datés sont :

- `docs/00_PROJECT/GITHUB_BASELINE_AUDIT_20260804.md` ;
- `docs/00_PROJECT/BRANCH_INVENTORY_20260804.csv` ;
- `docs/00_PROJECT/BOOTSTRAP_INTEGRATION_ASSESSMENT_20260804.md` ;
- `docs/00_PROJECT/PR_CONTENT_RECONCILIATION_20260804.csv` ;
- `docs/00_PROJECT/CANONICAL_PROJECT_STATE_20260804.md` ;
- `docs/00_PROJECT/OPEN_DECISIONS_AND_EXECUTION_GATES_20260804.md` ;
- `docs/00_PROJECT/ISSUE_MIGRATION_DRAFT_20260804.csv` ;
- `docs/00_PROJECT/HANDOFF_TO_NEXT_AGENT_20260804.md`.

La PR nº 1 reste en brouillon, ouverte et non fusionnée. `main` reste minimale.

### Phase 9 — Taxonomie et groupes de pairs

**Statut courant corrigé : STRUCTURE_PRESENT / TESTED / NOT_ACTIVE**

Sont présents et testés :

- quatre classes d'actifs ;
- sept sous-classes autorisées ;
- neuf modèles de classification ;
- 54 routes pays vers niveau local de marché, région et Afrique ;
- 486 règles de routage développées ;
- 432 catégories et groupes de pairs structurels.

Restent ouverts :

- modèle final Fund/SubFund/ShareClass ;
- membres réels et historiques des groupes de pairs ;
- bornes obligataires et profils diversifiés ;
- distinction définitive `NATIONAL` / `LOCAL_MARKET` ;
- `INVESTMENT_SCOPE`.

### Phase 10 — Blocs de référence et benchmarks

**Statut courant corrigé : STRUCTURE_PRESENT / TESTED / NOT_ACTIVE**

Les 432 blocs et leurs rôles sont générés de manière déterministe. Cette présence structurelle ne signifie pas que les séries fournisseurs, licences, méthodologies WTI Bench, taux sans risque ou MAR sont validés.

### Phase 11

Le statut reste inchangé : WTI, WTI Bench, ratios et classements ne sont pas actifs.

### Ordre immédiat préservé

```text
OF-ARCH-001
→ OF-SOURCE-001
→ OF-ARCH-002
→ OF-ARCH-003
→ OF-ARCH-004
```

Les sujets `LOCAL_MARKET`, `INVESTMENT_SCOPE`, reproductibilité du classeur et alignement documentaire restent proposés et ne réordonnent pas cette chaîne.

---

## MISE A JOUR LOOP ENGINEERING — 2026-08-05

Les phases historiques restent ci-dessus. L'état courant vérifié est :

```text
OF-ARCH-001   VERIFIED_COMPLETE
OF-SOURCE-001 VERIFIED_COMPLETE
OF-ARCH-002   VERIFIED_COMPLETE
OF-ARCH-003   VERIFIED_COMPLETE
OF-ARCH-004   IMPLEMENTED_WITH_OPEN_GOVERNANCE_BLOCKER
```

### Phase 0 — état courant

**Statut : LOOP_ENGINEERING_INTEGRATION / OF-DOC-003**

La mémoire permanente est réconciliée et le standard documentaire complet est intégré sans remplacer les canoniques historiques. Les nouveaux points d'entrée sont `00_START_HERE.md`, `AGENTS.md`, `SOURCE_OF_TRUTH.md`, `STATUS.md` et `NEXT_ACTION.md`.

### Phase 1 — état courant

**Statut : IMPLEMENTED, AUDITED, BLOCKER DE GOUVERNANCE 012 OUVERT**

Les quatre premiers gates et `OF-SOURCE-001` ont été mis en œuvre. La sortie complète de phase reste bloquée par l'immuabilité historique de la migration générée `012` et par des limites de concurrence/adoption documentées.

### Ordre de reprise

```text
1. clôturer OF-DOC-003 et vérifier la CI documentaire ;
2. autoriser séparément la résolution du blocker migration 012 ;
3. réconcilier la stratégie d'intégration de la PR nº 1 ;
4. décider le traitement des trois Markdown uniques de la PR nº 2 ;
5. seulement ensuite évaluer le démarrage de OF-DATA-001.
```

`OF-DATA-001` reste `NOT_STARTED`. Aucune phase technique ou production n'est lancée par cette mise à jour.