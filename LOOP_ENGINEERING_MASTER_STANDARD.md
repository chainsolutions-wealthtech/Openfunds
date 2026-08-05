# Standard maître de Loop Engineering pour tout nouveau projet

## 1. Finalité

Ce standard transforme un projet en système d’ingénierie itératif, vérifiable,
auto-correcteur et transmissible. Il est indépendant d’un secteur, d’une entreprise,
d’un langage, d’une plateforme et d’une IA particulière.

Le kit comprend **176 fichiers Markdown** :

- **40 fichiers CORE**, obligatoires dès le premier commit ;
- **76 fichiers BUILD**, obligatoires avant un développement significatif ;
- **11 fichiers PRODUCTION**, obligatoires avant une mise en production ;
- **38 fichiers CONDITIONNELS**, activés selon la nature du projet ;
- **11 modèles ou fichiers de support**.

Tous les fichiers peuvent être présents dès le premier commit, mais seuls les fichiers `CORE` doivent être renseignés immédiatement. Les autres sont activés lorsqu’ils deviennent applicables, afin d’éviter une documentation vide ou bureaucratique.

## 2. Principe fondamental

La mémoire du projet ne réside pas dans une conversation, une branche, un agent,
un ordinateur ou une personne. Elle réside dans les documents canoniques,
les décisions ADR, l’historique Git, les tests, les preuves et l’état vérifié
des environnements.

## 3. Boucle universelle

Observer → Comprendre → Formuler une hypothèse → Planifier →
Exécuter un petit changement → Tester → Comparer → Corriger ou annuler →
Documenter → Transmettre → Définir la prochaine action → Reboucler.

## 4. Documents de reprise immédiate

Toute reprise doit être possible en lisant :

1. `00_START_HERE.md`
2. `SOURCE_OF_TRUTH.md`
3. `PROJECT_CONTEXT.md`
4. `LOOP_ENGINEERING.md`
5. `LOOP_CONTRACT.md`
6. `LOOP_STATE.md`
7. `CURRENT_ITERATION.md`
8. `NEXT_ACTION.md`
9. `STATUS.md`
10. `HANDOFF.md`

## 5. Règles Git

- Une tâche cohérente ne possède qu’une seule branche active.
- La branche appartient à la tâche, jamais à l’IA ou à la conversation.
- Toute création de branche est précédée d’une recherche des branches et PR existantes.
- La branche principale est protégée.
- Aucun push direct.
- Aucun force-push ou effacement destructif non approuvé.
- Toute branche fusionnée est supprimée.
- Toute branche active apparaît dans `STATUS.md`.

## 6. Règles de preuve

Une action n’est pas considérée terminée sans preuve adaptée :

- test ;
- sortie de commande ;
- commit ;
- PR ;
- comparaison ;
- capture ;
- métrique ;
- log ;
- health check ;
- vérification de données ;
- approbation documentée.

## 7. Non-régression

Avant toute modification, établir le comportement existant et les contrats.
Après modification, exécuter les contrôles ciblés et globaux applicables.
Toute correction de bug ajoute un test de reproduction.
Toute opération risquée possède un rollback.

## 8. Coordination des IA

Toutes les IA lisent les mêmes documents canoniques.
Leurs droits peuvent différer, mais leur contexte et leurs règles ne divergent pas.
Les fichiers spécifiques à un outil restent courts et renvoient vers `AGENTS.md`.

## 9. Fin de boucle

À la fin de toute session, mettre à jour :

- `LOOP_STATE.md`
- `CURRENT_ITERATION.md`
- `STATUS.md`
- `WORK_LOG.md`
- `NEXT_ACTION.md`
- `HANDOFF.md`

Puis, selon les événements :

- `TODO.md`
- `DECISIONS.md`
- `RISKS.md`
- `LESSONS_LEARNED.md`
- `CHANGELOG.md`
- la documentation technique ;
- l’état de production.

## 10. Critère de maturité

Un nouvel intervenant doit pouvoir déterminer sans supposition :

- ce que le projet cherche à accomplir ;
- ce qui est inclus et exclu ;
- l’état réel ;
- la branche et le commit courants ;
- la tâche et l’itération actives ;
- les décisions déjà prises ;
- les tests requis ;
- les risques et blocages ;
- le résultat attendu ;
- la preuve attendue ;
- la prochaine action exacte ;
- le rollback applicable.


## Adaptation Openfunds

Ce standard est appliqué par `AGENTS.md`, `LOOP_CONTRACT.md` et les registres de `docs/09-loop/`. Les sources canoniques historiques du dépôt restent prioritaires selon `SOURCE_OF_TRUTH.md`.
