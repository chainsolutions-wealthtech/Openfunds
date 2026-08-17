# Prochaine action autorisée

```text
CURRENT_LOOP: OF-LOOP-SOURCE-002
CURRENT_TASK: OF-SOURCE-002_EN_COURS
LAST_VERIFIED_WAVE: 08
NEXT_UNIT: ROLE_COVERAGE_AUDIT + ERITREA_PRIMARY_SOURCE_WATCH
STATUS: READY_FOR_READ_ONLY_AUDIT
WRITE_GATE: CURRENT_OFFICIAL_PRIMARY_EVIDENCE + COLLISION_REVIEW + CLOSED_ALLOWLIST + TDD_RED
```

## État courant vérifié — 17 août 2026

Les Waves 04 à 08 ont été exécutées sur la branche gouvernée existante, sans nouvelle branche, sans modification de `main`, sans déploiement et sans persistance runtime.

```text
AFRICAN_COUNTRIES: 54
COUNTRY_COVERAGE: 53 / 54
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 1
UNCOVERED_COUNTRY: ERYTHREE
ORGANIZATIONS: 141 = 121 VALIDATED + 20 PENDING
ORGANIZATION_SCOPE_ROLES: 199 = 155 VALIDATED + 44 PENDING
```

La Wave 08 est protégée par le contrat `tests/test_institutional_registry_wave08.py`. Les Waves 01 à 08 sont vérifiées sur Python 3.11 et 3.12. L'Érythrée reste volontairement absente : aucune organisation ne doit être créée tant qu'une source primaire officielle actuelle n'est pas vérifiée.

## Prochaine phase de OF-SOURCE-002

La couverture `53/54` signifie qu'au moins une institution nationale est identifiée dans 53 pays ; elle ne signifie pas que tous les rôles institutionnels exigés sont complets.

La prochaine unité doit être un audit en lecture seule de la couverture par rôle pour les 54 pays et zones pertinentes :

1. mesurer exactement, par pays, les rôles présents et manquants ;
2. préserver BCEAO, BEAC, AMF-UMOA, COSUMAF, UMOA-Titres, BRVM et BVMAC à leur scope de zone ;
3. distinguer rôle national absent, rôle zonal compétent, `NOT_APPLICABLE`, `NOT_PUBLISHED` et preuve insuffisante ;
4. rechercher uniquement les lacunes prioritaires avec sources officielles primaires ;
5. ne jamais déduire `FUND_REGULATOR` d'une compétence générale de marché ;
6. ne jamais fusionner artificiellement assurance et pensions ;
7. produire une allowlist fermée avant chaque nouvelle écriture ;
8. conserver l'Érythrée en blocker tant que le gate primaire n'est pas satisfait.

## Blockers institutionnels maintenus

```text
ERYTHREE            PRIMARY_OFFICIAL_SOURCE_NOT_VERIFIED
FMDQ                REQUIRES_ROLE_MODEL_REVIEW
SEC_ZAMBIA          CURRENT_OFFICIAL_DOMAIN_INTEGRITY_BLOCKER
IRA_URBRA_UGANDA    COMBINED_ROLE_MODEL_MISMATCH
RBM_FUND_REGULATOR  PRIMARY_CIS_PROOF_NOT_SUFFICIENT
```

## Openfunds — gate réévalué

Le blocage historique « version officielle et licence inconnues » est levé : la version officielle courante vérifiée est `2.13.0`, publiée le `2026-03-23`, et la licence officielle est `CC BY-ND 4.0` avec attribution.

Le manifeste gouverné est :

```text
data/openfunds/source_manifest_v2.13.0.json
```

`OF-MAP-001` reste cependant incomplet tant que le Field List officiel v2.13.0 n'est pas archivé **sans modification**, hashé SHA256 et parsé déterministement. Aucun catalogue reconstruit ou identifiant inventé n'est autorisé.

## Interdictions maintenues

Ne pas importer d'historique réel sans stockage durable, ne pas modifier ou fermer la PR nº2 sans réconciliation, ne pas fusionner/retargeter la PR nº1, ne pas travailler sur `main`, ne pas créer de branche/PR, ne pas activer WTI/WTI Bench et ne pas déployer sans satisfaction des gates correspondants.
