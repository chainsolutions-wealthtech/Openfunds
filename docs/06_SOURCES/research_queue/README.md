# File d’attente de recherche des sources officielles — PR nº 2

## Statut

```text
RESEARCH_CANDIDATE
CANONIQUE : NON
CHARGEMENT AUTOMATIQUE : INTERDIT
MIGRATION : AUCUNE
COLLECTION_TESTED : NON
HISTORIQUE CHARGE : NON
```

Cette file conserve uniquement les éléments de recherche utiles transmis par la PR nº 2, branche `agent/official-africa-source-handoff-20260803`.

Elle ne remplace aucun fichier de `data/reference/` et ne constitue pas une seconde source de vérité. Toute future intégration doit respecter l’arbitrage `ADR-021`, le modèle d’endpoint retenu par `OF-ARCH-002`, la gestion des dates inconnues de `ADR-022` et la stratégie de migrations de `ADR-023`.

## Point de contrôle de l’intégration documentaire

```text
PR CIBLE        #1
BRANCHE CIBLE   architecture/africafunds-country-indicators-v0.1
SHA AVANT AJOUT d0edaf521509d071c11b80ed9c3d1f1a881ab902
PR SOURCE       #2
BRANCHE SOURCE  agent/official-africa-source-handoff-20260803
```

## Actifs conservés

- `OFFICIAL_SOURCE_INVENTORY_20260803.csv` : 72 preuves de recherche, 16 colonnes, 11 périmètres, 39 organisations référencées ;
- `CANONICAL_INTEGRATION_MATRIX_20260803.csv` : 45 actions candidates, dépendances, statuts recommandés et interdictions.

Les deux fichiers conservent les libellés de la transmission. Les valeurs telles que `ENDPOINT_VERIFIED_DESK_RESEARCH`, `URL_LINKED`, `SOURCE_IDENTIFIED`, `MIXED`, `D03_D06` ou `NGN_USD` sont des informations de recherche et non des valeurs canoniques automatiquement acceptées.

## Utilité immédiate

La transmission évite de recommencer :

- la recherche des banques centrales, offices statistiques, bourses, régulateurs et agences de dette pour onze périmètres ;
- l’identification des pages officielles de taux, adjudications, courbes, indices et statistiques ;
- la distinction initiale entre taux directeurs, taux sans risque, taux interbancaires, taux bancaires et rendements souverains ;
- l’identification de MONIA, IBWAR, TMM, TRE, CONIA, NOFR, NOFRI, NIBOR, NITTY, KESONIA, TIMP et Repo Rate Namibia ;
- la préparation des travaux `OF-SOURCE-002`, `OF-SOURCE-003` et des phases 6 et 8 de `ROADMAP.md`.

## Organisations candidates à examiner

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
FMDQ
```

Les codes `BSE`, `NBE` et `ESX` nécessitent notamment un contrôle de collision dans le namespace global. L’identité juridique et les rôles de `FMDQ` doivent être contrôlés avant toute insertion.

## Rôles candidats à arbitrer

Deux rôles de la transmission ne figurent pas encore explicitement dans `ORGANIZATION_ROLES.csv` :

```text
MONETARY_STATISTICS_PROVIDER
FIXED_INCOME_MARKET_OPERATOR
```

Ils doivent être comparés à `CENTRAL_BANK`, `INTERBANK_MARKET_OPERATOR`, `STOCK_EXCHANGE`, `GOVERNMENT_SECURITIES_AGENCY` et `OTHER_OFFICIAL_DATA_PROVIDER` afin d’éviter un doublon sémantique.

`RISK_FREE_RATE` reste d’abord une caractéristique de série. Il ne doit pas être transformé automatiquement en rôle institutionnel.

## Séries nommées prioritaires

```text
MAROC      MONIA
GHANA      IBWAR
UEMOA      TAUX INTERBANCAIRE BCEAO
TUNISIE    TMM
TUNISIE    TRE
EGYPTE     CONIA
NIGERIA    NOFR ON
NIGERIA    NOFRI 30D
NIGERIA    NOFRI 90D
NIGERIA    NOFRI 180D
NIGERIA    NIBOR PAR TENOR
NIGERIA    NITTY PAR TENOR
NIGERIA    MPR
KENYA      KESONIA
CEMAC      TIMP
NAMIBIE    REPO RATE
ETHIOPIE   OVERNIGHT INTERBANK
ETHIOPIE   7-DAY INTERBANK
```

Aucune date de début historique n’est attestée par cette transmission. Les codes fournisseur exacts et politiques de révision restent à vérifier.

## Règles financières à préserver

Ne jamais fusionner automatiquement :

- taux directeur ;
- facilité de dépôt ;
- facilité de prêt marginal ;
- taux sans risque overnight ;
- indice composé d’un taux sans risque ;
- taux interbancaire offert ;
- taux interbancaire moyen pondéré ;
- taux d’épargne ;
- taux de dépôt à terme ;
- taux de prêt ;
- taux de découvert ;
- rendement de bon du Trésor ;
- rendement obligataire primaire ;
- rendement obligataire secondaire ;
- point de courbe observé ;
- courbe interpolée ;
- taux forward calculé.

Pour le Nigeria, NOFR, NOFRI 30D, 90D et 180D, NIBOR, NITTY, MPR, NTB et FGN Bonds restent des objets distincts.

## UEMOA et CEMAC

- conserver une série véritablement régionale une seule fois au niveau de la zone ;
- conserver le pays émetteur des titres souverains ;
- ne pas créer une dette ou une courbe souveraine fictive UEMOA/CEMAC ;
- ne pas dupliquer BCEAO ou BEAC pour chaque pays membre ;
- ne pas modifier les collecteurs, seeds ou statuts BCEAO/BEAC pendant l’exploitation de cette file.

## Indices actions

Candidats de recherche :

```text
MASI
GSE COMPOSITE INDEX
BRVM COMPOSITE
TUNINDEX
EGX30 ET AUTRES INDICES EGX SELON METHODOLOGIE
NGX ALL-SHARE INDEX
NSE ALL SHARE INDEX
BVMAC ALL SHARE INDEX
BOTSWANA DOMESTIC COMPANY INDEX
NSX OVERALL
NSX LOCAL
```

Chaque future série doit préciser `PRICE_INDEX`, `GROSS_TOTAL_RETURN_INDEX`, `NET_TOTAL_RETURN_INDEX` ou `RECONSTRUCTED_TOTAL_RETURN_INDEX`. Aucun grand indice éthiopien ne doit être déclaré sans méthodologie officielle.

## Sources soumises à licence ou demande

```text
GSE HISTORICAL DATA
BRVM HISTORICAL DATA
FMDQ MARKET DATA
NGX HISTORICAL DATA
NSE HISTORICAL DATA
NSX / EVENTUELLE LICENCE FTSE
```

Ces éléments doivent rester `REQUIRES_LICENSE_REVIEW`. Une URL publique de présentation ne donne pas automatiquement le droit de télécharger ou republier l’historique.

## Incohérences déjà identifiées dans la PR nº 1

La future réconciliation devra contrôler sans correction automatique :

1. `PS_TUNISIE_OPCVM` est marqué `PARTIAL_HISTORY_LOADED` alors que l’import canonique de la base tunisienne n’est pas présent dans le dépôt ;
2. certains cas de test BCEAO/BEAC restent `TO_IMPLEMENT` alors que les preuves live correspondantes sont `COLLECTION_TESTED` ;
3. les CSV génériques BCEAO/BEAC restent en décalage avec les seeds SQL validés ;
4. `source.endpoint` et `source.source_endpoint` ne sont pas encore définitivement arbitrés ;
5. les plages de domaines comme `D03_D06`, les fréquences `MIXED` et les devises composites comme `NGN_USD` ne sont pas des valeurs canoniques finales.

## Ordre d’exploitation

```text
OF-ARCH-001
→ OF-SOURCE-001
→ OF-ARCH-002
→ OF-ARCH-003
→ OF-ARCH-004
→ REVUE DES ROLES
→ REVUE DES ORGANISATIONS
→ RELATIONS ORGANISATION-ROLE-PERIMETRE
→ ENDPOINTS SPECIALISES
→ MAPPINGS
→ SERIES FOURNISSEURS
→ SPECIFICATIONS
→ COLLECTEURS
→ FIXTURES ET TESTS
→ PREUVES DE COLLECTE
→ PERSISTANCE
→ COUVERTURE HISTORIQUE
```

## Critère de sortie de la file de recherche

Un élément ne quitte cette file que lorsqu’il possède, selon sa nature :

- une identité officielle revue ;
- un code sans collision ;
- un rôle et un périmètre validés ;
- un endpoint réel vérifié ;
- une série native précise ;
- une fréquence, unité, devise et maturité non ambiguës ;
- une licence examinée ;
- une spécification testée sur un artefact réel ;
- un SHA-256 ;
- un test d’idempotence ;
- une preuve compatible avec le niveau de statut demandé.
