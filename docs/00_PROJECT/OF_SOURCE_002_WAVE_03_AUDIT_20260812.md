# OF-SOURCE-002 — Wave 03 institutional audit — 2026-08-12

```text
TASK_ID: OF-SOURCE-002
LOOP_ID: OF-LOOP-SOURCE-002
WAVE: 03
MODE: READ_ONLY_AUDIT_COMPLETED
AUDIT_START_HEAD: b0d69e33b5fd249dcc4011fe25437967b6105ecf
PRODUCTION_DEPLOYED: NO
RUNTIME_DATABASE_CHANGED: NO
REAL_HISTORY_LOADED: NO
NEW_BRANCH_CREATED: NO
NEW_PR_CREATED: NO
PR2_MODIFIED: NO
```

## 1. Objet

Poursuivre `OF-SOURCE-002` par un troisième lot contrôlé de quatre pays : `OUGANDA`, `ZAMBIE`, `ZIMBABWE`, `MALAWI`.

L'audit vérifie uniquement l'identité institutionnelle, le rôle prouvé et le domaine officiel primaire. Il n'autorise ni endpoint spécialisé, ni provider series, ni collection specification, ni SQL runtime, ni historique.

## 2. Baseline au départ

```text
AFRICAN_COUNTRIES: 54
ORGANIZATIONS: 71 = 51 VALIDATED + 20 PENDING
COUNTRIES_WITH_COUNTRY_SCOPED_ORGANIZATION: 14
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 40
ORGANIZATION_SCOPE_ROLES: 114 = 70 VALIDATED + 44 PENDING
SOURCE_ENDPOINTS: 43 = 20 VALIDATED + 23 PENDING
```

## 3. Ouganda

Sources officielles contrôlées :

```text
BOU         https://www.bou.or.ug/
CMA_UGANDA  https://cmauganda.co.ug/
USE_UGANDA  https://www.use.or.ug/
UBOS        https://www.ubos.org/
```

Preuves retenues :

- Bank of Uganda est la banque centrale de la République d'Ouganda ;
- Capital Markets Authority est l'autorité statutaire de régulation et de développement du marché des capitaux ;
- CMA régule explicitement les Collective Investment Schemes et leurs gestionnaires ;
- Uganda Securities Exchange est un securities exchange approuvé/licencié ;
- Uganda Bureau of Statistics est la source officielle et l'organe de coordination/supervision du National Statistical System.

Relations autorisées :

```text
BOU        CENTRAL_BANK
CMA_UGANDA CAPITAL_MARKET_REGULATOR
CMA_UGANDA FUND_REGULATOR
USE_UGANDA STOCK_EXCHANGE
UBOS       STATISTICS_OFFICE
```

Les régulateurs ougandais de l'assurance et des retraites restent hors allowlist : les deux fonctions sont séparées entre IRA et URBRA, alors que le rôle canonique actuel `INSURANCE_PENSION_REGULATOR` est combiné. Aucune fusion sémantique n'est inventée.

## 4. Zambie

Sources officielles retenues :

```text
BOZ        https://www.boz.zm/
LUSE       https://www.luse.co.zm/
ZAMSTATS   https://www.zamstats.gov.zm/
PIA_ZAMBIA https://www.pia.org.zm/
```

Preuves retenues :

- Bank of Zambia se présente explicitement comme la banque centrale et assure les mandats de stabilité/prudence prévus par la loi ;
- Lusaka Securities Exchange est la principale securities exchange de Zambie et exploite le marché de titres ;
- Zambia Statistics Agency est l'entité statutaire désignée pour la publication des statistiques officielles ;
- Pensions and Insurance Authority régule explicitement les deux domaines pensions et assurance.

Relations autorisées :

```text
BOZ        CENTRAL_BANK
LUSE       STOCK_EXCHANGE
ZAMSTATS   STATISTICS_OFFICE
PIA_ZAMBIA INSURANCE_PENSION_REGULATOR
```

### Incident de preuve — SEC Zambia

Le domaine historiquement associé à la Securities and Exchange Commission, `https://www.seczambia.org.zm/`, retourne actuellement un site de paris en turc sur sa racine. Des pages anciennes/indexées du même domaine et des sources gouvernementales zambiennes confirment l'existence légale de la SEC et sa compétence sur les securities/collective investment schemes, mais l'intégrité du domaine institutionnel courant n'est pas suffisamment fiable pour inscrire `SEC_ZAMBIA` comme `VALIDATED` dans cette vague.

Statut de décision :

```text
SEC_ZAMBIA: EXCLUDED_FROM_WAVE_03_ALLOWLIST
REASON: CURRENT_OFFICIAL_DOMAIN_INTEGRITY_BLOCKER
CAPITAL_MARKET_REGULATOR_ZAMBIA: NOT_WRITTEN_IN_WAVE_03
FUND_REGULATOR_ZAMBIA: NOT_WRITTEN_IN_WAVE_03
```

Aucune URL compromise ou ambiguë ne doit entrer dans `ORGANIZATIONS.csv` sous statut `VALIDATED`.

## 5. Zimbabwe

Sources officielles contrôlées :

```text
RBZ          https://www.rbz.co.zw/
SEC_ZIMBABWE https://seczim.co.zw/
ZSE          https://www.zse.co.zw/
ZIMSTAT      https://zimstat.co.zw/
IPEC         https://ipec.co.zw/
```

Preuves retenues :

- Reserve Bank of Zimbabwe se définit comme banque centrale et exerce son mandat de stabilité monétaire/financière ;
- Securities and Exchange Commission of Zimbabwe est le régulateur des securities et capital markets ;
- SECZim publie et administre le cadre des Collective Investment Schemes ;
- Zimbabwe Stock Exchange exploite le marché réglementé des titres ;
- ZIMSTAT produit et coordonne les statistiques officielles ;
- Insurance and Pensions Commission régule explicitement assurance et pensions.

Relations autorisées :

```text
RBZ          CENTRAL_BANK
SEC_ZIMBABWE CAPITAL_MARKET_REGULATOR
SEC_ZIMBABWE FUND_REGULATOR
ZSE          STOCK_EXCHANGE
ZIMSTAT      STATISTICS_OFFICE
IPEC         INSURANCE_PENSION_REGULATOR
```

## 6. Malawi

Sources officielles contrôlées :

```text
RBM         https://www.rbm.mw/
MSE_MALAWI  https://www.mse.co.mw/
NSO_MALAWI  https://www.nsomalawi.mw/
```

Preuves retenues :

- Reserve Bank of Malawi est la banque centrale ;
- le site officiel RBM présente explicitement une fonction `Capital Markets & Microfinance Supervision` ;
- le même cadre institutionnel présente `Pensions and Insurance Supervision`, ce qui satisfait le rôle canonique combiné ;
- Malawi Stock Exchange est la bourse licenciée opérant sous le Financial Services Act et le Securities Act ;
- National Statistical Office est le principal département gouvernemental responsable de la collecte et diffusion des statistiques officielles.

Relations autorisées :

```text
RBM        CENTRAL_BANK
RBM        CAPITAL_MARKET_REGULATOR
RBM        INSURANCE_PENSION_REGULATOR
MSE_MALAWI STOCK_EXCHANGE
NSO_MALAWI STATISTICS_OFFICE
```

`FUND_REGULATOR` n'est pas attribué à RBM dans cette vague : les pages primaires examinées prouvent la supervision du marché des capitaux mais ne fournissent pas une preuve suffisamment explicite de la compétence spécifique sur les Collective Investment Schemes/OPC selon la sémantique de ce rôle.

## 7. Collision review

Codes proposés :

```text
BOU
CMA_UGANDA
USE_UGANDA
UBOS
BOZ
LUSE
ZAMSTATS
PIA_ZAMBIA
RBZ
SEC_ZIMBABWE
ZSE
ZIMSTAT
IPEC
RBM
MSE_MALAWI
NSO_MALAWI
```

Recherche effectuée dans le dépôt avant écriture : aucune collision exacte détectée.

Les suffixes explicites évitent les collisions sémantiques avec les codes déjà présents (`CMA`, `CMA_KENYA`, `CMA_RWANDA`, `NSE`, `NBS_NIGERIA`, `NBS_TANZANIA`, etc.).

## 8. Allowlist fermée de vague 03

### Organisations — 16

```text
BOU
CMA_UGANDA
USE_UGANDA
UBOS
BOZ
LUSE
ZAMSTATS
PIA_ZAMBIA
RBZ
SEC_ZIMBABWE
ZSE
ZIMSTAT
IPEC
RBM
MSE_MALAWI
NSO_MALAWI
```

### Relations — 20

```text
BOU          CENTRAL_BANK                    OUGANDA
CMA_UGANDA   CAPITAL_MARKET_REGULATOR         OUGANDA
CMA_UGANDA   FUND_REGULATOR                   OUGANDA
USE_UGANDA   STOCK_EXCHANGE                   OUGANDA
UBOS         STATISTICS_OFFICE                OUGANDA

BOZ          CENTRAL_BANK                    ZAMBIE
LUSE         STOCK_EXCHANGE                  ZAMBIE
ZAMSTATS     STATISTICS_OFFICE               ZAMBIE
PIA_ZAMBIA   INSURANCE_PENSION_REGULATOR      ZAMBIE

RBZ          CENTRAL_BANK                    ZIMBABWE
SEC_ZIMBABWE CAPITAL_MARKET_REGULATOR         ZIMBABWE
SEC_ZIMBABWE FUND_REGULATOR                   ZIMBABWE
ZSE          STOCK_EXCHANGE                  ZIMBABWE
ZIMSTAT      STATISTICS_OFFICE               ZIMBABWE
IPEC         INSURANCE_PENSION_REGULATOR      ZIMBABWE

RBM          CENTRAL_BANK                    MALAWI
RBM          CAPITAL_MARKET_REGULATOR         MALAWI
RBM          INSURANCE_PENSION_REGULATOR      MALAWI
MSE_MALAWI   STOCK_EXCHANGE                  MALAWI
NSO_MALAWI   STATISTICS_OFFICE               MALAWI
```

## 9. Hors allowlist

- `SEC_ZAMBIA` tant que l'intégrité de son domaine officiel courant n'est pas rétablie/confirmée ;
- `FUND_REGULATOR` Malawi ;
- IRA Uganda / URBRA sans décision de modélisation du rôle combiné ;
- aucun ministère des finances, office de dette, index provider ou FX reference provider ;
- aucun endpoint spécialisé, provider series, collection specification ou collection evidence ;
- aucune migration SQL runtime ;
- aucune donnée historique.

## 10. Gate de sortie

```text
HEAD_RESOLVED: YES
4_NEW_COUNTRIES_RESEARCHED: YES
PRIMARY_OFFICIAL_EVIDENCE: YES_FOR_ALLOWLIST
CODE_COLLISIONS: NONE
SEC_ZAMBIA_DOMAIN_RISK_BLOCKED: YES
MALAWI_FUND_ROLE_NOT_INVENTED: YES
WAVE_03_ALLOWLIST_DEFINED: YES
CANONICAL_DATA_CHANGED_DURING_AUDIT: NO
```

La phase read-only est close. La prochaine phase est TDD : contrat RED de vague 03, puis organisations, puis relations, avec GREEN requis sur Python 3.11/3.12 avant clôture.
