# Canonical Taxonomy PostgreSQL Persistence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Persist the existing canonical taxonomy V0.1 into PostgreSQL through a deterministic, checksum-governed forward migration without activating unvalidated methodologies.

**Architecture:** Existing `data/canonical/*.csv` and `MATRIX_MANIFEST_V0_1.json` remain Git authoring surfaces. A deterministic Python generator emits frozen migration 017; `migrations/manifest.json` registers it at order 170 with a check-only generator contract; PostgreSQL becomes runtime truth only after migration application.

**Tech Stack:** Python 3.11/3.12, PostgreSQL 16, CSV/JSON standard library, existing governed migration runner, GitHub Actions.

## Global Constraints

- Existing migrations 001–016 are immutable.
- No `DROP`, `DELETE`, or `TRUNCATE`.
- No new branch and no merge to `main` during implementation.
- No fabricated business-validity dates.
- Preserve `NULL != 0` semantics.
- Preserve UEMOA/CEMAC market-zone routing semantics.
- Preserve `STRUCTURE_PREFILLED` and `NOT_ACTIVE` methodology/production status.
- SQL generation must be deterministic from committed canonical authoring inputs.
- All writes must remain additive and regression-tested.

---

### Task 1: Lock the generator contract with RED tests

**Files:**
- Create: `tests/test_generate_canonical_taxonomy_sql.py`
- Read: `data/canonical/ASSET_CLASSES_V0_1.csv`
- Read: `data/canonical/ASSET_SUBCLASSES_V0_1.csv`
- Read: `data/canonical/FUND_SCOPE_ROUTING_V0_1.csv`
- Read: `data/canonical/CATEGORY_TEMPLATE_MATRIX_V0_1.csv`
- Read: `data/canonical/SCOPE_REFERENCE_OVERRIDES_V0_1.csv`
- Read: `data/canonical/ANALYTICS_REFERENCE_REQUIREMENTS_V0_1.csv`

**Interfaces:**
- Consumes: canonical CSV files with `;` delimiter.
- Produces contract for `scripts/generate_canonical_taxonomy_sql.py`.

- [ ] **Step 1: Write failing tests**

Tests must assert:

```python
from scripts.generate_canonical_taxonomy_sql import build_sql, load_sources

sources = load_sources(ROOT / "data" / "canonical")
sql = build_sql(sources)
assert "create schema if not exists taxonomy" in sql.lower()
assert "drop " not in sql.lower()
assert "delete " not in sql.lower()
assert "truncate " not in sql.lower()
assert "STRUCTURE_PREFILLED" in sql
assert "NOT_ACTIVE" in sql
```

Also derive expected row counts directly from committed CSV files and assert one emitted row per authoring row.

- [ ] **Step 2: Run RED**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest -v tests.test_generate_canonical_taxonomy_sql
```

Expected: failure because `scripts.generate_canonical_taxonomy_sql` does not exist.

- [ ] **Step 3: Commit RED contract**

Commit only the new test file.

---

### Task 2: Implement deterministic SQL generation

**Files:**
- Create: `scripts/generate_canonical_taxonomy_sql.py`
- Test: `tests/test_generate_canonical_taxonomy_sql.py`

**Interfaces:**
- `load_sources(root: Path) -> dict[str, list[dict[str, str]]]`
- `build_sql(sources: dict[str, list[dict[str, str]]]) -> str`
- CLI options: `--source-dir`, `--output`, `--check`

- [ ] **Step 1: Implement strict CSV/JSON loading**

Use `csv.DictReader(..., delimiter=";")`, UTF-8, exact file names, stable row ordering, and explicit failure on duplicate canonical keys.

- [ ] **Step 2: Implement SQL literal escaping**

Use a single helper:

```python
def sql_literal(value: str | None) -> str:
    if value is None or value == "":
        return "NULL"
    return "'" + value.replace("'", "''") + "'"
```

No interpolated identifiers from source data.

- [ ] **Step 3: Emit additive schema/table DDL**

Create the seven dedicated `taxonomy.*` tables from the design. Add primary keys and foreign keys only where the canonical source guarantees them.

- [ ] **Step 4: Emit deterministic idempotent inserts**

Use `INSERT ... ON CONFLICT (...) DO UPDATE` only for fields owned by the taxonomy authoring surface. Never overwrite unrelated runtime fields.

- [ ] **Step 5: Implement `--check`**

`--check` regenerates in memory and fails if the committed output differs byte-for-byte.

- [ ] **Step 6: Run GREEN unit tests**

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest -v tests.test_generate_canonical_taxonomy_sql
```

Expected: PASS.

- [ ] **Step 7: Commit generator + tests**

---

### Task 3: Materialize and govern migration 017

**Files:**
- Create: `schemas/taxonomy/017_canonical_fund_taxonomy_v0_1.sql`
- Modify: `migrations/manifest.json`
- Test: existing `scripts/run_migrations.py --plan`

**Interfaces:**
- Generator output path is the migration file.
- Manifest entry ID: `017_CANONICAL_FUND_TAXONOMY_V0_1`
- Manifest order: `170`

- [ ] **Step 1: Generate migration**

```bash
python scripts/generate_canonical_taxonomy_sql.py \
  --source-dir data/canonical \
  --output schemas/taxonomy/017_canonical_fund_taxonomy_v0_1.sql
```

- [ ] **Step 2: Register manifest entry**

Append:

```json
{
  "order": 170,
  "id": "017_CANONICAL_FUND_TAXONOMY_V0_1",
  "path": "schemas/taxonomy/017_canonical_fund_taxonomy_v0_1.sql",
  "generator": {
    "script": "scripts/generate_canonical_taxonomy_sql.py",
    "arguments": [
      "--check",
      "--source-dir", "data/canonical",
      "--output", "schemas/taxonomy/017_canonical_fund_taxonomy_v0_1.sql"
    ],
    "mode": "CHECK_ONLY_FROZEN_ARTIFACT"
  }
}
```

- [ ] **Step 3: Validate migration plan**

```bash
PYTHONDONTWRITEBYTECODE=1 python scripts/run_migrations.py --plan
```

Expected final plan line begins `170 PENDING 017_CANONICAL_FUND_TAXONOMY_V0_1`.

- [ ] **Step 4: Verify generator check**

```bash
python scripts/generate_canonical_taxonomy_sql.py --check \
  --source-dir data/canonical \
  --output schemas/taxonomy/017_canonical_fund_taxonomy_v0_1.sql
```

Expected: success.

- [ ] **Step 5: Commit frozen migration + manifest**

---

### Task 4: Add PostgreSQL 16 integration contract

**Files:**
- Create: `tests/test_canonical_taxonomy_postgres.py`
- Modify or create focused GitHub Actions workflow path for taxonomy migration CI.

**Interfaces:**
- Uses existing `scripts/run_migrations.py`.
- Uses ephemeral PostgreSQL 16.

- [ ] **Step 1: Write integration assertions**

Assert exact database counts equal current canonical source counts, plus representative semantics:

```text
BENIN -> local market scope UEMOA
COTE_DIVOIRE -> local market scope UEMOA
CAMEROUN -> local market scope CEMAC
GABON -> local market scope CEMAC
NIGERIA -> local market scope NIGERIA
MAROC -> local market scope MAROC
```

Also assert category templates remain `NOT_ACTIVE` and no release is marked production-active.

- [ ] **Step 2: Apply full migration chain to empty PostgreSQL 16**

```bash
python scripts/run_migrations.py --apply --database-url "$DATABASE_URL"
python scripts/run_migrations.py --verify --database-url "$DATABASE_URL"
```

- [ ] **Step 3: Re-run apply**

Run `--apply` a second time and assert all migrations are skipped and counts do not change.

- [ ] **Step 4: Add CI matrix where applicable**

Python contract tests run on 3.11 and 3.12; PostgreSQL integration uses PostgreSQL 16.

- [ ] **Step 5: Commit integration contract**

---

### Task 5: Record the architectural decision and project state

**Files:**
- Create: `docs/00_PROJECT/ADR-029_CANONICAL_TAXONOMY_AUTHORING_AND_RUNTIME.md`
- Modify: `DECISIONS.md`
- Modify: `data/canonical/README.md`
- Modify: `TODO.md`
- Modify: `SUIVI.md`
- Modify: `CHANGELOG.md`
- Modify: `NEXT_ACTION.md`

**Interfaces:**
- Documents the accepted authoring/runtime split and migration 017.

- [ ] **Step 1: Write ADR-029**

Record:

```text
Git canonical CSV/JSON = governed authoring/review
Generated frozen SQL = deterministic migration representation
PostgreSQL = runtime source of truth after application
Migration 017 = first governed taxonomy persistence release
Production activation = explicitly excluded
```

- [ ] **Step 2: Reconcile stale TODO/SUIVI statements**

Mark structural taxonomy persistence complete only if PostgreSQL integration is GREEN. Keep methodology, provider-series validation, WTI/WTI Bench and production activation tasks open.

- [ ] **Step 3: Update NEXT_ACTION**

Point to the next highest-value unblocked task after migration 017, prioritizing existing `PENDING` institutional roles and the official Openfunds Field List gate.

- [ ] **Step 4: Commit documentation**

---

### Task 6: Final regression verification

**Files:**
- No new implementation files unless a regression requires a focused fix.

- [ ] **Step 1: Run canonical matrix generator check**

```bash
python scripts/generate_fund_category_matrices.py --check
```

- [ ] **Step 2: Run taxonomy generator check**

```bash
python scripts/generate_canonical_taxonomy_sql.py --check --source-dir data/canonical --output schemas/taxonomy/017_canonical_fund_taxonomy_v0_1.sql
```

- [ ] **Step 3: Run unit test suite relevant to migration, taxonomy, institutional registry and canonical matrix**

Use Python 3.11 and 3.12 in CI.

- [ ] **Step 4: Run PostgreSQL 16 migration/integration suite**

Full chain from empty database and second idempotent apply must pass.

- [ ] **Step 5: Verify PR head and changed-file scope**

Confirm the branch is still `architecture/africafunds-country-indicators-v0.1`, PR #1 remains draft unless separately authorized, and no `main` mutation occurred.

- [ ] **Step 6: Record exact verified HEAD in `SUIVI.md`**
