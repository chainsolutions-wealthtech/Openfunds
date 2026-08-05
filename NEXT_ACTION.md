# Prochaine action autorisée

```text
TASK_ID: TO_BE_AUTHORIZED
CURRENT_LOOP: OF-LOOP-DOC-003_COMPLETED
STATUS: STOPPED_PENDING_USER_AUTHORIZATION
```

## Action candidate

Résoudre dans une phase technique séparée le blocker de gouvernance de `OF-ARCH-004` : figer la migration générée `012`, transformer la génération historique en contrôle de reproductibilité et imposer une nouvelle migration forward pour toute évolution.

## Préconditions

Nouvel identifiant de tâche libre, audit du HEAD, allowlist technique, ADR actualisé, tests du runner, verrouillage/concurrence évalués et CI PostgreSQL 16.

## Interdictions maintenues

Ne pas commencer `OF-DATA-001`, retargeter ou fusionner la PR nº 1, modifier la PR nº 2, travailler sur `main` ou déployer sans autorisation explicite.
