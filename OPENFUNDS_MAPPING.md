# MAPPING OPENFUNDS VERS LE MODELE CANONIQUE

## État courant — 2026-08-22

```text
VERSION_OFFICIELLE                    2.13.0 FINAL / 2026-03-23
SOURCE_SHA256                         40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4
OFFICIAL_FIELD_RECORDS                1869
CONCRETE_IDS                          1849
PARAMETERIZED_XX_TEMPLATES              20
CANONICAL_CORE_FIELDS                  143
CANONICAL_EXTENSION_FIELDS             152
CANONICAL_TOTAL_FIELDS                 295
REVIEWED_MAPPING_ROWS                   93
MAPPED_EXTERNAL_IDS                     50
UNMAPPED_EXTERNAL_IDS                 1819
MAPPED_CANONICAL_IDS                    53
LATEST_BATCH                            27
LATEST_MAPPING                    MAP-000093
OF-MAP-001                         TERMINE
OF-MAP-002                         EN_COURS
RECENT_REMOTE_CI                  PENDING_NOT_OBSERVABLE
```

Le registre canonique est fermé structurellement jusqu'à Batch 27. Cela ne signifie ni mapping complet des 1 869 records, ni GREEN CI récent, ni activation production.

## Autorités machine

```text
data/openfunds/official/v2.13.0/openfunds_fields_v2.13.0.pdf
data/openfunds/official/v2.13.0/openfunds_fields_v2.13.0.pdf.sha256
scripts/parse_openfunds_v2_13_0.py
data/openfunds/mapping/v2.13.0/MAPPING_REGISTRY.csv
data/openfunds/mapping/v2.13.0/mapping_manifest.json
scripts/validate_openfunds_mapping_registry.py
```

Le registre de revue complémentaire est désormais :

```text
data/openfunds/mapping/v2.13.0/REVIEW_OUTCOMES.csv
scripts/validate_openfunds_review_outcomes.py
tests/test_openfunds_review_outcomes.py
```

`REVIEW_OUTCOMES.csv` est volontairement **sparse**. Il ne duplique pas les OF-IDs présents dans `MAPPING_REGISTRY.csv`.

## Doctrine de couverture reason-classifiée

Pour tout OF-ID officiel, le résultat final doit être dérivable vers une catégorie explicite :

```text
MAPPED_CANONICAL
MAPPED_DERIVED
NO_CANONICAL_EQUIVALENT
DEFERRED_NOT_REQUIRED_FOR_PRODUCT
GATED_VENDOR_OR_LICENSE
TO_CONFIRM
UNREVIEWED   # état calculé de travail, jamais matérialisé comme fausse ligne de mapping
```

Règles :

1. les catégories mappées sont dérivées de `MAPPING_REGISTRY.csv` ;
2. le fichier sparse ne stocke que les décisions non mappées/deferred/gated/TO_CONFIRM ;
3. un OF-ID déjà mappé ne peut pas être dupliqué dans `REVIEW_OUTCOMES.csv` ;
4. chaque décision sparse exige un `REASON_CODE` ;
5. chaque OF-ID et chaque source reference doivent exister dans l'inventaire officiel checksum-locké ;
6. `TO_CONFIRM` reste un blocker et n'est jamais compté comme terminé ;
7. les templates `XX` restent des templates ;
8. `DEFERRED_NOT_REQUIRED_FOR_PRODUCT` est une décision de périmètre produit, pas un jugement sur l'importance générale du champ Openfunds ;
9. aucune génération artificielle de 1 869 lignes `UNMAPPED` n'est autorisée.

Le validator calcule une partition : mapped / reviewed nonmapped / vendor gated / to-confirm / unreviewed. La somme doit être exactement 1 869.

## Principes de mapping permanents

```text
OPENFUNDS FIELD
→ OFFICIAL VERSION + SHA256
→ FIELD LEVEL / TYPE / VALUES / CARDINALITY
→ EXISTING CANONICAL TARGET AUDIT
→ RED CONTRACT
→ OPTIONAL FORWARD MIGRATION IF NEEDED
→ EXPLICIT TRANSFORMATION
→ CANONICAL FIELD / RELATION
→ VALIDATION
→ IMPORT/EXPORT GATES
→ DIFF REVIEW
```

- Openfunds est un standard d'échange, jamais le schéma physique runtime.
- Un champ externe ne devient pas automatiquement une colonne.
- Une valeur absente ne devient ni zéro, ni date, ni devise inventée.
- Les concepts répétables deviennent des relations/lignes versionnées, pas des pipe strings canoniques.
- Les vendor identifiers gardent leur scheme propre et leurs gates d'usage.
- Les tests historiques ne figent pas la taille cumulative future du registre.

## Batches 01–05 — baselines distantes vérifiées

```text
Batch 01 domicile/ISIN              GREEN 32065216172
Batch 02 Fund/ShareClass currency   GREEN 32067722365
Batch 03 Valor/WKN                  GREEN 32069647430
Batch 04 distribution policy        GREEN 32070575644
Batch 05 SEDOL Listing              GREEN 32071858346
```

SEDOL reste runtime import/export `NO` derrière `EXPLICIT_SEDOL_LICENSING_CLEARANCE`.

## Batches 06–19 — modèle Listing, temps, multicurrency, lifecycle

Implémentés structurellement, mais sans nouvelle attestation distante observable :

- MIC, primary listing, listing date ;
- quote-unit semantics ;
- listing business status ;
- Bloomberg/RIC Listing et iNAV identifiers ;
- listing inception price ;
- NAV/trading-price frequencies ;
- valuation time + IANA semantics ;
- additional dealing currencies ;
- precise lifecycle phase ;
- repeatable lifecycle events ;
- investment/dealing access status.

Invariants : Listing status ≠ bitemporal `is_current`; iNAV ≠ Listing identity; timezone label ≠ IANA; lifecycle ≠ investment status.

## Batches 20–27 — ETF / passive / replication / benchmark / tracked index

### Batch 20

`OFST010580 Is ETF` -> Share Class `is_etf`. Jamais inféré au niveau Fund.

### Batch 21

`OFST010720 Is Passive Fund` -> Fund `is_passive`. Jamais utilisé pour inférer ETF.

### Batch 22

`OFST010900/010901` -> méthodologie de réplication Fund. Les détails `hybrid` sont normalisés en lignes.

### Batch 23

`OFST023200 Benchmark` -> composantes benchmark ordonnées : ordre, nom, poids optionnel explicite.

### Batch 24

`OFST023205` -> identifiants Bloomberg des composantes benchmark, alignés par ordre. Runtime `NO/NO` derrière revue d'usage propriétaire projet.

### Batch 25

`OFST023800/023805/023810` -> tracked index Share Class : nom, devise/mode, type.

`OFST023805` vide signifie explicitement `LOCAL_CURRENCY` avec `currency_id = NULL` ; aucune devise Share Class n'est inventée.

### Batch 26

`OFST023820/023830` -> identifiants tracked-index Bloomberg/RIC. RIC reste case-sensitive ; normalisation trim-only.

### Batch 27

`OFST023850 Denomination Base` -> ratio positif explicite `Fund Price / Index`.

Aucun prix de fonds ni niveau d'index n'est déduit de ce ratio.

## Gates ouverts

```text
PRODUCT_REQUIRED_FAMILIES          EN_COURS
REASON_CLASSIFIED_1869_REVIEW      EN_COURS
RECENT_REMOTE_CI                   PENDING_NOT_OBSERVABLE
SEDOL_RUNTIME                      LICENSING_CLEARANCE_REQUIRED
BLOOMBERG_RIC_RUNTIME              PROPRIETARY_USAGE_REVIEW_REQUIRED
PERSISTENT_POSTGRESQL              NOT_CONFIGURED
IMMUTABLE_RAW_STORE                NOT_CONFIGURED
COMPLETE_HISTORIES                 NOT_LOADED
BENCHMARK_RFR_MAR                  NOT_FULLY_VALIDATED
WTI_WTI_BENCH                      NOT_ACTIVE
PRODUCTION_API_UI                  NOT_IMPLEMENTED
PRODUCTION_DEPLOYMENT              NOT_CONFIGURED
```

## Prochaine famille — A1 Identity / Names / Legal Structure

Avant toute migration 040 :

1. extraire les OF-IDs exacts relatifs aux noms Fund/SubFund/Share Class, langue, structure umbrella, legal form et rôles organisationnels ;
2. contrôler Field Level, datatype, cardinalité et valeurs officielles ;
3. auditer migration 015 et les relations/événements déjà présents ;
4. réutiliser le canonique existant si possible ;
5. écrire le RED de la famille ;
6. créer migration 040 uniquement si un besoin produit réel n'est pas représentable sans perte ;
7. append mappings uniquement après preuve ;
8. vérifier le diff puis réconcilier manifest/CI/docs.

Manufacturer, Management Company et Investment Manager doivent rester des rôles distincts ; aucune égalité implicite n'est autorisée.

---

## Historique de référence

Les rapports datés sous `docs/00_PROJECT/` conservent les états et preuves de chaque batch antérieur. Le présent document est la vue courante et ne réécrit pas rétroactivement ces checkpoints.
