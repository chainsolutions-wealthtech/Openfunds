# GitHub baseline audit — 2026-08-04

## 1. Immutable point of control

```text
REPOSITORY        chainsolutions-wealthtech/Openfunds
WORK_BRANCH       architecture/africafunds-country-indicators-v0.1
START_HEAD_SHA    cce82f3276d408ddb71366f5236c10282f0b6614
KNOWN_HEAD_SHA    cce82f3276d408ddb71366f5236c10282f0b6614
SHA_CHANGED       NO
DEFAULT_BRANCH    main
MAIN_HEAD_SHA     946145e4b33a6289eb340a16bf5c651cb9bbee7c
```

The work-branch head matched the supplied control SHA before any write. No unexplained commit was found.

## 2. Repository state

- Private repository.
- Default branch `main` contains only the initial one-line README at `946145e4b33a6289eb340a16bf5c651cb9bbee7c`.
- Twelve branches were observed.
- Eight bootstrap-suffixed branches plus `bootstrap-final` are identical to `main` and contain no unique commit.
- Three branches contain material work:
  - `architecture/canonical-model-v1-bootstrap`;
  - `architecture/africafunds-country-indicators-v0.1`;
  - `agent/official-africa-source-handoff-20260803`.

See `BRANCH_INVENTORY_20260804.csv`.

## 3. Pull requests

### PR #1

```text
STATE          OPEN
DRAFT          TRUE
MERGED         FALSE
MERGEABLE      TRUE
BASE           architecture/canonical-model-v1-bootstrap
HEAD           architecture/africafunds-country-indicators-v0.1
HEAD_SHA       cce82f3276d408ddb71366f5236c10282f0b6614
COMMITS        173
CHANGED_FILES  122
ADDITIONS      16316
DELETIONS      1
REVIEWS        0
```

Five latest observed workflow runs at the audited head completed successfully:

- Collector Tests;
- Source Endpoint Schema Tests;
- Daily Africa FX Staging;
- BCEAO FX Live Smoke;
- BEAC FX Live Smoke.

These successful runs do not imply that the checks are required by a branch ruleset.

### PR #2

```text
STATE          OPEN
DRAFT          TRUE
MERGED         FALSE
MERGEABLE      TRUE
BASE           architecture/africafunds-country-indicators-v0.1
HEAD           agent/official-africa-source-handoff-20260803
HEAD_SHA       81d32b83e6a87d01c4e66c2c2db00199b4553d70
COMMITS        5
CHANGED_FILES  5
ADDITIONS      1373
DELETIONS      0
REVIEWS        0
```

No PR was retargeted, closed, merged or otherwise changed.

## 4. Corrected current volume

The historical audit recorded 95 files, and the first documentation consolidation recorded 104 files. Those figures remain valid as historical snapshots.

The current GitHub PR metadata reports **122 changed files** for PR #1. This current number supersedes 104 only for the present PR tip; it does not rewrite the historical logs.

## 5. Current implementation status

### Implemented and tested

- BCEAO and BEAC snapshot collectors;
- localized parsing and FX transformation;
- XOF and XAF provider series kept separate;
- raw SHA256 lineage in pilot runs;
- idempotent PostgreSQL loader tests;
- endpoint reconciliation tests;
- daily dual-source staging;
- deterministic fund classification matrix generator;
- tests for 54 routes, 486 routing rules and 432 unique category/reference blocks.

### Structure present and tested, but not active

- four asset classes and seven permitted subclasses;
- local-market, regional and Africa routing;
- 486 fund routing rules;
- 432 categories, peer groups and reference blocks;
- reference-role slots for peer group, WTI, market benchmark, WTI Bench, risk-free rate and MAR;
- Excel review export metadata and checksum.

The generated objects remain `STRUCTURE_PREFILLED / NOT_ACTIVE`.

### Not active or not complete

- no live WTI calculation;
- no live WTI Bench calculation;
- no production rankings, ratios or generalized analytics engine;
- no complete history for BCEAO/BEAC;
- no persistent production PostgreSQL;
- no permanent immutable raw object store;
- no complete Openfunds field mapping;
- no final Fund/SubFund/ShareClass model;
- no production API or frontend;
- Tunisia and Nigeria fund archives not integrated into this repository.

## 6. Business invariants preserved

1. PostgreSQL is the intended runtime truth.
2. Versioned files support authoring and review of small governed references, subject to ADR-021.
3. Raw artifacts must become immutable evidence.
4. Openfunds is a mapping/exchange layer, not the internal physical schema.
5. `LEGAL_COUNTRY` is distinct from `LOCAL_MARKET_SCOPE`.
6. BRVM implies UEMOA as common local-market scope.
7. BVMAC implies CEMAC as common local-market scope.
8. UEMOA remains in `AFRICA_OUEST`; CEMAC remains in `AFRICA_CENTRALE`.
9. Investment scope is proposed and not implemented.
10. Peer Group, WTI, Market Benchmark, WTI Bench, Risk-Free Rate and MAR are distinct.
11. The 486 rules and 432 blocks are `STRUCTURE_PREFILLED / NOT_ACTIVE`.
12. WTI, WTI Bench, ratios and rankings are not active.
13. `COLLECTION_TESTED` does not mean history loaded.
14. BCEAO/BEAC are tested snapshots, not complete histories.
15. `research_queue` remains non-canonical `RESEARCH_CANDIDATE`.
16. Unknown dates are never invented.
17. Calculated observations never replace native observations.
18. XOF and XAF remain distinct provider-series families.

## 7. Primary risks

- CSV/SQL double authoring remains unresolved.
- Endpoint models remain to be unified.
- Unknown business-date semantics remain open.
- Migration execution is manually ordered.
- Fund/SubFund/ShareClass remains incomplete.
- `NATIONAL` versus `LOCAL_MARKET` terminology is inconsistent across older and newer documents.
- Current routing does not yet model investment geography independently of legal domicile.
- Excel export reproducibility from repository inputs/generator is not yet fully demonstrated.
- PR #1 is large and has no independent review.
- `main` remains non-representative.

## 8. Connector limitations

- Organization-level GitHub Projects, rulesets, environments, secrets and external automation references are not exposed by the connected actions used here.
- The connector does not return a complete ordered list of commits for a non-default branch. Bootstrap assessment therefore uses aggregate comparison metadata, known commit anchors and verified blob equality for all 13 deliverables.
- External references outside the repository cannot be declared absent; branch deletion remains gated by an external-reference check.

## 9. No-action conclusion

This audit authorizes no retargeting, merge, PR closure, issue creation, workflow change, branch deletion or production deployment.
