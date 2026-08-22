# OF Canonical Foundation — A0 Reconciliation — 2026-08-22

## FACTS

```text
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
PR: #1 DRAFT / OPEN / UNMERGED
BASE: architecture/canonical-model-v1-bootstrap
MIGRATION_CHAIN_IMPLEMENTED: 001..039
LATEST_MIGRATION: 039_TRACKED_INDEX_DENOMINATION_BASE
LATEST_MIGRATION_ORDER: 390
CANONICAL_CORE_FIELDS: 143
CANONICAL_EXTENSION_FIELDS: 152
CANONICAL_TOTAL_FIELDS: 295
MAPPING_BATCHES_IMPLEMENTED: BATCH_01..BATCH_27
MAPPING_ROWS: 93
MAPPED_OPENFUNDS_IDS: 50
UNMAPPED_OPENFUNDS_IDS: 1819
MAPPED_CANONICAL_IDS: 53
LATEST_MAPPING_ID: MAP-000093
LATEST_EXTERNAL_ID: OFST023850
PRODUCTION_DEPLOYED: NO
PERSISTENT_PRODUCTION_DB_ACTIVATED: NO
IMMUTABLE_PRODUCTION_RAW_STORE_ACTIVATED: NO
```

## EVIDENCE

- `migrations/manifest.json` registers 39 governed migrations and ends at order 390 / `039_TRACKED_INDEX_DENOMINATION_BASE`.
- `data/dictionary/extensions/tracked_index_denomination_base_v1/00_metadata.json` declares one additional canonical field for migration 039.
- `data/openfunds/mapping/v2.13.0/MAPPING_REGISTRY.csv` ends at `MAP-000093`, mapping `OFST023850` to `OF_FUND_SHARE_CLASS_TRACKED_INDEX_DENOMINATION_BASE`.
- `data/openfunds/mapping/v2.13.0/mapping_manifest.json` is reconciled through Batch 27 at 295 canonical fields, 93 mapping rows, 50 mapped official IDs and 53 mapped canonical IDs.
- `.github/workflows/of-map-002-mapping-registry.yml` now executes the Batch 27 and denomination-base dictionary contracts and validates the extension.
- `.github/workflows/migration-runner.yml` now expects 39 migrations, executes `tests.test_tracked_index_denomination_base_model` and asserts the `fund.share_class_tracked_index.denomination_base` column.

## LIMITS

The connected GitHub status surface still exposes no recent workflow run/status for the exact recent branch heads. Therefore:

```text
IMPLEMENTED != REMOTELY_GREEN
CURRENT_RECENT_CI_STATE: PENDING_REMOTE_CI_ATTESTATION
```

The last remotely attested baselines remain the historical runs already recorded by the project. No newer GREEN state is invented.

The project is not globally complete. Persistent production PostgreSQL, immutable production object storage, complete histories, production API, web application, WTI/WTI Bench activation and deployment remain outside A0.

## RISKS

- The mapping manifest was reserialized compactly during A0 because the connected Contents API rejected a large pretty-printed replacement. Semantic historical batch/policy/history objects were preserved and the resulting file was re-read from GitHub for verification.
- Two transient staging files were created and removed while working around the large-file write limitation. No staging file remains in the active tree; history was not rewritten or force-pushed.
- Vendor-sensitive SEDOL/Bloomberg/RIC import/export gates remain unchanged.

## DECISIONS

1. A0 is a state-reconciliation gate, not a product-completion claim.
2. Machine manifests and exact registry contents take precedence over stale prose counts.
3. Historical documentation is preserved; living documents receive superseding current-state sections.
4. New migration numbers start at 040 only when a product-required Openfunds semantic cannot be represented safely by the existing canonical model.
5. Openfunds mapping coverage will be completed through reason-classified outcomes rather than fake `UNMAPPED` mapping rows.
6. PR #1 remains Draft/Open/Unmerged and deployment remains forbidden until the final explicit human deployment gate.

## NEXT_ACTION

Proceed with the validated implementation plan:

`docs/superpowers/plans/2026-08-22-openfunds-canonical-foundation-completion-plan.md`

Immediate next unit:

```text
TASK_4: OPENFUNDS REVIEW OUTCOMES REGISTRY
THEN: A1 IDENTITY / NAMES / LEGAL STRUCTURE
```

The outcome registry must remain sparse for explicitly reviewed non-mapping/deferment/gate cases and must derive mapped IDs from the authoritative mapping registry. It must never materialize 1,869 artificial `UNMAPPED` rows.
