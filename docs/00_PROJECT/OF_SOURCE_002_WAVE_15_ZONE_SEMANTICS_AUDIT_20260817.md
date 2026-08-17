# OF-SOURCE-002 — Wave 15 zone semantics audit — 2026-08-17

## Scope

Wave 15 reviews only the residual UEMOA/CEMAC zone relations for which the repository already has explicit rows. It does not infer new country roles and it does not promote the Common Monetary Area (`CMA`) as a monetary union.

## Exact promotion allowlist

```text
UEMOA;MONETARY_UNION;UEMOA;MONETARY_ZONE
UEMOA;SUPRANATIONAL_AUTHORITY;UEMOA;MONETARY_ZONE
CEMAC;MONETARY_UNION;CEMAC;MONETARY_ZONE
CEMAC;SUPRANATIONAL_AUTHORITY;CEMAC;MONETARY_ZONE
BCEAO;INTERBANK_MARKET_OPERATOR;UEMOA;MONETARY_ZONE
BEAC;INTERBANK_MARKET_OPERATOR;CEMAC;MONETARY_ZONE
```

## Evidence and semantic decision

### UEMOA

Primary official evidence:

- https://www.uemoa.int/
- https://www.uemoa.int/organes/la-commission

The institution identifies itself as the `Union Economique et Monétaire Ouest Africaine`. Its Commission is explicitly the executive organ of the Union, exercising powers conferred by the Treaty in the Union's general interest and representing the Commission externally. This supports both the broad canonical `MONETARY_UNION` and `SUPRANATIONAL_AUTHORITY` roles.

### CEMAC

Primary official evidence:

- https://cemac.int/
- https://cemac.int/commission/
- https://cemac.int/traities-conventiosns/

CEMAC identifies itself as the `Communauté Économique et Monétaire de l'Afrique Centrale`, comprising six member states. The official treaty collection includes the convention governing the `Union Monétaire de l'Afrique Centrale (UMAC)`, while the Commission acts as the Community's central executive institution across common-market and economic, monetary and financial policy departments. Within this repository's broad role definition — an organization grouping several countries around a common currency or monetary policy — the existing `CEMAC / MONETARY_UNION` row is semantically acceptable. The Commission/Community also exercises cross-country competence, satisfying `SUPRANATIONAL_AUTHORITY`.

### BCEAO

Primary official evidence:

- https://www.bceao.int/fr/appels-offres/marche-mon%C3%A9taire
- https://www.bceao.int/fr/documents/operations-effectuees-sur-le-marche-interbancaire-de-lumoa-0

BCEAO operates the monetary-policy liquidity auctions, publishes the UMOA interbank-market evolution and the actual interbank operations, and is the central bank for the zone. The canonical `INTERBANK_MARKET_OPERATOR` definition covers an institution or platform of the interbank and monetary market; the existing relationship is therefore supported.

### BEAC

Primary official evidence:

- https://www.beac.int/politique-monetaire/mise-oeuvre-de-politique-monetaire/
- https://www.beac.int/economie-stats/statistiques-marche-monetaire/

BEAC states that the CEMAC money market is organized in two levels: an interbank compartment and BEAC intervention compartments. It calculates the daily weighted interbank rate (TIMP), carries out liquidity interventions and publishes money-market/interbank statistics. This directly supports the existing `INTERBANK_MARKET_OPERATOR` relation.

## Explicit non-promotion: CMA

```text
CMA;MONETARY_UNION;CMA;MONETARY_ZONE
```

The Common Monetary Area is deliberately retained `PENDING`. Its legal/operational structure is a monetary arrangement/area and should not be forced into the stronger canonical `MONETARY_UNION` label without a dedicated role-model decision.

## Mutation rule

For the six allowlisted rows, mutate only:

```text
VALIDATION_STATUS: PENDING -> VALIDATED
SOURCE_NOTE: OFFICIAL_ZONE_SEMANTICS_VERIFIED_2026_08_17_WAVE15
```

No organization, role, scope, relationship role, primary flag or business-validity date may change.

## Expected post-state

Starting from Wave 14's verified state `199 = 189 VALIDATED + 10 PENDING`, this wave should yield:

```text
TOTAL_SCOPE_ROLES: 199
VALIDATED: 195
PENDING: 4
```

Expected residual existing PENDING relations:

```text
EGX;INDEX_PROVIDER;EGYPTE;COUNTRY
NSE;INDEX_PROVIDER;KENYA;COUNTRY
NGX;INDEX_PROVIDER;NIGERIA;COUNTRY
CMA;MONETARY_UNION;CMA;MONETARY_ZONE
```
