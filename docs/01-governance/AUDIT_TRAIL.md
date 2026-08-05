# Piste d’audit
```text
STATUS: ACTIVE
TIER: BUILD
INTEGRATION_ACTION: CREATE_CANONICAL
CANONICAL_AUTHORITY: docs/01-governance/AUDIT_TRAIL.md
TASK_ID: OF-DOC-003
LAST_VERIFIED: 2026-08-05
```

## Finalité

Définir quelles actions doivent laisser une preuve et sous quelle forme.

## À tracer

- Changements Git.
- Décisions.
- Migrations.
- Déploiements.
- Accès sensibles.
- Actions automatisées avec écriture.
- Modifications de configuration.
- Exceptions aux règles.

## Champs

Horodatage, acteur, cible, action, résultat, identifiant de tâche et preuve.

## Application à Openfunds

- respecter `SOURCE_OF_TRUTH.md` et les ADR acceptés ;
- résoudre le HEAD et les PR dynamiquement avant toute action ;
- conserver les statuts de maturité sans les surévaluer ;
- relier toute modification à une tâche `OF-*`, une preuve et un handoff ;
- ne pas modifier les chemins techniques pendant une boucle documentaire.

## Gouvernance du document

**Propriétaire fonctionnel :** gouvernance du projet, personne nominative à définir. **Lecteurs :** mainteneurs, data engineers, analystes, reviewers et assistants IA. **Mise à jour :** lors d’un changement de périmètre, de décision, de preuve, de risque ou de procédure concernée.

## Checklist

- [ ] source canonique et documents liés identifiés ;
- [ ] faits distingués des propositions ;
- [ ] preuves et dates renseignées ;
- [ ] risques, exceptions et prochaine action consignés ;
- [ ] aucun secret ni statut exagéré.
