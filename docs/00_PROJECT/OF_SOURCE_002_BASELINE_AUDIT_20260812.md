# OF-SOURCE-002 — Baseline institutional coverage audit — 2026-08-12

```text
TASK_ID: OF-SOURCE-002
MODE: READ_ONLY_AUDIT_COMPLETED
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
AUDIT_START_HEAD: ddeee85042d37803bd27bc9cda81cc2e67856c57
PLAN_HEAD: 8841193c03ea89fd51c0fd8cba3b7d420aab3e00
PRODUCTION_DEPLOYED: NO
RUNTIME_DATABASE_CHANGED: NO
REAL_HISTORY_LOADED: NO
PR2_MODIFIED: NO
```

## 1. Objet

Établir la baseline réelle de `OF-SOURCE-002` avant toute modification des registres institutionnels. L’audit compare les 54 pays canoniques avec `ORGANIZATIONS.csv`, `ORGANIZATION_ROLES.csv`, `ORGANIZATION_SCOPE_ROLES.csv`, `SOURCE_ENDPOINTS.csv` et les actifs de recherche de la PR nº2.

La PR nº2 reste une source de recherche non canonique. Aucune ligne de cette PR n’est copiée aveuglément et aucun statut de collecte/historique n’est promu à partir de desk research.

## 2. Baseline chiffrée

```text
AFRICAN_COUNTRIES: 54
ORGANIZATIONS_TOTAL: 40
ORGANIZATIONS_VALIDATED: 20
ORGANIZATIONS_PENDING: 20
COUNTRY_SCOPED_ORGANIZATIONS: 33
ZONE_OR_OTHER_ORGANIZATIONS: 7
COUNTRIES_WITH_COUNTRY_SCOPED_ORGANIZATION: 7
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 47

ORGANIZATION_SCOPE_ROLES_TOTAL: 70
ORGANIZATION_SCOPE_ROLES_VALIDATED: 26
ORGANIZATION_SCOPE_ROLES_PENDING: 44

SOURCE_ENDPOINTS_TOTAL: 43
SOURCE_ENDPOINTS_VALIDATED: 20
SOURCE_ENDPOINTS_PENDING: 23
```

Pays possédant actuellement au moins une organisation propre :

```text
AFRIQUE_DU_SUD
MAROC
GHANA
NIGERIA
TUNISIE
EGYPTE
KENYA
```

Le reste des 54 pays ne possède pas encore d’organisation country-scoped dans `ORGANIZATIONS.csv`. Les pays UEMOA/CEMAC peuvent néanmoins disposer de structures communes au niveau zone ; cette présence ne doit pas être comptée comme une institution nationale lorsqu’un rôle est national.

## 3. Réconciliation de la PR nº2

La PR nº2 propose 16 nouvelles organisations. Aucun des 16 codes proposés n’existe actuellement comme `ORGANIZATION_CODE` dans le registre de la branche de contrôle.

Classification après audit :

| Code | Scope | Classification | Gate |
|---|---|---|---|
| BOB | BOTSWANA | NEW_ORGANIZATION_CANDIDATE | identité + rôle central bank vérifiés sur domaine officiel |
| NBFIRA | BOTSWANA | NEW_ORGANIZATION_CANDIDATE | identité + capital markets/funds/insurance/pensions vérifiés |
| BSE | BOTSWANA | NEW_ORGANIZATION_CANDIDATE | identité + stock exchange vérifiés |
| STATISTICS_BOTSWANA | BOTSWANA | NEW_ORGANIZATION_CANDIDATE | identité + statistics office vérifiés |
| BON | NAMIBIE | NEW_ORGANIZATION_CANDIDATE | identité + central bank vérifiés |
| NAMFISA | NAMIBIE | NEW_ORGANIZATION_CANDIDATE | identité + capital markets/funds/insurance/pensions vérifiés |
| NSX | NAMIBIE | NEW_ORGANIZATION_CANDIDATE | identité + stock exchange vérifiés ; nom courant Namibia Securities Exchange |
| NSA_NAMIBIA | NAMIBIE | NEW_ORGANIZATION_CANDIDATE | identité + statistics office vérifiés |
| NBE | ETHIOPIE | NEW_ORGANIZATION_CANDIDATE | identité + central bank vérifiés |
| ECMA | ETHIOPIE | NEW_ORGANIZATION_CANDIDATE | identité + capital-market/fund regulation vérifiés |
| ESX | ETHIOPIE | NEW_ORGANIZATION_CANDIDATE | identité + securities exchange vérifiés |
| ESS_ETHIOPIA | ETHIOPIE | NEW_ORGANIZATION_CANDIDATE | identité + statistics office vérifiés |
| AMF_UMOA | UEMOA | NEW_ORGANIZATION_CANDIDATE | identité + capital-market/fund regulation vérifiés |
| UMOA_TITRES | UEMOA | NEW_ORGANIZATION_CANDIDATE | identité + appui/gestion des émissions publiques vérifiés |
| COSUMAF | CEMAC | NEW_ORGANIZATION_CANDIDATE | identité + capital-market/fund regulation vérifiés |
| FMDQ | NIGERIA | REQUIRES_ROLE_MODEL_REVIEW | identité vérifiable, mais rattachement exact à la taxonomie de rôles à décider séparément |

## 4. Sources officielles contrôlées pour la vague 01

```text
BOB                 https://www.bankofbotswana.bw/
NBFIRA              https://www.nbfira.org.bw/
BSE                 https://www.bse.co.bw/
STATISTICS_BOTSWANA https://www.statsbots.org.bw/
BON                 https://www.bon.com.na/
NAMFISA             https://www.namfisa.com.na/
NSX                 https://nsx.com.na/
NSA_NAMIBIA         https://nsa.org.na/
NBE                 https://nbe.gov.et/
ECMA                https://ecma.gov.et/
ESX                 https://esx.et/
ESS_ETHIOPIA        https://ess.gov.et/
AMF_UMOA            https://www.amf-umoa.org/
UMOA_TITRES         https://www.umoatitres.org/
COSUMAF             https://webcosumaf.org/
```

Les preuves contrôlées portent sur l’identité institutionnelle et les rôles indiqués. Elles n’attestent aucune collecte, aucune série historique et aucune persistance PostgreSQL.

## 5. Allowlist d’écriture — vague 01

### Organisations autorisées

```text
BOB
NBFIRA
BSE
STATISTICS_BOTSWANA
BON
NAMFISA
NSX
NSA_NAMIBIA
NBE
ECMA
ESX
ESS_ETHIOPIA
AMF_UMOA
UMOA_TITRES
COSUMAF
```

### Relations de rôle autorisées

```text
BOB                 CENTRAL_BANK                       BOTSWANA
NBFIRA              CAPITAL_MARKET_REGULATOR            BOTSWANA
NBFIRA              FUND_REGULATOR                      BOTSWANA
NBFIRA              INSURANCE_PENSION_REGULATOR         BOTSWANA
BSE                 STOCK_EXCHANGE                      BOTSWANA
STATISTICS_BOTSWANA STATISTICS_OFFICE                   BOTSWANA

BON                 CENTRAL_BANK                        NAMIBIE
NAMFISA             CAPITAL_MARKET_REGULATOR            NAMIBIE
NAMFISA             FUND_REGULATOR                      NAMIBIE
NAMFISA             INSURANCE_PENSION_REGULATOR         NAMIBIE
NSX                 STOCK_EXCHANGE                      NAMIBIE
NSA_NAMIBIA         STATISTICS_OFFICE                   NAMIBIE

NBE                 CENTRAL_BANK                        ETHIOPIE
ECMA                CAPITAL_MARKET_REGULATOR            ETHIOPIE
ECMA                FUND_REGULATOR                      ETHIOPIE
ESX                 STOCK_EXCHANGE                      ETHIOPIE
ESS_ETHIOPIA        STATISTICS_OFFICE                   ETHIOPIE

AMF_UMOA            CAPITAL_MARKET_REGULATOR            UEMOA
AMF_UMOA            FUND_REGULATOR                      UEMOA
UMOA_TITRES         GOVERNMENT_SECURITIES_AGENCY        UEMOA
COSUMAF             CAPITAL_MARKET_REGULATOR            CEMAC
COSUMAF             FUND_REGULATOR                      CEMAC
```

## 6. Éléments explicitement hors allowlist

- `FMDQ` jusqu’à revue du rôle canonique exact ;
- tout `INDEX_PROVIDER` non vérifié pendant cette vague ;
- tout `FX_REFERENCE_RATE_PROVIDER` non vérifié pendant cette vague ;
- ministères des finances et offices de dette non étudiés pendant cette vague ;
- endpoints spécialisés, provider series et collection specifications : vague ultérieure ;
- aucune ligne de `COLLECTION_TEST_EVIDENCE.csv` ;
- aucune migration SQL runtime ;
- aucun historique réel.

## 7. Critère de sortie de l’audit

```text
HEAD_AND_LINEAGE_VERIFIED: YES
54_COUNTRY_BASELINE_MEASURED: YES
PR2_CANDIDATES_RECONCILED: YES
CODE_COLLISION_OBSERVED_FOR_ALLOWLIST: NO
OFFICIAL_IDENTITY_EVIDENCE_CHECKED: YES
ALLOWLIST_DEFINED: YES
CANONICAL_REFERENCE_CHANGED_DURING_AUDIT: NO
```

La phase read-only est close. L’étape suivante peut créer un contrôle exécutable des invariants institutionnels, puis intégrer la vague 01 en petits commits. `OF-SOURCE-002` reste `EN_COURS` et ne pourra être clôturé qu’après couverture documentée des 54 pays et des rôles attendus, avec `NOT_APPLICABLE/NOT_PUBLISHED` explicites lorsqu’ils sont justifiés.
