# REGLES DE QUALITE OPENFUNDS

## 1. PRINCIPES

1. aucune valeur manquante ne devient zéro ;
2. aucune correction n'efface silencieusement la version précédente ;
3. toute valeur publiée est reliée à une source ;
4. les observations et calculs restent distincts ;
5. les règles sont versionnées et reproductibles ;
6. une anomalie n'est pas corrigée automatiquement sans règle approuvée.

## 2. STATUTS

```text
PENDING
PROVISIONAL
VALIDATED
REJECTED
SUPERSEDED
MISSING
NOT_PUBLISHED
NOT_APPLICABLE
UNKNOWN
CONFLICT
```

Les statuts ne sont pas interchangeables.

## 3. IDENTITE ET REFERENTIELS

### QR-ID-001 — Unicité des identifiants

Chaque identifiant canonique et code actif doit être unique dans son namespace.

### QR-ID-002 — Stabilité

Un changement de nom ne change pas l'identifiant canonique.

### QR-ID-003 — Intégrité référentielle

Toute FK ou code référencé doit exister ou être explicitement mis en quarantaine.

### QR-ID-004 — Codes techniques

Codes canoniques en majuscules, sans accent, sans apostrophe et avec underscore.

## 4. DATES ET TEMPORALITE

### QR-DATE-001 — Dates valides

Les dates doivent être calendaires et ne pas être futures sauf événement annoncé explicitement.

### QR-DATE-002 — Cohérence des périodes

```text
valid_to >= valid_from
```

lorsque les deux dates sont connues.

### QR-DATE-003 — Date économique distincte

La date de collecte ne remplace jamais l'observation date ou l'effective date.

### QR-DATE-004 — Date inconnue

Aucune valeur artificielle telle que `1900-01-01` n'est autorisée.

### QR-DATE-005 — Révisions

Chaque vintage ou correction conserve sa date de publication et d'enregistrement.

## 5. NOMBRES, UNITES ET DEVISES

### QR-NUM-001 — Parsing localisé

Gérer espaces, espaces insécables, virgules et points sans interprétation à l'aveugle.

### QR-NUM-002 — Valeurs brutes

Conserver la chaîne source et la règle de parsing avec la valeur numérique.

### QR-NUM-003 — Unité explicite

Aucune valeur numérique publiée sans unité, multiplicateur ou convention connue.

### QR-FX-001 — Devise native

La devise de la donnée native est conservée. Une conversion ne la remplace pas.

### QR-FX-002 — Convention canonique

```text
1 SOURCE CURRENCY UNIT = X TARGET CURRENCY UNITS
```

### QR-FX-003 — Lignée de conversion

La conversion référence l'observation FX exacte, la date, le taux, la formule et la méthodologie.

### QR-FX-004 — XOF/XAF

Les profils, séries et observations XOF et XAF restent séparés.

## 6. SOURCES ET ARTEFACTS

### QR-SRC-001 — URL

Une URL est déclarée `VALIDATED` uniquement après vérification.

### QR-SRC-002 — SHA256

Tout artefact brut collecté possède un SHA256 vérifié.

### QR-SRC-003 — Immutabilité

Deux artefacts de contenu différent ne partagent pas le même identifiant de contenu.

### QR-SRC-004 — Provenance minimale

```text
organization
endpoint
source_url
retrieved_at
sha256
parser_version
```

### QR-SRC-005 — Provenance fine

Lorsque disponible : page, feuille, table, ligne, colonne, cellule, chemin JSON/XML.

## 7. SERIES TEMPORELLES

### QR-TS-001 — Clé logique

La clé dépend du type de série et doit inclure l'objet, la date, le type d'observation, la devise et la source/vintage appropriés.

### QR-TS-002 — Idempotence

Une ingestion identique retourne `SKIPPED_IDENTICAL` ou équivalent, sans doublon.

### QR-TS-003 — Correction

Une valeur modifiée crée une nouvelle version et supersède la précédente.

### QR-TS-004 — Gaps

Un jour sans publication est distinct d'une collecte échouée et d'une valeur manquante.

### QR-TS-005 — Fréquence

La fréquence native est conservée. Une série hebdomadaire n'est pas artificiellement quotidienne.

## 8. FONDS ET IDENTIFIANTS EXTERNES

### QR-FUND-001 — Résolution d'entité

Aucune fusion de fonds sur simple similarité de nom.

### QR-FUND-002 — Alias

Un alias doit avoir une preuve et une période ou un statut de validation.

### QR-ISIN-001 — ISIN

Valider longueur, alphabet, structure pays et chiffre de contrôle ; une valeur invalide est conservée comme brute mais non publiée comme ISIN validé.

### QR-LEI-001 — LEI

Valider format et checksum avant validation.

### QR-EVENT-001 — Evénements

Fusion, absorption, changement de nom et transfert doivent préciser objets source/cible, dates, preuve et statut.

## 9. CALCULS

### QR-CALC-001 — Entrées

Chaque résultat calculé référence ses entrées.

### QR-CALC-002 — Méthodologie

Formule, version, calendrier et règles d'arrondi sont obligatoires.

### QR-CALC-003 — Reproductibilité

Le même jeu d'entrées et la même version produisent le même résultat.

### QR-WTI-001 — Univers

Un fonds ne contribue que s'il est membre et éligible à la date du calcul.

### QR-WTI-002 — Absence d'interpolation

Aucune VL artificielle n'est créée entre deux publications.

### QR-BENCH-001 — Indépendance

WTI Bench ne doit pas dépendre de la performance observée des fonds composant le WTI, sauf méthodologie explicitement approuvée qui ne doit pas porter ce rôle.

## 10. COUVERTURE ET FRAICHEUR

Mesures minimales :

```text
first_observation_date
last_observation_date
observation_count
expected_observation_count
completeness_ratio
freshness_status
method_break_count
```

Le statut `COMPLETE_HISTORY_LOADED` exige un inventaire officiel et un contrôle de couverture.

## 11. SEVERITE

- `ERROR` : empêche la publication ou le chargement canonique ;
- `WARNING` : charge possible avec statut provisoire ;
- `INFO` : observation ou amélioration ;
- `QUARANTINE` : donnée conservée hors publication ;
- `BLOCKER` : empêche la progression de la phase.

## 12. TRACE D'UNE CORRECTION

Chaque correction doit permettre de retrouver :

- valeur précédente ;
- valeur corrigée ;
- source de correction ;
- date ;
- règle appliquée ;
- acteur ou processus ;
- justification ;
- version remplacée.

## 13. IMPLEMENTATION

Les premières règles machine-readable existent dans `data/reference/country_data_quality_rules_v0.1.csv`. Leur généralisation exécutable relève de `OF-QA-001`.
