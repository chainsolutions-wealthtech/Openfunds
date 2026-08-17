# Prochaine action autorisée

```text
CURRENT_LOOP: OF-LOOP-SOURCE-002
CURRENT_TASK: OF-SOURCE-002_EN_COURS
LAST_VERIFIED_WAVE: 10
NEXT_UNIT: WAVE_11_EXCHANGE_ROLE_REVALIDATION + SERIES_ROLE_EVIDENCE_PLAN + ERITREA_PRIMARY_SOURCE_WATCH
STATUS: READY_FOR_READ_ONLY_AUDIT
WRITE_GATE: CURRENT_OFFICIAL_PRIMARY_EVIDENCE + COLLISION_REVIEW + CLOSED_ALLOWLIST + TDD_RED
```

## État courant vérifié — 17 août 2026

Les Waves 01 à 10 ont été exécutées sur la branche gouvernée existante, sans nouvelle branche, sans modification de `main` et sans déploiement de production.

```text
AFRICAN_COUNTRIES: 54
COUNTRY_COVERAGE: 53 / 54
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 1
UNCOVERED_COUNTRY: ERYTHREE
ORGANIZATIONS: 141 = 121 VALIDATED + 20 PENDING
ORGANIZATION_SCOPE_ROLES: 199 = 171 VALIDATED + 28 PENDING
```

Wave 10 a promu exactement 12 relations country-scoped déjà présentes, sans création ni retargeting, sous contrat TDD RED→GREEN et avec validation Python 3.11/3.12. Le rapport de clôture est `docs/00_PROJECT/OF_SOURCE_002_WAVE_10_COMPLETION_20260817.md`.

L'Érythrée reste volontairement absente : aucune organisation country-scoped ne doit être créée tant qu'une source primaire officielle actuelle n'est pas vérifiée.

## Audit effectif post-Wave10

Le workflow lecture seule `OF-SOURCE-002 Post-Wave10 Audit` a vérifié :

```text
MONETARY_AUTHORITY              11 pays sans groupe couvert
STATISTICS                       3 pays sans groupe couvert
CAPITAL_MARKET_REGULATION       18 pays sans groupe couvert
FUND_REGULATION                 19 pays sans groupe couvert
INSURANCE_PENSION_REGULATION    44 pays sans groupe couvert
EXCHANGE                        20 pays sans groupe couvert
FISCAL_DEBT                     40 pays sans groupe couvert
```

Les chiffres sont calculés à partir des rôles `VALIDATED` country-scoped **et** des rôles zonaux validés hérités ; ils ne doivent pas être lus comme un simple comptage d'organisations nationales.

## Inventaire exact des 28 PENDING

```text
FX_REFERENCE_RATE_PROVIDER   9
INDEX_PROVIDER               9
STOCK_EXCHANGE               3
MONETARY_UNION               3
SUPRANATIONAL_AUTHORITY      2
INTERBANK_MARKET_OPERATOR    2
TOTAL                       28

COUNTRY        17
MONETARY_ZONE  11
```

### Prochaine unité : Wave 11 — bourses encore PENDING

La prochaine unité est limitée aux trois relations institutionnelles simples suivantes :

```text
EGX / STOCK_EXCHANGE / EGYPTE
GSE / STOCK_EXCHANGE / GHANA
NGX / STOCK_EXCHANGE / NIGERIA
```

Avant toute promotion :

1. résoudre l'identité juridique et le domaine officiel actuel de chaque bourse ;
2. prouver directement sur une source primaire officielle que l'entité est bien l'opérateur de la bourse ;
3. vérifier que le code organisation existant désigne la bonne entité et non une société holding/groupe distincte ;
4. conserver toute ligne ambiguë `PENDING` ;
5. produire un audit Wave 11, une allowlist fermée et un test RED ;
6. ne modifier que `VALIDATION_STATUS` et `SOURCE_NOTE` des lignes prouvées ;
7. vérifier les contrats Waves 01→11 sur Python 3.11/3.12 avant commit.

### Rôles de séries — vagues séparées

Les 18 lignes suivantes ne doivent pas être promues par simple identité institutionnelle :

```text
FX_REFERENCE_RATE_PROVIDER   9
INDEX_PROVIDER               9
```

Pour `FX_REFERENCE_RATE_PROVIDER`, la preuve doit établir la publication/propriété de la série de référence FX pertinente. Pour `INDEX_PROVIDER`, la preuve doit établir la responsabilité de calcul/publication de l'indice, et pas seulement l'existence de la bourse.

### Rôles zonaux — revue sémantique séparée

```text
MONETARY_UNION            3
SUPRANATIONAL_AUTHORITY   2
INTERBANK_MARKET_OPERATOR 2
```

Ces rôles exigent une revue sémantique dédiée. En particulier, `CMA / MONETARY_UNION` ne doit pas être promu sans vérifier que la terminologie canonique `MONETARY_UNION` est bien adaptée à la Common Monetary Area et non seulement à un arrangement monétaire.

## Blockers institutionnels maintenus

```text
ERYTHREE            PRIMARY_OFFICIAL_SOURCE_NOT_VERIFIED
FMDQ                REQUIRES_ROLE_MODEL_REVIEW
SEC_ZAMBIA          CURRENT_OFFICIAL_DOMAIN_INTEGRITY_BLOCKER
IRA_URBRA_UGANDA    COMBINED_ROLE_MODEL_MISMATCH
RBM_FUND_REGULATOR  PRIMARY_CIS_PROOF_NOT_SUFFICIENT
```

## Taxonomie — gate structurel fermé

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

Cette clôture structurelle n'autorise pas l'activation de WTI, WTI Bench, benchmarks, RFR, MAR ou autres calculs sans leurs validations propres.

## Openfunds — gate réévalué

La version officielle vérifiée est `2.13.0`, publiée le `2026-03-23`, sous licence officielle `CC BY-ND 4.0` avec attribution. Le manifeste gouverné est :

```text
data/openfunds/source_manifest_v2.13.0.json
```

`OF-MAP-001` reste incomplet tant que le Field List officiel v2.13.0 n'est pas archivé **sans modification**, hashé SHA256 et parsé déterministement. Aucun catalogue reconstruit ou identifiant inventé n'est autorisé.

## Interdictions maintenues

Ne pas importer d'historique réel sans stockage durable, ne pas modifier ou fermer la PR nº2 sans réconciliation, ne pas fusionner/retargeter la PR nº1, ne pas travailler sur `main`, ne pas créer de branche/PR, ne pas activer WTI/WTI Bench et ne pas déployer sans satisfaction des gates correspondants.
