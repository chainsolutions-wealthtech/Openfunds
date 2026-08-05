# Gestion des changements
```text
STATUS: ACTIVE
TIER: BUILD
INTEGRATION_ACTION: CREATE_CANONICAL
CANONICAL_AUTHORITY: docs/01-governance/CHANGE_MANAGEMENT.md
TASK_ID: OF-DOC-003
LAST_VERIFIED: 2026-08-05
```

## Finalité

Classifier et contrôler les changements standards, normaux, urgents et critiques.

## Données minimales

Objectif, périmètre, risques, dépendances, tests, migration, rollback, fenêtre, responsable, validation et résultat.

## Urgence

Une urgence ne supprime jamais la traçabilité, les contrôles critiques ou le rollback.

## Application à Openfunds

- respecter `SOURCE_OF_TRUTH.md` et les ADR acceptés ;
- résoudre le HEAD et les PR dynamiquement avant toute action ;
- conserver les statuts de maturité sans les surévaluer ;
- relier toute modification à une tâche `OF-*`, une preuve et un handoff ;
- ne pas modifier les chemins techniques pendant une boucle documentaire.

## Gouvernance du document

**Propriétaire fonctionnel :** gouvernance du projet, personne nominative à définir. **Lecteurs :** mainteneurs, data engineers, analystes, reviewers et assistants IA.

## Checklist

- [ ] source canonique et documents liés identifiés ;
- [ ] faits distingués des propositions ;
- [ ] preuves et dates renseignées ;
- [ ] risques, exceptions et prochaine action consignés ;
- [ ] aucun secret ni statut exagéré.
