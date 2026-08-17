# OF-SOURCE-002 — Wave 13 — Clôture FX_REFERENCE_RATE_PROVIDER

Date : 2026-08-17
Statut : `VERIFIED_COMPLETE_FOR_WAVE_SCOPE`

## Verdict

Les neuf relations `FX_REFERENCE_RATE_PROVIDER` préexistantes ont été promues de `PENDING` à `VALIDATED` après preuve primaire officielle de publication de taux/cours FX par l'organisation concernée.

Aucune organisation, aucun rôle, aucun scope et aucune relation n'ont été créés.

## Allowlist promue

```text
BCEAO;FX_REFERENCE_RATE_PROVIDER;UEMOA;MONETARY_ZONE
BEAC;FX_REFERENCE_RATE_PROVIDER;CEMAC;MONETARY_ZONE
SARB;FX_REFERENCE_RATE_PROVIDER;AFRIQUE_DU_SUD;COUNTRY
BAM;FX_REFERENCE_RATE_PROVIDER;MAROC;COUNTRY
BOG;FX_REFERENCE_RATE_PROVIDER;GHANA;COUNTRY
CBN;FX_REFERENCE_RATE_PROVIDER;NIGERIA;COUNTRY
BCT;FX_REFERENCE_RATE_PROVIDER;TUNISIE;COUNTRY
CBE;FX_REFERENCE_RATE_PROVIDER;EGYPTE;COUNTRY
CBK;FX_REFERENCE_RATE_PROVIDER;KENYA;COUNTRY
```

Note source appliquée :

```text
OFFICIAL_FX_REFERENCE_PUBLICATION_VERIFIED_2026_08_17_WAVE13
```

## TDD

### RED

Run institutionnel : `32065421538`.

Waves 01→12 : GREEN.

Wave 13 : échec attendu uniquement sur :

- neuf tuples encore `PENDING` ;
- ancien `SOURCE_NOTE` ;
- post-état encore `178 VALIDATED / 21 PENDING`.

L'unicité et l'absence de retargeting des neuf lignes étaient déjà vertes.

### GREEN

Workflow one-shot : `.github/workflows/of-source-002-wave13-promote.yml`

Run : `32065501479` — `SUCCESS`.

Le workflow a vérifié :

```text
PROMOTION_EXACT_ALLOWLIST: SUCCESS
PYTHON_3_11_FULL_INSTITUTIONAL_SUITE: SUCCESS
PYTHON_3_12_FULL_INSTITUTIONAL_SUITE: SUCCESS
TOTAL_ROLE_ROWS: 199
VALIDATED: 187
PENDING: 12
FX_REFERENCE_RATE_PROVIDER_PENDING: 0
GIT_DIFF_CHECK: SUCCESS
CHANGED_DATA_FILES: ORGANIZATION_SCOPE_ROLES.csv ONLY
COMMIT_PUSH: SUCCESS
```

## Résiduel exact

```text
INDEX_PROVIDER               5
MONETARY_UNION               3
SUPRANATIONAL_AUTHORITY      2
INTERBANK_MARKET_OPERATOR    2
TOTAL                       12
```

## Limites conservées

Cette vague ne valide pas automatiquement :

- les endpoints de collecte ;
- chaque provider series ;
- les fréquences ;
- les unités et conventions de cotation ;
- les historiques disponibles ;
- la qualité/completude des séries ;
- `INTERBANK_MARKET_OPERATOR` pour BCEAO/BEAC.

Ces éléments restent sous `OF-SOURCE-003` ou sous une revue sémantique séparée.

## État institutionnel après Wave 13

```text
AFRICAN_COUNTRIES: 54
COUNTRY_COVERAGE: 53 / 54
UNCOVERED_COUNTRY: ERYTHREE
ORGANIZATIONS: 141 = 121 VALIDATED + 20 PENDING
ORGANIZATION_SCOPE_ROLES: 199 = 187 VALIDATED + 12 PENDING
WAVES_VERIFIED: 01..13
```

L'Érythrée reste volontairement non peuplée faute de source primaire officielle actuelle vérifiée.
