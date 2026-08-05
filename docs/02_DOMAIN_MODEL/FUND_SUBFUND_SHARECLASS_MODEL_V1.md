# Fund / SubFund / ShareClass canonical model — v1

```text
TASK: OF-DATA-001
ADR: ADR-030
RUNTIME_MIGRATION: schemas/fund/015_fund_subfund_shareclass_core.sql
STATUS: IMPLEMENTATION_IN_PROGRESS
```

## 1. Canonical hierarchy

```text
                                  fund.entity
                       +---------------+---------------+
                       |               |               |
                     FUND           SUBFUND        SHARE_CLASS
                       |               |               |
             fund.fund_profile  fund.subfund_profile  fund.share_class_profile
```

Permitted current structural paths:

```text
Standalone vehicle
FUND [STANDALONE]
└── SHARE_CLASS

Umbrella vehicle
FUND [UMBRELLA]
└── SUBFUND
    └── SHARE_CLASS
```

A share class never has two current structural parents. A subfund never exists
as a mandatory technical placeholder for a standalone fund.

## 2. Separation of concerns

| Concern | Canonical relation |
|---|---|
| Stable technical identity | `fund.entity` |
| Lifecycle and domicile | `fund.entity_state` |
| Fund legal form and structure | `fund.fund_profile` |
| Compartment attributes | `fund.subfund_profile` |
| Class currency and distribution policy | `fund.share_class_profile` |
| Legal/current/former names and aliases | `fund.entity_name` |
| ISIN, LEI, regulator and local IDs | `fund.entity_identifier` |
| Fund/subfund/share-class parentage | `fund.structure_relationship` |
| Rename, merger, transfer, liquidation | `fund.entity_event` |
| Entity and organization roles in events | `fund.event_participant` |

Names and identifiers do not define the stable entity ID. A correction or
renaming therefore does not silently create a new fund.

## 3. Cardinalities

```text
FUND [STANDALONE] 1 ─── N SHARE_CLASS
FUND [UMBRELLA]   1 ─── N SUBFUND
SUBFUND           1 ─── N SHARE_CLASS

ENTITY            1 ─── N ENTITY_STATE_VERSION
ENTITY            1 ─── N NAME_VERSION
ENTITY            1 ─── N IDENTIFIER_VERSION
EVENT             1 ─── N EVENT_PARTICIPANT
```

A current validated profile is unique per entity and profile type. Historical
versions remain available after supersession.

## 4. Country examples used by the tests

### Morocco — standalone SICAV

```text
FUND_MAR_STANDALONE_TEST [FUND / STANDALONE / SICAV]
└── SHARE_MAR_A_TEST [SHARE_CLASS / MAD]
```

No subfund is generated.

### Tunisia — umbrella FCP

```text
FUND_TUN_UMBRELLA_TEST [FUND / UMBRELLA / FCP]
└── SUBFUND_TUN_BOND_TEST [SUBFUND / COMPARTMENT]
    └── SHARE_TUN_BOND_A_TEST [SHARE_CLASS / TND]
```

The subfund preserves a current legal name, a former name and an alias as three
distinct rows. A management-transfer event links the transferred subfund, former
manager and new manager.

### Nigeria — standalone unit trust with multiple classes

```text
FUND_NGA_STANDALONE_TEST [FUND / STANDALONE / UNIT_TRUST]
├── SHARE_NGA_ACC_TEST  [ACCUMULATING / NGN]
└── SHARE_NGA_DIST_TEST [DISTRIBUTING / NGN]
```

The presence of several share classes does not turn the fund into an umbrella.

## 5. Current path projection

`fund.current_share_class_path` resolves every validated share class to:

```text
share_class_id
subfund_id nullable
fund_id
```

For a direct standalone class, `subfund_id` is `NULL`. For an umbrella class, it
contains the real compartment.

`fund.structure_quality_issue` identifies validated subfunds or share classes
that lack the required current parent. It is a quality surface, not a mechanism
that invents missing relationships.

## 6. Identity rules

Current validated external identifiers are unique by:

```text
identifier_scheme
issuer_organization_id or global namespace
normalized_value
```

This blocks a current ISIN from being attached to two canonical entities while
allowing historical values to remain after explicit supersession.

Current primary names are unique per entity, role and language. Former names and
aliases may coexist with the legal name.

## 7. Event model

Supported initial events include:

```text
LAUNCH
RENAME
MERGER
ABSORPTION
SPLIT
MANAGEMENT_TRANSFER
DOMICILE_TRANSFER
LEGAL_FORM_CHANGE
SUSPENSION
REACTIVATION
CLOSURE
LIQUIDATION
```

Entity participant roles include predecessor, successor, surviving entity,
absorbed entity, source/target and transferred entity. Organization participant
roles include former and new manager.

The event model records the fact and its evidence. It does not automatically
rewrite structural history; reviewed ingestion logic must apply the corresponding
new versions and close superseded relationships.

## 8. Temporal model

Every business-date field is paired with a status. Unknown dates are represented
as `NULL`, never as a sentinel date. Current-system knowledge is identified by:

```text
recorded_at
superseded_at
is_current
```

A row visible through a `current_*` view is both current and `VALIDATED`.

## 9. What this model does not yet deliver

- no production fund or NAV history;
- no service-provider mandate table;
- no document-to-fund relation;
- no taxonomy classification migration;
- no Openfunds field mapping;
- no persistent collection environment;
- no automatic merger or transfer processor;
- no API or UI view model.

These are downstream uses of the stabilized identity and hierarchy, not reasons
to merge them into the structural core.
