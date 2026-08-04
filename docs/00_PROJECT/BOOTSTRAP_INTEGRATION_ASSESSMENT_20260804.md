# Bootstrap integration assessment — 2026-08-04

## 1. Scope

Repository: `chainsolutions-wealthtech/Openfunds`  
Bootstrap branch: `architecture/canonical-model-v1-bootstrap`  
Bootstrap head: `136abf71f0825075361f8c7446e19c6f6476a3a5`  
Complete branch: `architecture/africafunds-country-indicators-v0.1`  
Complete branch head at audit start: `cce82f3276d408ddb71366f5236c10282f0b6614`  
Common ancestor between the two branches: `23ce7c7f00206f37eeec50dfccf03fa2cb7505ea`

No branch, pull request, workflow, code, SQL or data file was modified by this assessment.

## 2. Commit-history finding

The bootstrap is 13 commits ahead of `main`. The complete branch and bootstrap are historically divergent: the complete branch is 173 commits ahead and 7 commits behind the bootstrap when compared from their common ancestor.

The connector exposes aggregate comparison metadata and individual commits when a SHA is known, but it does not expose the complete ordered commit list for a non-default branch. Therefore this assessment does **not invent** the ten commit SHAs that were not returned. It audits all 13 bootstrap deliverables at their current tips, plus the three known anchor commits:

- `23ce7c7f00206f37eeec50dfccf03fa2cb7505ea` — uploaded source analysis, common ancestor;
- `14c7f4b839acd59862455d50fd9c2f7d8502077b` — country relationship SQL model, PR #1 recorded base SHA;
- `136abf71f0825075361f8c7446e19c6f6476a3a5` — country relationship validation documentation, current bootstrap head.

## 3. File-level assessment of all 13 bootstrap deliverables

Every current bootstrap blob below has the **same blob SHA** on the complete branch. Consequently, the complete branch already preserves the complete net content of the bootstrap, despite the divergent commit graph.

| BOOTSTRAP_COMMIT | PURPOSE | FILES | BLOB_SHA | STILL_VALID | SUPERSEDED_IN_PR1 | CORRECTED_IN_PR1 | CONFLICTING_DECISION | SAFE_TO_MERGE_ALONE |
|---|---|---|---|---|---|---|---|---|
| `COMMIT_SHA_NOT_EXPOSED / AFRICA_COUNTRIES.csv` | African country routing/reference registry | `data/reference/AFRICA_COUNTRIES.csv` | `1c5d025e1b1b6a874cec54ae0a02ac369aea3b0c` | YES | NO | NO | NONE | NO_REDUNDANT_BASELINE_COMMIT |
| `COMMIT_SHA_NOT_EXPOSED / AFRICA_REGIONS.csv` | Continent and five geographic regions | `data/reference/AFRICA_REGIONS.csv` | `047f06bd1cc2bed0e3dfdb40e9481614bda51e96` | YES | NO | NO | NONE | NO_REDUNDANT_BASELINE_COMMIT |
| `COMMIT_SHA_NOT_EXPOSED / COUNTRY_RELATIONSHIPS.csv` | 266 country relationships | `data/reference/COUNTRY_RELATIONSHIPS.csv` | `56dd5061489b8f6d4e9df644a809a31ad4b014d4` | YES | NO | NO | VALID_FROM_MODEL_OPEN_UNDER_ADR_022 | NO_REDUNDANT_BASELINE_COMMIT |
| `COMMIT_SHA_NOT_EXPOSED / MARKET_ZONES.csv` | UEMOA CEMAC CMA market zones | `data/reference/MARKET_ZONES.csv` | `d8dde508028afdfeb4e290cb450052ea9910e5ba` | YES | NO | NO | LOCAL_MARKET_VS_NATIONAL_REQUIRES_DECISION | NO_REDUNDANT_BASELINE_COMMIT |
| `COMMIT_SHA_NOT_EXPOSED / UPLOADED_SOURCE_ANALYSIS` | Analysis of uploaded matrices and Tunisia source corpus | `docs/00_PROJECT/UPLOADED_SOURCE_ANALYSIS_2026_08_03.md` | `475b3138be0e515769eb2f8ce802f4223996e5ed` | YES | NO | NO | NONE | NO_REDUNDANT_BASELINE_COMMIT |
| `COMMIT_SHA_NOT_EXPOSED / HYBRID_ARCHITECTURE_ADR` | Hybrid canonical API-first Atomic Design architecture | `docs/00_VISION/Architecture_Decision_Hybrid_API_Atomic_Design.md` | `92c3528e631ec9848815c6cf223af71f78f90cbf` | YES | NO | NO | NONE | NO_REDUNDANT_BASELINE_COMMIT |
| `COMMIT_SHA_NOT_EXPOSED / FUND_RELATIONSHIP_MODEL_DOC` | Fund relationship conceptual model | `docs/01_ARCHITECTURE/Fund_Relationship_Information_Model_v0.1.md` | `e1c8efe2d4a071e404445445e505395f50caad86` | YES | NO | NO | FUND_SUBFUND_SHARECLASS_IMPLEMENTATION_OPEN | NO_REDUNDANT_BASELINE_COMMIT |
| `COMMIT_SHA_NOT_EXPOSED / COUNTRY_MARKET_UNIVERSE` | Country-centric market universe | `docs/02_DOMAIN_MODEL/Reference/Country_CountryCentric_Market_Universe.md` | `ed8bd600fb3caaa8c1f621bc61d301b80fd93fda` | YES | NO | NO | LOCAL_MARKET_AND_INVESTMENT_SCOPE_OPEN | NO_REDUNDANT_BASELINE_COMMIT |
| `COMMIT_SHA_NOT_EXPOSED / MOROCCO_PILOT` | Morocco pilot scope | `docs/03_PILOTS/Morocco/Morocco_Pilot_Scope.md` | `2c4ca8f6a635ffb65e54cd7c65f2d40fe444b79d` | YES | NO | NO | METHODOLOGIES_AND_SOURCES_NOT_ACTIVE | NO_REDUNDANT_BASELINE_COMMIT |
| `COMMIT_SHA_NOT_EXPOSED / COUNTRY_RELATIONSHIP_VALIDATION` | Validation rules and relationship counts | `docs/04_GEOGRAPHY/COUNTRY_RELATIONSHIPS_VALIDATION.md` | `85d50ae755990f336ce83dcfe0586466ad23c562` | YES | NO | NO | NATIONAL_TAXONOMY_TEXT_REQUIRES_RECONCILIATION | NO_REDUNDANT_BASELINE_COMMIT |
| `COMMIT_SHA_NOT_EXPOSED / COUNTRY_RELATIONSHIP_MODEL_DOC` | Country relationship domain documentation | `docs/04_GEOGRAPHY/COUNTRY_RELATIONSHIP_MODEL.md` | `5505d477bf54a427931b62138e65d6d11fce3fd0` | YES | NO | NO | DATE_AND_SCOPE_DECISIONS_OPEN | NO_REDUNDANT_BASELINE_COMMIT |
| `COMMIT_SHA_NOT_EXPOSED / COUNTRY_RELATIONSHIP_SQL` | Country relationship SQL proposal | `schemas/reference/002_country_relationships.sql` | `394ee892c9d41e1ca038b1b7b411dbbdc990bb54` | YES_AS_PROPOSAL | NO | NO | VALID_FROM_NOT_NULL_CONFLICT;NOT_PRODUCTION_MIGRATION | NO_REDUNDANT_BASELINE_COMMIT |
| `COMMIT_SHA_NOT_EXPOSED / FUND_RELATIONSHIP_SQL` | Fund taxonomy SQL proposal | `schemas/taxonomy/fund_relationship_information_model_v0.1.sql` | `9881a226660f102d99f2910f819bf0b4efb8fb82` | YES_AS_PROPOSAL | NO | NO | FUND_SUBFUND_SHARECLASS_INCOMPLETE;NOT_PRODUCTION_MIGRATION | NO_REDUNDANT_BASELINE_COMMIT |

## 4. Strategy A

```text
bootstrap → main
then PR #1 → main
```

### Benefits

- Presents the original foundation separately.
- Can be useful if the bootstrap is independently reviewed as a releaseable unit.

### Risks

- The current bootstrap content is already present byte-for-byte in the complete branch.
- A separate merge would create an unnecessary intermediate baseline.
- Proposal SQL contains known open decisions and must not be presented as production migrations.
- The historical divergence can complicate review even though the tip blobs match.
- `main` would temporarily expose an incomplete state without the later documentation, tests, collectors and canonical matrix.

## 5. Strategy B

```text
complete branch → main directly
```

### Benefits

- Produces one coherent reviewed baseline.
- Includes the full documentation, tested collectors, matrix generator, tests and source governance.
- Avoids an intermediate duplicated bootstrap merge.
- Preserves all 13 bootstrap deliverables because their current blob SHAs match.

### Risks

- The pull request is large and requires independent review.
- Critical decisions remain open and must be listed as gates.
- The branch-specific workflow triggers must be reviewed before a later merge.
- A direct merge must not imply production deployment or active WTI/WTI Bench calculations.

## 6. Recommendation

**Recommend `STRATEGY_B`, subject to review and all execution gates.**

The recommendation is based on verified content equality, not an assumption: all 13 bootstrap deliverables have identical tip blob SHAs in the complete branch. No bootstrap merge is required to preserve their current content.

This assessment does not authorize retargeting, merging or closing any pull request.
