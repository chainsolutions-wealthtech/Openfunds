# Sources de vérité Openfunds

```text
STATUS: ACTIVE
OWNER: PROJECT_GOVERNANCE
LAST_VERIFIED: 2026-09-10
CURRENT_HEAD_POLICY: RESOLVE_DYNAMICALLY
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
```

## Principe directeur

La mémoire canonique du projet appartient au dépôt Git versionné et aux autorités explicitement désignées ci-dessous. Une conversation Claude, ChatGPT, Codex, Copilot, Gemini, Cursor, un résumé externe ou une mémoire d’agent ne constitue jamais une source de vérité du projet.

Les agents peuvent utiliser leur contexte pour retrouver le projet, mais ils doivent réconcilier ce contexte avec GitHub et les documents canoniques avant toute écriture.

## Hiérarchie d’autorité

| Sujet | Autorité | Rôle | Ne constitue pas |
|---|---|---|---|
| Point d’entrée | `00_START_HERE.md` | ordre obligatoire de découverte | spécification métier |
| Gouvernance | `GOVERNANCE.md`, `AGENTS.md`, décisions/ADR acceptées | règles d’intervention et autorisations | préférence locale d’un agent |
| État Git | GitHub sur la branche de contrôle résolue dynamiquement | HEAD, commits, arbres, PR, workflows et checks | SHA historique non revérifié |
| État courant | `STATUS.md` | photographie opérationnelle actuelle | historique complet |
| Prochaine action | `NEXT_ACTION.md` | unité de reprise autorisée | backlog complet |
| Boucle active | `LOOP_STATE.md`, `CURRENT_ITERATION.md`, `LOOP_ENGINEERING.md` | état, méthode et critères de boucle | conversation en cours |
| Tâches | `TODO.md` | identifiants, statuts, dépendances et critères | simple commentaire |
| Continuité | `SUIVI.md`, `WORK_LOG.md`, `HANDOFF.md` | historique, preuves et reprise | état runtime |
| Changements livrés | `CHANGELOG.md` + Git | évolution versionnée | intention non implémentée |
| Décisions | `DECISIONS.md` et ADR acceptés | décisions structurantes et justification | proposition non acceptée |
| Architecture | `ARCHITECTURE.md`, ADR et spécifications gouvernées | modèle cible et contraintes | code isolé non réconcilié |
| Fund core dictionary | `data/dictionary/spec_v1/` | authoring des 143 champs physiques `fund.*` | catalogue D00–D17 |
| Extensions canoniques | paquets gouvernés sous `data/dictionary/extensions/` + migrations correspondantes | extension additive du canonique | réécriture du core |
| D00–D17 | `data/indicator_catalog/v1/` | authoring des 420 définitions pays-indicateurs | preuve de collecte/historique |
| Markdown D00–D17 historiques | `docs/04_DATA_GOVERNANCE/indicator_catalog/` | bootstrap et audit de fidélité | source d’authoring après bootstrap |
| SQL D00–D17 | migration générée/frozen correspondante | représentation runtime versionnée | source d’authoring |
| Migrations | `migrations/manifest.json` + ledger runtime | ordre et intégrité d’application | autorisation de production |
| Mapping Openfunds | `data/openfunds/mapping/v2.13.0/MAPPING_REGISTRY.csv` + manifeste/validateurs gouvernés | mappings réellement revus | catalogue artificiel d’IDs non revus |
| Review outcomes Openfunds | `data/openfunds/mapping/v2.13.0/REVIEW_OUTCOMES.csv` + validateur | décisions sparse non mappées/gated/deferred/à confirmer | mapping canonique implicite |
| Pilotes FX validés | `data/reference/VALIDATED_FX_REFERENCE_REGISTRY.csv` | authoring compact des pilotes validés | historique complet |
| PostgreSQL | vérité runtime après migration vérifiée | état appliqué | vérité d’authoring Git |
| `research_queue` | recherche non canonique | candidats et preuves | source canonique |
| Openfunds officiel | archive/version/checksum gouvernés | standard externe d’échange | schéma physique interne |
| Artefacts bruts | stockage immuable par SHA-256 lorsqu’il est configuré | preuve source | valeur canonique validée |

## Règle de conflit

En cas de contradiction :

1. ne pas choisir automatiquement la valeur la plus récente en apparence ;
2. ne jamais privilégier la mémoire d’un assistant sur une autorité du dépôt ;
3. conserver toutes les preuves ;
4. identifier l’autorité propriétaire du sujet ;
5. ouvrir ou compléter une décision tracée lorsque la contradiction est structurante ;
6. réconcilier les documents d’état sans réécrire l’histoire.

Un snapshot historique reste historique. L’état courant doit être placé dans une section explicitement plus récente plutôt que d’effacer les anciennes preuves.

## État vérifié lors de la réconciliation du 2026-09-10

La baseline Git observée avant la migration de gouvernance est :

```text
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
BASELINE_HEAD: eeaa07194fcb46fa0cf0859d5061a30ffc5602c0
PR_1: DRAFT / OPEN / UNMERGED
RULESETS: NONE_OBSERVED
PRODUCTION_DEPLOYED: NO
```

Le dernier run `OF-MAP-002 Mapping Registry` observé sur le parent `275ec7a10658cfc5a9f5822eb2315bf01138fc10` est rouge : le job d’intégration officielle/canonique passe, tandis que les jobs unitaires Python 3.11/3.12 échouent sur le contrat Batch 07 relatif à `NO_PARENT_CURRENCY_INFERENCE`. Le HEAD documentaire `eeaa0719…` ne doit donc pas être présenté comme récemment GREEN.

Les états fonctionnels et compteurs produit les plus récents restent sous l’autorité de `STATUS.md` et `NEXT_ACTION.md` après réconciliation ; ce fichier n’a pas vocation à recopier leurs compteurs.

## Règles d’évolution d’une autorité

Toute évolution structurante d’une source de vérité exige :

- analyse d’impact ;
- décision/ADR lorsque nécessaire ;
- tâche ou boucle identifiable ;
- vérification de non-régression ;
- mise à jour des documents de continuité concernés ;
- vérification du HEAD distant après écriture.

Créer une nouvelle représentation concurrente est interdit lorsqu’une autorité existante peut être étendue ou adaptée.
