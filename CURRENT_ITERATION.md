# Itération courante

```text
LOOP_ID: OF-LOOP-SOURCE-002
ITERATION: 002
TASK_ID: OF-SOURCE-002
STATUS: EN_COURS
DATE: 2026-08-12
WAVE_01_STATUS: VERIFIED_COMPLETE
WAVE_01_CI_RUN: 31592700354
CURRENT_WAVE: 02
CURRENT_MODE: READ_ONLY_AUDIT
```

## Hypothèse courante

Les institutions nécessaires à la couverture des 54 pays peuvent être intégrées progressivement sans inventer de rôles, sans confondre organisation, endpoint, série et collecte, et sans transformer un inventaire de découverte en vérité runtime PostgreSQL.

## Résultat de l’itération précédente

La vague 01 a ajouté 15 organisations et 22 relations de rôles officiellement prouvées pour Botswana, Namibie, Éthiopie, UEMOA et CEMAC. La couverture en pays possédant au moins une organisation nationale est passée de 7 à 10 sur 54.

La boucle TDD a été vérifiée : RED avant intégration, validateur exécutable ajouté, puis GREEN final sur Python 3.11/3.12 avec le workflow `Institutional Registry` run `31592700354`.

## Itération 002 — objectif

1. dresser la liste exacte des 44 pays sans organisation country-scoped ;
2. mesurer les rôles manquants des 10 pays déjà représentés ;
3. rechercher uniquement des sources officielles primaires ;
4. séparer `VERIFIED`, `SOURCE_IDENTIFIED`, `PENDING`, `NOT_PUBLISHED` et `NOT_APPLICABLE` ;
5. vérifier les collisions de codes ;
6. produire une allowlist avant toute nouvelle écriture.

## Interdictions

Aucun nouvel endpoint, provider series, historique, migration runtime, branche, PR, merge, retargeting ou déploiement n’est autorisé par cette itération read-only. `FMDQ` reste hors allowlist tant que son rôle canonique exact n’est pas arbitré.
