# Handoff Loop Engineering

## Handoff actif — Openfunds Product Finalization

```text
DATE: 2026-09-10
LOOP_ID: OF-LOOP-PRODUCT-FINALIZATION-001
TASK_STREAM: OF-MAP-002
SUBPROJECT: CANONICAL_FOUNDATION_COMPLETION
STATUS: EN_COURS
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
CURRENT_HEAD_POLICY: RESOLVE_DYNAMICALLY
GOVERNANCE_RECONCILIATION: OF-DOC-003 / COMPLETE_SOCLE_TRANCHE
PR_1: DRAFT / OPEN / UNMERGED
PR_1_BASE: architecture/canonical-model-v1-bootstrap
MIGRATIONS: 001..039
LATEST_MIGRATION: 039_TRACKED_INDEX_DENOMINATION_BASE
CANONICAL_FIELDS: 295
MAPPING_BATCHES: BATCH_01..BATCH_27
MAPPING_ROWS: 93
MAPPED_OPENFUNDS_IDS: 50
UNMAPPED_OPENFUNDS_IDS: 1819
MAPPED_CANONICAL_IDS: 53
LATEST_MAPPING: MAP-000093 / OFST023850
RECENT_REMOTE_CI: FAILURE_KNOWN
RECENT_REMOTE_CI_RUN: 32541124896
RECENT_REMOTE_CI_HEAD: 275ec7a10658cfc5a9f5822eb2315bf01138fc10
GITHUB_RULESETS: NONE_OBSERVED
PRODUCTION_DEPLOYED: NO
```

## Autorités de reprise

1. `00_START_HERE.md`
2. `GOVERNANCE.md`
3. `README.md`
4. `AGENTS.md`
5. `SOURCE_OF_TRUTH.md`
6. `STATUS.md`
7. `NEXT_ACTION.md`
8. `LOOP_STATE.md`
9. `CURRENT_ITERATION.md`
10. `LOOP_ENGINEERING.md`
11. `DEFINITION_OF_DONE.md`
12. `TODO.md` et `SUIVI.md`
13. `DECISIONS.md` / ADR pertinents
14. `WORK_LOG.md`
15. `CHANGELOG.md`
16. `docs/00_PROJECT/OF_DOC_003_GOVERNANCE_RECONCILIATION_20260910.md`
17. spécifications, plans, tests et fichiers directement concernés par la tâche suivante.

Toujours résoudre le HEAD distant courant avant écriture. Les SHA de ce fichier sont des preuves datées et non une substitution à GitHub.

## Gouvernance réconciliée

La tranche `OF-DOC-003` du 2026-09-10 a renforcé le socle de continuité sans copier le métier Regulatory :

- mémoire canonique = dépôt Git versionné ;
- conversations et assistants = non canoniques ;
- ordre de découverte obligatoire ;
- hiérarchie des sources de vérité ;
- Loop Engineering détaillé jusqu'à `VERIFY_REMOTE_STATE` ;
- Definition of Done racine ;
- CI réconciliée avec la preuve réellement observable ;
- aucune branche/PR/main/production modifiée hors branche de contrôle existante.

Rapport : `docs/00_PROJECT/OF_DOC_003_GOVERNANCE_RECONCILIATION_20260910.md`.

## A0 fermé structurellement

Les surfaces machine sont alignées jusqu'à migration 039 / Batch 27 :

- `migrations/manifest.json` : 39 migrations, ordre final 390 ;
- `mapping_manifest.json` : 295 champs, 93 mappings, 50 OF-IDs, 53 cibles ;
- OF-MAP-002 : extension 039 + Batch27 câblés ;
- migration-runner : test 039 + compteur 39 + assertion `denomination_base` ;
- mapping registry : append-only jusqu'à `MAP-000093`.

Cette fermeture structurelle n'est pas une preuve de CI récente verte.

## CI réellement observée

```text
WORKFLOW: OF-MAP-002 Mapping Registry
RUN: 32541124896
HEAD: 275ec7a10658cfc5a9f5822eb2315bf01138fc10
OVERALL: FAILURE
OFFICIAL_CANONICAL_INTEGRATION: PASS
PYTHON_3_11_UNIT: FAILURE
PYTHON_3_12_UNIT: FAILURE
FAILURE: BATCH_07_EXPECTS_NO_PARENT_CURRENCY_INFERENCE_IN_NOTES
```

Ne jamais supprimer ou affaiblir l'assertion pour obtenir du vert. La correction doit être déterminée à partir du contrat, du mapping, de l'historique et des tests.

## Point de reprise exact

```text
NEXT_TASK: Restore OF-MAP-002 Batch 07 contract and remote CI
NEXT_AFTER_GREEN: Task 4 — reason-classified Openfunds review outcomes
NEXT_AFTER_TASK_4: A1 Identity / Names / Legal Structure
NEXT_MIGRATION_NUMBER_IF_AND_ONLY_IF_REQUIRED: 040
```

### Task 4 — surfaces déjà présentes

```text
data/openfunds/mapping/v2.13.0/REVIEW_OUTCOMES.csv
scripts/validate_openfunds_review_outcomes.py
tests/test_openfunds_review_outcomes.py
```

`REVIEW_OUTCOMES.csv` contient actuellement son en-tête gouverné. Ne créer aucune ligne sans revue réelle et preuve correspondante.

Le registre doit rester sparse et compléter `MAPPING_REGISTRY.csv`, pas le dupliquer. Les IDs mappés restent dérivés du registre existant.

Allowed outcomes :

```text
MAPPED_CANONICAL
MAPPED_DERIVED
NO_CANONICAL_EQUIVALENT
DEFERRED_NOT_REQUIRED_FOR_PRODUCT
GATED_VENDOR_OR_LICENSE
TO_CONFIRM
```

### Task 4 — tests obligatoires

Le validator doit refuser : doublon OF-ID, OF-ID inconnu, outcome invalide, reason code absent sur un outcome non mappé et SHA source différent de la source officielle verrouillée.

Le calcul fusionné doit produire au minimum : mapped, reviewed nonmapped/deferred, vendor gated, to-confirm, unreviewed et total officiel 1869.

## Invariants actifs

- ne jamais fabriquer des lignes `UNMAPPED` ;
- `NULL != 0` ;
- aucune date/devise/valeur synthétique ;
- benchmark ≠ tracked index ;
- lifecycle ≠ investment status ;
- ETF Share Class ≠ passive Fund ;
- vendor identifiers gated jusqu'à clearance ;
- RIC case-preserving ;
- historique migration/mapping immuable ;
- aucune migration 040 avant audit officiel démontrant un manque canonique réel ;
- `IMPLEMENTED != REMOTELY_GREEN` ;
- `COMMIT_CREATED != LOOP_VERIFIED`.

## Blockers externes

```text
GITHUB_NATIVE_RULESET       NONE_OBSERVED
PERSISTENT_PRODUCTION_DB    NOT_CONFIGURED
IMMUTABLE_RAW_STORE         NOT_CONFIGURED
COMPLETE_HISTORIES          NOT_LOADED
SEDOL_RUNTIME               LICENSING_CLEARANCE_REQUIRED
BLOOMBERG_RIC_RUNTIME       PROPRIETARY_USAGE_REVIEW_REQUIRED
RFR_MAR_WTI                 NOT_FULLY_VALIDATED_OR_ACTIVE
PRODUCTION_API_UI           NOT_IMPLEMENTED
PRODUCTION_DEPLOY           NOT_CONFIGURED
```

---

## Handoff historique — OF-LOOP-SOURCE-002

Le handoff institutionnel précédent reste historique et ses rapports restent valides dans leur périmètre. Son dernier snapshot vérifié était Wave 03, run `31595575537`, avec Wave 04 en audit lecture seule. Cette boucle n'est plus la prochaine action globale du projet mais ne doit pas être supprimée ni réécrite rétroactivement.
