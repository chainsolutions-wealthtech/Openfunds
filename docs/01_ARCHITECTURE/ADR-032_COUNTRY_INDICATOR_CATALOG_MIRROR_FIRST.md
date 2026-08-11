
# ADR-032 — Catalogue pays-indicateurs D00–D17 mirror-first

```text
STATUS: ACCEPTED
DATE: 2026-08-11
TASK: OF-DATA-003
LOOP: OF-LOOP-DATA-003
SUPERSEDES: ADR-024 FOR D00_D17_ONLY
```

## Contexte

Les 420 définitions D00–D17 existaient dans sept Markdown avec des contrats de colonnes différents. D00 exposait notamment définition/nature/mandatory alors que D01–D17 n’exposaient pas systématiquement ces informations. Les mappings sources utilisaient en outre des codes métier distincts des codes canoniques. Centraliser ces objets ne devait donc ni inventer les champs absents, ni réécrire la terminologie source, ni déclarer une collecte ou un historique inexistant.

## Décision

La stratégie `MIRROR_FIRST` est acceptée. Les sept Markdown historiques restent des inputs de bootstrap et d’audit de fidélité. Après bootstrap, l’unique autorité logique d’authoring est :

```text
data/indicator_catalog/v1/
```

Elle est partitionnée en `00_metadata.json` et D00–D17 pour permettre une revue par domaine sans créer de registre concurrent.

## Sémantique des absences

Une information absente de la source reste `null` avec un statut explicite tel que `NOT_AUTHORED`. Une traduction, unité, devise, granularité ou méthode de calcul n’est jamais déduite silencieusement. `NULL`, `UNKNOWN`, `NOT_AUTHORED`, `NOT_APPLICABLE` et zéro restent distincts.

## Nature source et nature canonique

`source_nature` conserve uniquement ce que la source legacy a effectivement déclaré. `canonical_nature` est une classification de gouvernance séparée et traçable :

```text
RAW
METADATA
EVENT
CALCULATED
```

La décision `OF-DATA-003-A` produit actuellement 298 RAW, 85 METADATA, 7 EVENT et 30 CALCULATED. Cette classification n’est pas présentée comme une assertion fournisseur.

## Historique et preuve

`target_history` est une exigence de couverture. Il ne prouve jamais qu’un historique a été collecté ou chargé. La v1 fixe :

```text
history_status = NOT_ASSERTED_BY_DEFINITION_CATALOGUE
```

Les statuts de mapping source, spécification de collecte, test de collecte, historique et calcul restent indépendants.

## Identités distinctes

Les identifiants suivants ne doivent pas être fusionnés implicitement :

```text
CANONICAL_INDICATOR_CODE
MAPPING_OR_BUSINESS_CODE
PROVIDER_SERIES_CODE
```

Les relations pays/zone, sources, provider series, observations et calculs restent dans leurs couches relationnelles dédiées.

## Sorties et SQL

Le générateur déterministe produit JSON expansé, CSV UTF-8 `;`, Markdown et SQL. `schemas/reference/016_country_indicator_catalog.sql` est une migration frozen générée et collision-safe. Elle ne crée que `ref.indicator_domain` et `ref.indicator_definition` et ne charge aucune observation pays.

## Conséquences

- une seule autorité logique de définition D00–D17 ;
- 420 codes uniques vérifiés ;
- aucune matrice 54×420 dupliquée manuellement ;
- aucune transformation silencieuse d’une définition en preuve de collecte ;
- PostgreSQL peut matérialiser le catalogue sans devenir une deuxième surface d’authoring Git ;
- ADR-024 est remplacé par ADR-032 pour D00–D17 et par ADR-031 pour le cœur `fund.*`.

## Limites

Aucun catalogue officiel Openfunds, aucune histoire pays, aucune série fournisseur complète, aucun calcul actif et aucun déploiement de production ne sont autorisés ou prouvés par cet ADR.
