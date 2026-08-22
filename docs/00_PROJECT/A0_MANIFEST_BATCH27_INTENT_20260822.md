# A0 — Batch 27 manifest reconciliation intent

This checkpoint records the exact machine-derived state before reconciling `data/openfunds/mapping/v2.13.0/mapping_manifest.json`.

```text
MIGRATIONS: 39 (latest 039_TRACKED_INDEX_DENOMINATION_BASE / order 390)
CANONICAL_CORE_FIELDS: 143
CANONICAL_EXTENSION_FIELDS: 152
CANONICAL_TOTAL_FIELDS: 295
MAPPING_ROWS: 93
MAPPED_OPENFUNDS_IDS: 50
UNMAPPED_OPENFUNDS_IDS: 1819
MAPPED_CANONICAL_IDS: 53
LATEST_MAPPING: MAP-000093 / OFST023850
REMOTE_CI_ATTESTATION: PENDING / recent exact-head checks not exposed by connected GitHub surface
```

Derivation: Batch 26 manifest recorded 294 canonical fields, 92 mapping rows, 49 mapped Openfunds IDs and 52 mapped canonical IDs. Migration 039 dictionary extension contributes one physical field and `MAP-000093` contributes one new external ID and one new canonical target.

No production activation, merge, PR retargeting, `main` mutation or deployment is authorized by this checkpoint.
