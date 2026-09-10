# Prochaine action autorisée

```text
STATUS_DATE: 2026-09-10
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
PR_1: DRAFT / OPEN / UNMERGED
CURRENT_HEAD_POLICY: RESOLVE_DYNAMICALLY
CURRENT_IMPLEMENTED_MIGRATION_CHAIN: 001..039
LATEST_MIGRATION: 039_TRACKED_INDEX_DENOMINATION_BASE / ORDER 390
CURRENT_CANONICAL_INVENTORY: 295 = 143_CORE + 152_EXTENSIONS
CURRENT_MAPPING: BATCH_01..27 / 93_ROWS / 50_OF_IDS / 53_CANONICAL_IDS
UNMAPPED_OPENFUNDS_IDS: 1819
LATEST_MAPPING: MAP-000093 / OFST023850
LAST_OBSERVED_MAPPING_CI_HEAD: 275ec7a10658cfc5a9f5822eb2315bf01138fc10
LAST_OBSERVED_MAPPING_CI_RUN: 32541124896
RECENT_REMOTE_CI: FAILURE_KNOWN
PRODUCTION_DEPLOYED: NO
```

## Autorité de reprise

Lire dans cet ordre :

1. `00_START_HERE.md`
2. `GOVERNANCE.md`
3. `README.md`
4. `AGENTS.md`
5. `SOURCE_OF_TRUTH.md`
6. `STATUS.md`
7. ce fichier
8. `LOOP_STATE.md`
9. `CURRENT_ITERATION.md`
10. `LOOP_ENGINEERING.md`
11. `DEFINITION_OF_DONE.md`
12. `TODO.md` / `SUIVI.md`
13. `DECISIONS.md` / ADR pertinents
14. les spécifications et tests de la tâche sélectionnée.

Résoudre le HEAD GitHub courant avant toute écriture. Les SHA présents ici décrivent des preuves datées et ne remplacent jamais cette vérification.

## Action immédiate — restaurer le contrat CI existant de OF-MAP-002

Le dernier run pertinent observé `OF-MAP-002 Mapping Registry` (`32541124896`) est rouge sur son HEAD `275ec7a10658cfc5a9f5822eb2315bf01138fc10`.

État observé :

```text
OFFICIAL_CANONICAL_INTEGRATION: PASS
UNIT_TEST_PYTHON_3_11: FAILURE
UNIT_TEST_PYTHON_3_12: FAILURE
FAILURE_CONTRACT: BATCH_07 / NO_PARENT_CURRENCY_INFERENCE
```

Le test attend que `NO_PARENT_CURRENCY_INFERENCE` soit présent dans `NOTES` pour la ligne Batch 07 concernée. La prochaine intervention technique doit déterminer, à partir du contrat, de l'historique Git, du mapping source et des tests, si la ligne de données a perdu cette note ou si une autre incohérence compatible explique l'échec.

### Règles de correction

- ne pas supprimer ou affaiblir l'assertion pour obtenir du vert ;
- ne pas inventer de sémantique métier ;
- conserver l'invariant déjà documenté : devise locale/tracked-index non inférée d'une devise parent ;
- utiliser TDD/RED → GREEN pour toute correction de comportement ou fixture ;
- vérifier Python 3.11 et 3.12 ;
- vérifier également le job d'intégration officielle/canonique ;
- comparer les outputs et compteurs avec la baseline ;
- persister les preuves avant de déclarer le run vert.

## Ensuite — Canonical Foundation / Task 4

Une fois la CI existante restaurée, reprendre la Task 4 `reason-classified Openfunds review outcomes registry`.

Les surfaces existent déjà :

```text
data/openfunds/mapping/v2.13.0/REVIEW_OUTCOMES.csv
scripts/validate_openfunds_review_outcomes.py
tests/test_openfunds_review_outcomes.py
```

Le registre `REVIEW_OUTCOMES.csv` observé lors de la réconciliation du 2026-09-10 contient actuellement son en-tête gouverné mais aucune ligne d'outcome ne doit être inventée. Continuer seulement à partir des cas réellement revus et prouvés.

Outcomes autorisés :

```text
MAPPED_CANONICAL
MAPPED_DERIVED
NO_CANONICAL_EQUIVALENT
DEFERRED_NOT_REQUIRED_FOR_PRODUCT
GATED_VENDOR_OR_LICENSE
TO_CONFIRM
```

### Règles Task 4

- ne jamais générer 1 869 faux `UNMAPPED` ;
- le registre d'outcomes reste sparse pour les cas explicitement revus non mappés/gated/deferred ;
- les OF-IDs mappés sont dérivés de `MAPPING_REGISTRY.csv` ;
- un OF-ID ne peut appartenir qu'à une catégorie terminale ;
- `TO_CONFIRM` reste un blocker ;
- chaque outcome non mappé possède un reason code ;
- l'OF-ID doit exister dans l'inventaire officiel checksum-locked v2.13.0 ;
- le SHA source reste `40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4` tant que la source officielle versionnée ne change pas.

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
GITHUB_NATIVE_RULESET    NONE_OBSERVED
PERSISTENT_DB            NOT_CONFIGURED
IMMUTABLE_RAW_STORE      NOT_CONFIGURED
COMPLETE_HISTORIES       NOT_LOADED
SEDOL_RUNTIME            EXPLICIT_LICENSING_CLEARANCE_REQUIRED
BLOOMBERG_RIC_RUNTIME    EXPLICIT_PROPRIETARY_IDENTIFIER_USAGE_REVIEW_REQUIRED
BENCHMARK_RFR_MAR        NOT_FULLY_VALIDATED
WTI_WTI_BENCH            NOT_ACTIVE
PRODUCTION_API_UI        NOT_IMPLEMENTED
PRODUCTION_DEPLOY        NOT_CONFIGURED
```

## Interdictions

Ne pas toucher `main`, ne pas créer de branche/PR supplémentaire, ne pas retargeter/fusionner/mettre Ready PR #1, ne pas force-push ou réécrire l'historique, ne pas déployer, ne pas activer production et ne pas charger des données réelles sans porte explicite.
