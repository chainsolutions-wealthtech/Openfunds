# OF-SOURCE-002 — Wave 04 institutional audit — 2026-08-12

```text
TASK_ID: OF-SOURCE-002
LOOP_ID: OF-LOOP-SOURCE-002
WAVE: 04
MODE: READ_ONLY_AUDIT_COMPLETED
AUDIT_START_HEAD: 972dc0c0e4e12b75272d6e2a409352f33b42e283
PRODUCTION_DEPLOYED: NO
RUNTIME_DATABASE_CHANGED: NO
REAL_HISTORY_LOADED: NO
NEW_BRANCH_CREATED: NO
NEW_PR_CREATED: NO
PR2_MODIFIED: NO
```

## 1. Objet

Poursuivre `OF-SOURCE-002` par un quatrième lot contrôlé : `ANGOLA`, `MOZAMBIQUE`, `CABO_VERDE`, `SEYCHELLES`.

L'audit vérifie l'identité institutionnelle, le rôle prouvé, le domaine officiel actuel et les collisions de codes. Il n'autorise aucun endpoint spécialisé, provider series, collection specification, SQL runtime ou historique.

## 2. Baseline au départ

```text
AFRICAN_COUNTRIES: 54
ORGANIZATIONS: 87 = 67 VALIDATED + 20 PENDING
COUNTRIES_WITH_COUNTRY_SCOPED_ORGANIZATION: 18
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 36
ORGANIZATION_SCOPE_ROLES: 134 = 90 VALIDATED + 44 PENDING
SOURCE_ENDPOINTS: 43 = 20 VALIDATED + 23 PENDING
```

## 3. Angola

Sources officielles actuelles contrôlées :

```text
BNA         https://www.bna.ao/
CMC_ANGOLA  https://www.cmc.ao/
BODIVA      https://www.bodiva.ao/
INE_ANGOLA  https://www.ine.gov.ao/
```

Preuves retenues :

- Banco Nacional de Angola est la banque centrale et publie les fonctions de politique monétaire, stabilité, marchés et supervision ;
- Comissão do Mercado de Capitais est l'autorité publique de régulation du marché de capitaux ;
- CMC encadre explicitement les Organismos de Investimento Colectivo / fundos de investimento ;
- BODIVA exploite le marché réglementé de valeurs mobilières angolais ;
- Instituto Nacional de Estatística produit et diffuse les statistiques officielles dans le Sistema Estatístico Nacional.

Relations autorisées :

```text
BNA        CENTRAL_BANK
CMC_ANGOLA CAPITAL_MARKET_REGULATOR
CMC_ANGOLA FUND_REGULATOR
BODIVA     STOCK_EXCHANGE
INE_ANGOLA STATISTICS_OFFICE
```

Aucun rôle assurance/pension n'est attribué dans cette vague.

## 4. Mozambique

Sources officielles actuelles contrôlées :

```text
BANCO_MOCAMBIQUE  https://www.bancomoc.mz/
BVM_MOZAMBIQUE    https://www.bvm.co.mz/
INE_MOZAMBIQUE    https://www.ine.gov.mz/
```

Preuves retenues :

- Banco de Moçambique est la banque centrale ;
- il publie en 2026 l'Aviso n.º 3/GBM/2026 établissant les règles relatives à la qualification des investisseurs sur le Mercado de Valores Mobiliários ;
- son registre normatif contient l'Aviso n.º 6/GBM/2019 concernant les ratios et limites prudentiels des fundos de investimento ;
- sa page de supervision de conduite précise en revanche que les entreprises d'assurance et les sociétés gestionnaires de fonds de pension ne sont pas dans son périmètre de supervision ;
- Bolsa de Valores de Moçambique exploite le marché de valeurs mobilières ;
- Instituto Nacional de Estatística est l'organe exécutif central du Sistema Estatístico Nacional et produit les statistiques officielles.

Relations autorisées :

```text
BANCO_MOCAMBIQUE CENTRAL_BANK
BANCO_MOCAMBIQUE CAPITAL_MARKET_REGULATOR
BANCO_MOCAMBIQUE FUND_REGULATOR
BVM_MOZAMBIQUE   STOCK_EXCHANGE
INE_MOZAMBIQUE   STATISTICS_OFFICE
```

`INSURANCE_PENSION_REGULATOR` est explicitement hors allowlist pour Banco de Moçambique.

## 5. Cabo Verde

Sources officielles actuelles contrôlées :

```text
BCV              https://www.bcv.cv/
AGMVM            https://www.bcv.cv/
BVC              https://bvc.cv/
INE_CABO_VERDE   https://ine.cv/
```

Preuves retenues :

- Banco de Cabo Verde se définit explicitement comme la banque centrale de la République de Cabo Verde ;
- Auditoria Geral do Mercado de Valores Mobiliários (AGMVM) est un service placé sous le Gouverneur du BCV chargé de la supervision/régulation du marché des valeurs mobilières ;
- AGMVM supervise explicitement les sociétés gestionnaires et fonds d'investissement ;
- Bolsa de Valores de Cabo Verde exploite le marché boursier national ;
- Instituto Nacional de Estatística de Cabo Verde publie des opérations et séries statistiques officielles, avec publications encore actives en 2026.

Relations autorisées :

```text
BCV             CENTRAL_BANK
AGMVM           CAPITAL_MARKET_REGULATOR
AGMVM           FUND_REGULATOR
BVC             STOCK_EXCHANGE
INE_CABO_VERDE  STATISTICS_OFFICE
```

### Modélisation AGMVM

`AGMVM` est conservée comme organisation de découverte/rôle afin de représenter explicitement l'autorité fonctionnelle, avec `SOURCE_NOTE` indiquant qu'il s'agit d'un service sous le Gouverneur du BCV. Cela ne prétend pas lui attribuer une personnalité juridique indépendante.

## 6. Seychelles

Sources officielles actuelles contrôlées :

```text
CBS               https://www.cbs.sc/
FSA_SEYCHELLES    https://fsaseychelles.sc/
MERJ_EXCHANGE     https://merj.exchange/
NBS_SEYCHELLES    https://www.nbs.gov.sc/
```

Preuves retenues :

- Central Bank of Seychelles est la banque centrale et l'institution principale pour la politique monétaire ;
- Financial Services Authority supervise les Capital Markets & Collective Investment Schemes ;
- FSA supervise également l'assurance et les pensions, ce qui satisfait le rôle canonique combiné ;
- le répertoire officiel des entités régulées FSA identifie `MERJ Exchange Limited`, son site `merj.exchange` et son statut de securities exchange ;
- National Bureau of Statistics compile et diffuse les statistiques officielles.

Relations autorisées :

```text
CBS            CENTRAL_BANK
FSA_SEYCHELLES CAPITAL_MARKET_REGULATOR
FSA_SEYCHELLES FUND_REGULATOR
FSA_SEYCHELLES INSURANCE_PENSION_REGULATOR
MERJ_EXCHANGE  STOCK_EXCHANGE
NBS_SEYCHELLES STATISTICS_OFFICE
```

Le fait que l'accès automatisé direct à `merj.exchange` puisse être limité par `robots.txt` n'est pas utilisé comme preuve institutionnelle ; l'identité et le domaine sont confirmés par le répertoire officiel FSA.

## 7. Revue des collisions

Codes proposés :

```text
BNA
CMC_ANGOLA
BODIVA
INE_ANGOLA
BANCO_MOCAMBIQUE
BVM_MOZAMBIQUE
INE_MOZAMBIQUE
BCV
AGMVM
BVC
INE_CABO_VERDE
CBS
FSA_SEYCHELLES
MERJ_EXCHANGE
NBS_SEYCHELLES
```

Recherche effectuée dans le dépôt au HEAD d'audit : aucune collision exacte détectée.

Les codes contextualisés évitent volontairement les ambiguïtés : `CMC_ANGOLA`, `BVM_MOZAMBIQUE`, `INE_ANGOLA`, `INE_MOZAMBIQUE`, `INE_CABO_VERDE`, `FSA_SEYCHELLES`, `NBS_SEYCHELLES`.

## 8. Allowlist fermée vague 04

### Organisations — 15

```text
BNA
CMC_ANGOLA
BODIVA
INE_ANGOLA
BANCO_MOCAMBIQUE
BVM_MOZAMBIQUE
INE_MOZAMBIQUE
BCV
AGMVM
BVC
INE_CABO_VERDE
CBS
FSA_SEYCHELLES
MERJ_EXCHANGE
NBS_SEYCHELLES
```

### Relations — 21

```text
BNA              CENTRAL_BANK                    ANGOLA
CMC_ANGOLA       CAPITAL_MARKET_REGULATOR         ANGOLA
CMC_ANGOLA       FUND_REGULATOR                   ANGOLA
BODIVA           STOCK_EXCHANGE                   ANGOLA
INE_ANGOLA       STATISTICS_OFFICE                ANGOLA

BANCO_MOCAMBIQUE CENTRAL_BANK                    MOZAMBIQUE
BANCO_MOCAMBIQUE CAPITAL_MARKET_REGULATOR         MOZAMBIQUE
BANCO_MOCAMBIQUE FUND_REGULATOR                   MOZAMBIQUE
BVM_MOZAMBIQUE   STOCK_EXCHANGE                   MOZAMBIQUE
INE_MOZAMBIQUE   STATISTICS_OFFICE                MOZAMBIQUE

BCV              CENTRAL_BANK                    CABO_VERDE
AGMVM            CAPITAL_MARKET_REGULATOR         CABO_VERDE
AGMVM            FUND_REGULATOR                   CABO_VERDE
BVC              STOCK_EXCHANGE                   CABO_VERDE
INE_CABO_VERDE   STATISTICS_OFFICE                CABO_VERDE

CBS               CENTRAL_BANK                    SEYCHELLES
FSA_SEYCHELLES    CAPITAL_MARKET_REGULATOR         SEYCHELLES
FSA_SEYCHELLES    FUND_REGULATOR                   SEYCHELLES
FSA_SEYCHELLES    INSURANCE_PENSION_REGULATOR      SEYCHELLES
MERJ_EXCHANGE     STOCK_EXCHANGE                   SEYCHELLES
NBS_SEYCHELLES    STATISTICS_OFFICE                SEYCHELLES
```

## 9. Hors allowlist

- aucun ministère des finances, office de dette, index provider ou FX reference provider ;
- aucune assurance/pension Angola, Mozambique ou Cabo Verde dans cette vague ;
- aucun rôle `INSURANCE_PENSION_REGULATOR` pour Banco de Moçambique, explicitement contraire à sa page de supervision ;
- aucun endpoint spécialisé, provider series, collection specification ou collection evidence ;
- aucune migration SQL runtime ;
- aucune donnée historique ;
- aucune modification de PR nº2, `main` ou cible de PR nº1 ;
- aucune nouvelle branche/PR.

## 10. Gate de sortie

```text
HEAD_RESOLVED: YES
4_NEW_COUNTRIES_RESEARCHED: YES
PRIMARY_OFFICIAL_EVIDENCE: YES_FOR_ALLOWLIST
CODE_COLLISIONS: NONE
MOZAMBIQUE_INSURANCE_PENSION_NEGATIVE_SCOPE: PRESERVED
AGMVM_DEPENDENCY_ON_BCV: DOCUMENTED
MERJ_DOMAIN_CONFIRMED_BY_FSA_DIRECTORY: YES
WAVE_04_ALLOWLIST_DEFINED: YES
CANONICAL_DATA_CHANGED_DURING_AUDIT: NO
```

La phase read-only est close. La prochaine phase est TDD : contrat RED vague 04, puis organisations, puis relations, avec GREEN Python 3.11/3.12 requis avant clôture.
