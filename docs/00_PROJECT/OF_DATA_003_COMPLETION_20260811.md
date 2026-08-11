
# OF-DATA-003 — Rapport de clôture du catalogue D00–D17

```text
DATE: 2026-08-11
TASK_ID: OF-DATA-003
LOOP_ID: OF-LOOP-DATA-003
STATUS: VERIFIED_COMPLETE
BRANCH: architecture/africafunds-country-indicators-v0.1
START_HEAD: 145461e04ba9affd2b11fedaf56ed4ad49171b5d
VALIDATED_TECHNICAL_HEAD: 0777afffad950e779234ef09f3f2b9031ec41ce7
CURRENT_HEAD_POLICY: RESOLVE_DYNAMICALLY
PRODUCTION_DEPLOYED: NO
REAL_COUNTRY_DATA_LOADED: NO
```

## 1. Décision retenue

L’utilisateur a validé l’Option A : `MIRROR_FIRST`. Les 420 définitions sont reproduites fidèlement depuis les sept Markdown existants ; une information absente reste `null` avec statut explicite. Aucune traduction, unité, devise, méthode, source ou preuve d’historique n’est inventée.

## 2. Volumétrie vérifiée

| Domaine | Nombre |
|---|---:|
| D00 | 15 |
| D01 | 20 |
| D02 | 16 |
| D03 | 24 |
| D04 | 14 |
| D05 | 26 |
| D06 | 24 |
| D07 | 23 |
| D08 | 28 |
| D09 | 29 |
| D10 | 45 |
| D11 | 24 |
| D12 | 48 |
| D13 | 12 |
| D14 | 9 |
| D15 | 16 |
| D16 | 17 |
| D17 | 30 |
| **Total** | **420** |

Tous les codes respectent `Dnn.CODE` et sont uniques.

## 3. Source d’authoring

```text
data/indicator_catalog/v1/
```

Le paquet contient 19 fichiers : `00_metadata.json` puis D00–D17. Les sept Markdown historiques sont figés comme inputs de bootstrap/audit ; ils ne concurrencent plus le paquet JSON comme source d’authoring.

## 4. Classification gouvernée

```text
DECISION: OF-DATA-003-A
RAW: 298
METADATA: 85
EVENT: 7
CALCULATED: 30
```

`source_nature` reste inchangée et distincte de `canonical_nature`. Chaque classification porte décision, version et règle.

## 5. Preuve, historique et statuts

Le catalogue maintient des statuts indépendants pour définition, mapping source, spécification, test de collecte, historique et calcul. `target_history` reste un horizon cible et :

```text
history_status = NOT_ASSERTED_BY_DEFINITION_CATALOGUE
```

pour les 420 objets. Cette boucle ne transforme donc jamais « 10 ans » en « 10 ans chargés ».

## 6. Sorties déterministes

Le générateur produit JSON expansé, CSV UTF-8 `;`, Markdown exhaustif et SQL. Empreintes :

```text
JSON  1d19a2d612b4d34e6d83f96100c6b073acd3791f96418aaca7cf1a097ad58184
CSV   7d0f549684bdf91164ad98b7d912510784c8a2f07b4a8d0d86ecdc3e4a34ee94
MD    a2044c0ebff3ba90a839eb7ee30ff388952b53a8380360f7cf7d8d15bb3f4730
SQL   fa00298ca8371cf1f95e20d809cc82b97774ea3cf0bf8fa2945cf269d0982432
```

Le manifeste vérifie toute dérive.

## 7. Migration 016

`016_COUNTRY_INDICATOR_CATALOG` est enregistrée à l’ordre 160. Elle crée uniquement :

```text
ref.indicator_domain
ref.indicator_definition
```

Le seed est additif/idempotent et fait échouer les collisions sémantiques au lieu de les masquer. Aucun objet d’observation, `country_series`, historique pays ou donnée de production n’est chargé.

## 8. TDD et corrections transparentes

La boucle a respecté RED → GREEN pour le parseur, le paquet d’authoring, la classification, les sorties et la migration. Deux anomalies de validation ont été conservées dans l’historique et corrigées sans force-push :

1. la CI réappliquait la classification dans son workspace avant de calculer le manifeste ; la phrase de métadonnées changeait le hash JSON alors que le SQL restait identique. `d8b3a2d6…` rend le paquet commité strictement autoritaire ;
2. un test Fund/SubFund/ShareClass supposait que `015` devait être la dernière migration globale. `0777afffad950e779234ef09f3f2b9031ec41ce7` vérifie désormais le vrai invariant : `015` reste l’unique migration canonique du domaine `fund`, indépendamment des migrations de référence ultérieures.

## 9. Preuves finales

### Country Indicator Catalog

```text
RUN_ID: 31484468846
CONCLUSION: SUCCESS
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
```

Les deux jobs valident le paquet commité, régénèrent les quatre sorties, exécutent les tests contractuels, vérifient l’identité octet pour octet et publient des artefacts de revue.

### Governed Migration Runner

```text
RUN_ID: 31484586710
HEAD_SHA: 0777afffad950e779234ef09f3f2b9031ec41ce7
CONCLUSION: SUCCESS
```

Le run réussit : frozen contract 016, tests runner/catalogue/funds, plan, double application sur PostgreSQL 16 vide, verify, assertions 18/420 et 298/85/7/30, fixtures funds, puis adoption d’une base initialisée sans ledger.

## 10. Critères d’acceptation

```text
18_DOMAINS: PASSED
420_UNIQUE_CODES: PASSED
MIRROR_FIDELITY: PASSED
NULL_NOT_INVENTED: PASSED
SOURCE_NATURE_PRESERVED: PASSED
CANONICAL_NATURE_GOVERNED: PASSED
INDEPENDENT_EVIDENCE_STATES: PASSED
CSV_SEMICOLON: PASSED
DETERMINISTIC_JSON_CSV_MD_SQL: PASSED
MANIFEST_SHA256: PASSED
MIGRATION_016_REGISTERED: PASSED
POSTGRESQL_16_DOUBLE_APPLY: PASSED
POSTGRESQL_16_RUNTIME_COUNTS: PASSED
HISTORY_INVENTION: ZERO
OPENFUNDS_IDENTIFIER_INVENTION: ZERO
PRODUCTION_DEPLOYED: NO
REAL_DATA_IMPORTED: NO
```

## 11. Prochaine porte

`OF-MAP-001` reste bloqué faute de catalogue Openfunds officiel versionné/licencié. La prochaine tâche non bloquée de priorité haute est `OF-SOURCE-002`, à démarrer en lecture seule par une matrice de couverture des institutions des 54 pays et par la vérification des preuves officielles.
