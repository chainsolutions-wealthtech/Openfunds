# Règles communes pour tous les agents et assistants

```text
STATUS: ACTIVE
AUTHORITY: COMMON_AI_AND_HUMAN_ENTRY_POINT
TASK_ID: OF-DOC-003
LOOP_ID: OF-LOOP-DOC-003
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
BASELINE_END_SHA: 59f6475102b8a0c5b1274060afc412db787f2caf
```

## Ordre d’amorçage

Tout agent doit lire `00_START_HERE.md`, ce fichier, `SOURCE_OF_TRUTH.md`,
`STATUS.md`, `NEXT_ACTION.md`, `TODO.md`, `SUIVI.md`, `DECISIONS.md`, puis les
audits datés les plus récents avant de proposer une écriture.

## Vérification dynamique obligatoire

1. résoudre le HEAD courant de `architecture/africafunds-country-indicators-v0.1` ;
2. vérifier que `59f6475102b8a0c5b1274060afc412db787f2caf` est toujours ancêtre ;
3. inventorier tous les commits ajoutés après la baseline ;
4. vérifier les douze branches et les PR nº 1 et nº 2 ;
5. rechercher toute collision d’identifiant `OF-*` et `OF-LOOP-*` ;
6. arrêter en cas de divergence non comprise ou de modification concurrente.

## Branche et PR

- seule branche d’écriture autorisée pour la boucle actuelle : `architecture/africafunds-country-indicators-v0.1` ;
- ne jamais travailler directement sur `main` ;
- ne créer aucune branche ou PR sans autorisation explicite ;
- ne pas modifier, fermer, fusionner ou retargeter la PR nº 2 ;
- ne pas fusionner ou retargeter la PR nº 1 ;
- commits fast-forward uniquement, sans réécriture d’historique.

## Non-régression métier

Préserver PostgreSQL comme vérité runtime, openfunds comme couche de mapping,
les couches raw/normalisé/validé/canonique/analytique/API/UI, la bitemporalité,
la provenance, la séparation Fund/SubFund/ShareClass, identité/noms/alias,
pays/région/zone de marché, XOF/XAF, native/EUR/USD, observé/calculé,
catégorie/peers/WTI/benchmark/WTI Bench/RFR/MAR, `NULL != 0` et l’absence de
date inventée.

## Frontières de statut

```text
STRUCTURE_PREFILLED != PRODUCTION_ACTIVE
NOT_ACTIVE != CALCULATED_PRODUCT_AVAILABLE
METHODOLOGY_TO_VALIDATE != VALIDATED_METHODOLOGY
COLLECTION_TESTED != HISTORY_LOADED
PROPOSED_SQL != PRODUCTION_MIGRATION
RESEARCH_CANDIDATE != CANONICAL_SOURCE
IMPLEMENTED != VERIFIED_COMPLETE
```

## Preuves

Toute affirmation doit pointer vers un commit, un diff, un test, un workflow,
un artefact, un document daté ou un état d’environnement réellement observé.
Ne jamais déclarer un contrôle réussi s’il n’a pas été exécuté.

## Transmission

Mettre à jour `LOOP_STATE.md`, `CURRENT_ITERATION.md`, `WORK_LOG.md`,
`NEXT_ACTION.md`, `STATUS.md` et `HANDOFF.md`. Le rapport final doit séparer
fait, preuve, limite, risque, décision et prochaine action.
