
# Openfunds — point d’entrée obligatoire

```text
STATUS: ACTIVE
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
CURRENT_HEAD_POLICY: RESOLVE_DYNAMICALLY
DOCUMENTARY_BASELINE_END: 59f6475102b8a0c5b1274060afc412db787f2caf
LATEST_VERIFIED_TECHNICAL_HEAD: 0777afffad950e779234ef09f3f2b9031ec41ce7
LAST_VERIFIED: 2026-08-11
```

## Finalité

Ce fichier est le premier document à lire pour toute intervention humaine ou IA. Il ne remplace pas les documents historiques : il ordonne les autorités à consulter avant toute écriture.

## Lecture obligatoire

1. `AGENTS.md` ;
2. `SOURCE_OF_TRUTH.md` ;
3. `STATUS.md` ;
4. `NEXT_ACTION.md` ;
5. `LOOP_STATE.md` et `CURRENT_ITERATION.md` ;
6. `TODO.md`, `SUIVI.md`, `DECISIONS.md` ;
7. le rapport de clôture le plus récent sous `docs/00_PROJECT/` ;
8. les ADR liés à la tâche candidate.

## Contrôle Git obligatoire

Résoudre dynamiquement le HEAD de la branche de contrôle, vérifier la lignée depuis la baseline documentaire et inventorier tout commit postérieur au dernier HEAD technique validé. Arrêter en cas de divergence non comprise ou d’intervention concurrente sur les mêmes fichiers.

## Gates techniques vérifiés

```text
OF-ARCH-001   VERIFIED_COMPLETE
OF-SOURCE-001 VERIFIED_COMPLETE
OF-ARCH-002   VERIFIED_COMPLETE
OF-ARCH-003   VERIFIED_COMPLETE
OF-ARCH-004   VERIFIED_COMPLETE
OF-DATA-001   VERIFIED_COMPLETE
OF-DATA-002   VERIFIED_COMPLETE
OF-DATA-003   VERIFIED_COMPLETE
```

## Interdictions permanentes

Ne pas travailler directement sur `main`, créer une branche/PR, force-push, fusionner ou retargeter une PR, déployer ou charger des données réelles sans une porte explicite. `COLLECTION_TESTED` ne signifie jamais `HISTORY_LOADED` et une définition de catalogue n’est jamais une observation.
