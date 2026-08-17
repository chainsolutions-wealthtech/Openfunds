# MAPPING OPENFUNDS VERS LE MODELE CANONIQUE

Dernière mise à jour : `2026-08-17`.

## 1. STATUT REEL

```text
PRINCIPE ARCHITECTURAL                   ACCEPTE
VERSION OFFICIELLE COURANTE VERIFIEE    2.13.0
DATE DE RELEASE VERIFIEE                 2026-03-23
LICENCE OFFICIELLE VERIFIEE             CC BY-ND 4.0 / attribution www.openfunds.org
MANIFESTE DE PROVENANCE                  PRESENT
BINAIRE FIELD LIST 2.13.0                ARCHIVE SANS MODIFICATION / CHECKSUM LOCKED
SHA256 OFFICIEL ARCHIVE                  40b562a10e92cf809449302e8c9eacf785f5c8a66ff644d1a5c36fc4380cebb4
TAILLE BINAIRE                            2,957,096 OCTETS
NOMBRE DE PAGES                           745
CATALOGUE PARSE MACHINE-READABLE         NON ENCORE CONSTRUIT
MAPPING CHAMP PAR CHAMP                  NON ENCORE CONSTRUIT
EXPORT OPENFUNDS                         NON IMPLEMENTE
```

Le manifeste gouverné est :

```text
data/openfunds/source_manifest_v2.13.0.json
```

L'artefact officiel byte-identical est :

```text
data/openfunds/official/v2.13.0/openfunds_fields_v2.13.0.pdf
```

avec sa preuve :

```text
data/openfunds/official/v2.13.0/openfunds_fields_v2.13.0.pdf.sha256
data/openfunds/official/v2.13.0/SOURCE_AND_LICENSE.md
```

Le gate d'archivage binaire de `OF-MAP-001` est donc fermé. Le gate restant est désormais **le parsing déterministe du PDF checksum-locké et la validation de l'inventaire réel des champs**. Aucun contenu du catalogue ne doit être reconstitué depuis une source secondaire ou inventé.

Tâches : `OF-MAP-001` et `OF-MAP-002`.

## 2. PRINCIPE

Le modèle canonique constitue la source interne de vérité. Openfunds est une représentation externe versionnée.

```text
OPENFUNDS_FIELD
→ SOURCE_VERSION
→ PARSING
→ NORMALIZATION
→ CANONICAL_ENTITY
→ CANONICAL_FIELD_OR_RELATION
→ VALIDATION
```

Pour l'export, la chaîne est inversée avec une règle explicite de formatage et de perte éventuelle.

La licence officielle impose que le contenu openfunds redistribué reste non modifié. L'archive officielle reste donc byte-identical. Les mappings internes constituent des métadonnées séparées : ils ne modifient jamais le catalogue officiel archivé.

## 3. STRUCTURE DU REGISTRE DE MAPPING

| Attribut | Description |
|---|---|
| `MAPPING_ID` | identifiant stable du mapping |
| `STANDARD_CODE` | `OPENFUNDS` |
| `STANDARD_VERSION` | version officielle |
| `EXTERNAL_FIELD_ID` | identifiant officiel |
| `EXTERNAL_FIELD_NAME` | nom officiel |
| `EXTERNAL_DESCRIPTION` | description officielle sourcée |
| `EXTERNAL_DATA_TYPE` | type attendu |
| `EXTERNAL_OBJECT` | objet openfunds concerné |
| `CARDINALITY` | cardinalité externe |
| `REQUIREMENT_LEVEL` | obligatoire/facultatif/conditionnel |
| `CANONICAL_ENTITY` | objet canonique cible |
| `CANONICAL_FIELD_IDS` | un ou plusieurs champs cibles |
| `MAPPING_STATUS` | statut normalisé |
| `TRANSFORMATION_RULE` | transformation |
| `NORMALIZATION_RULE` | normalisation |
| `VALIDATION_RULE` | contrôle |
| `INFORMATION_LOSS` | perte éventuelle |
| `COMPLEMENTARY_DATA` | données complémentaires nécessaires |
| `IMPORT_SUPPORTED` | oui/non/partiel |
| `EXPORT_SUPPORTED` | oui/non/partiel |
| `VALID_FROM` | début de validité du mapping |
| `VALID_TO` | fin de validité |
| `VALIDATION_STATUS` | proposition ou validation |
| `SOURCE_REFERENCE` | provenance du standard |

## 4. STATUTS DE MAPPING

```text
DIRECT
TRANSFORMED
ONE_TO_MANY
MANY_TO_ONE
UNSUPPORTED_EXTERNAL_FIELD
CANONICAL_ONLY
TO_CONFIRM
VALIDATED
DEPRECATED
REPLACED
```

## 5. REGLES

1. un champ externe ne devient pas automatiquement une colonne ;
2. un mapping peut viser une relation, un événement ou une série ;
3. la version du standard est obligatoire ;
4. une transformation doit être déterministe et testable ;
5. les listes de valeurs externes sont mappées vers des référentiels versionnés ;
6. les pertes d'information sont déclarées ;
7. les extensions internes restent possibles ;
8. les valeurs brutes d'import sont conservées ;
9. les exports sont produits depuis le canonique, jamais depuis une source fournisseur brute ;
10. un changement de version ne remplace pas silencieusement le mapping antérieur ;
11. le catalogue officiel archivé reste byte-identical à la source conformément à la licence ;
12. aucun identifiant, nom, type ou cardinalité officiel ne peut être inventé ;
13. tout parser doit vérifier le SHA256 de l'archive avant extraction ;
14. tout contenu dérivé reste séparé de l'archive officielle et ne peut être présenté comme document officiel modifié ;
15. la redistribution publique de contenus transformés doit rester compatible avec la clause `NoDerivatives` ; le mapping canonique privilégie donc les références/provenances séparées plutôt que la réécriture de l'original.

## 6. OBJETS CANONIQUES CIBLES

Le modèle Fund/SubFund/ShareClass et le dictionnaire canonique étant stabilisés, les cibles suivantes peuvent être utilisées pour préparer le registre de mapping sans anticiper les champs externes :

- FundGroup ;
- Fund ;
- SubFund ;
- ShareClass ;
- Organization et rôles ;
- Identifier ;
- Classification ;
- Benchmark ;
- Fee ;
- Eligibility ;
- Distribution ;
- Document ;
- RegulatoryData ;
- ESGData ;
- Event ;
- TimeSeries.

## 7. PROCESSUS DE CONSTRUCTION

```text
1. VERSION OFFICIELLE                       FAIT — 2.13.0
2. SOURCE / DATE / LICENCE                  FAIT — manifeste gouverné
3. ARCHIVER FIELD LIST ORIGINAL             FAIT — archive byte-identical
4. CALCULER SHA256 / MEDIA TYPE             FAIT — SHA256 verrouillé
5. AUDITER LE LAYOUT PDF                    PROCHAINE UNITE
6. PARSER LE CATALOGUE DETERMINISTEMENT     APRES 5
7. VALIDER IDS / TYPES / CARDINALITES       APRES 6
8. GENERER LE REGISTRE DE MAPPING           APRES 6
9. PROPOSER LES MAPPINGS                    APRES 6
10. REVOIR PAR DOMAINE                      APRES 9
11. TESTER IMPORT ET EXPORT                 APRES 9
12. VERSIONNER                              CONTINU
13. PUBLIER LES ECARTS DE COUVERTURE        APRES 9
```

## 8. CRITERES D'ACCEPTATION

### OF-MAP-001

- version officielle enregistrée — **FAIT** ;
- licence et attribution enregistrées — **FAIT** ;
- fichier officiel v2.13.0 archivé sans modification — **FAIT** ;
- SHA256 et type MIME enregistrés — **FAIT** ;
- parsing déterministe — **OUVERT** ;
- nombre de champs et identifiants vérifiés — **OUVERT** ;
- aucune donnée officielle inventée — **INVARIANT**.

`OF-MAP-001` reste `EN_COURS` jusqu'à clôture des deux points ouverts.

### OF-MAP-002

- mapping humain et machine-readable ;
- chaque champ officiel référencé/provenancé ;
- champs sans équivalent clairement identifiés ;
- transformations testées ;
- compatibilité par version ;
- rapport de couverture ;
- fixtures d'import/export ;
- documentation des pertes d'information.

## 9. GATES ACTUELS REELS

Les anciens blocages suivants sont levés :

```text
VERSION OFFICIELLE INCONNUE            LEVE
LICENCE A VERIFIER                     LEVE
DICTIONNAIRE CANONIQUE INCOMPLET       LEVE
FUND/SUBFUND/SHARECLASS INSTABLE       LEVE
OFFICIAL_FIELD_LIST_ARCHIVE            LEVE
OFFICIAL_FIELD_LIST_SHA256             LEVE
```

Le gate restant est précis :

```text
OPENFUNDS_V2_13_0_DETERMINISTIC_PARSE = PENDING
OFFICIAL_FIELD_INVENTORY_VALIDATION    = PENDING
```

Le rapport permanent du gate d'archive est :

```text
docs/00_PROJECT/OF_MAP_001_OPENFUNDS_V2_13_0_OFFICIAL_ARCHIVE_COMPLETION_20260817.md
```

Aucun mapping champ-par-champ officiel ne doit être déclaré complet avant ces validations.
