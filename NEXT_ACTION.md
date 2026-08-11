
# Prochaine action autorisée

```text
CURRENT_LOOP: OF-LOOP-DATA-003_COMPLETED
CURRENT_TASK: OF-DATA-003_VERIFIED_COMPLETE
NEXT_CANDIDATE: OF-SOURCE-002
STATUS: READY_FOR_READ_ONLY_AUDIT
WRITE_GATE: VERIFY_COVERAGE_AND_EVIDENCE_FIRST
```

## Phase candidate

Compléter les institutions des 54 pays sans confondre organisation connue, rôle supposé, endpoint identifié, endpoint vérifié et collecte testée.

## Audit préalable obligatoire

1. résoudre dynamiquement le HEAD ;
2. inventorier les 54 pays et les rôles institutionnels attendus ;
3. comparer `ORGANIZATIONS`, `ORGANIZATION_SCOPE_ROLES`, `SOURCE_ENDPOINTS` et les mappings ;
4. mesurer la couverture par pays et rôle ;
5. séparer `VERIFIED`, `SOURCE_IDENTIFIED`, `PENDING`, `NOT_PUBLISHED` et `NOT_APPLICABLE` ;
6. ne promouvoir aucune URL ou institution sans preuve officielle ;
7. définir une allowlist avant toute écriture.

## Gate externe maintenu

`OF-MAP-001` reste bloqué tant qu’un catalogue Openfunds officiel, versionné, licencié et archivé n’est pas disponible. Aucun identifiant Openfunds ne doit être inventé.

## Interdictions maintenues

Ne pas importer d’historique réel, modifier la PR nº 2, fusionner/retargeter la PR nº 1, travailler sur `main`, créer branche/PR, activer WTI/WTI Bench ou déployer sans porte explicite.
