# Prochaine action autorisée

```text
CURRENT_LOOP: OF-LOOP-ARCH-005_COMPLETED
STATUS: STOPPED_PENDING_USER_AUTHORIZATION
NEXT_CANDIDATE_TASK: OF-DATA-001
```

## Action candidate

Stabiliser le modèle `Fund / SubFund / ShareClass`, les structures sans compartiment, les identités/noms/alias et les événements de fusion ou transfert.

## Préconditions

- résoudre à nouveau le HEAD, les branches et les deux PR ;
- vérifier les rapports `OF-ARCH-005` et les workflows du HEAD technique ;
- définir exemples juridiques Maroc, Tunisie, Nigeria et cas de fonds sans compartiment ;
- approuver cardinalités, temporalité, provenance, migration et tests de non-duplication ;
- rechercher la collision de l’identifiant et créer une nouvelle boucle.

## Interdictions maintenues

Ne pas fusionner ou retargeter la PR nº 1, modifier la PR nº 2, travailler sur `main`, déployer ou charger des historiques avant autorisation explicite.
