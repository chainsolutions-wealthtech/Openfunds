# Openfunds — point d’entrée obligatoire

```text
STATUS: ACTIVE
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
CURRENT_HEAD_POLICY: RESOLVE_DYNAMICALLY
LAST_GOVERNANCE_RECONCILIATION_DATE: 2026-09-10
LAST_GOVERNANCE_BASELINE_HEAD: eeaa07194fcb46fa0cf0859d5061a30ffc5602c0
PR_1: DRAFT / OPEN / UNMERGED
PRODUCTION_DEPLOYED: NO
```

## Finalité

Ce fichier est le premier document à lire pour toute intervention humaine, IA ou automatisée. Il ne remplace aucune autorité historique ou métier : il impose l’ordre de découverte du dépôt avant toute écriture et évite qu’une conversation devienne une source de vérité parallèle.

La mémoire canonique appartient au dépôt Git versionné. Toute valeur de HEAD, PR, CI ou état distant doit être résolue dynamiquement au moment de l’intervention.

## Lecture obligatoire

Lire, dans cet ordre, avant toute modification :

1. `00_START_HERE.md` ;
2. `GOVERNANCE.md` ;
3. `README.md` ;
4. `AGENTS.md` ;
5. `SOURCE_OF_TRUTH.md` ;
6. `STATUS.md` ;
7. `NEXT_ACTION.md` ;
8. `LOOP_STATE.md` ;
9. `CURRENT_ITERATION.md` ;
10. `LOOP_ENGINEERING.md` ;
11. `TODO.md` et `SUIVI.md` ;
12. `DECISIONS.md` et les ADR liés à la tâche ;
13. `WORK_LOG.md` et `HANDOFF.md` ;
14. `CHANGELOG.md` ;
15. le rapport de clôture ou de réconciliation le plus récent sous `docs/00_PROJECT/` ;
16. les spécifications, plans, schémas, tests et fichiers directement concernés par la tâche.

Les adaptateurs d’assistant (`CLAUDE.md`, instructions Copilot ou autres) ne créent aucune autorité concurrente : ils renvoient vers cette chaîne.

## Contrôle Git obligatoire avant écriture

1. confirmer le repository et la branche de contrôle ;
2. résoudre le HEAD distant courant ;
3. comparer ce HEAD au dernier état documenté ;
4. vérifier PR, commits récents, workflows et checks pertinents ;
5. identifier toute intervention concurrente sur les mêmes fichiers ;
6. établir une baseline explicite ;
7. arrêter l’écriture en cas de divergence non comprise.

Un ancien SHA présent dans un rapport daté reste une preuve historique et ne doit jamais être interprété comme le HEAD courant sans vérification.

## Contrôle d’impact obligatoire

Avant toute modification, déterminer les impacts possibles sur :

- modèle canonique et identifiants ;
- migrations et données ;
- mappings Openfunds ;
- sources et provenance ;
- API et contrats ;
- calculs et méthodologies ;
- tests et CI ;
- documentation et mémoire persistante ;
- compatibilité historique et production.

Toujours privilégier :

```text
REUTILISER
→ CORRIGER
→ RENFORCER
→ ETENDRE
→ MIGRER COMPATIBLEMENT
```

avant toute réécriture.

## Loop Engineering obligatoire

Toute intervention suit `LOOP_ENGINEERING.md` et possède, selon sa portée, une tâche `OF-*` ou un identifiant de boucle, une baseline, des critères d’acceptation, une analyse d’impact, des preuves de vérification, des conditions d’arrêt et une prochaine action déterministe.

## État de CI observé lors de la réconciliation du 2026-09-10

Le HEAD de baseline `eeaa07194fcb46fa0cf0859d5061a30ffc5602c0` est un commit documentaire. Le dernier run `OF-MAP-002 Mapping Registry` observé sur son parent `275ec7a10658cfc5a9f5822eb2315bf01138fc10` est `FAILURE` : l’intégration officielle/canonique passe, mais les jobs unitaires Python 3.11 et 3.12 échouent sur le contrat Batch 07 car `NO_PARENT_CURRENCY_INFERENCE` est attendu dans `NOTES` et absent de la ligne concernée. Ce défaut est un gap technique connu ; il ne doit pas être masqué par la migration documentaire.

La règle reste :

```text
IMPLEMENTED != REMOTELY_GREEN
```

## Interdictions permanentes

Sans porte explicite, ne pas :

- travailler directement sur `main` ;
- créer une nouvelle branche ou une nouvelle PR ;
- force-push ou réécrire l’historique ;
- retargeter, fusionner ou passer Ready la PR #1 ;
- déployer ou activer la production ;
- charger des données réelles ;
- supprimer un document ou un identifiant parce qu’il semble redondant ;
- affaiblir un test pour obtenir du vert ;
- inventer une preuve, une date, une source, un statut ou un résultat.

`COLLECTION_TESTED` ne signifie jamais `HISTORY_LOADED` et une définition de catalogue n’est jamais une observation.
