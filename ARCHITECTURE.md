# ARCHITECTURE OPENFUNDS

## 1. PRINCIPE DIRECTEUR

```text
REAL_WORLD_DATA
→ RAW_SOURCE
→ NORMALIZED_SOURCE
→ VALIDATION
→ CANONICAL_MODEL
→ ANALYTICAL_MODEL
→ API_RESOURCE
→ UI_VIEW_MODEL
```

PostgreSQL est la source de vérité des entités, relations, historiques, mappings et décisions qualité. Les fichiers originaux sont conservés dans un stockage immuable. Les index de recherche, caches, graphes, entrepôts analytiques et view models sont dérivés et reconstruisibles.

## 2. COUCHES

| Couche | Responsabilité | Etat actuel |
|---|---|---|
| Raw | conserver fichier, URL, métadonnées et SHA256 | implémenté pour les pilotes FX, stockage permanent absent |
| Normalisation | dates, nombres, codes et libellés fournisseurs | implémenté pour BCEAO/BEAC FX |
| Validation | contrôles, conflits, confiance et décisions | partiel |
| Canonique | objets stables et relations historisées | schémas et référentiels partiels |
| Analytique | conversions, indices, WTI, risques et classements | conversions FX seulement |
| API | contrats versionnés | documenté, non implémenté |
| Présentation | view models et Atomic Design | documenté, non implémenté |

## 3. SCHEMAS LOGIQUES POSTGRESQL

```text
ref        référentiels stables
source     organisations, endpoints, séries, runs et artefacts
afund/fund identités fonds et classes
taxonomy   classes, catégories, appartenances et références
market     observations de marché et séries temporelles
calc       observations calculées, indices et contributions
quality    règles et décisions qualité
```

Les noms physiques définitifs restent à stabiliser. Le domaine fonds utilise actuellement le schéma `fund`; la séparation complète Fund/SubFund/ShareClass reste ouverte.

## 4. CHAINE DE SOURCE

```text
ORGANIZATION
→ ORGANIZATION_SCOPE_ROLE
→ ENDPOINT
→ INDICATOR_SOURCE_MAPPING
→ PROVIDER_SERIES
→ COLLECTION_SPECIFICATION
→ COLLECTION_RUN
→ RAW_ARTIFACT
→ EXTRACTION_RECORD
→ OBSERVATION
→ VALIDATION_DECISION
→ CALCULATED_OBSERVATION
```

Une organisation peut avoir plusieurs rôles et endpoints. Un endpoint n'est jamais confondu avec l'organisation.

## 5. CHAINE FONDS ET TAXONOMIE

```text
FUND_IDENTITY
→ LEGAL_STRUCTURE
→ SUBFUND
→ SHARE_CLASS
→ COUNTRY
→ ASSET_CLASS
→ SUB_ASSET_CLASS
→ CATEGORY_MEMBERSHIP
→ PEER_GROUP
→ REFERENCE_BLOCK
```

Le modèle cible exige six rattachements possibles : catégorie et sous-catégorie aux niveaux national, régional et Afrique.

Chaque catégorie possède quatre rôles :

```text
PRIMARY_MARKET_INDEX
SECONDARY_MARKET_INDEX
WTI
WTI_BENCH
```

## 6. TEMPS ET VERSIONNEMENT

La validité métier et la connaissance système sont distinctes :

```text
valid_from / valid_to
recorded_at / superseded_at
```

Les observations ajoutent notamment :

```text
observation_date
publication_date
retrieved_at
ingested_at
calculated_at
corrected_at
```

Une version corrigée ne supprime pas l'ancienne. Une date métier inconnue ne doit pas être inventée ; son modèle final relève de `ADR-022`.

## 7. IDENTIFIANTS

- UUID pour les clés techniques internes ;
- codes canoniques stables et lisibles pour les échanges ;
- codes en majuscules, sans accent, sans apostrophe, séparés par underscore ;
- identifiants fournisseurs conservés séparément ;
- anciens codes et alias historisés.

La stratégie complète de namespace et de génération doit être finalisée avec le modèle fonds.

## 8. ARCHITECTURE D'EXECUTION ACTUELLE

```text
GITHUB ACTIONS
├── tests Python 3.11 / 3.12
├── PostgreSQL 16 éphémère
├── smoke test BCEAO live
├── smoke test BEAC live
├── test de schéma endpoint
└── staging quotidien FX
```

Le workflow quotidien peut charger PostgreSQL via `OPENFUNDS_DATABASE_URL`, mais aucun environnement persistant n'est configuré dans le dépôt.

## 9. INVARIANTS DE NON-REGRESSION

1. aucune donnée brute écrasée ;
2. aucune valeur manquante convertie en zéro ;
3. observations et calculs séparés ;
4. XOF et XAF ne partagent pas les séries fournisseurs ;
5. source value date prioritaire sur la date du run ;
6. corrections versionnées ;
7. WTI distinct de WTI Bench ;
8. géographie distincte des zones de marché ;
9. API et UI ne modifient pas directement la vérité canonique ;
10. un fichier ou une table vide ne vaut pas fonctionnalité terminée.

## 10. ECARTS A RESOUDRE

- `source.endpoint` versus `source.source_endpoint` ;
- CSV versus seeds SQL ;
- `valid_from` obligatoire versus date inconnue ;
- Fund/SubFund/ShareClass ;
- absence de migration runner ;
- stockage brut et PostgreSQL persistants ;
- catalogue machine-readable des champs et indicateurs.

Les décisions sont suivies dans `DECISIONS.md` et les tâches dans `TODO.md`.

---

## 11. RECONCILIATION DOCUMENTAIRE — 2026-08-05

Cette section supersède uniquement l'état courant de la section 10 ; elle ne supprime pas son historique.

```text
OF-ARCH-001   VERIFIED_COMPLETE
OF-SOURCE-001 VERIFIED_COMPLETE
OF-ARCH-002   VERIFIED_COMPLETE
OF-ARCH-003   VERIFIED_COMPLETE
OF-ARCH-004   IMPLEMENTED_WITH_OPEN_GOVERNANCE_BLOCKER
```

Les écarts `source.endpoint`, authoring CSV/SQL et dates métier inconnues ont été décidés, implémentés et testés. Un runner de 14 migrations existe et a réussi ses scénarios PostgreSQL 16 documentés. `source.endpoint` est le modèle physique runtime ; la proposition `source.source_endpoint` reste non opérationnelle. Les dates inconnues sont explicites et ne sont pas inventées.

Le blocker restant porte sur l'immuabilité historique de la migration générée `012`, rematérialisée avant le calcul de checksum. Cette mission documentaire ne modifie pas ce mécanisme.

Le modèle Fund/SubFund/ShareClass, le stockage brut durable, PostgreSQL persistant et le catalogue machine-readable restent ouverts. `OF-DATA-001` n'est pas commencé.

Pour l'état vivant, lire `STATUS.md`, `SOURCE_OF_TRUTH.md`, `NEXT_ACTION.md` et `docs/00_PROJECT/PERMANENT_DOCUMENT_RECONCILIATION_20260805.md`. Le chemin `docs/03-architecture/ARCHITECTURE.md` est un index vers le présent document canonique.