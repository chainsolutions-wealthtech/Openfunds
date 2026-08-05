# Frozen authoring snapshots for generated migrations

This directory preserves the exact governed input used to create each generated
SQL migration. A snapshot is historical evidence, not the current authoring
surface.

```text
data/reference/VALIDATED_FX_REFERENCE_REGISTRY.csv
= active governed authoring registry

migrations/sources/NNN_*.csv
= immutable input snapshot for migration NNN

schemas/reference/NNN_*.sql
= immutable generated migration artifact
```

Rules:

1. snapshot number and SQL migration number must match;
2. neither file is modified after commit and application;
3. manifest checks use the frozen snapshot, never the changing active registry;
4. an authoring change creates a new snapshot and a new forward migration;
5. no snapshot proves historical data coverage or production activation.

Current frozen pair:

- `012_validated_fx_reference_registry.csv`;
- `schemas/reference/012_validated_fx_reference_registry.sql`.
