# OF-DOC-003 — Réconciliation du socle de gouvernance — 2026-09-10

```text
TASK_ID: OF-DOC-003
LOOP_ID: OF-LOOP-DOC-003-RECONCILIATION-20260910
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
START_HEAD: eeaa07194fcb46fa0cf0859d5061a30ffc5602c0
REFERENCE_MODEL: chainsolutions-wealthtech/Regulatory governance mechanism only
MIGRATION_MODE: ADDITIVE / IMPROVEMENT_ONLY / ZERO_REGRESSION
BUSINESS_RULE_COPY: FORBIDDEN
MAIN_MUTATION: NO
NEW_BRANCH: NO
NEW_PR: NO
PR_RETARGET_OR_MERGE: NO
PRODUCTION_ACTION: NO
```

## Objet

Réconcilier et renforcer le socle de gouvernance d'Openfunds afin qu'un humain ou un agent IA puisse reprendre le projet à partir du dépôt lui-même, sans dépendre de la mémoire d'une conversation et sans importer les règles métier propres au dépôt Regulatory.

Le modèle de référence fournit la discipline de gouvernance, de mémoire persistante, de source de vérité, de non-régression, de Loop Engineering et de Definition of Done. Les autorités métier Openfunds restent propriétaires de leurs données, mappings, migrations, méthodologies et décisions.

## Baseline observée avant écriture

```text
REPOSITORY: chainsolutions-wealthtech/Openfunds
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
START_HEAD: eeaa07194fcb46fa0cf0859d5061a30ffc5602c0
PR_1: DRAFT / OPEN / UNMERGED
PR_BASE: architecture/canonical-model-v1-bootstrap
PRODUCTION_DEPLOYED: NO
GITHUB_RULESETS: NONE_OBSERVED
```

Le dépôt possédait déjà un socle important : `GOVERNANCE.md`, `AGENTS.md`, `00_START_HERE.md`, `SOURCE_OF_TRUTH.md`, `STATUS.md`, `NEXT_ACTION.md`, `LOOP_STATE.md`, `CURRENT_ITERATION.md`, `LOOP_ENGINEERING.md`, `TODO.md`, `SUIVI.md`, `WORK_LOG.md`, `HANDOFF.md`, `CHANGELOG.md`, `DECISIONS.md`, `CLAUDE.md` et des documents de gouvernance sous `docs/`.

La migration n'avait donc pas pour objet de recopier Regulatory, mais de combler les écarts et de réconcilier les autorités existantes.

## Écarts constatés

1. `00_START_HERE.md` et `SOURCE_OF_TRUTH.md` contenaient encore une photographie ancienne autour du 11 août alors que le projet avait progressé jusqu'au 22 août et au-delà.
2. `LOOP_ENGINEERING.md` décrivait la méthode mais ne portait pas encore le contrat opérationnel complet jusqu'à `VERIFY_REMOTE_STATE` et `SELECT_NEXT`.
3. `DEFINITION_OF_DONE.md` n'existait pas à la racine.
4. `STATUS.md` et `NEXT_ACTION.md` indiquaient encore que la CI récente n'était pas observable.
5. La CI est désormais observable et montre un échec réel du workflow `OF-MAP-002 Mapping Registry` sur le parent technique `275ec7a10658cfc5a9f5822eb2315bf01138fc10`.
6. Aucun GitHub Ruleset n'est observé ; l'enforcement natif GitHub reste donc moins fort que la gouvernance déclarative.

## CI réconciliée

```text
WORKFLOW: OF-MAP-002 Mapping Registry
RUN_ID: 32541124896
OBSERVED_HEAD: 275ec7a10658cfc5a9f5822eb2315bf01138fc10
OVERALL: FAILURE
OFFICIAL_CANONICAL_INTEGRATION: PASS
UNIT_PYTHON_3_11: FAILURE
UNIT_PYTHON_3_12: FAILURE
```

Cause observée : le contrat Batch 07 attend `NO_PARENT_CURRENCY_INFERENCE` dans `NOTES` pour la ligne concernée, et cette valeur est absente. La migration documentaire ne modifie ni le test ni les données concernées et ne transforme jamais cet échec en succès documentaire.

## Changements de gouvernance réalisés

### `00_START_HERE.md`

- ordre de lecture obligatoire réconcilié ;
- HEAD résolu dynamiquement ;
- contrôle Git avant écriture ;
- analyse d'impact ;
- règles de non-régression ;
- état CI réellement observé ;
- interdictions de branche/PR/main/production conservées.

### `SOURCE_OF_TRUTH.md`

- hiérarchie explicite des autorités ;
- GitHub comme autorité de l'état Git ;
- dépôt versionné comme mémoire canonique ;
- conversation/agent explicitement non canonique ;
- règle de conflit ;
- distinction authoring, runtime, recherche et preuve ;
- gap Ruleset enregistré.

### `LOOP_ENGINEERING.md`

Contrat détaillé adopté :

```text
DISCOVER
→ BASELINE
→ SELECT
→ IMPACT_ANALYSIS
→ IMPLEMENT_COMPATIBLY
→ VERIFY
→ REGRESSION_CHECK
→ CORRECT_IF_REQUIRED
→ VERIFY_AGAIN
→ PERSIST_STATE
→ COMMIT
→ VERIFY_REMOTE_STATE
→ SELECT_NEXT
```

### `DEFINITION_OF_DONE.md`

Nouveau document racine ajouté avec critères de clôture sur :

- autorité et périmètre ;
- lecture/analyse ;
- implémentation compatible ;
- vérification ;
- non-régression ;
- mémoire persistante ;
- état Git distant ;
- handoff ;
- interdiction de sur-déclarer les statuts.

### `STATUS.md` / `NEXT_ACTION.md`

- état CI corrigé de `PENDING_NOT_OBSERVABLE` vers `FAILURE_KNOWN` ;
- gap GitHub Ruleset explicité ;
- prochaine action technique fixée : réconcilier l'échec Batch 07 sans affaiblir le contrat ;
- Task 4 conservée comme étape suivante après restauration de la CI.

## Non-régression et préservation

Aucun des éléments suivants n'a été modifié par cette tranche :

```text
CODE_METIER
MIGRATIONS_001_039
CANONICAL_MODEL
MAPPING_REGISTRY
REVIEW_OUTCOMES_DATA
TEST_ASSERTIONS
WORKFLOW_LOGIC
PR_BASE
PR_STATE
MAIN
PRODUCTION
REAL_DATA
```

Aucune règle Regulatory relative à des prospectus, AMF-UMOA, sanctions, clauses réglementaires ou `ready_for_submission` n'a été copiée dans Openfunds.

## Gouvernance native GitHub

```text
RULESETS: NONE_OBSERVED
```

Verdict : la gouvernance documentaire et méthodologique peut être forte sans être intégralement enforced par GitHub. Ce gap doit rester visible et être traité dans une future décision/gate administratif distinct ; il ne doit pas être corrigé implicitement au milieu d'une migration documentaire.

## Reprise déterministe

Après cette réconciliation, un nouvel agent doit :

1. lire `00_START_HERE.md` ;
2. résoudre le HEAD distant courant ;
3. lire `GOVERNANCE.md`, `AGENTS.md`, `SOURCE_OF_TRUTH.md`, `STATUS.md`, `NEXT_ACTION.md` ;
4. vérifier la CI réelle ;
5. reprendre par la réparation gouvernée de `OF-MAP-002` Batch 07 ;
6. ne reprendre Task 4 qu'après restauration du contrat existant ;
7. ne toucher ni `main`, ni la structure de PR, ni la production sans gate explicite.

## Verdict de cette tranche

```text
GOVERNANCE_SOCLE: RECONCILED
PERSISTENT_MEMORY: STRENGTHENED
LOOP_ENGINEERING: COMPLETE_CONTRACT_INSTALLED
DEFINITION_OF_DONE: INSTALLED
BUSINESS_REGRESSION_INTRODUCED: NONE_BY_SCOPE
CI_GREEN: NO
CI_FAILURE: PREEXISTING_AND_DOCUMENTED
GITHUB_NATIVE_ENFORCEMENT: GAP_OPEN
PRODUCTION: UNCHANGED / NO
NEXT_ACTION: FIX_OF_MAP_002_BATCH_07_WITHOUT_WEAKENING_CONTRACT
```

Cette tranche ne sera considérée entièrement clôturée qu'après persistance dans les documents de suivi concernés et vérification distante finale du HEAD/PR.
