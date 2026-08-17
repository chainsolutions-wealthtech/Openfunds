# OF-MAP-002 — Batch 01 — Clôture domicile + ISIN

Date : 2026-08-17
Statut : `VERIFIED_COMPLETE_FOR_BATCH_SCOPE`

## Verdict

Le premier lot de mapping Openfunds v2.13.0 → dictionnaire canonique est validé sans élargissement artificiel de couverture.

```text
REVIEWED_MAPPING_ROWS: 4
MAPPED_EXTERNAL_IDS: 2
UNMAPPED_EXTERNAL_IDS: 1867
MAPPED_CANONICAL_IDS: 4
OFFICIAL_FIELD_COUNT: 1869
CANONICAL_FIELD_COUNT: 143
```

## Mappings validés

### OFST010010 — Fund Domicile Alpha-2

- cible : `OF_FUND_FUND_ENTITY_STATE_DOMICILE_COUNTRY_ID`
- statut : `TRANSFORMED`
- règle : `ISO_3166_ALPHA2_TO_REF_GEOGRAPHY_UUID`
- import : oui
- export : oui via lookup inverse gouverné
- perte d'information : aucune.

### OFST020000 — ISIN

Décomposition one-to-many vers l'entité historisée `FUND_ENTITY_IDENTIFIER` :

1. `OF_FUND_FUND_ENTITY_IDENTIFIER_IDENTIFIER_VALUE` — `IDENTITY` ;
2. `OF_FUND_FUND_ENTITY_IDENTIFIER_IDENTIFIER_SCHEME` — `CONSTANT_ISIN` ;
3. `OF_FUND_FUND_ENTITY_IDENTIFIER_NORMALIZED_VALUE` — `TRIM_AND_UPPERCASE_ISIN`.

La valeur normalisée n'est pas exportée seule comme source Openfunds.

## Vérifications

Run `32065216172` :

```text
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
OFFICIAL_PDF_REPARSE_1869: SUCCESS
CANONICAL_DICTIONARY_143: SUCCESS
CANONICAL_ENTITY_CONSISTENCY: SUCCESS
DUPLICATE_EXTERNAL_CANONICAL_PAIR_GUARD: SUCCESS
REPOSITORY_UNCHANGED: SUCCESS
```

Résumé émis par le validator :

```json
{
  "canonical_field_count": 143,
  "mapped_canonical_ids": 4,
  "mapped_external_ids": 2,
  "official_field_count": 1869,
  "reviewed_mapping_rows": 4,
  "unmapped_external_ids": 1867
}
```

## Ce que cette clôture ne signifie pas

- `OF-MAP-002` n'est pas terminé globalement ;
- les 1867 OF-ID restants ne sont ni invalides ni artificiellement marqués `UNMAPPED` dans le registre ;
- les noms Fund/SubFund/Umbrella et language tags ne sont pas encore mappés ;
- aucune donnée de production n'est importée par ce mapping ;
- aucun champ officiel n'a été modifié ou reconstruit.

## Prochaine unité

Continuer par un lot de champs simples dont les transformations sont explicitement démontrables. Traiter les noms dans une boucle dédiée qui modélise correctement Fund/SubFund/Umbrella, `name_role`, langue et normalisation au lieu d'un mapping naïf vers `name_text`.
