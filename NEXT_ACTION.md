# Prochaine action autorisée

```text
CURRENT_LOOP: OF-LOOP-SOURCE-002
CURRENT_TASK: OF-SOURCE-002_EN_COURS
LAST_VERIFIED_WAVE: 09
NEXT_UNIT: POST_WAVE09_ROLE_COVERAGE_AUDIT + PENDING_ROLE_PROMOTION + ERITREA_PRIMARY_SOURCE_WATCH
STATUS: READY_FOR_READ_ONLY_AUDIT
WRITE_GATE: CURRENT_OFFICIAL_PRIMARY_EVIDENCE + COLLISION_REVIEW + CLOSED_ALLOWLIST + TDD_RED
```

## État courant vérifié — 17 août 2026

Les Waves 01 à 09 ont été exécutées sur la branche gouvernée existante, sans nouvelle branche, sans modification de `main` et sans déploiement de production.

```text
AFRICAN_COUNTRIES: 54
COUNTRY_COVERAGE: 53 / 54
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 1
UNCOVERED_COUNTRY: ERYTHREE
ORGANIZATIONS: 141 = 121 VALIDATED + 20 PENDING
ORGANIZATION_SCOPE_ROLES: 199 = 159 VALIDATED + 40 PENDING
```

Les Waves 01 à 09 sont protégées par les contrats `tests/test_institutional_registry*.py` et les contrôles Python 3.11/3.12. Wave 09 a promu, sans duplication, les rôles zonaux existants `BCEAO/CENTRAL_BANK/UEMOA`, `BEAC/CENTRAL_BANK/CEMAC`, `BRVM/COMMON_STOCK_EXCHANGE/UEMOA` et `BVMAC/COMMON_STOCK_EXCHANGE/CEMAC`.

L'Érythrée reste volontairement absente : aucune organisation country-scoped ne doit être créée tant qu'une source primaire officielle actuelle n'est pas vérifiée.

## Prochaine phase de OF-SOURCE-002

La couverture `53/54` signifie qu'au moins une institution nationale est identifiée dans 53 pays ; elle ne signifie pas que tous les rôles institutionnels exigés sont complets.

La prochaine unité doit repartir d'un audit post-Wave09 reproductible de la couverture par rôle pour les 54 pays et leurs scopes de marché/monétaires :

1. recalculer exactement les groupes de rôles encore manquants après les promotions Wave 09 ;
2. inventorier les 40 relations `PENDING` restantes avant de créer toute nouvelle organisation ;
3. promouvoir d'abord les lignes existantes lorsqu'une source primaire officielle actuelle confirme exactement le rôle et le scope ;
4. préserver BCEAO, BEAC, AMF-UMOA, COSUMAF, UMOA-Titres, BRVM et BVMAC à leur scope zonal ;
5. distinguer rôle national absent, rôle zonal compétent, `NOT_APPLICABLE`, `NOT_PUBLISHED` et preuve insuffisante ;
6. ne jamais déduire `FUND_REGULATOR` d'une compétence générale de marché ;
7. ne jamais fusionner artificiellement assurance et pensions ;
8. produire une allowlist fermée et un test RED avant chaque promotion/ajout ;
9. conserver l'Érythrée en blocker tant que le gate primaire n'est pas satisfait.

## Blockers institutionnels maintenus

```text
ERYTHREE            PRIMARY_OFFICIAL_SOURCE_NOT_VERIFIED
FMDQ                REQUIRES_ROLE_MODEL_REVIEW
SEC_ZAMBIA          CURRENT_OFFICIAL_DOMAIN_INTEGRITY_BLOCKER
IRA_URBRA_UGANDA    COMBINED_ROLE_MODEL_MISMATCH
RBM_FUND_REGULATOR  PRIMARY_CIS_PROOF_NOT_SUFFICIENT
```

## Taxonomie — gate structurel fermé

La taxonomie V0.1 est désormais persistée par la migration gouvernée :

```text
017_CANONICAL_FUND_TAXONOMY_V0_1
ORDER: 170
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
POSTGRESQL_16: SUCCESS
FULL_CHAIN_001_TO_017: SUCCESS
SECOND_APPLY_IDEMPOTENCE: SUCCESS
CANONICAL_STATUS: STRUCTURE_PREFILLED
PRODUCTION_STATUS: NOT_ACTIVE
```

Cette clôture structurelle n'autorise pas l'activation de WTI, WTI Bench, benchmarks, RFR, MAR ou autres calculs sans leurs propres validations de sources, méthodologies et historiques.

## Openfunds — gate réévalué

Le blocage historique « version officielle et licence inconnues » est levé : la version officielle courante vérifiée est `2.13.0`, publiée le `2026-03-23`, et la licence officielle est `CC BY-ND 4.0` avec attribution.

Le manifeste gouverné est :

```text
data/openfunds/source_manifest_v2.13.0.json
```

`OF-MAP-001` reste incomplet tant que le Field List officiel v2.13.0 n'est pas archivé **sans modification**, hashé SHA256 et parsé déterministement. Aucun catalogue reconstruit ou identifiant inventé n'est autorisé.

## Interdictions maintenues

Ne pas importer d'historique réel sans stockage durable, ne pas modifier ou fermer la PR nº2 sans réconciliation, ne pas fusionner/retargeter la PR nº1, ne pas travailler sur `main`, ne pas créer de branche/PR, ne pas activer WTI/WTI Bench et ne pas déployer sans satisfaction des gates correspondants.
