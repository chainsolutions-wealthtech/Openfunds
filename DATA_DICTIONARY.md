# DICTIONNAIRE DE DONNEES CANONIQUE

## 1. STATUT

```text
SPECIFICATION DE GOUVERNANCE : CREEE
DICTIONNAIRE COMPLET : NON ENCORE PEUPLE
```

Les définitions sont actuellement dispersées dans les schémas SQL, référentiels CSV et documents D00-D17. Ce fichier définit la structure obligatoire du futur dictionnaire unique ; il ne prétend pas que tous les champs sont déjà recensés ou validés.

Tâches : `OF-DATA-002` et `OF-DATA-003`.

## 2. COLONNES OBLIGATOIRES

Chaque champ canonique doit comporter :

| Attribut | Description |
|---|---|
| `FIELD_ID` | identifiant canonique stable |
| `TECHNICAL_NAME` | nom technique en majuscules/underscore ou convention SQL approuvée |
| `FUNCTIONAL_NAME_FR` | libellé fonctionnel français |
| `FUNCTIONAL_NAME_EN` | libellé anglais |
| `DEFINITION` | sémantique précise |
| `DOMAIN_CODE` | domaine fonctionnel |
| `ENTITY_CODE` | objet propriétaire |
| `DATA_TYPE` | texte, date, nombre, booléen, UUID, JSON, etc. |
| `FORMAT` | masque ou représentation |
| `UNIT_CODE` | unité éventuelle |
| `CURRENCY_RULE` | devise native, devise cible ou non applicable |
| `NULLABILITY` | obligatoire, facultatif, conditionnel |
| `CARDINALITY` | 1, 0..1, 0..N, 1..N |
| `ALLOWED_VALUES` | énumération ou référentiel |
| `CONSTRAINTS` | contraintes métier et techniques |
| `VALIDATION_RULE` | règle de contrôle |
| `NORMALIZATION_RULE` | nettoyage et normalisation |
| `CALCULATION_RULE` | formule si calculé |
| `SOURCE_ROLE` | source privilégiée |
| `SOURCE_PRIORITY_RULE` | arbitrage entre sources |
| `HISTORY_METHOD` | snapshot, validité, bitemporel, append-only |
| `SENSITIVITY_LEVEL` | public, interne, restreint |
| `CONFIDENCE_RULE` | confiance et validation |
| `OPENFUNDS_FIELD_ID` | équivalent openfunds éventuel |
| `EXTERNAL_MAPPINGS` | autres standards |
| `EXAMPLE_VALUE` | exemple non ambigu |
| `STATUS` | proposé, validé, déprécié, remplacé |
| `SCHEMA_VERSION` | version du dictionnaire |
| `CREATED_AT` | création de la définition |
| `UPDATED_AT` | dernière modification |

## 3. IDENTIFIANTS DE CHAMPS

Convention proposée, à valider dans `ADR-024` :

```text
OF_<DOMAIN>_<ENTITY>_<FIELD>
```

Exemples de travail :

```text
OF_REF_COUNTRY_ISO_ALPHA3
OF_FUND_SHARE_CLASS_ISIN
OF_MARKET_NAV_VALUE
OF_SOURCE_RAW_ARTIFACT_SHA256
```

Ces exemples illustrent la convention ; ils ne constituent pas encore un catalogue validé.

## 4. CHAMPS TRANSVERSAUX MINIMAUX

| Champ conceptuel | Sémantique | Etat |
|---|---|---|
| `canonical_id` | identité interne stable | décidé |
| `canonical_code` | code lisible stable | décidé |
| `valid_from` | début de validité métier | décidé, nullabilité à arbitrer |
| `valid_to` | fin de validité métier | décidé |
| `recorded_at` | connaissance système | décidé |
| `superseded_at` | remplacement système | décidé |
| `source_id` | source ou assertion | partiellement implémenté |
| `validation_status` | état de validation | implémenté dans plusieurs domaines |
| `quality_status` | qualité de l'observation | partiellement implémenté |
| `confidence_score` | niveau de confiance | proposé/partiel |
| `schema_version` | version de structure | proposé |

## 5. FAMILLES A INVENTORIER

1. géographie ;
2. devises ;
3. organisations ;
4. sources ;
5. identité fonds ;
6. structure juridique ;
7. compartiments ;
8. classes de parts ;
9. fournisseurs de services ;
10. classifications ;
11. benchmarks ;
12. frais ;
13. documents ;
14. événements ;
15. NAV, AUM et dividendes ;
16. portefeuilles ;
17. performances et risques ;
18. réglementaire ;
19. ESG ;
20. indicateurs pays D00-D17 ;
21. qualité et provenance ;
22. mappings externes.

## 6. REGLES DE GOUVERNANCE

- une définition ne change pas silencieusement de sens ;
- toute rupture sémantique crée une nouvelle version ou un nouveau champ ;
- un renommage technique conserve un alias de compatibilité ;
- les unités et devises ne sont jamais implicites ;
- `NULL`, `UNKNOWN`, `NOT_APPLICABLE` et `NOT_PUBLISHED` restent distincts ;
- un champ calculé référence ses entrées et sa méthodologie ;
- chaque mapping externe indique la version du standard ;
- le Markdown devra être généré depuis le format maître, et non maintenu en double.

## 7. SOURCES D'INVENTAIRE EXISTANTES

```text
schemas/**/*.sql
data/reference/*.csv
docs/04_DATA_GOVERNANCE/indicator_catalog/*.md
docs/01_ARCHITECTURE/*.md
docs/06_SOURCES/*.md
```

## 8. CRITERES DE COMPLETUDE

Le dictionnaire ne sera déclaré complet qu'après :

- inventaire automatique et revue humaine ;
- suppression des doublons sémantiques ;
- validation des types et unités ;
- rattachement à une entité canonique ;
- documentation de l'historisation et de la provenance ;
- mapping openfunds lorsque applicable ;
- tests d'unicité, références et valeurs autorisées ;
- génération reproductible des vues humaines et migrations.
