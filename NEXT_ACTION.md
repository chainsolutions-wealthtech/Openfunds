# Prochaine action autorisée

```text
CURRENT_LOOP: OF-MAP-002 + OF-LOOP-SOURCE-002
CURRENT_TASK: OF-MAP-002_EN_COURS / OF-SOURCE-002_EN_COURS
LAST_VERIFIED_WAVE: 13
NEXT_UNIT: OPENFUNDS_MAPPING_BATCH_02 + RESIDUAL_INDEX_PROVIDER_AUDIT + ZONE_ROLE_SEMANTIC_REVIEW + ERITREA_PRIMARY_SOURCE_WATCH
STATUS: READY_FOR_INCREMENTAL_MAPPING_AND_READ_ONLY_RESIDUAL_SEMANTIC_AUDITS
WRITE_GATE: VERIFIED_OF_ID + VERIFIED_CANONICAL_FIELD_ID + EXPLICIT_TRANSFORMATION + CLOSED_ALLOWLIST + TDD_RED
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
ORGANIZATION_SCOPE_ROLES: 199 = 187 VALIDATED + 12 PENDING
WAVES_VERIFIED: 01..13
PENDING_FX_REFERENCE_RATE_PROVIDER: 0
PENDING_STOCK_EXCHANGE: 0
```

Inventaire résiduel exact :

```text
INDEX_PROVIDER               5
MONETARY_UNION               3
SUPRANATIONAL_AUTHORITY      2
INTERBANK_MARKET_OPERATOR    2
TOTAL                       12
```

Wave 13 a promu exactement les neuf relations `FX_REFERENCE_RATE_PROVIDER` préexistantes après preuve primaire officielle de publication de taux/cours FX. Cette promotion ne valide pas automatiquement endpoints, séries, fréquences, unités ou historiques ; ceux-ci restent sous `OF-SOURCE-003`.

Preuves :

```text
docs/00_PROJECT/OF_SOURCE_002_WAVE_13_FX_REFERENCE_PROVIDER_AUDIT_20260817.md
docs/00_PROJECT/OF_SOURCE_002_WAVE_13_COMPLETION_20260817.md
RED_RUN: 32065421538
GREEN_RUN: 32065501479
```

L'Érythrée reste volontairement sans organisation country-scoped tant qu'une source primaire officielle actuelle n'est pas vérifiée.

## OF-MAP-001 — gate fermé

`OF-MAP-001` est `TERMINE`.

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
```

Source et parser :

```text
data/openfunds/official/v2.13.0/openfunds_fields_v2.13.0.pdf
scripts/parse_openfunds_v2_13_0.py
```

## OF-MAP-002 — unité active

Le registre gouverné existe et son validator est GREEN contre le vrai PDF officiel et les 143 FIELD_ID canoniques.

```text
REGISTRY: data/openfunds/mapping/v2.13.0/MAPPING_REGISTRY.csv
MANIFEST: data/openfunds/mapping/v2.13.0/mapping_manifest.json
VALIDATOR: scripts/validate_openfunds_mapping_registry.py
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
EMPTY_BASELINE_GREEN_RUN: 32064814922
HARDENED_VALIDATOR_GREEN_RUN: 32065124602
```

Invariants supplémentaires désormais imposés :

- doublon `(EXTERNAL_FIELD_ID, CANONICAL_FIELD_ID)` interdit ;
- `CANONICAL_ENTITY` doit correspondre à l'`ENTITY_CODE` réel du FIELD_ID ;
- les templates `XX` restent non développés ;
- le validator ne modifie pas le checkout.

### Batch 01 — fermé

Le premier lot réel est validé :

```text
REVIEWED_MAPPING_ROWS: 4
MAPPED_EXTERNAL_IDS: 2
UNMAPPED_EXTERNAL_IDS: 1867
MAPPED_CANONICAL_IDS: 4
GREEN_RUN: 32065216172
```

OF-ID traités :

```text
OFST010010  Fund Domicile Alpha-2
OFST020000  ISIN
```

Le domicile est transformé `ISO_3166_ALPHA2_TO_REF_GEOGRAPHY_UUID`. L'ISIN est décomposé one-to-many vers valeur, schéma `ISIN` et valeur normalisée de l'entité canonique d'identifiants.

Preuves :

```text
docs/00_PROJECT/OF_MAP_002_BATCH_01_DOMICILE_ISIN_AUDIT_20260817.md
docs/00_PROJECT/OF_MAP_002_BATCH_01_COMPLETION_20260817.md
```

### Prochaine unité OF-MAP-002

Construire Batch 02 uniquement sur des champs dont le niveau, le type et la transformation sont démontrables. Les noms Fund/SubFund/Umbrella ne doivent pas être mappés naïvement : ils nécessitent une boucle dédiée sur `name_role`, langue, normalisation et structure umbrella/subfund.

## OF-SOURCE-002 — prochaine unité

### INDEX_PROVIDER résiduel

```text
JSE
EGX
NSE
NGX
BVMT
```

Ces cinq relations restent `PENDING`. Une bourse validée comme `STOCK_EXCHANGE` ne devient pas automatiquement provider/administrator d'indice. Exiger une preuve officielle spécifique de calcul, administration, propriété ou publication de l'indice avant toute promotion.

### Rôles zonaux — revue sémantique distincte

```text
MONETARY_UNION             3
SUPRANATIONAL_AUTHORITY    2
INTERBANK_MARKET_OPERATOR  2
```

Ne pas promouvoir automatiquement BCEAO/BEAC comme `INTERBANK_MARKET_OPERATOR` à partir des seules preuves FX de Wave 13. `CMA / MONETARY_UNION` reste particulièrement à arbitrer : si le rôle canonique est trop fort, faire évoluer le modèle au lieu de forcer la donnée.

## OF-SOURCE-003 — toujours actif

La validation institutionnelle ne clôt pas la validation des 55 mappings/séries initiaux. Continuer à vérifier séparément :

```text
ENDPOINT
SERIE EXACTE
FREQUENCE
UNITE
CONVENTION DE COTATION
HISTORIQUE
METHODE
STATUT DE COLLECTE
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

## Blockers maintenus

```text
ERYTHREE            PRIMARY_OFFICIAL_SOURCE_NOT_VERIFIED
FMDQ                REQUIRES_ROLE_MODEL_REVIEW
SEC_ZAMBIA          CURRENT_OFFICIAL_DOMAIN_INTEGRITY_BLOCKER
IRA_URBRA_UGANDA    COMBINED_ROLE_MODEL_MISMATCH
RBM_FUND_REGULATOR  PRIMARY_CIS_PROOF_NOT_SUFFICIENT
PERSISTENT_DB       OPENFUNDS_DATABASE_URL / DURABLE_RUNTIME_NOT_CONFIGURED
IMMUTABLE_RAW_STORE NOT_CONFIGURED
```

## Interdictions maintenues

Ne pas importer d'historique réel sans stockage durable, ne pas modifier ou fermer la PR nº2 sans réconciliation, ne pas fusionner/retargeter la PR nº1, ne pas travailler sur `main`, ne pas créer de branche/PR, ne pas activer WTI/WTI Bench et ne pas déployer sans satisfaction des gates correspondants.
