# OF-SOURCE-002 — Wave 12 INDEX_PROVIDER audit

Date: 2026-08-17
Branch: `architecture/africafunds-country-indicators-v0.1`
Status: `CLOSED_ALLOWLIST_READY_FOR_TDD_RED`

## Objective

Review the nine remaining `INDEX_PROVIDER` relations under a stricter gate than institutional exchange identity.

`STOCK_EXCHANGE` and `INDEX_PROVIDER` are intentionally distinct roles. A validated exchange operator must not be promoted as an index provider unless a current primary official source demonstrates calculation, management, administration or publication of a named index or index family.

## Pre-state

```text
ORGANIZATION_SCOPE_ROLES: 199
VALIDATED: 174
PENDING: 25
PENDING_INDEX_PROVIDER: 9
```

Pending index-provider candidates before Wave 12:

```text
JSE                  | INDEX_PROVIDER | AFRIQUE_DU_SUD | COUNTRY
EGX                  | INDEX_PROVIDER | EGYPTE          | COUNTRY
GSE                  | INDEX_PROVIDER | GHANA           | COUNTRY
NSE                  | INDEX_PROVIDER | KENYA           | COUNTRY
CASABLANCA_BOURSE    | INDEX_PROVIDER | MAROC           | COUNTRY
NGX                  | INDEX_PROVIDER | NIGERIA         | COUNTRY
BVMT                 | INDEX_PROVIDER | TUNISIE         | COUNTRY
BVMAC                | INDEX_PROVIDER | CEMAC           | MONETARY_ZONE
BRVM                 | INDEX_PROVIDER | UEMOA           | MONETARY_ZONE
```

## Closed Wave 12 promotion allowlist

Only four existing tuples are authorized for the Wave 12 write gate:

```text
GSE               | INDEX_PROVIDER | GHANA | COUNTRY
CASABLANCA_BOURSE | INDEX_PROVIDER | MAROC | COUNTRY
BRVM              | INDEX_PROVIDER | UEMOA | MONETARY_ZONE
BVMAC             | INDEX_PROVIDER | CEMAC | MONETARY_ZONE
```

No organization, role, scope or relationship identity may be created, deleted or retargeted.

## Primary official evidence

### Ghana Stock Exchange — GSE

Official source:

```text
https://gse.com.gh/overview/
```

The Ghana Stock Exchange official overview documents the `GSE Composite Index (GSE-CI)` and `GSE Financial Stocks Index (GSE-FSI)` and describes their calculation rules, constituents, weighting methodology, base date and base index value.

Conclusion:

```text
GSE / INDEX_PROVIDER / GHANA = PROMOTABLE
```

The evidence is specific to GSE index calculation and is stronger than mere exchange identity.

### Casablanca Stock Exchange — CASABLANCA_BOURSE

Official source:

```text
https://www.casablanca-bourse.com/en/marche-du-cache/indices
```

The official index page explicitly states that the Casablanca Stock Exchange is the **Manager of the Casablanca Stock Exchange Indexes**, is responsible for daily management, and that the Index Manager ensures integrity, completeness, quality and accuracy of information related to composition, calculation, publication and adjustment of the indexes.

Conclusion:

```text
CASABLANCA_BOURSE / INDEX_PROVIDER / MAROC = PROMOTABLE
```

### BRVM — UEMOA

Official sources:

```text
https://www.brvm.org/fr/indices
https://www.brvm.org/fr/node/882187
```

The BRVM official site publishes the live BRVM index family, including BRVM 30, BRVM Composite, BRVM Prestige, sector indexes and total-return indexes. Its official communication on the 2023 index reorganization documents the introduction and composition principles of BRVM Prestige and BRVM 30 alongside BRVM Composite.

Conclusion:

```text
BRVM / INDEX_PROVIDER / UEMOA = PROMOTABLE
```

The scope remains `UEMOA / MONETARY_ZONE`; it must not be duplicated nationally.

### BVMAC — CEMAC

Official source:

```text
https://www.bvm-ac.org/echos-du-marche/avis-n059-2023-bvmac-dg-relatif-au-lancement-de-lindice-boursier-de-la-bvmac/
```

BVMAC's official notice states that the exchange will publish its first composite stock index, `BVMAC All Share Index`, and specifies the investment universe, base value, free-float weighting method, publication frequency and scientific-committee governance.

Conclusion:

```text
BVMAC / INDEX_PROVIDER / CEMAC = PROMOTABLE
```

The scope remains `CEMAC / MONETARY_ZONE`.

## Candidates deliberately held PENDING

### JSE / AFRIQUE_DU_SUD

The FTSE/JSE family involves a partnership with FTSE Russell and benchmark-administrator responsibilities can belong to FTSE Russell for parts of the series. The existing singular canonical role `INDEX_PROVIDER` is therefore too coarse to promote without a joint-provider/administrator semantic review.

Status:

```text
HOLD_PENDING_ROLE_MODEL_REVIEW
```

### EGX / EGYPTE

The official EGX domain exposes index-methodology resources, but direct content retrieval in the current audit was blocked/rejected. Exchange identity is already validated; index-provider responsibility remains insufficiently auditable for promotion in this wave.

Status:

```text
HOLD_PENDING_DIRECT_METHOD_DOCUMENT_VERIFICATION
```

### NSE / KENYA

No sufficiently direct current primary evidence establishing the exact index-provider/administrator responsibility was closed during this pass.

Status:

```text
HOLD_PENDING_PRIMARY_INDEX_PROVIDER_EVIDENCE
```

### NGX / NIGERIA

Wave 11 resolved the legal identity of Nigerian Exchange Limited as the securities exchange, distinct from Nigerian Exchange Group Plc. That result does not by itself establish the exchange as the canonical primary `INDEX_PROVIDER` for the intended index series.

Status:

```text
HOLD_PENDING_INDEX_ADMINISTRATION_EVIDENCE
```

### BVMT / TUNISIE

The official BVMT site publishes TUNINDEX/TUNINDEX20 information, but the current pass has not yet closed a methodology/administrator proof strong enough for the canonical provider role.

Status:

```text
HOLD_PENDING_INDEX_METHOD_GOVERNANCE_EVIDENCE
```

## TDD write gate

Before mutation:

1. add a Wave 12 test containing only the four authorized tuples;
2. require each tuple to exist exactly once;
3. observe RED because all four remain `PENDING` / old source notes;
4. all Waves 01–11 must remain green;
5. only after the exact RED is observed may the closed promotion workflow run.

Authorized mutable columns:

```text
VALIDATION_STATUS
SOURCE_NOTE
```

Required Wave 12 source note:

```text
OFFICIAL_INDEX_PROVIDER_VERIFIED_2026_08_17_WAVE12
```

Expected post-state if all four promotions pass:

```text
ORGANIZATION_SCOPE_ROLES: 199
VALIDATED: 178
PENDING: 21
PENDING_INDEX_PROVIDER: 5
```

No benchmark methodology, licence compatibility, benchmark selection or WTI activation follows automatically from validating the identity of an index provider.
