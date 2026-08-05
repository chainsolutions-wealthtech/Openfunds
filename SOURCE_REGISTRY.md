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
| `ORGANIZATIONS.csv` | inventaire d'identité des institutions | 40 organisations, couverture partielle |
| `ORGANIZATION_SCOPE_ROLES.csv` | inventaire des rôles par périmètre | 70 relations, statuts mixtes |
| `SOURCE_ENDPOINTS.csv` | inventaire pages, portails, API et répertoires | découverte partielle |
| `COUNTRY_OR_ZONE_INDICATOR_SOURCE_MAPPING.csv` | inventaire indicateur vers source | 55 mappings initiaux |
| `PROVIDER_SERIES.csv` | inventaire de séries candidates | couverture partielle |
| `COLLECTION_SPECIFICATIONS.csv` | templates et règles d'extraction | couverture partielle |
| `COLLECTION_TEST_EVIDENCE.csv` | preuve de tests live | BCEAO et BEAC FX |
| `VALIDATED_FX_REFERENCE_REGISTRY.csv` | authoring gouverné des pilotes FX validés | BCEAO/XOF et BEAC/XAF |
| `PILOT_COLLECTION_READINESS.csv` | préparation des pilotes | 6 lignes |

## 3. MODELE D'AUTORITE

Conformément à `ADR-003` et `ADR-021` :

```text
INVENTAIRES CSV GENERAUX
→ DECOUVERTE ET REVUE, STATUTS MIXTES

VALIDATED_FX_REFERENCE_REGISTRY.csv
→ AUTHORING GOUVERNE DES PILOTES FX COLLECTION_TESTED

GENERATION SQL DETERMINISTE
→ SYNCHRONISATION ADDITIVE

POSTGRESQL
→ SOURCE DE VERITE RUNTIME
```

Le générateur est :

```text
scripts/generate_validated_fx_reference_sql.py
```

La migration est générée sous :

```text
schemas/reference/012_validated_fx_reference_registry.sql
```

Commandes :

```bash
python scripts/generate_validated_fx_reference_sql.py
python scripts/generate_validated_fx_reference_sql.py --check
python -m unittest tests/test_validated_fx_reference_registry.py -v
```

Les migrations historiques 008 à 011 restent conservées et rejouables. La migration 012 est régénérée depuis le registre gouverné, puis appliquée deux fois dans PostgreSQL 16 avec assertions.

## 4. STATUTS DE SOURCE

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

## 5. SOURCES LIVE VALIDEES

### BCEAO FX

```text
SCOPE                 UEMOA
LOCAL_CURRENCY        XOF
ENDPOINT               BCEAO_FX_DAILY
COLLECTOR              BCEAO_FX_SNAPSHOT
CANONICAL_OUTPUTS      XOF_EUR, XOF_USD
STATUS                 COLLECTION_TESTED
HISTORY                CURRENT_SNAPSHOT_ONLY
EVIDENCE_RUN           30777722357
```

Preuve : `docs/06_SOURCES/BCEAO_FX_COLLECTION_TEST_EVIDENCE.md`.

### BEAC FX

```text
SCOPE                 CEMAC
LOCAL_CURRENCY        XAF
ENDPOINT               BEAC_FX_DAILY
COLLECTOR              BEAC_FX_SNAPSHOT
CANONICAL_OUTPUTS      XAF_EUR, XAF_USD
STATUS                 COLLECTION_TESTED
HISTORY                CURRENT_SNAPSHOT_ONLY
EVIDENCE_RUN           30779605759
```

Preuve : `docs/06_SOURCES/BEAC_FX_COLLECTION_TEST_EVIDENCE.md`.

Les endpoints génériques de découverte restent distincts des endpoints de collecte validés.

## 6. SOURCES PARTIELLEMENT INVENTORIEES

Premiers périmètres amorcés : Maroc, Ghana, Nigeria, Tunisie, Egypte, Kenya, Afrique du Sud, UEMOA et CEMAC.

Domaines principalement ciblés : PIB, inflation, taux directeurs, FX, dette, courbes, indices actions, fonds et OPCVM.

La présence d'une URL officielle ne prouve pas que la série exacte, son historique et son parseur sont identifiés.

## 7. SOURCES OPCVM

### Tunisie

Le CMF et la base SQLite analysée constituent un pilote riche. La base n'est pas encore intégrée dans ce dépôt. Statut : `EXTERNAL_SOURCE_ANALYSED`.

### Nigeria

La SEC Nigeria est identifiée comme régulateur et source des fichiers hebdomadaires. Le pipeline complet d'audit et d'import depuis 2011 n'est pas présent. Statut : `SOURCE_IDENTIFIED / INGESTION_NOT_IMPLEMENTED`.

## 8. PREUVE OBLIGATOIRE

Un endpoint ou une série validée doit conserver : URL officielle, date de vérification, organisation et rôle, périmètre, fréquence, formats, conditions d'accès, méthode, spécification, test de collecte, artefact, SHA256, date économique, avertissements et erreurs.

Le registre gouverné stocke explicitement le run ID, le SHA256, la date de valeur, le timestamp de récupération, la version du parseur et le nombre d'observations.

## 9. SYNCHRONISATION BCEAO / BEAC

`OF-ARCH-001` et `OF-SOURCE-001` sont implémentés pour les pilotes FX testés :

- source d'authoring unique déclarée ;
- endpoints de collecte spécifiques ;
- mappings bruts, EUR et USD ;
- séries brutes et calculées ;
- spécifications brutes et calculées ;
- preuve de run reliée ;
- génération SQL déterministe ;
- double application PostgreSQL ;
- test de corruption de preuve ;
- aucune revendication d'historique complet.

Cette clôture ne concerne pas les taux directeurs, interbancaires, indices ou historiques complets.

## 10. COUVERTURE CIBLE PAR PAYS

Au minimum : banque centrale, institut statistique, ministère des finances, agence de dette, bourse, régulateur marchés/fonds, régulateur assurance/pension, dépositaire central si utile, séries macro/marché prioritaires et statut explicite pour les données non publiées.

## 11. REGLE DE PUBLICATION

Une source ne peut alimenter une donnée canonique publiée que si son identité et son rôle sont connus, l'endpoint est vérifié, la série et son unité sont identifiées, l'artefact brut est conservé, les contrôles passent, la provenance est disponible et le statut l'autorise.
