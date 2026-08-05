# Brouillon de mise à jour de la description de la PR nº 1

Ce fichier est un brouillon. La PR nº 1 n’est pas modifiée par cette
intervention.

---

## Purpose

Consolider l’architecture canonique Openfunds/AfricaFunds, les référentiels
africains, la matrice déterministe de classification, la provenance des sources
et les pilotes FX BCEAO/BEAC, sans prétendre que les historiques, les calculs,
l’API ou le modèle fonds final sont terminés.

## Verified architecture gates

### OF-ARCH-001 — governed reference authoring

`VERIFIED_COMPLETE`

- `VALIDATED_FX_REFERENCE_REGISTRY.csv` est l’autorité d’authoring des deux
  pilotes FX validés ;
- le SQL de synchronisation est généré de manière déterministe ;
- PostgreSQL reste la vérité runtime après application ;
- les grands CSV restent des inventaires de découverte.

### OF-SOURCE-001 — BCEAO / BEAC reconciliation

`VERIFIED_COMPLETE`

- XOF et XAF restent séparés ;
- endpoints, mappings, provider series et collection specifications validés ;
- preuves de run et SHA-256 reliés ;
- statuts `VALIDATED` et `COLLECTION_TESTED` ;
- aucune revendication d’historique complet.

### OF-ARCH-002 — canonical endpoint model

`VERIFIED_COMPLETE`

```text
source.endpoint
= CANONICAL PHYSICAL RUNTIME RELATION

source.source_endpoint
= PRESERVED NON-OPERATIONAL PROPOSAL
```

Les FK opérationnelles utilisent `source.endpoint`. Les fichiers de proposition
sont exclus du manifeste.

### OF-ARCH-003 — explicit business-date knowledge

`VERIFIED_COMPLETE`

- `KNOWN`, `APPROXIMATE`, `UNKNOWN`, `NOT_APPLICABLE` ;
- dates inconnues à `NULL` ;
- aucune date artificielle ;
- vues courantes déterministes ;
- rejeu compatible avec le scénario PostgreSQL testé.

### OF-ARCH-004 — governed migration runner

`IMPLEMENTED_WITH_OPEN_GOVERNANCE_BLOCKER`

Implémenté et testé :

- manifeste de 14 migrations ;
- ordre, IDs et chemins uniques ;
- ledger PostgreSQL ;
- SHA-256 et métadonnées contrôlés ;
- transaction migration + ledger ;
- `plan`, `apply`, `verify` ;
- base PostgreSQL 16 vide ;
- double application ;
- scénario de base complète sans ledger ;
- checksum drift et entrée inconnue bloqués ;
- propositions exclues ;
- procédure de réparation.

Blocker ouvert :

- la migration générée `012` est rematérialisée depuis le CSV avant hashing et
  n’est pas figée comme blob Git ;
- la règle future doit geler l’ancien SQL et créer une nouvelle migration pour
  toute évolution du registre ;
- concurrence sans advisory lock et adoptions partielles restent seulement
  partiellement couvertes.

Le run technique validé est :

```text
WORKFLOW: Governed Migration Runner
RUN_ID: 30965690163
HEAD_SHA: 5a6ed3da39571e331e8317e3759cd7068165c66d
RESULT: completed / success
```

Le commit `202f23d5...` est documentaire et n’est pas un nouveau run technique.

## Structurally present

- 54 pays, cinq régions et zones de marché/monétaires ;
- devises et paires FX locale/EUR/USD ;
- organisations, rôles, endpoints, mappings, provider series et specs initiales ;
- structure de taxonomie et routage déterministe ;
- collecteurs et lignée FX BCEAO/BEAC ;
- documentation de gouvernance, sources, modèles et qualité.

## Tested implementation

- génération de la matrice de classification ;
- tests des routes UEMOA/CEMAC ;
- collecteurs BCEAO et BEAC ;
- conservation buy/sell et calculs canoniques ;
- artefacts SHA-256 et provenance ;
- chargement PostgreSQL idempotent ;
- contrats endpoint ;
- dates métier explicites ;
- runner de migrations dans ses scénarios CI ;
- workflows Python et PostgreSQL dédiés.

## Honest limitations

Cette PR ne fournit pas encore :

- modèle final Fund/SubFund/ShareClass ;
- catalogue officiel openfunds ni mapping complet ;
- dictionnaire canonique machine-readable complet ;
- historiques complets des 54 pays ;
- stockage brut immuable durable ;
- PostgreSQL persistant de production ;
- imports OPCVM Tunisie/Nigeria ;
- groupes de pairs réels et historiques ;
- benchmarks validés ;
- WTI, WTI Bench, métriques ou classements actifs ;
- API, SDK ou frontend.

Les pilotes FX restent `COLLECTION_TESTED`, pas
`PARTIAL_HISTORY_LOADED` ou `COMPLETE_HISTORY_LOADED`.

## Integration status

```text
PR_STATE: OPEN
DRAFT: TRUE
MERGED: FALSE
MERGEABLE: FALSE
BASE_BRANCH: architecture/canonical-model-v1-bootstrap
BASE_HEAD: 136abf71f0825075361f8c7446e19c6f6476a3a5
HEAD: 202f23d5a5be961d6f8338984b04655eda336a6b
MERGE_BASE: 23ce7c7f00206f37eeec50dfccf03fa2cb7505ea
AHEAD_BY: 183
BEHIND_BY: 7
```

Six des sept fichiers propres au bootstrap sont identiques par blob. Le conflit
réel concerne `schemas/reference/002_country_relationships.sql`; la version
AfricaFunds contient les correctifs monotones à préserver.

La stratégie recommandée reste un retargeting futur vers `main` (`Strategy B`),
mais aucun retargeting n’est autorisé par ce brouillon. Cette décision exige une
nouvelle vérification et une autorisation explicite.

## Remaining review blockers

1. gouverner et corriger l’immuabilité de la migration générée `012` ;
2. réconcilier les documents permanents devenus obsolètes ;
3. approuver la stratégie d’intégration de PR nº 1 ;
4. décider du sort des trois Markdown uniques de PR nº 2 ;
5. stabiliser Fund/SubFund/ShareClass avant les imports massifs ;
6. choisir le format maître du dictionnaire ;
7. obtenir/versionner le catalogue officiel openfunds ;
8. valider les méthodologies et séries de benchmark.

## Safety

- aucun déploiement production ;
- aucun secret versionné ;
- aucune suppression de données ;
- aucun modèle de proposition exécuté par le manifeste ;
- `main` n’est pas modifiée par cette PR tant qu’aucune fusion n’est autorisée ;
- les statuts structurels ne sont pas présentés comme données historiques
  complètes ou produits calculés actifs.

## Documentation entry points

- `docs/00_PROJECT/ARCHITECTURE_GATE_CHAIN_FINAL_AUDIT_20260805.md`
- `docs/00_PROJECT/MIGRATION_RUNNER_RISK_REVIEW_20260805.md`
- `docs/00_PROJECT/PR1_BASE_DIVERGENCE_RECONCILIATION_20260805.md`
- `docs/00_PROJECT/NEXT_PHASE_READINESS_20260805.md`
- `docs/00_PROJECT/PR1_DESCRIPTION_UPDATE_DRAFT_20260805.md`
- `TODO.md`
- `SUIVI.md`
- `DECISIONS.md`
- `ARCHITECTURE.md`
- `DATA_MODEL.md`
- `SOURCE_REGISTRY.md`

## Immediate next step

Ne pas commencer `OF-DATA-001`.

La prochaine phase autorisée doit d’abord résoudre le blocker de gouvernance de
la migration générée `012`, réconcilier les documents permanents puis préparer
l’intégration de la PR nº 1 sans régression.
