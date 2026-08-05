# Réconciliation des documents permanents — 2026-08-05

```text
TASK_ID: OF-DOC-003
LOOP_ID: OF-LOOP-DOC-003
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
OBSERVED_HEAD: 3c54c54733e116f35ff63a0759c921afd58c57a6
BASELINE_END_SHA: 59f6475102b8a0c5b1274060afc412db787f2caf
MODE: ADDITIVE_DOCUMENTARY_RECONCILIATION
```

## Règle de supersession

Les états des 3 et 4 août restent historiques. La présente réconciliation ajoute
un état daté ; elle ne supprime aucune décision, métrique ou preuve antérieure.

| Document | Information obsolète | Preuve récente | Correction | Action | Statut |
|---|---|---|---|---|---|
| `README.md` | volumes 104, cinq workflows, architecture gates ouverts | audits du 5 août et PR nº 1 au HEAD `3c54c...` | renvoyer vers `STATUS.md`, conserver l’historique | note datée | RECONCILED |
| `TODO.md` | OF-ARCH-001/002/003 et OF-SOURCE-001 encore ouverts ; OF-ARCH-004 proposé | audit final indépendant | appliquer les cinq statuts vérifiés et ajouter OF-DOC-003 | mise à jour additive | RECONCILED |
| `SUIVI.md` | point de reprise OF-ARCH-001 | audit final et blocker 012 | consigner la chaîne terminée partiellement et Loop Engineering | entrée datée | RECONCILED |
| `ROADMAP.md` | phase 1 à arbitrer | implémentations et run PostgreSQL 16 | phase 1 vérifiée sauf blocker gouvernance 012 | note datée | RECONCILED |
| `CHANGELOG.md` | décisions encore à prendre | ADR-021/026/027/028 et audit | ajouter clôtures et blocker réel | entrée datée | RECONCILED |
| `DECISIONS.md` | ADR-022/023 encore proposés | ADR-027/028 acceptés | enregistrer supersession sans effacer les propositions | note datée | RECONCILED |
| `ARCHITECTURE.md` | endpoints, dates et runner listés comme écarts | tests et ADR récents | marquer résolus ; conserver blocker 012 | note datée | RECONCILED |
| `DATA_MODEL.md` | dates et endpoint encore à décider | ADR-026/027 | actualiser état ; Fund/SubFund/ShareClass reste ouvert | note datée | RECONCILED |
| plan des branches | compteurs baseline uniquement | PR nº 1 à 184 commits, divergence 7 | ajouter observation dynamique et renvoi vers Loop | note datée | RECONCILED |
| handoff daté | reprise OF-ARCH-001 | audit final | préserver comme baseline et renvoyer vers `HANDOFF.md` | note datée | RECONCILED |

## Statuts applicables

```text
OF-ARCH-001   VERIFIED_COMPLETE
OF-SOURCE-001 VERIFIED_COMPLETE
OF-ARCH-002   VERIFIED_COMPLETE
OF-ARCH-003   VERIFIED_COMPLETE
OF-ARCH-004   IMPLEMENTED_WITH_OPEN_GOVERNANCE_BLOCKER
OF-DATA-001   NOT_STARTED
```

## Blockers et décisions non masqués

- migration générée 012 mutable historiquement ;
- concurrence du runner seulement partiellement couverte ;
- PR nº 1 non fusionnable dans sa base actuelle ;
- trois Markdown uniques de la PR nº 2 à décider ;
- modèle Fund/SubFund/ShareClass non commencé.

## Autorité

Les rapports datés restent preuves historiques. `STATUS.md`, `NEXT_ACTION.md`,
`SOURCE_OF_TRUTH.md`, `LOOP_STATE.md` et `HANDOFF.md` donnent l’état vivant.
