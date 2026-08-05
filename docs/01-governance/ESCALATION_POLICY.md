# Politique d’escalade
```text
STATUS: CONDITIONAL_NOT_ACTIVE
TIER: CONDITIONAL
INTEGRATION_ACTION: CREATE_CONDITIONAL
TASK_ID: OF-DOC-003
LAST_VERIFIED: 2026-08-05
```

## Finalité

Définir les situations, niveaux et destinataires d’escalade.

| Niveau | Déclencheur | Délai | Destinataire | Action autorisée |
|---|---|---|---|---|
| E1 | ambiguïté documentaire | avant écriture | mainteneur | suspendre la modification |
| E2 | divergence Git ou conflit de preuve | immédiat | responsable du dépôt | geler les écritures |
| E3 | secret, perte de données ou risque production | immédiat | sécurité/mainteneur | arrêter, préserver les preuves, révoquer si nécessaire |

## Applicabilité actuelle

`CONDITIONAL_NOT_ACTIVE` pour une organisation formelle : les propriétaires nominatifs sont à définir. La procédure d’arrêt reste applicable.
