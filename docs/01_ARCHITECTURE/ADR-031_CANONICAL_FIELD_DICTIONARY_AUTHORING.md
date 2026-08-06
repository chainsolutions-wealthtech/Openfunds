# ADR-031 — Source d’authoring du dictionnaire canonique des champs

```text
STATUS: ACCEPTED_FOR_CANONICAL_FUND_CORE
DATE: 2026-08-06
TASK: OF-DATA-002
LOOP: OF-LOOP-DATA-002
SUPERSEDES: ADR-024 FOR CANONICAL_FUND_CORE ONLY
```

## Contexte

`DATA_DICTIONARY.md` imposait un contrat riche, mais les définitions restaient
réparties entre SQL, CSV et Markdown. La migration gouvernée `015` a ensuite
stabilisé dix tables physiques Fund/SubFund/ShareClass et 143 colonnes. Il
fallait donc choisir une surface d’authoring unique, vérifiable et lisible en
revue Git sans maintenir manuellement plusieurs représentations concurrentes.

Aucun catalogue officiel Openfunds, accompagné d’une version et d’une preuve
archivée, n’est actuellement présent dans le dépôt. Un identifiant Openfunds ne
peut donc pas être déduit ou inventé.

## Décision

La source d’authoring gouvernée est le paquet JSON gouverné :

```text
data/dictionary/spec_v1/
```

Elle contient :

- les métadonnées et règles de gouvernance ;
- les 36 attributs obligatoires ;
- les valeurs par défaut ;
- les définitions bilingues des colonnes ;
- le contrat exact des dix tables et 143 colonnes ;
- les énumérations autorisées ;
- les clés étrangères ;
- le périmètre inclus et les exclusions explicites.

Le générateur déterministe :

```text
scripts/generate_canonical_field_dictionary.py
```

produit sous `build/dictionary/` :

```text
CANONICAL_FIELD_DICTIONARY_V1.json
CANONICAL_FIELD_DICTIONARY_V1.csv
CANONICAL_FIELD_DICTIONARY_V1.md
```

Le CSV est UTF-8 et utilise `;`. Les artefacts de build sont destinés aux
contrôles et à la revue ; ils ne sont pas une deuxième source d’authoring. Le
résumé humain commis sous `docs/04_DATA_GOVERNANCE/` expose le périmètre, la
volumétrie et les limites, tandis que la vue exhaustive est générée et publiée
comme artefact CI.

## Règles d’identité et de version

- `FIELD_ID` suit `OF_<DOMAIN>_<ENTITY>_<FIELD>` ;
- un changement sémantique crée un nouvel identifiant ou une nouvelle version ;
- un renommage physique conserve une trace de compatibilité ;
- aucune unité, devise ou règle d’historisation ne reste implicite ;
- `NULL`, `UNKNOWN`, `NOT_APPLICABLE` et `NOT_PUBLISHED` restent distincts ;
- les champs calculés doivent déclarer leurs entrées et méthodologies ;
- le manifeste SHA-256 détecte toute dérive de la source ou des sorties.

## Politique Openfunds

Tant qu’un catalogue officiel versionné et archivé n’est pas intégré :

```text
OPENFUNDS_FIELD_ID = null
openfunds_mapping_status = NOT_MAPPED_OFFICIAL_CATALOGUE_UNAVAILABLE
```

Cette absence explicite constitue le seul état autorisé. Le présent ADR ne
remplace ni `OF-MAP-001` ni `OF-MAP-002`.

## Contrôles obligatoires

La CI Python 3.11/3.12 vérifie :

1. la structure compacte et les 36 attributs ;
2. l’expansion à exactement 143 champs ;
3. l’unicité des IDs et noms techniques ;
4. la concordance exacte avec la migration `015` ;
5. l’absence d’identifiant Openfunds inventé ;
6. le CSV `;` et ses 143 lignes ;
7. les SHA-256 du manifeste ;
8. la reproductibilité de la vue Markdown exhaustive ;
9. la cohérence du résumé humain commis ;
10. la production d’artefacts de revue GitHub Actions.

## Périmètre déclaré complet

La v1 est complète uniquement pour les colonnes physiques du cœur canonique
`fund.*` créé par la migration `015`.

Sont exclus de cette déclaration :

- les vues dérivées ;
- `ref.*`, `source.*` et `market.*` ;
- D00–D17 ;
- les objets NAV, AUM, dividendes, portefeuille, frais, documents, prestataires,
  réglementaire, ESG et analytiques non encore présents dans le schéma runtime ;
- le mapping officiel Openfunds.

## Conséquences

- le cœur fonds dispose d’un catalogue complet, reproductible et testable ;
- les futures intégrations Tunisie et Nigeria disposent d’un contrat stable pour
  les identités, structures, noms, identifiants et événements ;
- les extensions futures doivent réutiliser cette gouvernance sans élargir
  silencieusement le statut de complétude ;
- `ADR-024` est remplacé par cet ADR pour le seul périmètre
  `CANONICAL_FUND_CORE` et reste ouvert pour les autres domaines.
