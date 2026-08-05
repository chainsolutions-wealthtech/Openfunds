# Prochaine action autorisée

```text
CURRENT_LOOP: OF-LOOP-DATA-001
TASK_ID: OF-DATA-001
STATUS: TECHNICAL_COMMIT_AND_CI_PENDING
```

## Action immédiate

Créer un commit fast-forward sur la branche de contrôle avec la migration `015`,
le manifeste, `ADR-030`, les tests et les documents de boucle, puis attendre et
inspecter les workflows GitHub Actions.

## Décision conditionnelle

- CI verte : documenter la clôture et passer `OF-DATA-001` à
  `VERIFIED_COMPLETE` ;
- CI rouge : conserver les preuves, analyser les logs et corriger uniquement par
  un nouveau commit forward.

## Interdictions maintenues

Ne pas charger de fonds réels, commencer `OF-DATA-002`, modifier la PR nº 2,
retargeter ou fusionner la PR nº 1, travailler sur `main`, créer une branche ou
une PR, réécrire l’historique ou déployer.
