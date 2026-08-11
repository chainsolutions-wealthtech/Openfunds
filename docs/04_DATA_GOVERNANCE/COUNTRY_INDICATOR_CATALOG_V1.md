
# Country Indicator Catalogue v1 — Gouvernance

```text
TASK: OF-DATA-003
STATUS: VERIFIED_COMPLETE
AUTHORING_AUTHORITY: data/indicator_catalog/v1/
DOMAIN_COUNT: 18
INDICATOR_COUNT: 420
CLASSIFICATION_DECISION: OF-DATA-003-A
```

## Autorité et fidélité

Les sept Markdown sous `docs/04_DATA_GOVERNANCE/indicator_catalog/` sont les sources historiques de bootstrap/audit. Le paquet JSON v1 est l’autorité d’authoring. Les sorties sous `build/indicator_catalog/` sont dérivées et ne doivent pas être éditées comme une deuxième source de vérité.

## Répartition gouvernée

| Nature canonique | Nombre |
|---|---:|
| RAW | 298 |
| METADATA | 85 |
| EVENT | 7 |
| CALCULATED | 30 |
| **Total** | **420** |

La nature canonique est une décision de gouvernance séparée de `source_nature`.

## Contrats essentiels

- code canonique unique `Dnn.CODE` ;
- domaine D00–D17 ;
- libellé source français conservé ;
- absence de traduction non sourcée = `null` / `NOT_AUTHORED` ;
- définition source absente = `null` / `NOT_AUTHORED` ;
- fréquence, unité, source préférée, usages, benchmark, priorité et horizon cible conservés quand présents ;
- provenance par fichier legacy et SHA-256 ;
- statuts `definition`, `source_mapping`, `collection_spec`, `collection_test`, `history`, `calculation` indépendants ;
- `history_status` ne peut pas être promu par le catalogue de définitions.

## Génération et contrôle

```text
python scripts/generate_country_indicator_catalog.py --check-authoring
python scripts/generate_country_indicator_catalog.py --generate-derived
python scripts/generate_country_indicator_catalog.py --check-derived
python -m unittest -v tests.test_country_indicator_catalog
python scripts/generate_country_indicator_catalog.py --check --source data/indicator_catalog/v1/00_metadata.json --output schemas/reference/016_country_indicator_catalog.sql
```

Les sorties générées sont :

```text
build/indicator_catalog/COUNTRY_INDICATOR_CATALOG_V1.json
build/indicator_catalog/COUNTRY_INDICATOR_CATALOG_V1.csv
build/indicator_catalog/COUNTRY_INDICATOR_CATALOG_V1.md
build/indicator_catalog/COUNTRY_INDICATOR_CATALOG_V1.sql
```

Le manifeste commité est `data/indicator_catalog/COUNTRY_INDICATOR_CATALOG_MANIFEST_V1.json`. Le SQL frozen commité est `schemas/reference/016_country_indicator_catalog.sql`.

## Empreintes v1

```text
JSON: 1d19a2d612b4d34e6d83f96100c6b073acd3791f96418aaca7cf1a097ad58184
CSV: 7d0f549684bdf91164ad98b7d912510784c8a2f07b4a8d0d86ecdc3e4a34ee94
MARKDOWN: a2044c0ebff3ba90a839eb7ee30ff388952b53a8380360f7cf7d8d15bb3f4730
SQL: fa00298ca8371cf1f95e20d809cc82b97774ea3cf0bf8fa2945cf269d0982432
```

## Preuves

```text
COUNTRY_INDICATOR_CATALOG_RUN: 31484468846 — SUCCESS
MIGRATION_RUNNER_RUN: 31484586710 — SUCCESS
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
POSTGRESQL_16_DOUBLE_APPLY: SUCCESS
```

## Revalidation de clôture

Toute modification de ce contrat de gouvernance doit redéclencher le workflow `Country Indicator Catalog` sur le HEAD documentaire concerné. La clôture n’est considérée stable qu’après validation de l’authoring package commité, régénération déterministe des quatre sorties et succès des tests contractuels Python 3.11/3.12. Cette règle ne transforme pas une validation CI en autorisation de déploiement ou de chargement de données réelles.

## Limites

Cette v1 centralise des définitions, pas des historiques. Elle ne prouve ni disponibilité d’une série pour un pays, ni endpoint vérifié, ni collecte testée, ni couverture complète, ni produit analytique actif. Aucun identifiant Openfunds officiel n’est inventé.
