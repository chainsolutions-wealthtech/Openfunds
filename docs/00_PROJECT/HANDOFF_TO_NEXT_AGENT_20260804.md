# Handoff to next agent — 2026-08-04

## 1. Repository point of control

```text
REPOSITORY       chainsolutions-wealthtech/Openfunds
WORK_BRANCH      architecture/africafunds-country-indicators-v0.1
START_HEAD_SHA   cce82f3276d408ddb71366f5236c10282f0b6614
EXPECTED_END     one documentation-only commit after START_HEAD_SHA
MAIN_HEAD_SHA    946145e4b33a6289eb340a16bf5c651cb9bbee7c
PR1              OPEN / DRAFT / NOT MERGED
PR2              OPEN / DRAFT / NOT MERGED
```

Resolve the branch head again before any future action.

## 2. Work completed by this intervention

- verified all twelve branch heads and their relation to `main`;
- confirmed the work-branch head had not changed;
- audited PR #1 and PR #2 without modification;
- compared all 13 bootstrap deliverables by blob SHA;
- confirmed all 13 bootstrap deliverables exist identically in the complete branch;
- reconciled PR #2 content;
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

## 4. PR #2 disposition

Exact copies already preserved:

- official source inventory CSV;
- canonical integration matrix CSV.

Still unique and requiring preservation/review:

- complete Africa market/rates/macro source handoff;
- complete non-regression and status rules;
- complete PR1 research exploitation guide.

Do not close PR #2 until those three documents are preserved or rejected with documented rationale.

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
- no active WTI/WTI Bench/ratios/rankings;
- collection-tested snapshots are not histories;
- no invented dates;
- observed and calculated values separate;
- XOF and XAF separate.

## 6. Exact restart point

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

## 8. Verification commands or equivalent connector checks

```text
resolve branch HEAD
compare HEAD with this handoff's END_HEAD_SHA
confirm PR #1 remains draft/open/not merged
confirm PR #2 remains draft/open/not merged
confirm no issues were created by this intervention
inspect changed files against the allowed documentation whitelist
confirm no workflow/code/SQL/data/test change
```

## 9. Ready-to-copy continuation prompt

```text
Continue the Openfunds project from the immutable baseline dated 2026-08-04.
First resolve the current HEAD of architecture/africafunds-country-indicators-v0.1
and compare it with the END_HEAD_SHA recorded in HANDOFF_TO_NEXT_AGENT_20260804.md.

Read the living branch exploitation plan, the eight dated baseline reports, TODO.md, SUIVI.md, DECISIONS.md and the source
registry before proposing any write.

Preserve this order:
OF-ARCH-001 → OF-SOURCE-001 → OF-ARCH-002 → OF-ARCH-003 → OF-ARCH-004.

Do not treat LOCAL_MARKET, INVESTMENT_SCOPE, a migration runner, merge policy,
auto-merge, Fund/SubFund/ShareClass, dates unknown, WTI, WTI Bench or workbook
reproducibility as already decided. Do not create a new branch, modify main,
retarget/merge/close a PR, create issues, or modify code/data/SQL/workflows/tests
unless the user explicitly authorizes a new execution phase.
```
