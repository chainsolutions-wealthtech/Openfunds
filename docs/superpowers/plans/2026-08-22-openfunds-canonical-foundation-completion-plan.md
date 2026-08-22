# Openfunds Canonical Foundation Completion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reconcile the current governed branch through migration 039 / Batch 27, then complete the product-required Openfunds canonical foundation with reason-classified coverage, PostgreSQL 16 migration safety, mapping/dictionary validation and fully synchronized living documentation.

**Architecture:** Preserve the existing PostgreSQL-first canonical model and checksum-locked Openfunds v2.13.0 mapping layer. Every family is audited against the official archive before code changes; existing canonical targets are reused, and new forward-only migrations/dictionary extensions are created only when a required semantic cannot be represented safely. Mapping changes remain append-only and are verified by exact Git diff.

**Tech Stack:** Python 3.11/3.12 tests, PostgreSQL 16, SQL migrations, JSON governed dictionaries, semicolon-delimited mapping registry, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-08-22-openfunds-canonical-foundation-completion-design.md`

## Global Constraints

- Work only on `architecture/africafunds-country-indicators-v0.1`.
- PR #1 remains Draft/Open/Unmerged; do not merge, retarget, mark ready or deploy.
- Do not mutate `main` and do not create another branch/PR.
- Historical migrations and validated mapping rows are immutable; all evolution is forward-only.
- `IMPLEMENTED != REMOTELY_GREEN`; only observable workflow evidence can establish remote GREEN.
- `NULL != 0`; never invent absent dates, currencies, NAVs, AUM, prices, fees, holdings or statuses.
- Openfunds is an exchange/mapping layer and never becomes the physical runtime schema.
- Vendor-sensitive identifiers remain runtime import/export gated until explicit clearance.
- Every new schema/mapping behavior follows RED contract -> minimal implementation -> workflow wiring -> exact diff review -> documentation/checkpoint.
- New migration numbers start at 040 and are allocated only when official semantics prove that no existing canonical target can safely represent the requirement.

---

### Task 1: A0 authoritative state lock and count derivation

**Files:**
- Read: `migrations/manifest.json`
- Read: `data/openfunds/mapping/v2.13.0/MAPPING_REGISTRY.csv`
- Read: `data/openfunds/mapping/v2.13.0/mapping_manifest.json`
- Read: `.github/workflows/migration-runner.yml`
- Read: `.github/workflows/of-map-002-mapping-registry.yml`
- Read: `data/dictionary/spec_v1/**`
- Read: `data/dictionary/extensions/**`

**Interfaces:**
- Consumes: PR #1 metadata and exact branch HEAD.
- Produces: exact authoritative counts used by all A0 reconciliation edits.

- [ ] **Step 1: Re-lock PR #1 and branch HEAD**

Call GitHub PR metadata and require:

```text
state=open
merged=false
draft=true
head=architecture/africafunds-country-indicators-v0.1
base=architecture/canonical-model-v1-bootstrap
```

Stop on any unexpected branch/base/state change.

- [ ] **Step 2: Derive migration count from `migrations/manifest.json`**

Expected current structural state after migration 039:

```text
latest_order=390
latest_id=039_SHARE_CLASS_TRACKED_INDEX_DENOMINATION_BASE
migration_count=39
```

Do not infer count from prose documents.

- [ ] **Step 3: Derive mapping counts from exact full registry content**

Compute from semicolon rows excluding the header:

```python
rows = registry_lines[1:]
reviewed_mapping_rows = len(rows)
mapped_external_ids = len({row[2] for row in parsed_rows})
mapped_canonical_ids = len({row[3] for row in parsed_rows})
unmapped_external_ids = 1869 - mapped_external_ids
```

Expected after `MAP-000093`:

```text
reviewed_mapping_rows=93
mapped_external_ids=50
unmapped_external_ids=1819
mapped_canonical_ids=53
```

- [ ] **Step 4: Derive canonical field count from core plus extension metadata**

Expected current inventory after migration 039:

```text
core=143
extensions=152
canonical_field_count=295
```

If the computed result differs, investigate the exact extension package rather than editing counts to expectation.

- [ ] **Step 5: Query exact HEAD status and workflow observability**

Check combined status and commit workflow runs for the exact head SHA. Record empty/unavailable results as `PENDING_REMOTE_CI_ATTESTATION`, never as failure or success.

- [ ] **Step 6: Commit nothing in Task 1**

Task 1 is a read/derive gate. The output is the verified input for Task 2.

---

### Task 2: A0 wire migration 039 and Batch 27 into machine manifests and CI

**Files:**
- Modify: `data/openfunds/mapping/v2.13.0/mapping_manifest.json`
- Modify: `.github/workflows/migration-runner.yml`
- Modify: `.github/workflows/of-map-002-mapping-registry.yml`
- Test: `tests/test_share_class_tracked_index_denomination_base_model.py`
- Test: `tests/test_share_class_tracked_index_denomination_base_dictionary_extension.py`
- Test: `tests/test_openfunds_mapping_batch27.py`

**Interfaces:**
- Consumes: authoritative counts from Task 1.
- Produces: machine surfaces structurally aligned through migration 039 / Batch 27.

- [ ] **Step 1: Verify the RED/implementation artifacts already exist**

Require:

```text
schemas/fund/039_share_class_tracked_index_denomination_base.sql
data/dictionary/extensions/share_class_tracked_index_denomination_base_v1/00_metadata.json
data/dictionary/extensions/share_class_tracked_index_denomination_base_v1/10_fields.json
tests/test_share_class_tracked_index_denomination_base_model.py
tests/test_share_class_tracked_index_denomination_base_dictionary_extension.py
tests/test_openfunds_mapping_batch27.py
```

- [ ] **Step 2: Update mapping manifest through Batch 27**

Set derived values, not hard-coded historical replacements:

```json
{
  "canonical_core_field_count": 143,
  "canonical_extension_field_count": 152,
  "canonical_field_count": 295,
  "current_coverage": {
    "reviewed_mapping_rows": 93,
    "mapped_external_ids": 50,
    "unmapped_external_ids": 1819,
    "mapped_canonical_ids": 53
  },
  "status": "BATCH_27_IMPLEMENTED_CANONICAL_295_PENDING_REMOTE_CI_ATTESTATION"
}
```

Append the extension path and Batch 27 metadata. Preserve every previous batch object byte-for-byte where practical.

- [ ] **Step 3: Wire OF-MAP-002**

Add paths and unit commands for:

```text
tests/test_share_class_tracked_index_denomination_base_dictionary_extension.py
tests/test_openfunds_mapping_batch27.py
data/dictionary/extensions/share_class_tracked_index_denomination_base_v1
```

Do not remove any prior test/extension.

- [ ] **Step 4: Wire migration-runner**

Add `tests/test_share_class_tracked_index_denomination_base_model.py` to both path filters and Fund-domain unit commands. Change runtime expected migration count from 38 to 39 and assert:

```sql
if not exists (
  select 1
  from information_schema.columns
  where table_schema='fund'
    and table_name='share_class_tracked_index'
    and column_name='denomination_base'
) then
  raise exception 'tracked-index denomination base migration 039 column is missing';
end if;
```

- [ ] **Step 5: Verify exact Git diffs**

For the registry, no change is expected in this task. For workflows/manifest, confirm only migration 039 / Batch 27 additions and count/status reconciliation occurred.

- [ ] **Step 6: Commit**

Use focused commits such as:

```text
ci: wire migration 039 and Openfunds Batch 27
meta: reconcile Openfunds manifest through Batch 27
```

---

### Task 3: A0 reconcile living state, task registry, handoff and PR body

**Files:**
- Modify: `STATUS.md`
- Modify: `NEXT_ACTION.md`
- Modify: `CURRENT_ITERATION.md`
- Modify: `LOOP_STATE.md`
- Modify: `TODO.md`
- Modify: `SUIVI.md`
- Modify: `CHANGELOG.md`
- Modify: `WORK_LOG.md`
- Modify: `HANDOFF.md`
- Modify: PR #1 body
- Create: `docs/00_PROJECT/OF_CANONICAL_FOUNDATION_A0_RECONCILIATION_20260822.md`

**Interfaces:**
- Consumes: Tasks 1-2 exact branch state.
- Produces: one consistent current-state narrative and restart point.

- [ ] **Step 1: Add current-state superseding sections instead of deleting history**

The current section must state at minimum:

```text
CONTROL_BRANCH=architecture/africafunds-country-indicators-v0.1
MIGRATIONS_IMPLEMENTED=001..039
CANONICAL_FIELDS=295
MAPPING_BATCHES_IMPLEMENTED=01..27
MAPPING_ROWS=93
MAPPED_OF_IDS=50
UNMAPPED_OF_IDS=1819
MAPPED_CANONICAL_IDS=53
REMOTE_CI=LATEST_RECENT_HEAD_PENDING_IF_UNOBSERVABLE
PR_1=DRAFT_OPEN_UNMERGED
PRODUCTION_DEPLOYED=NO
```

- [ ] **Step 2: Update `TODO.md` without deleting completed historical tasks**

Keep `OF-MAP-002` `EN_COURS` until product-required family completion and reason-classified coverage are complete. Add a current progress subsection pointing to the master/spec/plan documents.

- [ ] **Step 3: Update continuity documents**

`NEXT_ACTION.md` must point to Task 4/A1 and the current implementation plan. `HANDOFF.md` must contain the exact branch, PR, latest migration, latest mapping ID, blockers and next file set.

- [ ] **Step 4: Write dated A0 checkpoint**

The report separates:

```text
FACTS
EVIDENCE
LIMITS
RISKS
DECISIONS
NEXT_ACTION
```

- [ ] **Step 5: Replace only the PR body, not PR state/base**

PR #1 body must describe migrations through 039, Batch 27 counts, current product-finalization specs, remote CI rule and explicit non-claims. Do not mark ready or change base.

- [ ] **Step 6: Re-lock PR and HEAD after all A0 writes**

Confirm Draft/Open/Unmerged/base/head invariants again.

---

### Task 4: Introduce reason-classified official Openfunds review outcomes

**Files:**
- Create: `data/openfunds/mapping/v2.13.0/REVIEW_OUTCOMES.csv`
- Create: `scripts/validate_openfunds_review_outcomes.py`
- Create: `tests/test_openfunds_review_outcomes.py`
- Modify: `data/openfunds/mapping/v2.13.0/mapping_manifest.json`
- Modify: `.github/workflows/of-map-002-mapping-registry.yml`
- Modify: `OPENFUNDS_MAPPING.md`

**Interfaces:**
- Consumes: official checksum-locked inventory and existing mapping registry.
- Produces: explicit non-mapping/deferment/gate status without materializing fake mapping rows.

- [ ] **Step 1: Write the RED validator contract**

`tests/test_openfunds_review_outcomes.py` must require these columns:

```text
STANDARD_VERSION;EXTERNAL_FIELD_ID;OUTCOME;REASON_CODE;SOURCE_SHA256;SOURCE_REFERENCE;NOTES
```

Allowed outcomes:

```text
MAPPED_CANONICAL
MAPPED_DERIVED
NO_CANONICAL_EQUIVALENT
DEFERRED_NOT_REQUIRED_FOR_PRODUCT
GATED_VENDOR_OR_LICENSE
TO_CONFIRM
```

The validator must reject duplicate OF-IDs, unknown OF-IDs, invalid outcome values, blank reason codes for non-mapped outcomes and source SHA mismatches.

- [ ] **Step 2: Implement an initially sparse outcome registry**

Do not generate 1,869 rows. Populate only reviewed non-mapping/deferment/gate outcomes; mapped IDs are derivable from `MAPPING_REGISTRY.csv` and need not be duplicated unless the chosen validator requires a normalized merged view.

- [ ] **Step 3: Implement merged coverage calculation**

The validator must compute:

```text
mapped_external_ids
reviewed_nonmapped_external_ids
to_confirm_external_ids
unreviewed_external_ids
total_official_ids=1869
```

Every OF-ID must resolve to at most one terminal review category.

- [ ] **Step 4: Wire tests and official integration into OF-MAP-002**

Run on Python 3.11 and 3.12 and validate against the official PDF/checksum inventory.

- [ ] **Step 5: Document outcome semantics**

`OPENFUNDS_MAPPING.md` must state that `DEFERRED_NOT_REQUIRED_FOR_PRODUCT` is an explicit product-scope decision, not proof that the field is semantically unimportant globally.

---

### Task 5: A1 identity, names and legal-structure family

**Files:**
- Audit: official v2.13.0 field inventory for Fund/SubFund/ShareClass names, languages, legal form, umbrella relations and organization roles.
- Reuse: `schemas/fund/015_fund_subfund_shareclass_core.sql`
- Create only if required: next sequential `schemas/fund/04x_*.sql`
- Create only if required: matching `data/dictionary/extensions/*_v1/`
- Create: family-specific mapping tests under `tests/test_openfunds_mapping_batch*.py`
- Modify: mapping registry, mapping manifest, workflows, living docs.

**Interfaces:**
- Consumes: canonical core identity/event/relation structures.
- Produces: reversible product-required identity/legal mappings with no destructive rename/role collapse.

- [ ] **Step 1: Extract exact official records by semantic keywords and adjacent OF-ID blocks**

Search official inventory for:

```text
Fund Name
Share Class Name
Legal Name
Umbrella
Subfund
Language
Management Company
Manufacturer
Investment Manager
Legal Form
```

Record exact OF-ID, field level, datatype, allowed values/cardinality and official description before mapping.

- [ ] **Step 2: Inspect existing canonical fields/relations**

Prefer existing `fund.entity`, name/alias/relation/event structures. A new migration is justified only for missing semantics such as language-tagged names or explicit organization-role linkage not representable by existing models.

- [ ] **Step 3: Write RED family mapping contracts**

Tests must forbid:

```text
manufacturer -> investment_manager implicit collapse
legal_name -> display_name destructive overwrite
umbrella/subfund -> free-text parent name only
unknown language -> invented language code
```

- [ ] **Step 4: Implement minimal canonical additions and mappings**

Use append-only mapping rows and exact diff verification. Add dictionary extensions only for actual new physical fields/tables.

- [ ] **Step 5: Reconcile manifests/workflows/docs and checkpoint the family**

The family is complete only when no product-required identity/legal field remains `TO_CONFIRM`.

---

### Task 6: A2 dealing, eligibility and fees family

**Files:**
- Audit official Openfunds dealing/eligibility/fee records.
- Create/reuse normalized dealing-term, eligibility and fee structures.
- Test: new schema/dictionary/mapping family tests.

**Interfaces:**
- Consumes: Share Class identity, currency/timezone semantics.
- Produces: explicit dealing cutoff/frequency, minimums, eligibility and fee semantics.

- [ ] **Step 1: Audit exact official OF-IDs and cardinalities**

Group by semantics:

```text
subscription/redemption frequency
cutoff time/timezone
dealing calendar
minimum initial/subsequent investment
minimum holding
subscription/redemption fee
management/ongoing/performance fee
investor type/eligibility
distribution country
```

- [ ] **Step 2: RED contracts must distinguish zero from unknown**

Require explicit source evidence before storing a zero fee/minimum. Blank source stays null/unknown.

- [ ] **Step 3: Normalize repeated/applicable fees rather than adding many profile columns**

When a fee can repeat by type/currency/tier/applicability, use a versioned relation with fee type, numeric value/rate, basis, currency when applicable, effective status and provenance.

- [ ] **Step 4: Keep eligibility separate from domicile/distribution registration**

Investor eligibility, country registration and marketing/distribution country are separate canonical concepts.

- [ ] **Step 5: Append mappings, verify diffs, wire CI and checkpoint**

No product-required A2 field may remain `TO_CONFIRM` at exit.

---

### Task 7: A3 regulatory documents family

**Files:**
- Reuse/source lineage: `source.raw_artifact` and canonical entity relations.
- Create if absent: versioned `fund.document`/entity-document relation migration and dictionary package.
- Test: schema, dictionary, mapping and provenance constraints.

**Interfaces:**
- Consumes: canonical entities and source artifact identity.
- Produces: typed, language-aware, source-lineaged disclosure documents.

- [ ] **Step 1: Audit Openfunds document fields**

Cover at minimum prospectus, KID/KIID/PRIIPs, annual report and semi-annual report semantics present in v2.13.0.

- [ ] **Step 2: RED contract**

Reject a design where documents are unrelated URL columns on `share_class_profile`. Require document type, entity relation, language if known, source URL/artifact, date knowledge status and provenance.

- [ ] **Step 3: Implement normalized document model only if existing source/document structures cannot satisfy it**

Document binaries remain raw artifacts; canonical rows describe business/document identity and relationship.

- [ ] **Step 4: Map official fields and preserve unknown dates/languages**

No retrieval date may substitute for publication/effective date.

- [ ] **Step 5: CI/docs/checkpoint**

Document export/import behavior and any source URL persistence rules.

---

### Task 8: A4 distribution and lifecycle cash-event family

**Files:**
- Reuse: `fund.entity_event` where event semantics fit.
- Create if required: normalized cash distribution observation/event relation.
- Test: date/amount/currency semantics and no-zero inference.

**Interfaces:**
- Consumes: Share Class identity, currencies, lifecycle event framework.
- Produces: explicit distribution/dividend events distinct from distribution policy.

- [ ] **Step 1: Audit exact Openfunds distribution-event fields**

Identify amount, currency, ex-date, record date, payment date, frequency or related event semantics.

- [ ] **Step 2: RED tests**

Require:

```text
distribution_policy != actual_distribution_event
missing_event != zero_distribution
ex_date != payment_date
unknown_currency != share_class_currency inference
```

- [ ] **Step 3: Implement normalized event/observation structures if needed**

Preserve repeatability, source lineage and corrected versions.

- [ ] **Step 4: Map and checkpoint**

No product-required cash-event semantic ambiguity remains at exit.

---

### Task 9: A5 NAV, AUM and price observation semantics

**Files:**
- Audit existing `market`/`fund` observation schemas.
- Create if required: typed fund/share-class observation model migration(s).
- Test: source value date, publication/retrieval timestamps, currency/quote-unit, observation type and correction versioning.

**Interfaces:**
- Consumes: entities, currencies, listings, provenance.
- Produces: canonical source observations suitable for history/analytics without confusing NAV, AUM, bid/offer or market price.

- [ ] **Step 1: Inventory existing observation tables before creating a new one**

Reuse if existing tables can encode all required dimensions.

- [ ] **Step 2: RED semantic matrix**

Tests must enforce distinct types such as:

```text
NAV_PER_UNIT
NET_ASSETS_TOTAL
BID_PRICE
OFFER_PRICE
LISTING_MARKET_PRICE
```

and must forbid bid/offer -> NAV promotion without explicit source semantics.

- [ ] **Step 3: Implement provenance/versioning**

Keep business/value date, publication date, retrieved_at and recorded_at separate. Corrections never overwrite the prior source observation.

- [ ] **Step 4: Map product-required Openfunds valuation fields**

Attach each source field to the exact observation type and unit/currency semantics.

- [ ] **Step 5: PostgreSQL integration and checkpoint**

This task is the prerequisite for historical NAV/AUM ingestion in sub-project B/C.

---

### Task 10: A6 holdings and portfolio disclosure semantics

**Files:**
- Create/reuse portfolio disclosure and holding relation structures.
- Test: as-of date, disclosure completeness, instrument identity/name, quantity/value/currency/weight and provenance.

**Interfaces:**
- Consumes: Fund/Share Class entities and source artifacts.
- Produces: portfolio disclosures that distinguish complete portfolios from top-N/aggregate data.

- [ ] **Step 1: Audit official holdings/portfolio Openfunds fields and cardinality**

Identify whether v2.13.0 provides row-level holdings, disclosure metadata or document links and map only semantics actually present.

- [ ] **Step 2: RED completeness contract**

Require an explicit disclosure scope such as:

```text
COMPLETE
TOP_N
PARTIAL
AGGREGATED
UNKNOWN
```

Never infer `COMPLETE` from row count.

- [ ] **Step 3: Implement normalized disclosure/holding model if required**

Each holding carries source artifact/locator provenance; missing quantity/value/weight remains null.

- [ ] **Step 4: Map, validate and checkpoint**

Ensure the model can later ingest external African holdings even when Openfunds itself supplies only metadata/document references.

---

### Task 11: A7 classification and analytical prerequisites

**Files:**
- Reuse: taxonomy migration 017 and existing category/benchmark structures.
- Create only missing versioned assignment/reference relations.
- Test: scope, membership history and source lineage.

**Interfaces:**
- Consumes: entity hierarchy, benchmark/tracked-index, canonical taxonomy.
- Produces: prerequisites for peers, category analytics, RFR/MAR and later WTI/WTI Bench.

- [ ] **Step 1: Audit existing taxonomy/peer/reference model first**

Do not duplicate migration 017 structures.

- [ ] **Step 2: RED contracts**

Enforce separation between:

```text
national category
regional category
Africa category
peer group
benchmark
risk-free reference
MAR
WTI
WTI_Bench
```

- [ ] **Step 3: Implement only missing assignment/reference structures**

Assignments are versioned and source-lineaged; methodology products remain inactive until separately validated.

- [ ] **Step 4: Map relevant product-required Openfunds classification fields**

Avoid forcing Openfunds taxonomy labels directly into internal category codes without an explicit governed crosswalk.

- [ ] **Step 5: CI/docs/checkpoint**

Keep WTI/WTI Bench `NOT_ACTIVE` unless a later methodology gate is explicitly approved.

---

### Task 12: Canonical Foundation completion audit and handoff

**Files:**
- Modify: `data/openfunds/mapping/v2.13.0/mapping_manifest.json`
- Modify: `OPENFUNDS_MAPPING.md`
- Modify: all living state docs
- Create: `docs/00_PROJECT/OF_CANONICAL_FOUNDATION_COMPLETION_20260822.md`
- Modify: PR #1 body

**Interfaces:**
- Consumes: Tasks 4-11 completed family checkpoints.
- Produces: closed sub-project A and exact handoff to Durable Ingestion Runtime design/plan.

- [ ] **Step 1: Run reason-classified coverage audit**

For all 1,869 official records, derive exactly one of:

```text
mapped
reviewed_nonmapped_or_deferred
vendor_gated
to_confirm
unreviewed
```

Product-required families must have `to_confirm=0` and `unreviewed=0` within their family scope.

- [ ] **Step 2: Verify migration chain on PostgreSQL 16 CI surface**

Require current runner to contain every implemented migration and every family model test. Do not claim runtime GREEN without observable evidence.

- [ ] **Step 3: Verify mapping/dictionary workflow completeness**

Every extension and current batch test must be explicitly wired; historical tests must remain extensible and not freeze cumulative global counts.

- [ ] **Step 4: Reconcile documentation and PR body**

All living documents must agree on counts, latest migration/batch, known external blockers and next sub-project.

- [ ] **Step 5: Write completion report**

The report states both accomplishments and explicit non-claims:

```text
NO_PRODUCTION_DEPLOYMENT
NO_PERSISTENT_PRODUCTION_DB_ACTIVATION
NO_RAW_OBJECT_STORE_PRODUCTION_ACTIVATION
NO_CLAIM_OF_COMPLETE_HISTORICAL_LOAD
NO_API_OR_WEB_COMPLETION_YET
```

- [ ] **Step 6: Re-lock PR/head/checks**

Confirm PR remains Draft/Open/Unmerged and capture observable CI state.

- [ ] **Step 7: Transition to the next approved architectural sub-project**

Create/review the separate implementation plan for **Durable Ingestion and Raw-Data Runtime** before writing that subsystem.