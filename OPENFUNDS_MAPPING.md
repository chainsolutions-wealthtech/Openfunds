# MAPPING OPENFUNDS VERS LE MODELE CANONIQUE

## 1. STATUT REEL

```text
PRINCIPE ARCHITECTURAL : ACCEPTE
CATALOGUE OFFICIEL OPENFUNDS : NON PRESENT DANS LE DEPOT
MAPPING CHAMP PAR CHAMP : NON ENCORE CONSTRUIT
EXPORT OPENFUNDS : NON IMPLEMENTE
```

Ce document définit la méthode. Il ne crée aucun identifiant ou libellé officiel openfunds sans source officielle.

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

## 3. STRUCTURE DU FUTUR REGISTRE

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
10. un changement de version ne remplace pas silencieusement le mapping antérieur.

## 6. OBJETS CANONIQUES CIBLES ENVISAGES

- FundGroup ;
- LegalFund/Umbrella ;
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

Cette liste doit être alignée sur le modèle Fund/SubFund/ShareClass final.

## 7. PROCESSUS DE CONSTRUCTION

```text
1. OBTENIR UNE VERSION OFFICIELLE
2. CONSERVER SOURCE, DATE ET LICENCE
3. IMPORTER LE CATALOGUE EXTERNE
4. VALIDER TYPES ET CARDINALITES
5. STABILISER LE DICTIONNAIRE CANONIQUE
6. PROPOSER LES MAPPINGS
7. REVOIR PAR DOMAINE
8. TESTER IMPORT ET EXPORT
9. VERSIONNER
10. PUBLIER LES ECARTS DE COUVERTURE
```

## 8. CRITERES D'ACCEPTATION

- aucun champ officiel inventé ;
- chaque champ officiel sourcé ;
- mapping humain et machine-readable ;
- champs sans équivalent clairement identifiés ;
- transformations testées ;
- compatibilité par version ;
- rapport de couverture ;
- fixtures d'import/export ;
- documentation des pertes d'information.

## 9. BLOCAGES ACTUELS

- standard officiel non versionné dans le dépôt ;
- dictionnaire canonique incomplet ;
- structure Fund/SubFund/ShareClass non stabilisée ;
- politique de licence à vérifier ;
- aucun format maître de mapping encore approuvé.
