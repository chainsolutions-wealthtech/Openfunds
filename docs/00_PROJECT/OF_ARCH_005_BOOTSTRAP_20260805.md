# OF-ARCH-005 — Bootstrap de gel de la migration 012

```text
TASK: OF-ARCH-005
LOOP: OF-LOOP-ARCH-005
STATUS: BOOTSTRAP_IN_PROGRESS
START_HEAD: d81f78942c18f4f908da8e8500f83d1280eea570
DATE: 2026-08-05
```

Cette étape intermédiaire versionne le générateur en mode de vérification,
le snapshot d’authoring historique de `012` et un workflow ponctuel qui matérialise
puis committe exactement l’artefact SQL généré sur la branche autorisée.

Le workflow ponctuel sera transformé en garde de lecture seule après création de
l’artefact. Aucun déploiement, merge, retargeting ou démarrage de `OF-DATA-001`
n’est autorisé.
