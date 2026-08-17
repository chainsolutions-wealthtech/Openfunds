# OF-MAP-002 — Batch 01 — Domicile et ISIN

Date : 2026-08-17
Statut : `APPROVED_FOR_REGISTRY_INSERTION`

## Objet

Premier lot volontairement restreint du mapping Openfunds v2.13.0 → modèle canonique.

Le lot ne cherche pas à maximiser artificiellement le taux de couverture. Il ne retient que des correspondances dont la sémantique, le niveau Openfunds et la transformation vers le modèle canonique sont explicites.

## Source officielle gouvernée

```text
VERSION: 2.13.0
SHA256: 40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4
ARCHIVE: data/openfunds/official/v2.13.0/openfunds_fields_v2.13.0.pdf
```

Pages web officielles de revue :

- `https://www.openfunds.org/snippets/OFST010010.html`
- `https://openfunds.org/OFST020000`

## Mapping 1 — OFST010010 Fund Domicile Alpha-2

Openfunds définit `OFST010010` au niveau Fund comme le domicile du fonds encodé en ISO 3166-1 alpha-2.

Cible canonique :

```text
OF_FUND_FUND_ENTITY_STATE_DOMICILE_COUNTRY_ID
ENTITY_CODE: FUND_ENTITY_STATE
PHYSICAL_COLUMN: fund.entity_state.domicile_country_id
```

La cible physique est un identifiant UUID de géographie canonique et non un code alpha-2. La relation est donc :

```text
MAPPING_STATUS: TRANSFORMED
TRANSFORMATION_RULE: ISO_3166_ALPHA2_TO_REF_GEOGRAPHY_UUID
INFORMATION_LOSS: NONE
IMPORT_SUPPORTED: YES
EXPORT_SUPPORTED: YES
```

L'export suppose le lookup inverse du référentiel géographique gouverné. Aucun pays n'est déduit depuis le nom du fonds.

## Mapping 2 — OFST020000 ISIN

Openfunds définit `OFST020000` au niveau Share Class comme l'ISIN de la classe : 12 caractères alphanumériques, lettres en majuscules.

Le modèle canonique ne stocke pas un champ ISIN physique dédié. Il utilise une entité d'identifiants externes historisés :

```text
ENTITY_CODE: FUND_ENTITY_IDENTIFIER
TABLE: fund.entity_identifier
```

Un OFST020000 alimente donc trois attributs canoniques cohérents :

### Valeur source

```text
TARGET: OF_FUND_FUND_ENTITY_IDENTIFIER_IDENTIFIER_VALUE
RULE: IDENTITY
```

### Schéma d'identifiant

```text
TARGET: OF_FUND_FUND_ENTITY_IDENTIFIER_IDENTIFIER_SCHEME
RULE: CONSTANT_ISIN
```

### Valeur normalisée

```text
TARGET: OF_FUND_FUND_ENTITY_IDENTIFIER_NORMALIZED_VALUE
RULE: TRIM_AND_UPPERCASE_ISIN
```

Ces trois lignes partagent le même OF-ID source ; elles sont déclarées `ONE_TO_MANY`. Elles ne représentent pas trois champs Openfunds différents.

La normalisation ne change pas le sens de l'ISIN : elle applique seulement le format attendu par Openfunds et par le modèle canonique. La valeur source reste distincte de la valeur normalisée.

## Exclusions explicites du Batch 01

### OFST010110 — Legal Fund Name Only

Non inséré dans ce batch.

La sémantique Openfunds distingue le nom fonds/sous-fonds de l'umbrella, autorise des language tags et décrit une construction vers `Legal Fund Name Including Umbrella`. Notre modèle canonique sépare nom, `name_role`, langue, normalisation, entité et historique. Un mapping fiable nécessite donc un lot dédié sur les règles Fund/SubFund/Umbrella et language tags.

### Aucun template XX

Aucun template pays `XX` n'est instancié ou développé dans ce lot.

## Invariants préalables vérifiés

Le run `32065124602` a validé avant insertion :

```text
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
OFFICIAL_PDF_INVENTORY: SUCCESS
CANONICAL_DICTIONARY_EXPANSION: SUCCESS
DUPLICATE_EXTERNAL_CANONICAL_PAIR_GUARD: SUCCESS
CANONICAL_ENTITY_CONSISTENCY_GUARD: SUCCESS
REPOSITORY_UNCHANGED: SUCCESS
```

## Résultat attendu après insertion

```text
REVIEWED_MAPPING_ROWS: 4
MAPPED_EXTERNAL_IDS: 2
UNMAPPED_EXTERNAL_IDS: 1867
MAPPED_CANONICAL_IDS: 4
```

La couverture externe reste volontairement faible : la qualité sémantique prime sur le remplissage massif.
