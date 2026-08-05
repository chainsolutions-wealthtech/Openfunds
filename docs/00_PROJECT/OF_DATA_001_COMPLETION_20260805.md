# OF-DATA-001 completion record — Fund / SubFund / ShareClass

```text
DATE: 2026-08-05
TASK: OF-DATA-001
LOOP: OF-LOOP-DATA-001
ADR: ADR-030
STATUS: VERIFIED_COMPLETE
START_HEAD: e79c735b2cda8cc40a237b7deb3e379cc42bf1d9
VALIDATED_TECHNICAL_HEAD: 8ab1e75b2fd94566f9c0538ca33460140787c6bf
MIGRATION: 015_FUND_SUBFUND_SHARECLASS_CORE
MIGRATION_SHA256: 5ce14ea3de866c31c0452fccfe77827873dec976be3391b2d323e7daf88ef15d
```

## 1. Decision implemented

```text
STANDALONE
FUND -> SHARE_CLASS

UMBRELLA
FUND -> SUBFUND -> SHARE_CLASS
```

A standalone SICAV, FCP or unit trust does not receive a synthetic compartment.
A current subfund or share class has at most one current structural parent.

## 2. Canonical runtime objects

Migration `015` creates:

- `fund.entity`;
- `fund.entity_state`;
- `fund.fund_profile`;
- `fund.subfund_profile`;
- `fund.share_class_profile`;
- `fund.entity_name`;
- `fund.entity_identifier`;
- `fund.structure_relationship`;
- `fund.entity_event`;
- `fund.event_participant`;
- current-state and current-path views;
- structural quality view;
- structural relationship enforcement trigger.

Stable identity, current/former names, aliases, identifiers, profiles,
relationships and events are stored separately.

## 3. Compatibility and governance

The governed manifest now contains exactly fifteen migrations. The former
`schemas/taxonomy/fund_relationship_information_model_v0.1.sql` remains
preserved but excluded as a superseded draft.

Migration `015` deliberately does not create or modify the draft tables
`fund.fund` and `fund.share_class`. It creates no production fund row and performs
no destructive data operation.

## 4. Tested country structures

### Morocco

Standalone SICAV with one direct MAD share class and no subfund.

### Tunisia

Umbrella FCP with a real compartment and a TND share class. Legal name, former
name and alias are separate. A management-transfer event links the transferred
subfund, former manager and new manager.

### Nigeria

Standalone unit trust with accumulating and distributing NGN share classes,
without being reclassified as an umbrella.

## 5. Negative controls

The PostgreSQL fixture proves that:

- a duplicate current ISIN is rejected;
- a share class cannot receive two current structural parents;
- an umbrella fund cannot attach a share class directly;
- the legacy draft tables are absent from a clean governed database;
- validated fixture entities expose no structural quality issue.

## 6. CI evidence

| Workflow | Run | Result |
|---|---:|---|
| Governed Migration Runner | `30994140842` | `SUCCESS` |
| Collector Tests | `30994140840` | `SUCCESS` |
| Reference Registry Synchronization | `30994140910` | `SUCCESS` |
| Frozen Migration 012 Guard | `30994140896` | `SUCCESS` |

The governed migration job passed:

- fourteen Python unit tests;
- the fifteen-entry manifest plan;
- application to an empty PostgreSQL 16 database;
- second application and ledger verification;
- runtime contract assertions;
- Morocco, Tunisia and Nigeria fixtures;
- removal of the ledger followed by replay and revalidation of existing data.

## 7. Acceptance matrix

```text
ENTITIES_AND_CARDINALITIES_APPROVED: YES
STANDALONE_WITHOUT_FAKE_SUBFUND: YES
UMBRELLA_WITH_REAL_SUBFUND: YES
SICAV_FCP_UNIT_TRUST_FIXTURES: PASSED
IDENTITY_NAME_ALIAS_SEPARATION: PASSED
IDENTIFIER_NON_DUPLICATION: PASSED
MERGER_EVENT_MODEL: PASSED
MANAGEMENT_TRANSFER_MODEL: PASSED
MIGRATION_ADDITIVE: YES
EMPTY_POSTGRESQL_16: PASSED
DOUBLE_APPLY: PASSED
LEDGER_VERIFY: PASSED
EXISTING_DATA_WITHOUT_LEDGER: PASSED
PRODUCTION_HISTORY_LOADED: NO
PRODUCTION_DEPLOYMENT: NO
```

## 8. Transparent intermediate incident

Commit `8fa7c13becc4833d53da4239a4f0cbb5d7fb11e5` accidentally added a one-line
file named `NONEXISTENT`. It was not hidden or removed by history rewriting.
Commit `8ab1e75b...`, its direct descendant, removes that file and contains the
intended technical tree. The final diff from the loop start contains no
`NONEXISTENT` file.

No force-push, branch recreation or history rewrite occurred.

## 9. Deferred work

This phase does not provide:

- a populated canonical field dictionary;
- service-provider mandates;
- document-to-fund relationships;
- real fund, NAV, AUM or dividend histories;
- an official Openfunds field mapping;
- persistent production storage;
- API or UI resources.

## 10. Next gate

```text
OF-DATA-002 — populate the machine-readable canonical dictionary
STATUS: NOT_STARTED_BY_THIS_LOOP
AUTHORIZATION: REQUIRED
```
