# Prochaine action autorisée

```text
CURRENT_LOOP: OF-LOOP-SOURCE-002
CURRENT_TASK: OF-SOURCE-002_EN_COURS
LAST_VERIFIED_WAVE: 03
NEXT_WAVE: 04
STATUS: READY_FOR_READ_ONLY_AUDIT
WRITE_GATE: CURRENT_OFFICIAL_PRIMARY_EVIDENCE + COLLISION_REVIEW + CLOSED_ALLOWLIST
```

## Phase immédiate

Poursuivre la couverture institutionnelle des 54 pays sans confondre organisation connue, rôle supposé, endpoint identifié, endpoint vérifié et collecte testée.

Les trois premières vagues sont vérifiées. Le workflow `Institutional Registry` run `31595575537` est vert sur Python 3.11/3.12 avec 8/8 tests au HEAD de données vague 03 `5024a9767b1b9aecf8a6cd52d315ccfbf8384389`.

État courant :

```text
COUNTRY_COVERAGE: 18 / 54
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 36
ORGANIZATIONS: 87 = 67 VALIDATED + 20 PENDING
ORGANIZATION_SCOPE_ROLES: 134 = 90 VALIDATED + 44 PENDING
SOURCE_ENDPOINTS: 43 UNCHANGED
```

## Audit vague 04 obligatoire

1. résoudre dynamiquement le HEAD ;
2. sélectionner un lot contrôlé parmi les 36 pays encore sans organisation country-scoped ;
3. rechercher les institutions sur des sources officielles primaires actuelles uniquement ;
4. séparer `VERIFIED`, `SOURCE_IDENTIFIED`, `PENDING`, `NOT_PUBLISHED` et `NOT_APPLICABLE` ;
5. bloquer toute URL compromise, ambiguë ou historiquement détournée ;
6. vérifier toute collision de code avec `ORGANIZATIONS.csv` ;
7. ne pas déduire un rôle `FUND_REGULATOR` d'une simple compétence générale de marché ;
8. ne pas fusionner deux régulateurs distincts pour satisfaire artificiellement `INSURANCE_PENSION_REGULATOR` ;
9. produire une allowlist datée et fermée avant tout contrat TDD RED ;
10. seulement ensuite appliquer RED → organisations → rôles → GREEN.

## Blockers maintenus

```text
FMDQ               REQUIRES_ROLE_MODEL_REVIEW
SEC_ZAMBIA         CURRENT_OFFICIAL_DOMAIN_INTEGRITY_BLOCKER
IRA_URBRA_UGANDA   COMBINED_ROLE_MODEL_MISMATCH
RBM_FUND_REGULATOR PRIMARY_CIS_PROOF_NOT_SUFFICIENT
```

## Gate externe maintenu

`OF-MAP-001` reste bloqué tant qu’un catalogue Openfunds officiel, versionné, licencié et archivé n’est pas disponible. Aucun identifiant Openfunds ne doit être inventé.

## Interdictions maintenues

Ne pas importer d’historique réel, modifier la PR nº2, fusionner/retargeter la PR nº1, travailler sur `main`, créer branche/PR, activer WTI/WTI Bench ou déployer sans porte explicite.
