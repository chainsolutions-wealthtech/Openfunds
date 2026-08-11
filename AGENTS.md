
# Règles communes pour tous les agents et assistants

```text
STATUS: ACTIVE
AUTHORITY: COMMON_AI_AND_HUMAN_ENTRY_POINT
TASK_POLICY: RESOLVE_FROM_STATUS_AND_NEXT_ACTION
LOOP_POLICY: RESOLVE_FROM_LOOP_STATE
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
BASELINE_END_SHA: 59f6475102b8a0c5b1274060afc412db787f2caf
```

## Ordre d’amorçage

Tout agent doit lire `00_START_HERE.md`, ce fichier, `SOURCE_OF_TRUTH.md`, `STATUS.md`, `NEXT_ACTION.md`, `TODO.md`, `SUIVI.md`, `DECISIONS.md`, puis les audits/rapports datés les plus récents avant de proposer une écriture.

## Vérification dynamique obligatoire

1. résoudre le HEAD courant de la branche de contrôle ;
2. vérifier la lignée depuis la baseline documentaire ;
3. inventorier les commits ajoutés depuis le dernier HEAD technique validé ;
4. vérifier les PR nº 1 et nº 2 avant toute opération les concernant ;
5. rechercher toute collision d’identifiant `OF-*` et `OF-LOOP-*` ;
6. arrêter en cas de divergence non comprise ou de modification concurrente.

## Branche et PR

- seule branche d’écriture autorisée sans nouvelle décision : `architecture/africafunds-country-indicators-v0.1` ;
- ne jamais travailler directement sur `main` ;
- ne créer aucune branche ou PR sans autorisation explicite ;
- ne pas modifier, fermer, fusionner ou retargeter la PR nº 2 ;
- ne pas fusionner ou retargeter la PR nº 1 ;
- commits fast-forward uniquement, sans réécriture d’historique.

## Non-régression métier

Préserver PostgreSQL comme vérité runtime, Openfunds comme couche de mapping, les couches raw/normalisé/validé/canonique/analytique/API/UI, la bitemporalité, la provenance, Fund/SubFund/ShareClass, identité/noms/alias, pays/région/zone de marché, XOF/XAF, native/EUR/USD, observé/calculé, catégorie/peers/WTI/benchmark/WTI Bench/RFR/MAR, `NULL != 0` et l’absence de date inventée.

## Frontières de statut

```text
STRUCTURE_PREFILLED != PRODUCTION_ACTIVE
NOT_ACTIVE != CALCULATED_PRODUCT_AVAILABLE
METHODOLOGY_TO_VALIDATE != VALIDATED_METHODOLOGY
COLLECTION_TESTED != HISTORY_LOADED
PROPOSED_SQL != PRODUCTION_MIGRATION
RESEARCH_CANDIDATE != CANONICAL_SOURCE
IMPLEMENTED != VERIFIED_COMPLETE
DEFINITION_PRESENT != OBSERVATION_AVAILABLE
TARGET_HISTORY != HISTORY_LOADED
```

## Preuves et transmission

Toute affirmation doit pointer vers un commit, diff, test, workflow, artefact, document daté ou état d’environnement observé. Mettre à jour `LOOP_STATE.md`, `CURRENT_ITERATION.md`, `WORK_LOG.md`, `NEXT_ACTION.md`, `STATUS.md` et `HANDOFF.md`. Le rapport final sépare fait, preuve, limite, risque, décision et prochaine action.
