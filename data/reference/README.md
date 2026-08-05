# Governed reference registries

## Authority model

The broad semicolon-delimited CSV files in this directory remain discovery and review inventories. The collection-tested FX pilots have one governed authoring source:

```text
VALIDATED_FX_REFERENCE_REGISTRY.csv
→ deterministic validation and SQL generation
→ PostgreSQL runtime truth
```

PostgreSQL remains the canonical runtime source after the generated synchronization SQL is applied. Historical SQL seeds remain replayable but are not a competing authoring source.

## Commands

```bash
python scripts/generate_validated_fx_reference_sql.py
python scripts/generate_validated_fx_reference_sql.py --check
python -m unittest tests/test_validated_fx_reference_registry.py -v
```

The generated migration path is:

```text
schemas/reference/012_validated_fx_reference_registry.sql
```

It is generated during validation and deployment checks; never edit it manually.

## Evidence

The governed rows reference the controlled BCEAO and BEAC collection evidence, including workflow run ID, raw SHA256, value date, parser version and retrieval timestamp.

## Lifecycle boundary

The synchronized pilots are:

```text
VALIDATED
COLLECTION_TESTED
CURRENT_SNAPSHOT_ONLY
```

They are not:

```text
PARTIAL_HISTORY_LOADED
COMPLETE_HISTORY_LOADED
PRODUCTION_PERSISTENT
```

Generic discovery endpoints remain separate from the validated collector endpoints `BCEAO_FX_DAILY` and `BEAC_FX_DAILY`.
