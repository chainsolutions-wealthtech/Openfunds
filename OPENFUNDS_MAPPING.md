# MAPPING OPENFUNDS VERS LE MODELE CANONIQUE

Dernière mise à jour : `2026-08-17`.

## 1. Statut réel

```text
VERSION OFFICIELLE VERIFIEE          2.13.0
DATE DE RELEASE                      2026-03-23
DOCUMENT                             FINAL
LICENCE DOCUMENT OFFICIEL            CC BY-ND 4.0 / attribution openfunds.org
ARCHIVE OFFICIELLE                   BYTE-IDENTICAL / CHECKSUM-LOCKED
SHA256                               40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4
PDF                                  745 PAGES / 2,957,096 OCTETS
INVENTAIRE OFFICIEL                  1,869 OF-ID
IDS CONCRETS                         1,849
TEMPLATES PAYS XX                    20
CANONICAL CORE                       143 FIELDS
CANONICAL LISTING EXTENSION          34 FIELDS
CANONICAL INVENTORY FOR MAPPING      177 FIELDS
REVIEWED MAPPING ROWS                16
MAPPED EXTERNAL OF-ID                8
UNMAPPED EXTERNAL OF-ID              1,861
MAPPED CANONICAL FIELD_ID            10
OF-MAP-001                           TERMINE
OF-MAP-002                           EN_COURS — BATCH 01..05 VALIDES
```

## 2. Sources gouvernées

Archive officielle :

```text
data/openfunds/official/v2.13.0/openfunds_fields_v2.13.0.pdf
```

Checksum :

```text
data/openfunds/official/v2.13.0/openfunds_fields_v2.13.0.pdf.sha256
```

Parser checksum-gated :

```text
scripts/parse_openfunds_v2_13_0.py
```

Registre :

```text
data/openfunds/mapping/v2.13.0/MAPPING_REGISTRY.csv
```

Manifeste :

```text
data/openfunds/mapping/v2.13.0/mapping_manifest.json
```

Validateur :

```text
scripts/validate_openfunds_mapping_registry.py
```

## 3. Architecture canonique disponible

Le dictionnaire migration-015 reste immuable :

```text
data/dictionary/spec_v1/
143 champs
version 1.0.0
VALIDATED_FUND_CORE_SCOPE
```

La migration 019 a créé un modèle distinct de cotation :

```text
fund.listing
fund.listing_identifier
```

Son dictionnaire est une extension additive :

```text
data/dictionary/extensions/listing_v1/
34 champs
version 1.0.0
VALIDATED_LISTING_EXTENSION_SCOPE
```

Le validateur construit au runtime une union collision-free :

```text
143 + 34 = 177 FIELD_ID
```

Les collisions de FIELD_ID, incohérences d'entité ou dérives du `field_count` échouent fermées. Le core 143 n'est pas réécrit par les extensions.

ADR :

```text
docs/02_ARCHITECTURE/ADR-031_CANONICAL_LISTING_DICTIONARY_EXTENSION.md
```

## 4. Principes de mapping

Le canonique est la représentation interne ; Openfunds est un standard externe versionné.

```text
OPENFUNDS FIELD
→ SOURCE VERSION + SHA256
→ FIELD LEVEL / TYPE / VALUES / LICENCE
→ PARSING
→ TRANSFORMATION EXPLICITE
→ CANONICAL ENTITY
→ CANONICAL FIELD_ID
→ VALIDATION
→ IMPORT/EXPORT GATES
```

Règles impératives :

1. aucun OF-ID, nom, niveau, type ou valeur autorisée ne peut être inventé ;
2. l'archive officielle n'est jamais modifiée ;
3. un champ externe ne devient pas automatiquement une colonne ;
4. `CANONICAL_ENTITY` doit correspondre à l'entité gouvernée du FIELD_ID ;
5. une transformation doit être déterministe ;
6. toute perte d'information est explicite ;
7. `XX` reste un template et n'est pas développé artificiellement ;
8. les doublons `(EXTERNAL_FIELD_ID, CANONICAL_FIELD_ID)` sont interdits ;
9. un mapping sémantiquement valide peut rester non activable si une licence ou une dépendance runtime l'impose ;
10. le registre contient uniquement des mappings réellement revus — aucun catalogue artificiel de 1 869 lignes `UNMAPPED` ;
11. les anciens batches doivent rester forward-compatible et ne jamais figer la taille totale future du registre.

## 5. Batches vérifiés

### Batch 01 — domicile + ISIN

Run GREEN : `32065216172`.

```text
OFST010010 Fund Domicile Alpha-2
→ OF_FUND_FUND_ENTITY_STATE_DOMICILE_COUNTRY_ID
→ ISO_3166_ALPHA2_TO_REF_GEOGRAPHY_UUID

OFST020000 ISIN
→ identifier_value
→ identifier_scheme = ISIN
→ normalized_value
```

### Batch 02 — devises Fund / Share Class

Run GREEN : `32067722365`.

```text
OFST010410 Fund Currency
→ OF_FUND_FUND_PROFILE_BASE_CURRENCY_ID
→ ISO_4217_TO_REF_CURRENCY_UUID

OFST020540 Share Class Currency
→ OF_FUND_SHARE_CLASS_PROFILE_CURRENCY_ID
→ ISO_4217_TO_REF_CURRENCY_UUID
```

### Batch 03 — Valor + WKN

Run GREEN : `32069647430`.

```text
OFST020010 Valor
→ value / scheme VALOR / normalized value

OFST020015 WKN
→ value / scheme WKN / normalized value
```

SEDOL a été volontairement différé à ce stade parce que son `Field Level` officiel est `Listing`.

### Batch 04 — distribution policy

Run GREEN : `32070575644`.

```text
OFST020400 Share Class Distribution Policy
accumulating                → ACCUMULATING
accumulating & distributing → MIXED
distributing                → DISTRIBUTING
```

Aucune perte d'information.

### Batch 05 — SEDOL au bon niveau Listing

Audit officiel checksum-locké : `32071520665`.

Run GREEN mapping : `32071858346`.

Le record officiel établit :

```text
OF-ID       OFST020040
FIELD NAME  SEDOL
FIELD LEVEL Listing
DATA TYPE   string
```

Mapping :

```text
OFST020040
→ OF_FUND_LISTING_IDENTIFIER_IDENTIFIER_VALUE
→ OF_FUND_LISTING_IDENTIFIER_IDENTIFIER_SCHEME
→ OF_FUND_LISTING_IDENTIFIER_NORMALIZED_VALUE
```

Règles :

```text
IDENTITY
CONSTANT_SEDOL
TRIM_AND_UPPERCASE_SEDOL
```

Le record officiel contient une alerte de licence pouvant concerner ingestion, stockage ou distribution. Par conséquent :

```text
SEMANTIC_MAPPING    VALIDATED
INFORMATION_LOSS    NONE
IMPORT_SUPPORTED    NO
EXPORT_SUPPORTED    NO
ACTIVATION_GATE     EXPLICIT_SEDOL_LICENSING_CLEARANCE
```

Preuve permanente :

```text
docs/00_PROJECT/OF_MAP_002_BATCH_05_SEDOL_COMPLETION_20260817.md
```

## 6. Couverture actuelle

```text
OFFICIAL_FIELDS                1869
REVIEWED_MAPPING_ROWS            16
MAPPED_EXTERNAL_IDS               8
UNMAPPED_EXTERNAL_IDS          1861
CANONICAL_FIELDS_AVAILABLE      177
MAPPED_CANONICAL_IDS             10
```

Cette faible couverture n'est pas un défaut du registre : elle reflète la règle de ne valider que des équivalences démontrées.

## 7. Validation technique

Le validateur :

- reparse le PDF checksum-locké ;
- reconstruit les 143 FIELD_ID du core ;
- charge les extensions canoniques explicitement déclarées ;
- rejette les collisions ;
- vérifie les entités ;
- rejette les OF-ID inconnus ;
- rejette les FIELD_ID inconnus ;
- vérifie source SHA/reference ;
- laisse le checkout inchangé.

Union core+Listing GREEN : `32071385088`.

Batch 05 GREEN complet : `32071858346`.

## 8. Prochaine unité — Batch 06

Auditer dans le PDF officiel les champs de niveau `Listing` qui peuvent exploiter directement migration 019 :

```text
VENUE / MIC
LISTING CURRENCY
TICKER / LOCAL LISTING IDENTIFIER
PRIMARY LISTING INDICATOR
```

Pour chaque candidat :

1. rechercher l'OF-ID exact dans l'archive checksum-lockée ;
2. vérifier `Field Level`, type, description, valeurs et licence ;
3. confirmer que le champ canonique 019 existe ;
4. écrire un contrat TDD RED ;
5. ajouter uniquement les mappings démontrés ;
6. exiger GREEN Python 3.11/3.12 + intégration PDF officielle.

Les noms Fund/SubFund/Umbrella, documents, frais, benchmarks, eligibility, ESG et autres domaines complexes restent des boucles séparées : ne pas créer de fausses équivalences pour accélérer artificiellement le taux de couverture.

## 9. Gates encore ouverts

```text
FULL_1869_FIELD_MAPPING       EN_COURS
SEDOL_RUNTIME                 BLOQUE_PAR_LICENCE
PERSISTENT_POSTGRESQL         NON_CONFIGURE
IMMUTABLE_RAW_STORE           NON_CONFIGURE
COMPLETE_HISTORIES            NON_CHARGES
BENCHMARK_RFR_MAR             NON_COMPLETEMENT_VALIDES
WTI_WTI_BENCH                 NOT_ACTIVE
PRODUCTION_API_UI             NON_IMPLEMENTE
PRODUCTION_DEPLOYMENT         NON_CONFIGURE
```

`OF-MAP-001` est `TERMINE`. `OF-MAP-002` reste `EN_COURS` jusqu'à revue explicite du catalogue, sans objectif artificiel de 100 % si certains champs n'ont pas d'équivalent canonique ou sont juridiquement/techniquement non activables.
