# Prochaine action autorisée

```text
CURRENT_LOOP: OF-LOOP-DATA-002_COMPLETED
CURRENT_TASK: OF-DATA-002_VERIFIED_COMPLETE
NEXT_CANDIDATE: OF-DATA-003
STATUS: STOPPED_PENDING_USER_AUTHORIZATION
```

## Phase candidate

Centraliser les définitions D00–D17 dans un catalogue machine-readable gouverné,
sans confondre définition, source identifiée, collecte testée, historique chargé
et produit analytique actif.

## Audit préalable obligatoire

1. résoudre dynamiquement le HEAD de la branche active ;
2. inventorier toutes les définitions D00–D17 déjà présentes ;
3. établir le nombre réel d’objets et les collisions de codes ;
4. distinguer `RAW`, `METADATA`, `EVENT` et `CALCULATED` ;
5. préserver les statuts de preuve existants ;
6. choisir une source d’authoring sans créer de registre concurrent ;
7. définir une allowlist avant toute écriture.

## Critères proposés

Chaque objet devra au minimum exposer : code, domaine, définition bilingue,
nature, fréquence, unité, devise, granularité, sources possibles, usages,
méthode de calcul le cas échéant, historique, provenance, statut et version.

## Interdictions maintenues

Ne pas commencer automatiquement `OF-DATA-003`, importer des données réelles,
modifier la PR nº 2, fusionner ou retargeter la PR nº 1, travailler sur `main`,
créer une branche/PR, activer des calculs ou déployer sans nouvelle autorisation.
