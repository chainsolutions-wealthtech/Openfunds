# REGISTRE DES SOURCES OPENFUNDS

## 1. OBJECTIF

Le registre relie un besoin de donnée à l'institution officielle, à la série fournisseur, à la méthode de collecte, à l'artefact brut et à l'observation canonique.

```text
COUNTRY_OR_ZONE
→ ORGANIZATION
→ ROLE
→ ENDPOINT
→ INDICATOR_MAPPING
→ PROVIDER_SERIES
→ COLLECTION_SPECIFICATION
→ COLLECTION_RUN
→ RAW_ARTIFACT
→ OBSERVATION
```

## 2. FICHIERS MACHINE-READABLE

| Fichier | Rôle | Etat |
|---|---|---|
| `ORGANIZATION_ROLES.csv` | vocabulaire des rôles | 21 rôles présents |
| `ORGANIZATIONS.csv` | identité des institutions | 40 organisations, couverture partielle |
| `ORGANIZATION_SCOPE_ROLES.csv` | rôle par périmètre | 70 relations, statuts mixtes |
| `SOURCE_ENDPOINTS.csv` | pages, portails, API et répertoires | 43 endpoints, plusieurs `PENDING` |
| `COUNTRY_OR_ZONE_INDICATOR_SOURCE_MAPPING.csv` | indicateur vers source | 55 mappings initiaux |
| `PROVIDER_SERIES.csv` | séries natives | 50 lignes, majorité à préciser |
| `COLLECTION_SPECIFICATIONS.csv` | règles d'extraction | 17 specs/templates |
| `COLLECTION_TEST_EVIDENCE.csv` | preuve de tests live | BCEAO et BEAC FX |
| `PILOT_COLLECTION_READINESS.csv` | préparation des pilotes | 6 lignes |

## 3. STATUTS DE SOURCE

```text
TO_IDENTIFY
SOURCE_IDENTIFIED
URL_LINKED
SPECIFICATION_DRAFTED
COLLECTOR_IMPLEMENTED
COLLECTION_TESTED
PARTIAL_HISTORY_LOADED
COMPLETE_HISTORY_LOADED
NOT_PUBLISHED
NOT_APPLICABLE
DISCONTINUED
REPLACED
```

Le statut d'organisation, d'endpoint, de série et d'historique reste séparé.

## 4. SOURCES LIVE VALIDEES

### BCEAO FX

```text
SCOPE                 UEMOA
LOCAL_CURRENCY        XOF
COLLECTOR             BCEAO_FX_SNAPSHOT
CANONICAL_OUTPUTS     XOF_EUR, XOF_USD
STATUS                COLLECTION_TESTED
HISTORY               CURRENT_SNAPSHOT_ONLY
```

Preuve : `docs/06_SOURCES/BCEAO_FX_COLLECTION_TEST_EVIDENCE.md`.

### BEAC FX

```text
SCOPE                 CEMAC
LOCAL_CURRENCY        XAF
COLLECTOR             BEAC_FX_SNAPSHOT
CANONICAL_OUTPUTS     XAF_EUR, XAF_USD
STATUS                COLLECTION_TESTED
HISTORY               CURRENT_SNAPSHOT_ONLY
```

Preuve : `docs/06_SOURCES/BEAC_FX_COLLECTION_TEST_EVIDENCE.md`.

## 5. SOURCES PARTIELLEMENT INVENTORIEES

Premiers périmètres amorcés :

- Maroc ;
- Ghana ;
- Nigeria ;
- Tunisie ;
- Egypte ;
- Kenya ;
- Afrique du Sud ;
- UEMOA ;
- CEMAC.

Domaines principalement ciblés :

- PIB et inflation ;
- taux directeurs ;
- FX ;
- dette et courbes ;
- indices actions ;
- fonds et OPCVM.

La présence d'une URL officielle ne prouve pas que la série exacte, son historique et son parseur sont identifiés.

## 6. SOURCES OPCVM

### Tunisie

Le CMF et la base SQLite analysée constituent un pilote riche. La base n'est pas encore intégrée dans ce dépôt. Statut : `EXTERNAL_SOURCE_ANALYSED`.

### Nigeria

La SEC Nigeria est identifiée comme régulateur et source des fichiers hebdomadaires. Le pipeline complet d'audit et d'import depuis 2011 n'est pas présent. Statut : `SOURCE_IDENTIFIED / INGESTION_NOT_IMPLEMENTED`.

## 7. PREUVE OBLIGATOIRE

Un endpoint ou une série validée doit conserver :

- URL officielle ;
- date de vérification ;
- organisation et rôle ;
- périmètre pays/zone ;
- fréquence ;
- formats ;
- historique disponible ;
- conditions d'accès ;
- méthode de découverte ;
- spécification ;
- test de collecte ;
- artefact et SHA256 ;
- date économique extraite ;
- avertissements et erreurs.

## 8. DIVERGENCE ACTUELLE CSV / SQL

Les seeds SQL BCEAO/BEAC portent des objets spécifiques validés, alors que certains CSV conservent des objets génériques `PENDING`.

Cette divergence est suivie par :

```text
OF-ARCH-001
OF-SOURCE-001
ADR-021
```

Aucune nouvelle source ne doit multiplier les représentations avant la résolution de cet écart.

## 9. COUVERTURE CIBLE PAR PAYS

Au minimum :

- banque centrale ou autorité monétaire ;
- institut statistique ;
- ministère des finances ;
- trésor ou agence de dette ;
- bourse, si applicable ;
- régulateur marchés/fonds ;
- régulateur assurance/pension ;
- dépositaire central, si utile ;
- séries macro et marché prioritaires ;
- statut explicite pour les données non publiées.

## 10. REGLE DE PUBLICATION

Une source ne peut alimenter une donnée canonique publiée que si :

1. son identité et son rôle sont connus ;
2. l'endpoint est vérifié ;
3. la série et son unité sont identifiées ;
4. la collecte conserve l'artefact brut ;
5. les contrôles qualité passent ;
6. la provenance est disponible ;
7. le statut de validation l'autorise.
