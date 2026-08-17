# OF-SOURCE-002 — Wave 13 — Audit FX_REFERENCE_RATE_PROVIDER

Date : 2026-08-17
Statut : `CLOSED_ALLOWLIST_APPROVED_FOR_TDD`

## Objet

Réévaluer les neuf relations `FX_REFERENCE_RATE_PROVIDER` encore `PENDING` sans déduire ce rôle du seul fait qu'une organisation est une banque centrale.

Le critère est la publication actuelle, sur une source primaire officielle, d'une série, d'un cours, d'un taux de marché ou d'un taux de référence de change exploitable comme référence FX.

## Allowlist exacte

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

Aucune nouvelle organisation, aucun nouveau rôle, aucun changement de scope et aucun changement de `IS_PRIMARY` ne sont autorisés par cette vague.

## Preuves primaires officielles

### BCEAO — UEMOA

Source : `https://www.bceao.int/fr/cours/cours-de-reference-des-principales-devises-contre-Franc-CFA`

La BCEAO publie explicitement les `Cours de référence des principales devises contre Franc CFA`, datés par jour et exprimés en FCFA.

Verdict : `PROMOTABLE`.

### BEAC — CEMAC

Source : `https://www.beac.int/`

La BEAC publie des `Taux indicatifs de change` avec paires EUR/XAF, USD/XAF, GBP/XAF, etc., achat, vente et date de valeur. La qualification canonique `FX_REFERENCE_RATE_PROVIDER` désigne ici la responsabilité de publication d'une série de référence exploitable et non une affirmation que le libellé officiel de la BEAC contient le mot « référence ».

Verdict : `PROMOTABLE`.

### SARB — Afrique du Sud

Sources :

- `https://www.resbank.co.za/en/home/what-we-do/statistics/key-statistics/selected-historical-rates/`
- `https://www.resbank.co.za/en/home/what-we-do/statistics/key-statistics/current-market-rates`

La SARB publie des séries historiques de taux de change et des current market rates, avec documentation de taux moyens pondérés et données FX. Ses publications de marchés comprennent également des historiques Overnight Foreign Exchange (FX) Rate.

Verdict : `PROMOTABLE`.

### Bank Al-Maghrib — Maroc

Source : `https://www.bkam.ma/Marches/Principaux-indicateurs/Marche-des-changes/Cours-de-change/Cours-de-reference`

Bank Al-Maghrib publie des `Cours de référence` par devise et date, avec téléchargement CSV et service API.

Verdict : `PROMOTABLE`.

### Bank of Ghana — Ghana

Source : `https://www.bog.gov.gh/treasury-and-the-markets/daily-interbank-fx-rates/`

La Bank of Ghana publie les `Daily Interbank FX Rates`. La page décrit explicitement le calcul du `market reference (closing) rate` à partir des transactions spot soumises par les banques, puis sa publication quotidienne par la Bank of Ghana.

Verdict : `PROMOTABLE`.

### Central Bank of Nigeria — Nigeria

Source : `https://www.cbn.gov.ng/rates/ExchRateByCurrency.html`

La CBN publie les `NIGERIAN FOREIGN EXCHANGE MARKET (NFEM) RATES (₦/US$)`. La source officielle précise que le NFEM rate est dérivé en moyenne pondérée par les volumes et constitue l'`official exchange rate for the day`.

Verdict : `PROMOTABLE`.

### Banque Centrale de Tunisie — Tunisie

Source : `https://gosdmx.bct.gov.tn/gosdmx/pnrd?lang=FR`

Le portail officiel de données économiques et financières de la BCT expose une série `Taux de change` au sein des données macroéconomiques et financières et permet l'accès aux données/métadonnées associées.

Verdict : `PROMOTABLE`.

### Central Bank of Egypt — Égypte

Sources :

- `https://www.cbe.org.eg/en/economic-research/statistics/exchange-rates`
- `https://www.cbe.org.eg/en/economic-research/statistics/exchange-rates/historical-data`

La CBE publie les `Exchange Rates`, avec Average Market Rate en EGP, achat/vente par devise, ainsi que l'historique officiel correspondant.

Verdict : `PROMOTABLE`.

### Central Bank of Kenya — Kenya

Source : `https://www.centralbank.go.ke/`

Le site officiel CBK expose les `Daily KES Exchange Rates` (USD, GBP, EUR, etc.) datés quotidiennement.

Verdict : `PROMOTABLE`.

## Collision review

- les neuf lignes existent déjà exactement une fois dans `ORGANIZATION_SCOPE_ROLES.csv` ;
- elles sont toutes `PENDING` avant Wave 13 ;
- les rôles `CENTRAL_BANK` correspondants restent distincts ;
- aucune série de prix n'est déplacée vers le registre institutionnel ;
- cette promotion qualifie uniquement l'organisation comme fournisseur/publicateur de la référence FX ;
- les endpoints, provider-series, fréquences, méthodes et historiques restent sous `OF-SOURCE-003` et leurs propres gates.

## Changement autorisé après RED

Sur ces neuf lignes exactes uniquement :

```text
VALIDATION_STATUS: PENDING -> VALIDATED
SOURCE_NOTE: -> OFFICIAL_FX_REFERENCE_PUBLICATION_VERIFIED_2026_08_17_WAVE13
```

Tous les autres champs doivent rester byte-for-byte identiques.

## Post-état attendu

Avant Wave 13 :

```text
TOTAL_ROLE_ROWS: 199
VALIDATED: 178
PENDING: 21
FX_REFERENCE_RATE_PROVIDER_PENDING: 9
```

Après Wave 13 :

```text
TOTAL_ROLE_ROWS: 199
VALIDATED: 187
PENDING: 12
FX_REFERENCE_RATE_PROVIDER_PENDING: 0
```

Résiduel attendu :

```text
INDEX_PROVIDER               5
MONETARY_UNION               3
SUPRANATIONAL_AUTHORITY      2
INTERBANK_MARKET_OPERATOR    2
TOTAL                       12
```

## Interdictions

- ne pas promouvoir un autre rôle par effet de bord ;
- ne pas modifier les scopes ;
- ne pas créer de nouvelle relation ;
- ne pas traiter `INTERBANK_MARKET_OPERATOR` dans cette vague ;
- ne pas considérer la validation institutionnelle comme validation automatique d'un endpoint ou d'une série historique ;
- ne pas modifier `main` ou la structure de branche.
