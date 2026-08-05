# MODELE DE DONNEES CANONIQUE

## 1. OBJET

Ce document décrit les domaines, entités et relations cibles. Il distingue le modèle accepté, les brouillons SQL et les composants réellement peuplés.

## 2. DOMAINES PRINCIPAUX

| Domaine | Entités principales | Etat |
|---|---|---|
| Géographie | Continent, Region, Country, MarketZone | référentiels présents |
| Devise | Currency, FxPair, FxObservation | référentiel + pilote FX |
| Organisation | Organization, Role, ScopeRole | partiellement peuplé |
| Source | Endpoint, ProviderSeries, CollectionSpecification, Run, Artifact | partiel, FX opérationnel |
| Fonds | FundGroup, Umbrella, Fund, SubFund, ShareClass | modèle final non stabilisé |
| Identité | Identifier, Name, Alias, LegalIdentity | à compléter |
| Services | ManagementCompany, Depositary, Administrator, Auditor, Distributor | à modéliser complètement |
| Taxonomie | AssetClass, SubAssetClass, Category, Membership, PeerGroup | brouillon SQL |
| Références | ReferenceBlock, ReferenceRole, Benchmark, Index | brouillon SQL |
| Documents | Document, Version, ExtractionRecord | modèle source partiel |
| Evénements | CorporateAction, LegalEvent, ChangeEvent | à construire |
| Séries fonds | NAV, AUM, Dividend, Flow | NAV en brouillon, aucune donnée intégrée |
| Portefeuille | Portfolio, Holding, Security, Issuer | absent |
| Analytique | Return, RiskMetric, Rating, Ranking | absent |
| Pays | IndicatorDomain, IndicatorDefinition, Applicability, StatisticalObservation | proposition D00-D17 |
| Qualité | Rule, ValidationDecision, Conflict, Confidence | partiel |
| Mapping | ExternalStandard, ExternalField, FieldMapping | absent |

## 3. IDENTITE FONDS CIBLE

```text
FUND_GROUP / SPONSOR
→ LEGAL_UMBRELLA_OR_FUND
→ SUBFUND_OR_PORTFOLIO
→ SHARE_CLASS
```

Le modèle doit également couvrir un fonds sans compartiment. La relation ne doit pas forcer la création d'un faux compartiment économique.

### Eléments à séparer

- identité canonique ;
- dénomination courante ;
- anciennes dénominations et alias ;
- forme juridique ;
- statut ;
- juridiction ;
- identifiants ISIN, LEI et régulateur ;
- dates de lancement, clôture et liquidation ;
- entités de service et périodes de mandat.

L'implémentation actuelle n'est pas suffisante pour lancer un import massif de fonds.

## 4. RELATIONS FONDS

```text
FUND_OR_SUBFUND 1 ── N SHARE_CLASS
FUND_OR_SUBFUND N ── N ORGANIZATION_ROLE_ASSIGNMENT
FUND_OR_SUBFUND N ── N DOCUMENT
FUND_OR_SUBFUND N ── N EVENT
SHARE_CLASS 1 ── N NAV_OBSERVATION
SHARE_CLASS 1 ── N DIVIDEND_OBSERVATION
FUND_OR_SUBFUND 1 ── N AUM_OBSERVATION
FUND_OR_SUBFUND N ── N CLASSIFICATION_MEMBERSHIP
```

Toutes les relations susceptibles de changer portent une période de validité et une provenance.

## 5. GEOGRAPHIE ET MARCHE

```text
COUNTRY
├── BELONGS_TO_REGION
├── BELONGS_TO_CONTINENT
├── USES_CURRENCY
├── BELONGS_TO_MONETARY_ZONE
├── USES_MARKET_SCOPE
├── USES_CENTRAL_BANK
└── USES_COMMON_OR_NATIONAL_EXCHANGE
```

La zone monétaire ou de marché ne remplace jamais le rattachement géographique.

## 6. SOURCES ET PROVENANCE

```text
ORGANIZATION
1 ── N ORGANIZATION_SCOPE_ROLE
1 ── N ENDPOINT

ENDPOINT
1 ── N PROVIDER_SERIES
1 ── N SOURCE_DOCUMENT

PROVIDER_SERIES
1 ── N COLLECTION_SPECIFICATION
1 ── N OBSERVATION

SOURCE_DOCUMENT
1 ── N EXTRACTION_RECORD
```

Un `ExtractionRecord` peut pointer vers une page PDF, une feuille, une ligne, une colonne, une cellule ou un chemin JSON/XML.

## 7. OBSERVATIONS

### Observation native

Champs minimaux :

```text
observation_id
series_id
observation_date
publication_date
value
unit
currency_id
source_artifact_id
extraction_record_id
validation_status
recorded_at
superseded_at
```

### Observation calculée

Elle ajoute :

```text
input_observation_ids
calculation_definition_id
methodology_version
formula_or_rule
calculated_at
quality_status
```

Une observation calculée ne remplace jamais l'observation native.

## 8. TAXONOMIE

### Classes d'actifs retenues

```text
ACTIONS
OBLIGATIONS
DIVERSIFIE
MONETAIRE
```

### Sous-classes retenues

```text
OBLIGATIONS_CT
OBLIGATIONS_MT
OBLIGATIONS_LT
DIVERSIFIE_PRUDENT
DIVERSIFIE_EQUILIBRE
DIVERSIFIE_DYNAMIQUE
DIVERSIFIE_FLEXIBLE
MONETAIRE
```

### Génération

```text
GEOGRAPHIC_ENTITY + ASSET_CLASS [+ SUB_ASSET_CLASS]
→ CATEGORY_OR_SUBCATEGORY
```

Niveaux : `NATIONAL`, `REGIONAL`, `AFRICA`.

## 9. REFERENCES ET INDICES

```text
CATEGORY 1 ── 1 REFERENCE_BLOCK
REFERENCE_BLOCK 1 ── 4 REFERENCE_ROLE
```

Rôles :

```text
PRIMARY_MARKET_INDEX
SECONDARY_MARKET_INDEX
WTI
WTI_BENCH
```

Une affectation de série à un rôle est historisée. Le rôle n'est pas le nom de la série fournisseur.

## 10. MODELE PAYS ET INDICATEURS

```text
INDICATOR_DOMAIN
1 ── N INDICATOR_DEFINITION

COUNTRY_OR_ZONE
N ── N INDICATOR_DEFINITION
    via APPLICABILITY_RELATIONSHIP

APPLICABILITY_RELATIONSHIP
1 ── N PROVIDER_SERIES_MAPPING
```

Les 420 définitions sont partagées. Elles ne deviennent pas 420 colonnes dans une table pays.

## 11. TEMPORALITE

Tout fait historique doit distinguer :

- période économique ou juridique ;
- date de publication ;
- date de collecte ;
- date d'intégration ;
- date de correction ;
- période durant laquelle la version est courante dans le système.

Le modèle d'une date d'effet inconnue doit être finalisé avant les migrations fonds.

## 12. ETAT DES SCHEMAS EXISTANTS

| Fichier | Nature |
|---|---|
| `schemas/taxonomy/fund_relationship_information_model_v0.1.sql` | brouillon de domaine, non migration de production |
| `schemas/reference/country_indicator_information_model_v0.1.sql` | proposition explicite, à réconcilier |
| `schemas/reference/002_country_relationships.sql` | schéma relationnel à corriger pour les dates inconnues |
| `schemas/reference/003` à `007` | modèles opérationnels testés pour organisations et sources |
| `schemas/reference/008` à `011` | seeds et validation BCEAO/BEAC |
| `schemas/market/006_fx_observation_lineage.sql` | extension FX testée |

## 13. PROCHAINES DECISIONS

1. Fund/SubFund/ShareClass ;
2. source de vérité CSV/SQL ;
3. endpoint canonique ;
4. temporalité des dates inconnues ;
5. dictionnaire machine-readable ;
6. stratégie de migrations.

---

## 14. RECONCILIATION DOCUMENTAIRE — 2026-08-05

Cette section conserve les états historiques ci-dessus et actualise uniquement leur statut.

```text
OF-ARCH-001   VERIFIED_COMPLETE
OF-SOURCE-001 VERIFIED_COMPLETE
OF-ARCH-002   VERIFIED_COMPLETE
OF-ARCH-003   VERIFIED_COMPLETE
OF-ARCH-004   IMPLEMENTED_WITH_OPEN_GOVERNANCE_BLOCKER
```

`source.endpoint` est désormais le modèle physique runtime canonique ; `source.source_endpoint` reste une proposition non opérationnelle. Les dates métier inconnues sont modélisées par des statuts explicites et une valeur `NULL`, sans date sentinelle. Le runner gouverné possède un manifeste de 14 migrations et un ledger PostgreSQL.

La table de la section 12 reste une photographie ancienne : `schemas/reference/002_country_relationships.sql` et la sémantique des dates ont été corrigés et testés. Le blocker de migration `012` demeure ouvert : le SQL historique généré n'est pas figé comme artefact Git immuable.

Le domaine fonds demeure non stabilisé. `OF-DATA-001` n'est pas commencé et aucun import massif de fonds n'est autorisé. Pour l'état vivant, consulter `STATUS.md`, `SOURCE_OF_TRUTH.md` et `docs/00_PROJECT/ARCHITECTURE_GATE_CHAIN_FINAL_AUDIT_20260805.md`. `docs/03-architecture/DATA_MODEL.md` est un index vers le présent document canonique.