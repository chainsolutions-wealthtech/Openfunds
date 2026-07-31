# Architecture Decision Record — Hybrid Canonical Platform, API-First and Atomic Design

## Status

Accepted

## Decision date

2026-07-31

## Repository

`chainsolutions-wealthtech/Openfunds`

## Context

The ChainSolutions WealthTech canonical fund data model must become more expressive than openfunds while remaining interoperable with openfunds and other standards. It must support reference data, historical series, documents, events, regulatory datasets, analytics, provenance, validation and future AI use cases.

The platform must also expose all relevant canonical data through APIs and make the same data reusable by frontend applications structured according to Atomic Design.

## Decision

The platform adopts a hybrid polyglot architecture with PostgreSQL as the canonical source of truth.

The architecture combines:

- PostgreSQL for canonical, transactional and referential data;
- bitemporal historisation for business time and system time;
- an immutable business-event journal without requiring full event sourcing;
- object storage for original PDF, Excel, CSV, image, XML and JSON files;
- JSONB for raw, semi-structured and provider-specific payloads;
- derived search, analytics, graph and vector projections;
- API-first contracts for every publishable entity, relation, event and time series;
- frontend consumption through a design system organised according to Atomic Design.

No derived engine may directly alter canonical truth. All mutations must pass through governed application services and validated commands.

## Architectural principles

### 1. Canonical source of truth

PostgreSQL stores the authoritative state of entities, identifiers, relations, histories, sources, mappings and quality decisions.

### 2. API-first

Every domain object must be designed with a stable API representation from the beginning. Database tables are not exposed directly.

The API layer must provide:

- stable resource identifiers;
- versioned contracts;
- explicit field semantics;
- pagination, filtering, sorting and sparse fieldsets;
- temporal queries;
- provenance and quality metadata;
- bulk export and incremental synchronisation;
- access-control enforcement;
- deprecation policies;
- REST and, where useful, GraphQL representations;
- event delivery through webhooks, queues or change feeds when enabled.

### 3. Atomic Design compatibility

The model must support reusable UI components without binding business concepts to a specific frontend framework.

The frontend hierarchy is:

- Atoms: labels, values, badges, icons, dates, currencies, quality indicators, source indicators;
- Molecules: field/value rows, NAV cards, fee rows, identifier groups, status chips, document links;
- Organisms: fund identity panel, share-class panel, NAV chart, performance table, fee table, document centre, corporate-action timeline;
- Templates: fund page, share-class page, management-company page, comparison page, factsheet page;
- Pages: complete instances hydrated from API resources.

Atomic Design is a presentation architecture. Canonical entities remain independent of UI components. Components consume API view models derived from canonical resources.

### 4. Separate write models, canonical models and read models

The architecture distinguishes:

- ingestion models for raw observations;
- validation models for reconciliation and quality workflows;
- canonical models for authoritative data;
- API resource models for external contracts;
- UI view models for specific screens;
- analytical models for calculations and aggregates.

This separation prevents frontend requirements or source-specific formats from polluting the canonical schema.

### 5. Bitemporal history

Material facts must support:

- `valid_from` and `valid_to` for business validity;
- `recorded_at` and `superseded_at` for system knowledge;
- source and validation references;
- version and correction lineage.

### 6. Complete provenance

A published value should be traceable, where applicable, to:

- provider;
- source system;
- URL;
- document;
- file hash;
- worksheet;
- page;
- table;
- row;
- column;
- cell;
- extraction batch;
- parser version;
- transformation rule;
- confidence score;
- validation decision.

### 7. Rebuildable derived systems

Search indexes, analytical stores, graph projections, caches, vector stores and UI-specific materialised views are derived and reconstructible from the canonical database and immutable source artefacts.

## API resource families

The initial API taxonomy includes:

- `/countries`
- `/currencies`
- `/languages`
- `/calendars`
- `/organisations`
- `/management-companies`
- `/fund-groups`
- `/umbrellas`
- `/funds`
- `/sub-funds`
- `/share-classes`
- `/benchmarks`
- `/indices`
- `/portfolios`
- `/holdings`
- `/securities`
- `/issuers`
- `/navs`
- `/aum-observations`
- `/dividends`
- `/performance-observations`
- `/risk-metrics`
- `/fees`
- `/documents`
- `/corporate-actions`
- `/events`
- `/sources`
- `/lineage`
- `/quality-decisions`
- `/mappings`

The exact contracts will be documented through OpenAPI and, where relevant, GraphQL schemas.

## Canonical resource envelope

Every API resource should be capable of exposing a common envelope:

```json
{
  "id": "SC-0000000001",
  "type": "share_class",
  "attributes": {},
  "relationships": {},
  "validity": {
    "valid_from": null,
    "valid_to": null,
    "recorded_at": null,
    "superseded_at": null
  },
  "quality": {
    "status": "validated",
    "confidence_score": 1.0
  },
  "provenance": [],
  "links": {},
  "meta": {
    "schema_version": "0.1.0",
    "resource_version": 1
  }
}
```

This is a conceptual envelope, not yet a frozen wire format.

## Atomic Design mapping rules

1. No atom or molecule may query the database directly.
2. UI components consume typed API clients or server-side application services.
3. A canonical entity may feed several organisms and templates.
4. A single organism may aggregate several API resources.
5. UI-specific labels, ordering and formatting belong to presentation metadata, not core canonical attributes.
6. API responses may offer purpose-built projections, but canonical identifiers and lineage must remain recoverable.
7. Components must support loading, empty, partial, stale, error and restricted-data states.
8. Design tokens remain separate from financial and regulatory data.
9. Accessibility, localisation, currency formatting and date formatting are mandatory cross-cutting concerns.
10. Factsheets, dashboards and comparison screens must reuse the same canonical data and calculation definitions.

## Consequences

### Positive

- one governed source of truth;
- compatibility with multiple standards and clients;
- reusable data across APIs, web applications, mobile applications, reports and AI systems;
- frontend modularity without contaminating the canonical model;
- complete auditability and historical reconstruction;
- progressive scalability through derived specialised stores.

### Trade-offs

- more explicit modelling work;
- strict contract governance;
- need for schema and API version management;
- need to maintain projections and read models;
- stronger testing requirements across database, API and UI layers.

## Non-goals

- exposing physical database tables as public contracts;
- using Atomic Design as a database-modelling method;
- making Openfunds the internal canonical schema;
- adopting full event sourcing for every state change;
- introducing every specialised datastore at project start.

## Implementation sequence

1. Stabilise the metamodel and naming conventions.
2. Define canonical identifiers and bitemporal conventions.
3. Define reference domains.
4. Define organisation, fund, share-class and market-data domains.
5. Define common API resource envelopes and error contracts.
6. Generate initial OpenAPI schemas.
7. Define frontend design tokens and Atomic Design component contracts.
8. Build typed mappings from API resources to UI view models.
9. Add analytical, search, graph and AI projections only when justified by volume and use cases.

## Validation

This decision is approved as a foundational architecture rule for all subsequent modelling work in this repository.
