# Prochaine action autorisée

```text
CURRENT_LOOP: OF-LOOP-SOURCE-002
CURRENT_TASK: OF-SOURCE-002_EN_COURS
LAST_VERIFIED_WAVE: 01
NEXT_WAVE: 02
STATUS: READY_FOR_READ_ONLY_AUDIT
WRITE_GATE: OFFICIAL_PRIMARY_EVIDENCE + COLLISION_REVIEW + ALLOWLIST
```

## Phase immédiate

Poursuivre la couverture institutionnelle des 54 pays sans confondre organisation connue, rôle supposé, endpoint identifié, endpoint vérifié et collecte testée.

La vague 01 est vérifiée par le workflow `Institutional Registry` run `31592700354` sur Python 3.11/3.12. Elle a porté la couverture de 7 à 10 pays ayant au moins une organisation country-scoped. Il reste 44 pays sans organisation nationale dans le registre de découverte/revue.

## Audit vague 02 obligatoire

1. résoudre dynamiquement le HEAD ;
2. produire la liste exacte des 44 pays encore sans organisation country-scoped ;
3. mesurer, pour les 10 pays représentés, les rôles requis encore absents ou `PENDING` ;
4. rechercher les institutions sur des sources officielles primaires uniquement ;
5. séparer `VERIFIED`, `SOURCE_IDENTIFIED`, `PENDING`, `NOT_PUBLISHED` et `NOT_APPLICABLE` ;
6. vérifier toute collision de code avec `ORGANIZATIONS.csv` ;
7. garder les organisations de zone UEMOA/CEMAC au niveau zone ;
8. ne promouvoir aucune URL ou institution sans preuve officielle ;
9. produire une allowlist datée avant toute écriture de vague 02.

## Hors allowlist actuel

`FMDQ` reste `REQUIRES_ROLE_MODEL_REVIEW` : aucune écriture n’est autorisée avant arbitrage de son rôle canonique exact.

Aucun endpoint spécialisé, provider series, collection specification ou runtime SQL ne doit être ajouté pendant l’audit de vague 02.

## Gate externe maintenu

`OF-MAP-001` reste bloqué tant qu’un catalogue Openfunds officiel, versionné, licencié et archivé n’est pas disponible. Aucun identifiant Openfunds ne doit être inventé.

## Interdictions maintenues

Ne pas importer d’historique réel, modifier la PR nº2, fusionner/retargeter la PR nº1, travailler sur `main`, créer branche/PR, activer WTI/WTI Bench ou déployer sans porte explicite.
