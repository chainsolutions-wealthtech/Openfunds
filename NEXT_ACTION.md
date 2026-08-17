# Prochaine action autorisée

```text
CURRENT_LOOP: OF-MAP-002 + OF-LOOP-SOURCE-002
CURRENT_TASK: OF-MAP-002_EN_COURS / OF-SOURCE-002_EN_COURS
LAST_VERIFIED_WAVE: 12
NEXT_UNIT: OPENFUNDS_MAPPING_REGISTRY_BOOTSTRAP + FX_REFERENCE_SERIES_AUDIT + ERITREA_PRIMARY_SOURCE_WATCH
STATUS: READY_FOR_TDD_MAPPING_BOOTSTRAP_AND_READ_ONLY_FX_AUDIT
WRITE_GATE: VERIFIED_OF_ID + VERIFIED_CANONICAL_FIELD_ID + EXPLICIT_MAPPING_STATUS + CLOSED_ALLOWLIST + TDD_RED
```

## État courant vérifié — 17 août 2026

Le travail reste sur la branche gouvernée existante, sans nouvelle branche, sans modification de `main`, sans fusion/retargeting de la PR #1 et sans déploiement de production.

### Couverture institutionnelle

```text
AFRICAN_COUNTRIES: 54
COUNTRY_COVERAGE: 53 / 54
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 1
UNCOVERED_COUNTRY: ERYTHREE
ORGANIZATIONS: 141 = 121 VALIDATED + 20 PENDING
ORGANIZATION_SCOPE_ROLES: 199 = 178 VALIDATED + 21 PENDING
WAVES_VERIFIED: 01..12
PENDING_STOCK_EXCHANGE: 0
```

Inventaire résiduel exact :

```text
FX_REFERENCE_RATE_PROVIDER   9
INDEX_PROVIDER               5
MONETARY_UNION               3
SUPRANATIONAL_AUTHORITY      2
INTERBANK_MARKET_OPERATOR    2
TOTAL                       21

COUNTRY        12
MONETARY_ZONE   9
```

Wave 12 a promu seulement quatre `INDEX_PROVIDER` dont la responsabilité de calcul/gestion/publication d'indices était suffisamment prouvée : `GSE`, `CASABLANCA_BOURSE`, `BRVM` et `BVMAC`. `JSE`, `EGX`, `NSE`, `NGX` et `BVMT` restent volontairement `PENDING` tant que les responsabilités de provider/administrator ne sont pas suffisamment séparées.

Preuves :

```text
docs/00_PROJECT/OF_SOURCE_002_WAVE_12_INDEX_PROVIDER_AUDIT_20260817.md
docs/00_PROJECT/OF_SOURCE_002_WAVE_12_COMPLETION_20260817.md
```

L'Érythrée reste volontairement sans organisation country-scoped tant qu'une source primaire officielle actuelle n'est pas vérifiée.

## OF-MAP-001 — gate fermé

`OF-MAP-001` est maintenant `TERMINE`.

Source officielle archivée :

```text
data/openfunds/official/v2.13.0/openfunds_fields_v2.13.0.pdf
```

Invariants vérifiés :

```text
OPENFUNDS_VERSION: 2.13.0
DOCUMENT_STATUS: FINAL
DOCUMENT_DATE: 2026-03-23
PDF_PAGES: 745
PDF_BYTES: 2957096
SHA256: 40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4
FIELD_RECORDS: 1869
UNIQUE_OF_IDS: 1869
CONCRETE_IDS: 1849
PARAMETERIZED_COUNTRY_TEMPLATES_XX: 20
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
OFFICIAL_INVENTORY_RUN: 32061806859 SUCCESS
```

Le parser gouverné est :

```text
scripts/parse_openfunds_v2_13_0.py
```

Il vérifie obligatoirement le checksum avant extraction et n'écrit aucun catalogue officiel transformé dans le dépôt. Les templates `OFxx####XX` sont conservés exactement tels qu'ils existent dans le standard.

Preuves :

```text
docs/00_PROJECT/OF_MAP_001_OPENFUNDS_V2_13_0_OFFICIAL_ARCHIVE_COMPLETION_20260817.md
docs/00_PROJECT/OF_MAP_001_DETERMINISTIC_PARSE_COMPLETION_20260817.md
data/openfunds/source_manifest_v2.13.0.json
```

## OF-MAP-002 — unité active

Le prochain chantier Openfunds est le mapping versionné vers le modèle canonique.

### Architecture autorisée

Le registre de mapping doit rester **séparé du PDF officiel** et ne doit pas publier une réécriture du Field List sous forme de faux document officiel.

Chaque ligne mappée doit au minimum porter :

```text
MAPPING_ID
STANDARD_VERSION
EXTERNAL_FIELD_ID
CANONICAL_FIELD_ID
CANONICAL_ENTITY
MAPPING_STATUS
TRANSFORMATION_RULE
INFORMATION_LOSS
IMPORT_SUPPORTED
EXPORT_SUPPORTED
VALIDATION_STATUS
SOURCE_SHA256
SOURCE_REFERENCE
NOTES
```

### Invariants obligatoires

1. `STANDARD_VERSION` doit être `2.13.0` ;
2. tout `EXTERNAL_FIELD_ID` doit appartenir aux 1 869 OF-ID parsés depuis le PDF checksum-locké ;
3. aucun `OFxx####XX` ne peut être matérialisé en faux pays dans le registre source ;
4. toute cible `CANONICAL_FIELD_ID` doit exister dans `data/dictionary/spec_v1/` ;
5. une ligne peut rester `TO_CONFIRM` plutôt que forcer un mapping douteux ;
6. un mapping one-to-many/many-to-one doit être explicite ;
7. les pertes d'information et transformations doivent être déclarées ;
8. les mappings internes sont des métadonnées du projet, distinctes du document Openfunds officiel ;
9. aucun identifiant, type, définition ou cardinalité officiel ne doit être inventé ;
10. une CI doit reparser l'archive officielle et revalider toutes les références avant acceptation.

La première écriture autorisée est donc **le schéma/registre de mapping + son validateur + ses contrats**, pas une génération spéculative de 1 869 mappings.

## OF-SOURCE-002 — prochaine unité

### Wave 13 potentielle : FX_REFERENCE_RATE_PROVIDER

Les neuf lignes FX restantes doivent être vérifiées sur la publication/propriété de la série de change concernée, et non sur le simple statut de banque centrale.

Aucune promotion ne doit précéder :

```text
SOURCE PRIMAIRE OFFICIELLE ACTUELLE
+ SERIE FX IDENTIFIEE
+ ROLE/SCOPE EXACT
+ COLLISION REVIEW
+ CLOSED ALLOWLIST
+ TDD RED
```

Les cas seront traités par sous-vagues si la preuve n'est pas homogène.

### Rôles zonaux

```text
MONETARY_UNION             3
SUPRANATIONAL_AUTHORITY    2
INTERBANK_MARKET_OPERATOR  2
```

Ils restent dans une revue sémantique distincte. `CMA / MONETARY_UNION` ne doit pas être promu tant que le terme canonique n'est pas démontré comme adéquat à la Common Monetary Area.

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

## Blockers maintenus

```text
ERYTHREE            PRIMARY_OFFICIAL_SOURCE_NOT_VERIFIED
FMDQ                REQUIRES_ROLE_MODEL_REVIEW
SEC_ZAMBIA          CURRENT_OFFICIAL_DOMAIN_INTEGRITY_BLOCKER
IRA_URBRA_UGANDA    COMBINED_ROLE_MODEL_MISMATCH
RBM_FUND_REGULATOR  PRIMARY_CIS_PROOF_NOT_SUFFICIENT
```

## Interdictions maintenues

Ne pas importer d'historique réel sans stockage durable, ne pas modifier ou fermer la PR nº2 sans réconciliation, ne pas fusionner/retargeter la PR nº1, ne pas travailler sur `main`, ne pas créer de branche/PR, ne pas activer WTI/WTI Bench et ne pas déployer sans satisfaction des gates correspondants.
