# Itération courante

```text
LOOP_ID: OF-LOOP-DATA-001
ITERATION: 001
TASK_ID: OF-DATA-001
STATUS: IMPLEMENTATION_IN_PROGRESS
START_HEAD: e79c735b2cda8cc40a237b7deb3e379cc42bf1d9
TECHNICAL_HEAD: PENDING
DATE: 2026-08-05
```

## Hypothèse à tester

Les structures africaines ciblées peuvent être représentées par deux chemins
canoniques seulement : `FUND -> SHARE_CLASS` pour un fonds autonome et
`FUND -> SUBFUND -> SHARE_CLASS` pour un umbrella.

## Critères de sortie

- migration `015` gouvernée ;
- brouillon historique toujours exclu ;
- tests de cardinalité, identité, noms, identifiants et événements ;
- PostgreSQL 16 et adoption sans ledger réussis ;
- aucun historique de fonds ou déploiement production.
