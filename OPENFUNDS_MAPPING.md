# MAPPING OPENFUNDS VERS LE MODELE CANONIQUE

Dernière mise à jour : `2026-08-17`.

## 1. STATUT REEL

```text
PRINCIPE ARCHITECTURAL                   ACCEPTE
VERSION OFFICIELLE COURANTE VERIFIEE    2.13.0
DATE DE RELEASE VERIFIEE                 2026-03-23
LICENCE OFFICIELLE VERIFIEE             CC BY-ND 4.0 / attribution www.openfunds.org
MANIFESTE DE PROVENANCE                  PRESENT
BINAIRE FIELD LIST 2.13.0                A ARCHIVER SANS MODIFICATION
CATALOGUE PARSE MACHINE-READABLE         NON ENCORE CONSTRUIT
MAPPING CHAMP PAR CHAMP                  NON ENCORE CONSTRUIT
EXPORT OPENFUNDS                         NON IMPLEMENTE
```

Le manifeste gouverné est :

```text
data/openfunds/source_manifest_v2.13.0.json
```

La version et la licence ne constituent donc plus des blocages. Le gate restant de `OF-MAP-001` est l'archivage immuable du Field List officiel v2.13.0, son SHA256 et son parsing déterministe. Aucun contenu du catalogue ne doit être reconstitué depuis une source secondaire ou inventé.

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

La licence officielle impose que le contenu openfunds redistribué reste non modifié. Les mappings internes constituent donc des métadonnées séparées : ils ne modifient jamais le catalogue officiel archivé.

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
12. aucun identifiant, nom, type ou cardinalité officiel ne peut être inventé en l'absence du Field List archivé.

## 6. OBJETS CANONIQUES CIBLES

Le modèle Fund/SubFund/ShareClass et le dictionnaire canonique étant désormais stabilisés, les cibles suivantes peuvent être utilisées pour préparer le registre de mapping sans anticiper les champs externes :

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
3. ARCHIVER FIELD LIST ORIGINAL             BLOQUE — binaire officiel à matérialiser
4. CALCULER SHA256 / MEDIA TYPE             APRES 3
5. PARSER LE CATALOGUE DETERMINISTEMENT      APRES 3
6. VALIDER TYPES ET CARDINALITES             APRES 5
7. GENERER LE REGISTRE DE MAPPING VIDE       AUTORISE
8. PROPOSER LES MAPPINGS                     APRES 5
9. REVOIR PAR DOMAINE                        APRES 8
10. TESTER IMPORT ET EXPORT                  APRES 8
11. VERSIONNER                               CONTINU
12. PUBLIER LES ECARTS DE COUVERTURE         APRES 8
```

## 8. CRITERES D'ACCEPTATION

### OF-MAP-001

- version officielle enregistrée ;
- licence et attribution enregistrées ;
- fichier officiel v2.13.0 archivé sans modification ;
- SHA256 et type MIME enregistrés ;
- parsing déterministe ;
- nombre de champs et identifiants vérifiés ;
- aucune donnée officielle inventée.

### OF-MAP-002

- mapping humain et machine-readable ;
- chaque champ officiel sourcé ;
- champs sans équivalent clairement identifiés ;
- transformations testées ;
- compatibilité par version ;
- rapport de couverture ;
- fixtures d'import/export ;
- documentation des pertes d'information.

## 9. BLOCAGES ACTUELS REELS

Les anciens blocages suivants sont levés :

```text
VERSION OFFICIELLE INCONNUE       LEVE
LICENCE A VERIFIER                LEVE
DICTIONNAIRE CANONIQUE INCOMPLET  LEVE
FUND/SUBFUND/SHARECLASS INSTABLE  LEVE
```

Le blocage restant est précis :

```text
OFFICIAL_FIELD_LIST_2_13_0_ARCHIVE = PENDING
```

Tant que cet artefact n'est pas archivé et hashé, `OF-MAP-001` ne peut pas passer à `TERMINE` et `OF-MAP-002` ne peut pas contenir de mapping champ-par-champ officiel.
