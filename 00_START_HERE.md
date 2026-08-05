# Openfunds — point d’entrée obligatoire

```text
STATUS: ACTIVE
TASK_ID: OF-DOC-003
LOOP_ID: OF-LOOP-DOC-003
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
DOCUMENTARY_BASELINE_END: 59f6475102b8a0c5b1274060afc412db787f2caf
OBSERVED_HEAD_AT_INITIALIZATION: 3c54c54733e116f35ff63a0759c921afd58c57a6
LAST_VERIFIED: 2026-08-05
```

## Finalité

Ce fichier est le premier document à lire pour toute intervention humaine ou IA.
Il ne remplace pas les documents historiques : il les ordonne et indique la
source d’autorité à consulter avant toute écriture.

## Lecture obligatoire

1. `AGENTS.md` — règles communes aux humains et assistants ;
2. `SOURCE_OF_TRUTH.md` — autorités d’authoring, runtime et recherche ;
3. `STATUS.md` — état vérifié et limites ;
4. `NEXT_ACTION.md` — seule prochaine action autorisée ;
5. `LOOP_STATE.md` et `CURRENT_ITERATION.md` — boucle en cours ;
6. `TODO.md`, `SUIVI.md`, `DECISIONS.md` — mémoire permanente ;
7. `docs/00_PROJECT/ARCHITECTURE_GATE_CHAIN_FINAL_AUDIT_20260805.md` ;
8. `docs/00_PROJECT/MIGRATION_RUNNER_RISK_REVIEW_20260805.md`.

## Contrôle Git obligatoire

Avant toute écriture, résoudre dynamiquement le HEAD de `architecture/africafunds-country-indicators-v0.1` et vérifier
que `59f6475102b8a0c5b1274060afc412db787f2caf` en est toujours un ancêtre. Inventorier chaque commit postérieur.
Arrêter si la lignée diverge ou si une intervention parallèle touche les mêmes
fichiers.

## Statuts techniques à préserver

```text
OF-ARCH-001   VERIFIED_COMPLETE
OF-SOURCE-001 VERIFIED_COMPLETE
OF-ARCH-002   VERIFIED_COMPLETE
OF-ARCH-003   VERIFIED_COMPLETE
OF-ARCH-004   IMPLEMENTED_WITH_OPEN_GOVERNANCE_BLOCKER
OF-DATA-001   NOT_STARTED
```

## Interdictions permanentes de cette boucle

Aucune nouvelle branche, aucun travail sur `main`, aucune nouvelle PR, aucune
fusion, aucun retargeting, aucun force-push, aucun déploiement et aucune
modification technique. La migration générée `012` reste inchangée.

## Quand mettre ce document à jour

Uniquement lorsqu’un point d’entrée, une autorité documentaire ou la séquence de
reprise change. Toute modification doit être reliée à une tâche `OF-*`, une
preuve et une entrée dans `WORK_LOG.md`.
