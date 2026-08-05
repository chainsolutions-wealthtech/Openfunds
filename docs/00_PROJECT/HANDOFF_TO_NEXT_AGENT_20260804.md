# Handoff to next agent — 2026-08-04

## 1. Repository point of control

```text
REPOSITORY
chainsolutions-wealthtech/Openfunds

WORK_BRANCH
architecture/africafunds-country-indicators-v0.1

BASELINE_START_SHA
cce82f3276d408ddb71366f5236c10282f0b6614

BASELINE_END_SHA
59f6475102b8a0c5b1274060afc412db787f2caf

BASELINE_COMMIT_SHA
59f6475102b8a0c5b1274060afc412db787f2caf

BASELINE_COMMIT_PARENT_SHA
cce82f3276d408ddb71366f5236c10282f0b6614

BASELINE_COMMIT_MESSAGE
docs(project): establish immutable GitHub baseline and handoff [OF-DOC-002]

MAIN_HEAD_AT_BASELINE
946145e4b33a6289eb340a16bf5c651cb9bbee7c

CURRENT_HEAD_POLICY
RESOLVE_DYNAMICALLY_BEFORE_EVERY_ACTION_AND_COMPARE_WITH_BASELINE_END_SHA
```

`BASELINE_END_SHA` is the final commit of the audited documentary baseline.

The current branch HEAD is not frozen in this document. It must always be resolved dynamically from GitHub before any intervention and compared with `BASELINE_END_SHA`.

When the current HEAD is ahead of `BASELINE_END_SHA`, every additional commit must be inventoried and reviewed before any new write.

If `BASELINE_END_SHA` is no longer an ancestor of the current HEAD, the intervention must stop and the divergence must be reported.

Never attempt to record the SHA of a future corrective commit in this file. Any corrective commit SHA must be reported only in the external final report after the commit exists.

## 2. Work completed by the baseline intervention

- verified all twelve branch heads and their relation to `main`;
- confirmed the work-branch head had not changed before the baseline write;
- audited PR nº 1 and PR nº 2 without manual modification;
- compared all 13 bootstrap deliverables by blob SHA;
- confirmed all 13 bootstrap deliverables exist identically in the complete branch;
- reconciled PR nº 2 content;
- identified two exactly preserved CSVs and three unique detailed Markdown documents;
- corrected the current project-state interpretation;
- prepared a draft migration of P0/P1 tasks without creating issues;
- preserved the existing `OF-ARCH-001 → OF-SOURCE-001 → OF-ARCH-002 → OF-ARCH-003 → OF-ARCH-004` order.

## 3. Recommended integration strategy

```text
STRATEGY_B
complete branch → main directly
```

This is a recommendation only. It is not authorization to retarget or merge.

Reason: all 13 bootstrap deliverables have identical current blob SHAs in the complete branch, so a separate bootstrap merge is redundant and would create an incomplete intermediate baseline.

## 4. PR nº 2 disposition

Exact copies already preserved:

- official source inventory CSV;
- canonical integration matrix CSV.

Still unique and requiring preservation or explicit rejection:

- `AFRICA_MARKET_RATES_MACRO_SOURCE_HANDOFF_20260803.md`;
- `NON_REGRESSION_AND_STATUS_RULES_20260803.md`;
- `PR1_RESEARCH_ASSET_EXPLOITATION_GUIDE_20260803.md`.

Do not close, merge or retarget PR nº 2 until those three documents are preserved or rejected with documented rationale and the PR state is resolved again dynamically.

## 5. Invariants

- PostgreSQL runtime truth;
- governed versioned authoring files subject to ADR-021;
- immutable raw evidence;
- Openfunds mapping layer only;
- legal country distinct from local market;
- UEMOA/BRVM and CEMAC/BVMAC scopes retained;
- investment scope proposed, not implemented;
- peer group, WTI, market benchmark, WTI Bench, RFR and MAR distinct;
- 486/432 structures prefilled and inactive;
- `STRUCTURE_PREFILLED` does not mean production active;
- `NOT_ACTIVE` does not mean a calculated product exists;
- `METHODOLOGY_TO_VALIDATE` does not mean a validated methodology;
- no active WTI, WTI Bench, ratios or rankings;
- collection-tested snapshots are not histories;
- proposed SQL is not a production migration;
- research sources are not canonical sources;
- no invented dates;
- observed and calculated values separate;
- XOF and XAF separate.

## 6. Exact restart point

1. Resolve the current HEAD of `architecture/africafunds-country-indicators-v0.1`.

2. Compare the dynamically resolved HEAD with:

   ```text
   BASELINE_END_SHA
   59f6475102b8a0c5b1274060afc412db787f2caf
   ```

3. If the current HEAD is ahead of `BASELINE_END_SHA`, inventory and review every additional commit before any new write.

4. If `BASELINE_END_SHA` is not an ancestor of the current HEAD, stop and report the divergence.

5. Confirm PR nº 1 and PR nº 2 states dynamically before continuing.

6. Read the living plan and all dated evidence reports.

7. Resume the functional sequence only after the relevant execution gates:

```text
OF-ARCH-001
→ OF-SOURCE-001
→ OF-ARCH-002
→ OF-ARCH-003
→ OF-ARCH-004
```

Before those tasks, an independent review may use the audit reports to decide the future PR integration strategy. Do not start persistent history, production deployment or fund imports before the gates.

## 7. Files to read first

```text
docs/00_PROJECT/BRANCH_INVENTORY_AND_EXPLOITATION_PLAN.md
docs/00_PROJECT/GITHUB_BASELINE_AUDIT_20260804.md
docs/00_PROJECT/BRANCH_INVENTORY_20260804.csv
docs/00_PROJECT/BOOTSTRAP_INTEGRATION_ASSESSMENT_20260804.md
docs/00_PROJECT/PR_CONTENT_RECONCILIATION_20260804.csv
docs/00_PROJECT/CANONICAL_PROJECT_STATE_20260804.md
docs/00_PROJECT/OPEN_DECISIONS_AND_EXECUTION_GATES_20260804.md
docs/00_PROJECT/ISSUE_MIGRATION_DRAFT_20260804.csv
TODO.md
SUIVI.md
DECISIONS.md
```

## 8. Baseline post-commit verification

```text
BASELINE_END_SHA
59f6475102b8a0c5b1274060afc412db787f2caf

PR1_STATE
OPEN

PR1_DRAFT
TRUE

PR1_MERGED
FALSE

PR1_MERGEABLE_AT_BASELINE
TRUE

PR1_BASE
architecture/canonical-model-v1-bootstrap

PR1_HEAD
architecture/africafunds-country-indicators-v0.1

PR1_HEAD_SHA
59f6475102b8a0c5b1274060afc412db787f2caf

PR1_COMMITS
174

PR1_CHANGED_FILES
131

PR1_ADDITIONS
17577

PR1_DELETIONS
1

PR1_REQUESTED_REVIEWERS
NONE

PR1_REQUESTED_TEAM_REVIEWERS
NONE
```

Baseline diff:

```text
FILES_ADDED
9

FILES_MODIFIED
4

FILES_DELETED
0

TOTAL_PATHS
13

TOTAL_ADDITIONS
1261

TOTAL_DELETIONS
0

PYTHON_FILES_CHANGED
0

WORKFLOWS_CHANGED
0

SQL_FILES_CHANGED
0

CANONICAL_DATA_FILES_CHANGED
0

REFERENCE_DATA_FILES_CHANGED
0

TESTS_CHANGED
0

REQUIREMENTS_CHANGED
0

BINARY_FILES_CHANGED
0
```

These values describe the immutable baseline comparison from `cce82f3276d408ddb71366f5236c10282f0b6614` to `59f6475102b8a0c5b1274060afc412db787f2caf`. They are not a substitute for resolving the current branch state.

## 9. Baseline workflow runs

```text
WORKFLOW_NAME
Source Endpoint Schema Tests

RUN_ID
30950594176

STATUS
completed

CONCLUSION
success
```

```text
WORKFLOW_NAME
Collector Tests

RUN_ID
30950594182

STATUS
completed

CONCLUSION
success
```

```text
WORKFLOW_NAME
Daily Africa FX Staging

RUN_ID
30950594174

STATUS
completed

CONCLUSION
success
```

```text
WORKFLOW_NAME
BCEAO FX Live Smoke

RUN_ID
30950594266

STATUS
completed

CONCLUSION
success
```

```text
WORKFLOW_NAME
BEAC FX Live Smoke

RUN_ID
30950594179

STATUS
completed

CONCLUSION
success
```

These results are a snapshot of executions associated with `BASELINE_END_SHA`. They do not guarantee the result of future executions. Every new HEAD must be verified independently.

## 10. PR nº 2 observed state at baseline

```text
PR2_OBSERVED_RELATIVE_TO_BASELINE_END_SHA
59f6475102b8a0c5b1274060afc412db787f2caf

PR2_STATE
OPEN

PR2_DRAFT
TRUE

PR2_MERGED
FALSE

PR2_MERGEABLE_AT_OBSERVATION
TRUE

PR2_BASE
architecture/africafunds-country-indicators-v0.1

PR2_HEAD
agent/official-africa-source-handoff-20260803

PR2_HEAD_SHA
81d32b83e6a87d01c4e66c2c2db00199b4553d70

PR2_BRANCH_RELATION_AT_OBSERVATION
DIVERGED

PR2_AHEAD_BY
5

PR2_BEHIND_BY
43
```

The `mergeable` value is calculated dynamically by GitHub and must be checked again before any action.

The ahead/behind values are a snapshot taken against the AfricaFunds branch at `BASELINE_END_SHA`.

PR nº 2 must not be closed, merged or retargeted before preservation or an explicit decision concerning the three unique Markdown documents.

## 11. Verification commands or equivalent connector checks

```text
1. Resolve the current HEAD of
   architecture/africafunds-country-indicators-v0.1.

2. Compare the dynamically resolved HEAD with:

   BASELINE_END_SHA
   59f6475102b8a0c5b1274060afc412db787f2caf

3. If the current HEAD is ahead of BASELINE_END_SHA,
   inventory and review every additional commit before any new write.

4. If BASELINE_END_SHA is not an ancestor of the current HEAD,
   stop and report the divergence.

5. Confirm PR nº 1 and PR nº 2 states dynamically before continuing.

6. Confirm no unauthorized branch, PR, issue, reviewer, comment,
   workflow, code, SQL, data, test, binary or deployment change.
```

## 12. Ready-to-copy continuation prompt

```text
Continue the Openfunds project from the immutable documentary baseline dated 2026-08-04.

First resolve the current HEAD of:
architecture/africafunds-country-indicators-v0.1

Compare the dynamically resolved HEAD with:
BASELINE_END_SHA
59f6475102b8a0c5b1274060afc412db787f2caf

If the current HEAD is ahead, inventory and review every additional commit before any new write.
If BASELINE_END_SHA is not an ancestor of the current HEAD, stop and report the divergence.

Read the living branch exploitation plan, the eight dated baseline reports, TODO.md,
SUIVI.md, DECISIONS.md and the source registry before proposing any write.

Preserve this order:
OF-ARCH-001 → OF-SOURCE-001 → OF-ARCH-002 → OF-ARCH-003 → OF-ARCH-004.

Do not treat LOCAL_MARKET, INVESTMENT_SCOPE, a migration runner, merge policy,
auto-merge, Fund/SubFund/ShareClass, unknown dates, WTI, WTI Bench or workbook
reproducibility as already decided. Do not create a new branch, modify main,
retarget, merge or close a PR, create issues, add reviewers or comments, or modify
code, data, SQL, workflows or tests unless the user explicitly authorizes a new execution phase.
```
