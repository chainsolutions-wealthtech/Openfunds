# OF-SOURCE-002 — Wave 02 institutional audit — 2026-08-12

```text
TASK_ID: OF-SOURCE-002
LOOP_ID: OF-LOOP-SOURCE-002
WAVE: 02
MODE: READ_ONLY_AUDIT_COMPLETED
AUDIT_START_HEAD: 52720a0cac886277690f6c1bf9d7bc78bf01a42c
PRODUCTION_DEPLOYED: NO
RUNTIME_DATABASE_CHANGED: NO
REAL_HISTORY_LOADED: NO
NEW_BRANCH_CREATED: NO
NEW_PR_CREATED: NO
PR2_MODIFIED: NO
```

## 1. Objet

Continuer `OF-SOURCE-002` après la vague 01, sans tenter de remplir artificiellement les 54 pays en une seule écriture. La vague 02 mesure d'abord les rôles encore manquants des 10 pays déjà représentés et sélectionne quatre nouveaux pays dont les institutions peuvent être vérifiées sur des sources officielles primaires actuelles : `ALGERIE`, `MAURICE`, `RWANDA`, `TANZANIE`.

Aucune donnée canonique n'a été modifiée pendant cet audit. Les grands CSV institutionnels restent des inventaires de découverte/revue conformément à ADR-021.

## 2. Couverture pays au départ de la vague

```text
AFRICAN_COUNTRIES: 54
COUNTRIES_WITH_COUNTRY_SCOPED_ORGANIZATION: 10
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 44
```

Pays déjà représentés :

```text
AFRIQUE_DU_SUD
MAROC
GHANA
NIGERIA
TUNISIE
EGYPTE
KENYA
BOTSWANA
NAMIBIE
ETHIOPIE
```

Pays sans organisation country-scoped au départ de la vague 02 :

```text
ANGOLA
BURUNDI
BENIN
BURKINA_FASO
REPUBLIQUE_CENTRAFRICAINE
COTE_DIVOIRE
CAMEROUN
REPUBLIQUE_DEMOCRATIQUE_DU_CONGO
REPUBLIQUE_DU_CONGO
COMORES
CABO_VERDE
DJIBOUTI
ALGERIE
ERYTHREE
GABON
GUINEE
GAMBIE
GUINEE_BISSAU
GUINEE_EQUATORIALE
LIBERIA
LIBYE
LESOTHO
MADAGASCAR
MALI
MOZAMBIQUE
MAURITANIE
MAURICE
MALAWI
NIGER
RWANDA
SOUDAN
SENEGAL
SIERRA_LEONE
SOMALIE
SOUDAN_DU_SUD
SAO_TOME_ET_PRINCIPE
ESWATINI
SEYCHELLES
TCHAD
TOGO
TANZANIE
OUGANDA
ZAMBIE
ZIMBABWE
```

## 3. Audit des rôles des 10 pays déjà représentés

Cette matrice décrit l'état du registre au départ de la vague 02. `VALIDATED` signifie que la relation correspondante existe comme telle dans `ORGANIZATION_SCOPE_ROLES.csv`; `PENDING` signifie qu'un objet existe mais demande encore preuve/revalidation ; `MISSING` signifie qu'aucune relation correspondante n'est actuellement enregistrée.

| Pays | Banque centrale | Statistiques | Finance/dette | Bourse | Régulateur marché/fonds | Assurance/pension |
|---|---|---|---|---|---|---|
| Afrique du Sud | PENDING | MISSING | MISSING | PENDING | MISSING | MISSING |
| Maroc | VALIDATED | VALIDATED | VALIDATED | VALIDATED | VALIDATED | MISSING |
| Ghana | VALIDATED | VALIDATED | VALIDATED | PENDING | VALIDATED | MISSING |
| Nigeria | VALIDATED | PENDING | VALIDATED/PENDING | PENDING | VALIDATED | MISSING |
| Tunisie | VALIDATED | PENDING | VALIDATED | VALIDATED | VALIDATED | MISSING |
| Égypte | VALIDATED | PENDING | PENDING | PENDING | VALIDATED/PENDING | MISSING |
| Kenya | PENDING | PENDING | PENDING | VALIDATED | VALIDATED/PENDING | MISSING |
| Botswana | VALIDATED | VALIDATED | MISSING | VALIDATED | VALIDATED | VALIDATED |
| Namibie | VALIDATED | VALIDATED | MISSING | VALIDATED | VALIDATED | VALIDATED |
| Éthiopie | VALIDATED | VALIDATED | MISSING | VALIDATED | VALIDATED | MISSING |

La vague 02 ne modifie pas ces anciennes lignes. Une future vague de revalidation devra promouvoir ou corriger séparément les objets `PENDING` sur preuve officielle actuelle.

## 4. Pays sélectionnés pour la vague 02

### 4.1 Algérie

Sources officielles contrôlées :

```text
BANQUE_ALGERIE  https://www.bank-of-algeria.dz/
COSOB           https://cosob.dz/
SGBV            https://www.sgbv.dz/
ONS_ALGERIE     https://www.ons.dz/
```

Preuves retenues :

- la Banque d'Algérie se définit comme banque centrale et exerce les missions de stabilité monétaire, émission, changes et supervision bancaire ;
- la COSOB est l'autorité de régulation du marché financier algérien et régule explicitement les OPCVM ; la constitution d'un OPCVM requiert son agrément ;
- la SGBV exploite la Bourse d'Alger et publie la cote officielle ;
- l'Office National des Statistiques publie les statistiques économiques et sociales officielles du pays.

Relations autorisées :

```text
BANQUE_ALGERIE CENTRAL_BANK
COSOB          CAPITAL_MARKET_REGULATOR
COSOB          FUND_REGULATOR
SGBV           STOCK_EXCHANGE
ONS_ALGERIE    STATISTICS_OFFICE
```

### 4.2 Maurice

Sources officielles contrôlées :

```text
BOM                 https://www.bom.mu/
FSC_MAURITIUS       https://www.fscmauritius.org/
SEM                 https://www.stockexchangeofmauritius.com/
STATISTICS_MAURITIUS https://statsmauritius.govmu.org/
```

Preuves retenues :

- la Bank of Mauritius est la banque centrale de la République de Maurice ;
- la Financial Services Commission régule les marchés financiers non bancaires, les securities exchanges, les Collective Investment Schemes, l'assurance et les private pension schemes ;
- la Stock Exchange of Mauritius exploite le marché réglementé de valeurs mobilières ;
- Statistics Mauritius publie les statistiques officielles de la République de Maurice, avec programme de publication et séries économiques/sociales.

Relations autorisées :

```text
BOM                  CENTRAL_BANK
FSC_MAURITIUS        CAPITAL_MARKET_REGULATOR
FSC_MAURITIUS        FUND_REGULATOR
FSC_MAURITIUS        INSURANCE_PENSION_REGULATOR
SEM                  STOCK_EXCHANGE
STATISTICS_MAURITIUS STATISTICS_OFFICE
```

### 4.3 Rwanda

Sources officielles contrôlées :

```text
NBR        https://www.bnr.rw/
CMA_RWANDA https://www.cma.rw/
RSE        https://www.rse.rw/
NISR       https://www.statistics.gov.rw/
```

Preuves retenues :

- la National Bank of Rwanda se définit comme banque centrale, avec mandat de stabilité des prix et du système financier ;
- la NBR régule et supervise explicitement les secteurs assurance et pensions ;
- la Capital Market Authority a le double mandat de développer et réguler le marché des capitaux et les collective investment schemes ;
- la Rwanda Stock Exchange est la bourse nationale fournissant un marché réglementé ;
- le National Institute of Statistics of Rwanda coordonne et produit les statistiques officielles.

Relations autorisées :

```text
NBR        CENTRAL_BANK
NBR        INSURANCE_PENSION_REGULATOR
CMA_RWANDA CAPITAL_MARKET_REGULATOR
CMA_RWANDA FUND_REGULATOR
RSE        STOCK_EXCHANGE
NISR       STATISTICS_OFFICE
```

### 4.4 Tanzanie

Sources officielles contrôlées :

```text
BOT            https://www.bot.go.tz/
CMSA_TANZANIA  https://www.cmsa.go.tz/
DSE            https://dse.co.tz/
NBS_TANZANIA   https://www.nbs.go.tz/
```

Preuves retenues :

- la Bank of Tanzania se présente comme banque centrale et exerce les fonctions de politique monétaire, monnaie, stabilité et supervision financière ;
- la Capital Markets and Securities Authority dispose des pouvoirs de régulation du marché de capitaux et le cadre inclut explicitement les Collective Investment Schemes ;
- la Dar es Salaam Stock Exchange exploite le marché boursier tanzanien ;
- le National Bureau of Statistics a mandat de collecter, produire et diffuser les statistiques officielles et de coordonner le système statistique national.

Relations autorisées :

```text
BOT           CENTRAL_BANK
CMSA_TANZANIA CAPITAL_MARKET_REGULATOR
CMSA_TANZANIA FUND_REGULATOR
DSE           STOCK_EXCHANGE
NBS_TANZANIA  STATISTICS_OFFICE
```

Le rôle combiné `INSURANCE_PENSION_REGULATOR` n'est pas attribué en Tanzanie dans cette vague : les preuves examinées ne démontrent pas qu'une même organisation de l'allowlist couvre simultanément les deux sous-domaines selon la sémantique actuelle du rôle canonique.

## 5. Revue des collisions

Codes proposés :

```text
BANQUE_ALGERIE
COSOB
SGBV
ONS_ALGERIE
BOM
FSC_MAURITIUS
SEM
STATISTICS_MAURITIUS
NBR
CMA_RWANDA
RSE
NISR
BOT
CMSA_TANZANIA
DSE
NBS_TANZANIA
```

Recherche effectuée sur `data/reference/ORGANIZATIONS.csv` au HEAD de l'audit : aucune collision exacte détectée.

Les suffixes nationaux sont intentionnels pour éviter les collisions actuelles et futures :

- `CMA_RWANDA` ne collisionne ni avec `CMA` (Common Monetary Area) ni avec `CMA_KENYA` ;
- `NBS_TANZANIA` ne collisionne pas avec `NBS_NIGERIA` ;
- `FSC_MAURITIUS`, `STATISTICS_MAURITIUS` et `ONS_ALGERIE` sont explicitement contextualisés.

## 6. Allowlist d'écriture vague 02

### Organisations — 16

```text
BANQUE_ALGERIE
COSOB
SGBV
ONS_ALGERIE
BOM
FSC_MAURITIUS
SEM
STATISTICS_MAURITIUS
NBR
CMA_RWANDA
RSE
NISR
BOT
CMSA_TANZANIA
DSE
NBS_TANZANIA
```

### Relations organisation-rôle — 22

```text
BANQUE_ALGERIE CENTRAL_BANK                    ALGERIE
COSOB          CAPITAL_MARKET_REGULATOR         ALGERIE
COSOB          FUND_REGULATOR                   ALGERIE
SGBV           STOCK_EXCHANGE                   ALGERIE
ONS_ALGERIE    STATISTICS_OFFICE                ALGERIE

BOM                  CENTRAL_BANK                    MAURICE
FSC_MAURITIUS        CAPITAL_MARKET_REGULATOR         MAURICE
FSC_MAURITIUS        FUND_REGULATOR                   MAURICE
FSC_MAURITIUS        INSURANCE_PENSION_REGULATOR      MAURICE
SEM                  STOCK_EXCHANGE                   MAURICE
STATISTICS_MAURITIUS STATISTICS_OFFICE                MAURICE

NBR        CENTRAL_BANK                    RWANDA
NBR        INSURANCE_PENSION_REGULATOR      RWANDA
CMA_RWANDA CAPITAL_MARKET_REGULATOR         RWANDA
CMA_RWANDA FUND_REGULATOR                   RWANDA
RSE        STOCK_EXCHANGE                   RWANDA
NISR       STATISTICS_OFFICE                RWANDA

BOT           CENTRAL_BANK                    TANZANIE
CMSA_TANZANIA CAPITAL_MARKET_REGULATOR         TANZANIE
CMSA_TANZANIA FUND_REGULATOR                   TANZANIE
DSE           STOCK_EXCHANGE                   TANZANIE
NBS_TANZANIA  STATISTICS_OFFICE                TANZANIE
```

## 7. Hors allowlist

- aucun ministère des finances ou office de dette de ces quatre pays dans cette vague ;
- aucun `INDEX_PROVIDER`, `FX_REFERENCE_RATE_PROVIDER`, endpoint spécialisé, provider series ou collection specification ;
- aucun statut `COLLECTION_TESTED` ou historique ;
- aucune migration SQL runtime ;
- aucune institution d'assurance/pension algérienne ou tanzanienne sans revue sémantique supplémentaire ;
- aucune modification de PR nº2 ;
- aucune nouvelle branche/PR.

## 8. Gate de sortie de l'audit

```text
HEAD_RESOLVED: YES
44_COUNTRY_GAP_LISTED: YES
10_EXISTING_COUNTRIES_ROLE_GAPS_MEASURED: YES
4_NEW_COUNTRIES_OFFICIALLY_RESEARCHED: YES
CANDIDATE_CODE_COLLISIONS: NONE
WAVE_02_ALLOWLIST_DEFINED: YES
CANONICAL_DATA_CHANGED_DURING_AUDIT: NO
```

L'audit read-only est clos. La phase suivante peut appliquer TDD : écrire d'abord le contrat de vague 02, obtenir un RED contrôlé, puis intégrer uniquement les 16 organisations et 22 relations de rôle de cette allowlist.
