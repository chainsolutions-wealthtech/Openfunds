# Definition of Done — Openfunds

## Objet

Cette définition complète `GOVERNANCE.md` et `LOOP_ENGINEERING.md`. Elle ne remplace ni les critères d’acceptation métier des tâches `OF-*`, ni les ADR, ni les tests spécifiques.

Une tâche n’est pas terminée parce qu’un fichier a été créé, qu’un commit existe ou qu’un test isolé passe. Le niveau déclaré doit rester inférieur ou égal au niveau réellement prouvé.

## Critères obligatoires

Une unité de travail peut être déclarée terminée uniquement lorsque les critères applicables ci-dessous sont satisfaits ou qu’une exception explicitement documentée indique pourquoi un critère n’est pas applicable.

### 1. Autorité et périmètre

- repository et branche autorisés confirmés ;
- HEAD de départ enregistré ;
- tâche, boucle ou décision propriétaire identifiée ;
- périmètre et critères d’acceptation explicites ;
- gates humains/externes identifiés.

### 2. Lecture et analyse

- documents d’autorité lus avant écriture ;
- architecture et implémentation existantes comprises ;
- consommateurs/dépendances pertinents identifiés ;
- analyse d’impact réalisée ;
- aucune autorité parallèle inutile créée.

### 3. Implémentation compatible

- priorité donnée à la réutilisation et à l’extension de l’existant ;
- identifiants, données et contrats historiques préservés ou migrés explicitement ;
- aucune suppression/destruction implicite ;
- secrets absents du dépôt ;
- aucune règle métier, date, valeur, source ou preuve inventée.

### 4. Vérification

- tests pertinents exécutés ;
- CI pertinente observée lorsqu’elle est disponible ;
- génération/migration/validation déterministe contrôlée lorsque concernée ;
- erreurs préexistantes distinguées des régressions introduites ;
- aucun test supprimé ou affaibli uniquement pour obtenir du vert.

### 5. Non-régression

- comportement hors périmètre inchangé ou changement justifié ;
- compatibilité historique vérifiée ;
- identifiants stables conservés ;
- sources de vérité conservées ;
- données et provenance non perdues ;
- limites et blockers conservés honnêtement.

### 6. Documentation et mémoire persistante

Les autorités réellement concernées sont synchronisées parmi :

- `STATUS.md` ;
- `TODO.md` ;
- `SUIVI.md` ;
- `NEXT_ACTION.md` ;
- `LOOP_STATE.md` ;
- `CURRENT_ITERATION.md` ;
- `WORK_LOG.md` ;
- `HANDOFF.md` ;
- `CHANGELOG.md` ;
- `DECISIONS.md` / ADR ;
- architecture, spécifications, dictionnaires, mappings et documentation d’exploitation.

Une ancienne section historique n’est pas réécrite pour paraître actuelle : une réconciliation datée la supersède explicitement.

### 7. Git distant

- commit(s) attendu(s) créé(s) sur la branche autorisée ;
- force-push et réécriture d’historique absents ;
- HEAD distant final résolu ;
- fichiers modifiés comparés au périmètre attendu ;
- PR/branche/merge/retargeting inchangés sauf autorisation explicite ;
- état CI post-écriture rapporté exactement (`SUCCESS`, `FAILURE`, `PENDING`, non déclenché ou non observable).

### 8. Handoff

- résultat obtenu explicitement décrit ;
- preuves et limitations identifiées ;
- blockers encore ouverts identifiés ;
- prochaine action unique et déterministe ;
- aucune dépendance à la mémoire de la conversation pour reprendre.

## Interdictions de clôture

Une tâche ne peut pas être déclarée `TERMINE`, `VERIFIED_COMPLETE`, `GREEN`, `DEPLOYED`, `VALIDATED_FOR_PUBLICATION`, `HISTORY_LOADED` ou équivalent lorsque la preuve correspondante n’existe pas.

En particulier :

```text
IMPLEMENTED != REMOTELY_GREEN
COLLECTION_TESTED != HISTORY_LOADED
STRUCTURE_PRESENT != PRODUCTION_ACTIVE
COMMIT_CREATED != LOOP_VERIFIED
```

## Verdict de boucle

Une boucle se clôt par l’un des verdicts suivants :

```text
VERIFIED_COMPLETE
COMPLETE_WITH_EXTERNAL_GAPS
PARTIALLY_COMPLETE
BLOCKED
FAILED_REGRESSION
```

`VERIFIED_COMPLETE` exige que tous les critères applicables soient satisfaits et que l’état distant final ait été vérifié.
