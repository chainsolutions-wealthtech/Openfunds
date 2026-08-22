# Prochaine action autorisée

```text
STATUS_DATE: 2026-08-22
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
PR_1: DRAFT / OPEN / UNMERGED
CURRENT_IMPLEMENTED_MIGRATION_CHAIN: 001..039
LATEST_MIGRATION: 039_TRACKED_INDEX_DENOMINATION_BASE / ORDER 390
CURRENT_CANONICAL_INVENTORY: 295 = 143_CORE + 152_EXTENSIONS
CURRENT_MAPPING: BATCH_01..27 / 93_ROWS / 50_OF_IDS / 53_CANONICAL_IDS
UNMAPPED_OPENFUNDS_IDS: 1819
LATEST_MAPPING: MAP-000093 / OFST023850
LAST_REMOTELY_VERIFIED_MIGRATION_CHAIN: 001..019 / RUN 32070768364
LAST_REMOTELY_VERIFIED_CANONICAL_UNION: 177 / RUN 32071385088
LAST_REMOTELY_VERIFIED_MAPPING: BATCH_05 / RUN 32071858346
RECENT_REMOTE_CI: PENDING_NOT_OBSERVABLE
PRODUCTION_DEPLOYED: NO
```

## Autorité de reprise

Lire dans cet ordre :

1. `00_START_HERE.md`
2. `AGENTS.md`
3. `SOURCE_OF_TRUTH.md`
4. `STATUS.md`
5. ce fichier
6. `docs/superpowers/specs/2026-08-22-openfunds-product-finalization-design.md`
7. `docs/superpowers/specs/2026-08-22-openfunds-canonical-foundation-completion-design.md`
8. `docs/superpowers/plans/2026-08-22-openfunds-canonical-foundation-completion-plan.md`
9. `docs/00_PROJECT/OF_CANONICAL_FOUNDATION_A0_RECONCILIATION_20260822.md`

## A0 — état

```text
MACHINE_MANIFESTS_ALIGNED: YES THROUGH MIGRATION_039 / BATCH_27
OF_MAP_002_WIRED_THROUGH_BATCH_27: YES
MIGRATION_RUNNER_WIRED_THROUGH_039: YES
MAPPING_REGISTRY_APPEND_ONLY_THROUGH_MAP_000093: YES
RECENT_REMOTE_GREEN_ATTESTED: NO / NOT OBSERVABLE
```

`IMPLEMENTED != REMOTELY_GREEN` reste une règle dure.

## Prochaine unité : Task 4 — reason-classified review outcomes

Créer un registre machine-readable complémentaire pour les OF-IDs officiellement revus mais volontairement non représentés par une ligne de mapping canonique.

Fichiers prévus :

```text
data/openfunds/mapping/v2.13.0/REVIEW_OUTCOMES.csv
scripts/validate_openfunds_review_outcomes.py
tests/test_openfunds_review_outcomes.py
```

Outcomes autorisés :

```text
MAPPED_CANONICAL
MAPPED_DERIVED
NO_CANONICAL_EQUIVALENT
DEFERRED_NOT_REQUIRED_FOR_PRODUCT
GATED_VENDOR_OR_LICENSE
TO_CONFIRM
```

### Règles

- ne jamais générer 1 869 faux `UNMAPPED` ;
- le registre d'outcomes reste sparse pour les cas explicitement revus non mappés/gated/deferred ;
- les OF-IDs mappés sont dérivés de `MAPPING_REGISTRY.csv` ;
- un OF-ID ne peut appartenir qu'à une catégorie terminale ;
- `TO_CONFIRM` reste un blocker ;
- chaque outcome non mappé possède un reason code ;
- l'OF-ID doit exister dans l'inventaire officiel checksum-locked v2.13.0 ;
- le SHA source doit rester `40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4`.

Le validator doit calculer :

```text
mapped_external_ids
reviewed_nonmapped_external_ids
vendor_gated_external_ids
to_confirm_external_ids
unreviewed_external_ids
total_official_ids = 1869
```

Après Task 4, continuer **A1 Identity / Names / Legal Structure** par audit officiel avant toute migration 040.

## Règle migration 040+

Aucun numéro de migration ne doit être réservé à l'avance. Créer migration 040 uniquement si l'audit A1 démontre qu'un concept produit requis ne peut pas être représenté sans perte par le modèle canonique existant.

## Invariants permanents

- `NULL != 0` ;
- date absente ≠ date inventée ;
- quote-unit ≠ devise économique ;
- Listing identity ≠ iNAV identity ;
- lifecycle ≠ investment/dealing status ;
- ETF Share Class ≠ passive Fund ;
- benchmark ≠ tracked index ;
- tracked-index identifiers ≠ benchmark identifiers ;
- RIC case preserved ;
- `OFST023805` vide = `LOCAL_CURRENCY` sans inférence de devise ;
- `OFST023850` = ratio explicite `Fund Price / Index`, aucune inférence de prix ou niveau d'index ;
- vendor identifiers restent import/export `NO` avant clearance explicite.

## Blockers externes conservés

```text
PERSISTENT_DB           NOT_CONFIGURED
IMMUTABLE_RAW_STORE     NOT_CONFIGURED
COMPLETE_HISTORIES      NOT_LOADED
SEDOL_RUNTIME           EXPLICIT_LICENSING_CLEARANCE_REQUIRED
BLOOMBERG_RIC_RUNTIME   EXPLICIT_PROPRIETARY_IDENTIFIER_USAGE_REVIEW_REQUIRED
BENCHMARK_RFR_MAR       NOT_FULLY_VALIDATED
WTI_WTI_BENCH           NOT_ACTIVE
PRODUCTION_API_UI       NOT_IMPLEMENTED
PRODUCTION_DEPLOY       NOT_CONFIGURED
```

## Interdictions

Ne pas toucher `main`, ne pas créer de branche/PR supplémentaire, ne pas retargeter/fusionner/mettre Ready PR #1, ne pas déployer, ne pas activer production et ne pas charger des données réelles sans porte explicite.
