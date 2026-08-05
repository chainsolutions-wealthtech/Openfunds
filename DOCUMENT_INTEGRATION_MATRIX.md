# Matrice d’intégration documentaire

```text
TASK_ID: OF-DOC-003
LOOP_ID: OF-LOOP-DOC-003
KIT_VERSION: 1.0.0
KIT_MARKDOWN_FILES: 176
CONTROL_HEAD_AT_AUDIT: 3c54c54733e116f35ff63a0759c921afd58c57a6
```

Cette matrice a été décidée avant la création des chemins du kit. Légende : `EE` = `ENRICH_EXISTING`, `CC` = `CREATE_CANONICAL`, `CI` = `CREATE_INDEX`, `CA` = `CREATE_ADAPTER`, `CR` = `CREATE_REGISTER`, `CT` = `CREATE_TEMPLATE`, `CO` = `CREATE_CONDITIONAL`. `self` signifie que le nouveau chemin est son autorité après validation ; `hist` impose la conservation du contenu historique ; `inv` impose les invariants et preuves Openfunds. Applicabilité : `A` active, `C` conditionnelle.

| Fichier du kit | Correspondance existante | Action | Canonique final | Contenu à préserver | Risque de duplication | Applicabilité | Statut |
|---|---|---|---|---|---|---|---|
| `.github/ISSUE_TEMPLATE/bug_report.md` | — | CT | self | inv | L | A | CREATE |
| `.github/ISSUE_TEMPLATE/documentation.md` | — | CT | self | inv | L | A | CREATE |
| `.github/ISSUE_TEMPLATE/feature_request.md` | — | CT | self | inv | L | A | CREATE |
| `.github/ISSUE_TEMPLATE/incident.md` | — | CT | self | inv | L | A | CREATE |
| `.github/PULL_REQUEST_TEMPLATE.md` | — | CT | self | inv | L | A | CREATE |
| `.github/copilot-instructions.md` | `AGENTS.md` | CA | `AGENTS.md` | inv | H | C | ADAPTER |
| `00_START_HERE.md` | — | CC | self | inv | L | A | CREATE |
| `ACCEPTANCE_CRITERIA.md` | — | CC | self | inv | L | A | CREATE |
| `AGENTS.md` | — | CC | self | inv | L | A | CREATE |
| `ASSUMPTIONS.md` | — | CR | self | inv | L | A | CREATE |
| `BACKLOG.md` | `TODO.md` | CR | `TODO.md` | hist | H | A | VIEW |
| `BOOTSTRAP_CHECKLIST.md` | — | CC | self | inv | L | A | CREATE |
| `CHANGELOG.md` | `CHANGELOG.md` | EE | `CHANGELOG.md` | hist | H | A | ENRICH |
| `CLAUDE.md` | `AGENTS.md` | CA | `AGENTS.md` | inv | H | C | ADAPTER |
| `CONSTRAINTS.md` | — | CC | self | inv | L | A | CREATE |
| `CURRENT_ITERATION.md` | — | CC | self | inv | L | A | CREATE |
| `DECISIONS.md` | `DECISIONS.md` | EE | `DECISIONS.md` | hist | H | A | ENRICH |
| `DEPENDENCIES.md` | — | CR | self | inv | L | A | CREATE |
| `DOCUMENT_INDEX.md` | — | CR | self | inv | L | A | CREATE |
| `FILES_CATALOG.md` | — | CR | self | inv | L | A | CREATE |
| `GEMINI.md` | `AGENTS.md` | CA | `AGENTS.md` | inv | H | C | ADAPTER |
| `GLOSSARY.md` | — | CR | self | inv | L | A | CREATE |
| `HANDOFF.md` | — | CC | self | inv | L | A | CREATE |
| `LESSONS_LEARNED.md` | — | CR | self | inv | L | A | CREATE |
| `LOOP_CONTRACT.md` | — | CC | self | inv | L | A | CREATE |
| `LOOP_ENGINEERING.md` | — | CC | self | inv | L | A | CREATE |
| `LOOP_ENGINEERING_MASTER_STANDARD.md` | — | CC | self | inv | L | A | CREATE |
| `LOOP_STATE.md` | — | CC | self | inv | L | A | CREATE |
| `MANIFEST.md` | — | CR | self | inv | L | A | CREATE |
| `NEXT_ACTION.md` | — | CC | self | inv | L | A | CREATE |
| `NON_GOALS.md` | — | CC | self | inv | L | A | CREATE |
| `OPEN_QUESTIONS.md` | — | CR | self | inv | L | A | CREATE |
| `PROJECT_BRIEF.md` | `README.md` | CC | self | inv | M | A | CREATE |
| `PROJECT_CHARTER.md` | — | CC | self | inv | L | A | CREATE |
| `PROJECT_CONTEXT.md` | — | CC | self | inv | L | A | CREATE |
| `PROJECT_START_PROMPT.md` | — | CC | self | inv | L | A | CREATE |
| `README.md` | `README.md` | EE | `README.md` | hist | H | A | ENRICH |
| `REQUIREMENTS.md` | — | CC | self | inv | L | A | CREATE |
| `RISKS.md` | — | CR | self | inv | L | A | CREATE |
| `ROADMAP.md` | `ROADMAP.md` | EE | `ROADMAP.md` | hist | H | A | ENRICH |
| `SCOPE.md` | — | CC | self | inv | L | A | CREATE |
| `SECURITY.md` | — | CC | self | inv | L | A | CREATE |
| `SOURCE_OF_TRUTH.md` | — | CC | self | inv | L | A | CREATE |
| `STATUS.md` | — | CC | self | inv | L | A | CREATE |
| `SUCCESS_CRITERIA.md` | — | CC | self | inv | L | A | CREATE |
| `TODO.md` | `TODO.md` | EE | `TODO.md` | hist | H | A | ENRICH |
| `WORK_LOG.md` | — | CR | self | inv | L | A | CREATE |
| `docs/01-governance/AUDIT_TRAIL.md` | `SUIVI.md` | CR | self | hist | M | A | CREATE |
| `docs/01-governance/CHANGE_MANAGEMENT.md` | `GOVERNANCE.md` | CC | self | inv | M | A | CREATE |
| `docs/01-governance/DECISION_PROCESS.md` | `DECISIONS.md` | CI | `DECISIONS.md` | hist | H | A | INDEX |
| `docs/01-governance/DEFINITION_OF_DONE.md` | — | CC | self | inv | L | A | CREATE |
| `docs/01-governance/DEFINITION_OF_READY.md` | — | CC | self | inv | L | A | CREATE |
| `docs/01-governance/DOCUMENTATION_POLICY.md` | `GOVERNANCE.md` | CC | self | inv | M | A | CREATE |
| `docs/01-governance/ESCALATION_POLICY.md` | — | CO | self | inv | L | C | CREATE |
| `docs/01-governance/EXCEPTION_REGISTER.md` | — | CR | self | inv | L | A | CREATE |
| `docs/01-governance/OWNERSHIP.md` | — | CC | self | inv | L | A | CREATE |
| `docs/01-governance/PROJECT_RULES.md` | `GOVERNANCE.md` | CI | `GOVERNANCE.md` | hist | H | A | INDEX |
| `docs/01-governance/RACI.md` | — | CO | self | inv | L | C | CREATE |
| `docs/02-product/FEEDBACK_POLICY.md` | — | CO | self | inv | L | C | CREATE |
| `docs/02-product/PERSONAS.md` | — | CO | self | inv | L | C | CREATE |
| `docs/02-product/PRIORITIZATION.md` | `TODO.md` | CC | self | inv | M | A | CREATE |
| `docs/02-product/PRODUCT_VISION.md` | `README.md` | CC | self | inv | M | A | CREATE |
| `docs/02-product/RELEASE_CRITERIA.md` | — | CC | self | inv | L | A | CREATE |
| `docs/02-product/USER_STORIES.md` | — | CC | self | inv | L | A | CREATE |
| `docs/02-product/USE_CASES.md` | `README.md` | CC | self | inv | M | A | CREATE |
| `docs/02-product/VALIDATION_PLAN.md` | — | CC | self | inv | L | A | CREATE |
| `docs/03-architecture/API_CONTRACTS.md` | — | CO | self | inv | L | C | CREATE |
| `docs/03-architecture/ARCHITECTURE.md` | `ARCHITECTURE.md` | CI | `ARCHITECTURE.md` | hist | H | A | INDEX |
| `docs/03-architecture/ARCHITECTURE_REVIEW_CHECKLIST.md` | `ARCHITECTURE.md` | CC | self | inv | M | A | CREATE |
| `docs/03-architecture/COMPONENTS.md` | `ARCHITECTURE.md` | CC | self | inv | M | A | CREATE |
| `docs/03-architecture/DATA_FLOW.md` | `ARCHITECTURE.md` | CO | self | inv | M | C | CREATE |
| `docs/03-architecture/DATA_MODEL.md` | `DATA_MODEL.md` | CI | `DATA_MODEL.md` | hist | H | A | INDEX |
| `docs/03-architecture/INTEGRATIONS.md` | — | CO | self | inv | L | C | CREATE |
| `docs/03-architecture/INTERFACES.md` | `ARCHITECTURE.md` | CC | self | inv | M | A | CREATE |
| `docs/03-architecture/SYSTEM_CONTEXT.md` | `README.md + ARCHITECTURE.md` | CI | `README.md + ARCHITECTURE.md` | hist | H | A | INDEX |
| `docs/03-architecture/TECHNICAL_DEBT.md` | `TODO.md` | CR | self | inv | M | A | CREATE |
| `docs/04-development/BRANCH_POLICY.md` | plan des branches | CC | self | inv | M | A | CREATE |
| `docs/04-development/CODE_REVIEW.md` | — | CC | self | inv | L | A | CREATE |
| `docs/04-development/CODING_STANDARDS.md` | — | CC | self | inv | L | A | CREATE |
| `docs/04-development/COMMIT_CONVENTION.md` | — | CC | self | inv | L | A | CREATE |
| `docs/04-development/DEPENDENCY_MANAGEMENT.md` | — | CC | self | inv | L | A | CREATE |
| `docs/04-development/FEATURE_FLAGS.md` | — | CO | self | inv | L | C | CREATE |
| `docs/04-development/GIT_WORKFLOW.md` | plan des branches | CC | self | inv | M | A | CREATE |
| `docs/04-development/LOCAL_SETUP.md` | `README.md` | CC | self | inv | M | A | CREATE |
| `docs/04-development/MIGRATION_POLICY.md` | `ADR-028` | CO | self | inv | M | C | CREATE |
| `docs/04-development/NAMING_CONVENTIONS.md` | `ARCHITECTURE.md` | CC | self | inv | M | A | CREATE |
| `docs/04-development/PR_POLICY.md` | plan des branches | CC | self | inv | M | A | CREATE |
| `docs/04-development/REPOSITORY_STRUCTURE.md` | `README.md` | CC | self | inv | M | A | CREATE |
| `docs/05-quality/ACCESSIBILITY.md` | — | CO | self | inv | L | C | CREATE |
| `docs/05-quality/BUG_POLICY.md` | — | CC | self | inv | L | A | CREATE |
| `docs/05-quality/PERFORMANCE_TESTING.md` | — | CO | self | inv | L | C | CREATE |
| `docs/05-quality/QUALITY_GATES.md` | `QUALITY_RULES.md` | CC | self | inv | M | A | CREATE |
| `docs/05-quality/REGRESSION_POLICY.md` | `QUALITY_RULES.md` | CC | self | inv | M | A | CREATE |
| `docs/05-quality/RELEASE_CHECKLIST.md` | — | CC | self | inv | L | A | CREATE |
| `docs/05-quality/SECURITY_TESTING.md` | — | CO | self | inv | L | C | CREATE |
| `docs/05-quality/STATIC_ANALYSIS.md` | — | CC | self | inv | L | A | CREATE |
| `docs/05-quality/TEST_DATA.md` | — | CC | self | inv | L | A | CREATE |
| `docs/05-quality/TEST_MATRIX.md` | `QUALITY_RULES.md` | CR | self | inv | M | A | CREATE |
| `docs/05-quality/TEST_STRATEGY.md` | `QUALITY_RULES.md` | CI | `QUALITY_RULES.md` | hist | H | A | INDEX |
| `docs/05-quality/VALIDATION_PROTOCOL.md` | `QUALITY_RULES.md` | CC | self | inv | M | A | CREATE |
| `docs/06-delivery/BUILD.md` | — | CC | self | inv | L | A | CREATE |
| `docs/06-delivery/CI_CD.md` | workflows existants | CC | self | inv | M | A | CREATE |
| `docs/06-delivery/DEPLOYMENT.md` | — | CO | self | inv | L | C | CREATE |
| `docs/06-delivery/DEPRECATION.md` | — | CO | self | inv | L | C | CREATE |
| `docs/06-delivery/ENVIRONMENTS.md` | — | CC | self | inv | L | A | CREATE |
| `docs/06-delivery/HOTFIX.md` | — | CO | self | inv | L | C | CREATE |
| `docs/06-delivery/PRODUCTION_STATE.md` | — | CO | self | inv | L | C | CREATE |
| `docs/06-delivery/RELEASE_PROCESS.md` | — | CC | self | inv | L | A | CREATE |
| `docs/06-delivery/ROLLBACK.md` | — | CO | self | inv | L | C | CREATE |
| `docs/06-delivery/VERSIONING.md` | — | CC | self | inv | L | A | CREATE |
| `docs/07-operations/ALERTING.md` | — | CO | self | inv | L | C | CREATE |
| `docs/07-operations/BACKUP_RESTORE.md` | — | CO | self | inv | L | C | CREATE |
| `docs/07-operations/DISASTER_RECOVERY.md` | — | CO | self | inv | L | C | CREATE |
| `docs/07-operations/INCIDENT_RESPONSE.md` | — | CO | self | inv | L | C | CREATE |
| `docs/07-operations/MAINTENANCE.md` | — | CO | self | inv | L | C | CREATE |
| `docs/07-operations/MONITORING.md` | — | CO | self | inv | L | C | CREATE |
| `docs/07-operations/OBSERVABILITY.md` | — | CO | self | inv | L | C | CREATE |
| `docs/07-operations/POSTMORTEM_TEMPLATE.md` | — | CT | self | inv | L | C | CREATE |
| `docs/07-operations/RUNBOOK.md` | — | CO | self | inv | L | C | CREATE |
| `docs/07-operations/TROUBLESHOOTING.md` | — | CO | self | inv | L | C | CREATE |
| `docs/08-security/ACCESS_CONTROL.md` | `SECURITY.md` | CC | self | inv | M | A | CREATE |
| `docs/08-security/PRIVACY.md` | — | CO | self | inv | L | C | CREATE |
| `docs/08-security/SECRETS_MANAGEMENT.md` | `SECURITY.md` | CC | self | inv | M | A | CREATE |
| `docs/08-security/SECURITY_INCIDENT.md` | `SECURITY.md` | CO | self | inv | M | C | CREATE |
| `docs/08-security/SECURITY_REVIEW_CHECKLIST.md` | `SECURITY.md` | CC | self | inv | M | A | CREATE |
| `docs/08-security/THREAT_MODEL.md` | — | CO | self | inv | L | C | CREATE |
| `docs/08-security/VULNERABILITY_MANAGEMENT.md` | `SECURITY.md` | CC | self | inv | M | A | CREATE |
| `docs/09-loop/DRIFT_DETECTION.md` | — | CC | self | inv | L | A | CREATE |
| `docs/09-loop/EXPERIMENT_REGISTER.md` | — | CR | self | inv | L | A | CREATE |
| `docs/09-loop/FAILURE_REGISTER.md` | — | CR | self | inv | L | A | CREATE |
| `docs/09-loop/FEEDBACK_LOOP.md` | — | CC | self | inv | L | A | CREATE |
| `docs/09-loop/HYPOTHESIS_REGISTER.md` | `ASSUMPTIONS.md` | CR | self | inv | M | A | CREATE |
| `docs/09-loop/ITERATION_LOG.md` | `WORK_LOG.md` | CR | self | inv | M | A | CREATE |
| `docs/09-loop/ITERATION_PROTOCOL.md` | `LOOP_ENGINEERING.md` | CC | self | inv | M | A | CREATE |
| `docs/09-loop/LEARNING_REGISTER.md` | `LESSONS_LEARNED.md` | CR | self | inv | M | A | CREATE |
| `docs/09-loop/LOOP_HEALTH_CHECK.md` | `LOOP_STATE.md` | CC | self | inv | M | A | CREATE |
| `docs/09-loop/METRICS.md` | — | CC | self | inv | L | A | CREATE |
| `docs/09-loop/RESTART_PROTOCOL.md` | `HANDOFF.md` | CC | self | inv | M | A | CREATE |
| `docs/09-loop/RETROSPECTIVE.md` | `LESSONS_LEARNED.md` | CC | self | inv | M | A | CREATE |
| `docs/09-loop/ROOT_CAUSE_REGISTER.md` | — | CR | self | inv | L | A | CREATE |
| `docs/09-loop/STOP_CONDITIONS.md` | `LOOP_CONTRACT.md` | CC | self | inv | M | A | CREATE |
| `docs/10-ai/AI_CAPABILITIES.md` | `AGENTS.md` | CC | self | inv | M | A | CREATE |
| `docs/10-ai/AI_CONTEXT.md` | `PROJECT_CONTEXT.md` | CC | self | inv | M | A | CREATE |
| `docs/10-ai/AI_GOVERNANCE.md` | `AGENTS.md` | CC | self | inv | M | A | CREATE |
| `docs/10-ai/AI_HANDOFF.md` | `HANDOFF.md` | CC | self | inv | M | A | CREATE |
| `docs/10-ai/AI_OPERATING_RULES.md` | `AGENTS.md` | CI | `AGENTS.md` | hist | H | A | INDEX |
| `docs/10-ai/AI_REVIEW_POLICY.md` | `AGENTS.md` | CC | self | inv | M | A | CREATE |
| `docs/10-ai/AUTONOMY_LEVELS.md` | `AGENTS.md` | CC | self | inv | M | A | CREATE |
| `docs/10-ai/HUMAN_APPROVAL_MATRIX.md` | `AGENTS.md` | CC | self | inv | M | A | CREATE |
| `docs/10-ai/PROMPT_CATALOG.md` | — | CO | self | inv | L | C | CREATE |
| `docs/10-ai/PROMPT_CHANGELOG.md` | — | CO | self | inv | L | C | CREATE |
| `docs/10-ai/TOOL_POLICY.md` | `AGENTS.md` | CC | self | inv | M | A | CREATE |
| `docs/11-templates/CHANGE_REQUEST_TEMPLATE.md` | — | CT | self | inv | L | A | CREATE |
| `docs/11-templates/EXPERIMENT_TEMPLATE.md` | — | CT | self | inv | L | A | CREATE |
| `docs/11-templates/HANDOFF_TEMPLATE.md` | — | CT | self | inv | L | A | CREATE |
| `docs/11-templates/POSTMORTEM_TEMPLATE.md` | — | CT | self | inv | L | A | CREATE |
| `docs/11-templates/PR_DESCRIPTION_TEMPLATE.md` | — | CT | self | inv | L | A | CREATE |
| `docs/11-templates/RETROSPECTIVE_TEMPLATE.md` | — | CT | self | inv | L | A | CREATE |
| `docs/11-templates/RUNBOOK_TEMPLATE.md` | — | CT | self | inv | L | A | CREATE |
| `docs/11-templates/TASK_TEMPLATE.md` | — | CT | self | inv | L | A | CREATE |
| `docs/11-templates/TECH_SPEC_TEMPLATE.md` | — | CT | self | inv | L | A | CREATE |
| `docs/12-optional/AI_MODEL_RISK.md` | — | CO | self | inv | L | C | CREATE |
| `docs/12-optional/COMPLIANCE.md` | — | CO | self | inv | L | C | CREATE |
| `docs/12-optional/DATABASE.md` | — | CO | self | inv | L | C | CREATE |
| `docs/12-optional/DATA_DICTIONARY.md` | `DATA_DICTIONARY.md` | CI | `DATA_DICTIONARY.md` | hist | H | A | INDEX |
| `docs/12-optional/DATA_LINEAGE.md` | `DATA_MODEL.md + SOURCE_REGISTRY.md + QUALITY_RULES.md` | CI | sources listées | hist | H | A | INDEX |
| `docs/12-optional/DATA_QUALITY.md` | `QUALITY_RULES.md` | CI | `QUALITY_RULES.md` | hist | H | A | INDEX |
| `docs/12-optional/LEGAL_NOTICES.md` | — | CO | self | inv | L | C | CREATE |
| `docs/12-optional/LOCALIZATION.md` | — | CO | self | inv | L | C | CREATE |
| `docs/12-optional/MIGRATIONS.md` | `migrations/README.md + ADR-028` | CI | sources listées | hist | H | A | INDEX |
| `docs/12-optional/MOBILE.md` | — | CO | self | inv | L | C | CREATE |
| `docs/12-optional/RETENTION.md` | — | CO | self | inv | L | C | CREATE |
| `docs/12-optional/SLA_SLO.md` | — | CO | self | inv | L | C | CREATE |
| `docs/12-optional/THIRD_PARTY_SERVICES.md` | — | CO | self | inv | L | C | CREATE |
| `docs/adr/ADR-0000-template.md` | `DECISIONS.md` | CT | self | inv | M | A | CREATE |
| `docs/adr/README.md` | `DECISIONS.md` | CI | `DECISIONS.md` | hist | H | A | INDEX |

## Décision globale

Tous les chemins sont applicables physiquement. Les chemins `CO` restent `CONDITIONAL_NOT_ACTIVE`; leur présence n'active aucune capacité. Les cinq documents racine déjà présents sont enrichis sans suppression. Les index ne doivent jamais diverger de leurs sources canoniques.