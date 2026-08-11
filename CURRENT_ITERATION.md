
# Itération courante

```text
LOOP_ID: OF-LOOP-DATA-003
ITERATION: 001
TASK_ID: OF-DATA-003
STATUS: VERIFIED_COMPLETE
START_HEAD: 145461e04ba9affd2b11fedaf56ed4ad49171b5d
VALIDATED_TECHNICAL_HEAD: 0777afffad950e779234ef09f3f2b9031ec41ce7
DATE: 2026-08-11
```

## Hypothèse et verdict

**Hypothèse :** les 420 définitions D00–D17 peuvent être centralisées sans réécrire leurs sources, inventer les champs absents ni transformer des exigences de couverture en historiques chargés.

**Verdict : confirmé.** Un paquet JSON gouverné unique développe 18 domaines / 420 codes, conserve la provenance legacy, sépare `source_nature` de `canonical_nature`, génère quatre vues déterministes et alimente une migration additive testée sur PostgreSQL 16.

## Corrections de boucle

- TDD RED/GREEN pour le parseur, le paquet authoring, la classification, les sorties et la migration ;
- correction de la mutation CI du paquet d’authoring avant gel du manifeste ;
- correction d’un test funds qui supposait à tort que la migration `015` devait être la dernière migration globale ;
- aucun force-push ni réécriture d’historique.

## Limite

Cette itération ne charge aucune donnée réelle et ne valide ni disponibilité pays, ni historique complet, ni mapping Openfunds, ni calcul actif, ni production.
