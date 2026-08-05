# Itération courante

```text
LOOP_ID: OF-LOOP-DATA-001
ITERATION: 001
TASK_ID: OF-DATA-001
STATUS: VERIFIED_COMPLETE
START_HEAD: e79c735b2cda8cc40a237b7deb3e379cc42bf1d9
VALIDATED_TECHNICAL_HEAD: 8ab1e75b2fd94566f9c0538ca33460140787c6bf
DATE: 2026-08-05
```

## Hypothèse et verdict

**Hypothèse :** fonds autonomes et umbrellas peuvent partager une identité
canonique sans imposer un compartiment fictif.

**Verdict : confirmé.** Les deux chemins structurels, les versions, noms,
identifiants et événements sont appliqués et testés dans PostgreSQL 16.

## Limite

Cette itération ne peuple pas le dictionnaire, n’importe aucun historique de
fonds et ne configure aucun environnement de production.
