# Prochaine action autorisée

```text
CURRENT_LOOP: OF-LOOP-SOURCE-002 + OF-MAP-001_ARCHIVE_GATE
CURRENT_TASK: OF-SOURCE-002_EN_COURS / OF-MAP-001_EN_COURS
LAST_VERIFIED_WAVE: 11
NEXT_UNIT: OPENFUNDS_V2_13_0_OFFICIAL_FIELD_LIST_ARCHIVE + SERIES_ROLE_EVIDENCE_AUDIT + ERITREA_PRIMARY_SOURCE_WATCH
STATUS: READY_FOR_GOVERNED_ARCHIVE_AND_READ_ONLY_SERIES_AUDIT
WRITE_GATE: EXACT_OFFICIAL_ARTIFACT + SHA256 + UNALTERED_ARCHIVE + CLOSED_ALLOWLIST + TDD_RED
```

## État courant vérifié — 17 août 2026

Les Waves 01 à 11 ont été exécutées sur la branche gouvernée existante, sans nouvelle branche, sans modification de `main` et sans déploiement de production.

```text
AFRICAN_COUNTRIES: 54
COUNTRY_COVERAGE: 53 / 54
COUNTRIES_WITHOUT_COUNTRY_SCOPED_ORGANIZATION: 1
UNCOVERED_COUNTRY: ERYTHREE
ORGANIZATIONS: 141 = 121 VALIDATED + 20 PENDING
ORGANIZATION_SCOPE_ROLES: 199 = 174 VALIDATED + 25 PENDING
PENDING_STOCK_EXCHANGE: 0
```

Wave 11 a promu exactement trois relations `STOCK_EXCHANGE` déjà présentes (`EGX`, `GSE`, `NGX`), sans création ni retargeting, sous contrat TDD RED→GREEN et avec validation Python 3.11/3.12. Le rapport de clôture est :

```text
docs/00_PROJECT/OF_SOURCE_002_WAVE_11_COMPLETION_20260817.md
```

L'Érythrée reste volontairement absente : aucune organisation country-scoped ne doit être créée tant qu'une source primaire officielle actuelle n'est pas vérifiée.

## Audit effectif post-Wave11

Le workflow lecture seule `OF-SOURCE-002 Post-Wave11 Audit` a vérifié :

```text
MONETARY_AUTHORITY              11 pays sans groupe couvert
STATISTICS                       3 pays sans groupe couvert
CAPITAL_MARKET_REGULATION       18 pays sans groupe couvert
FUND_REGULATION                 19 pays sans groupe couvert
INSURANCE_PENSION_REGULATION    44 pays sans groupe couvert
EXCHANGE                        17 pays sans groupe couvert
FISCAL_DEBT                     40 pays sans groupe couvert
```

Ces chiffres combinent rôles country-scoped validés et compétences zonales validées héritées. Ils ne sont pas des instructions de créer artificiellement une organisation dans chaque pays.

## Inventaire exact des 25 PENDING

```text
FX_REFERENCE_RATE_PROVIDER   9
INDEX_PROVIDER               9
MONETARY_UNION               3
SUPRANATIONAL_AUTHORITY      2
INTERBANK_MARKET_OPERATOR    2
TOTAL                       25

COUNTRY        14
MONETARY_ZONE  11
```

Il ne reste aucune relation `STOCK_EXCHANGE` en attente.

## Unité prioritaire indépendante — OF-MAP-001

La source officielle exacte du Field List Openfunds v2.13.0 est désormais identifiée sur le domaine officiel Openfunds. Le document officiel est un PDF final v2.13.0 daté du 2026-03-23.

La prochaine écriture autorisée pour `OF-MAP-001` doit être strictement un archivage gouverné de l'artefact officiel **sans modification** :

1. télécharger le PDF depuis son URL officielle exacte ;
2. vérifier le magic `%PDF-` ;
3. vérifier que le document annonce `FINAL`, `Version 2.13.0` et `2026-03-23` ;
4. calculer SHA256 et taille binaire ;
5. conserver l'artefact byte-for-byte sans réécriture ;
6. enregistrer URL source, date/version, licence `CC BY-ND 4.0`, attribution et checksum ;
7. refuser toute substitution, conversion ou catalogue reconstruit ;
8. limiter le commit aux artefacts d'archive/provenance explicitement autorisés ;
9. seulement après ce gate, créer un parser déterministe et un catalogue structuré séparé de l'original sous licence.

Le manifeste existant reste :

```text
data/openfunds/source_manifest_v2.13.0.json
```

Il doit être mis à jour uniquement après archivage réussi avec le SHA256 réellement observé.

## OF-SOURCE-002 — prochaine phase

### Rôles de séries — audits dédiés

Les 18 lignes suivantes ne doivent jamais être promues sur la seule identité de l'institution :

```text
FX_REFERENCE_RATE_PROVIDER   9
INDEX_PROVIDER               9
```

Pour `FX_REFERENCE_RATE_PROVIDER`, la preuve doit établir la publication/propriété de la série FX de référence pertinente.

Pour `INDEX_PROVIDER`, la preuve doit établir la responsabilité de calcul, propriété ou publication de l'indice pertinent. Une bourse validée comme `STOCK_EXCHANGE` ne devient pas automatiquement `INDEX_PROVIDER`.

Les audits peuvent préparer des allowlists, mais aucune promotion ne doit précéder : source primaire officielle actuelle, définition exacte de la série, collision review, TDD RED et validation croisée des scopes.

### Rôles zonaux — revue sémantique séparée

```text
MONETARY_UNION             3
SUPRANATIONAL_AUTHORITY    2
INTERBANK_MARKET_OPERATOR  2
```

Ces rôles nécessitent une revue du modèle avant promotion. En particulier, `CMA / MONETARY_UNION` reste bloqué tant que le terme canonique `MONETARY_UNION` n'est pas démontré comme sémantiquement approprié à la Common Monetary Area.

## Blockers institutionnels maintenus

```text
ERYTHREE            PRIMARY_OFFICIAL_SOURCE_NOT_VERIFIED
FMDQ                REQUIRES_ROLE_MODEL_REVIEW
SEC_ZAMBIA          CURRENT_OFFICIAL_DOMAIN_INTEGRITY_BLOCKER
IRA_URBRA_UGANDA    COMBINED_ROLE_MODEL_MISMATCH
RBM_FUND_REGULATOR  PRIMARY_CIS_PROOF_NOT_SUFFICIENT
```

## Taxonomie — gate structurel fermé

```text
017_CANONICAL_FUND_TAXONOMY_V0_1
ORDER: 170
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
POSTGRESQL_16: SUCCESS
FULL_CHAIN_001_TO_017: SUCCESS
SECOND_APPLY_IDEMPOTENCE: SUCCESS
CANONICAL_STATUS: STRUCTURE_PREFILLED
PRODUCTION_STATUS: NOT_ACTIVE
```

Cette clôture structurelle n'autorise pas l'activation de WTI, WTI Bench, benchmarks, RFR, MAR ou autres calculs sans leurs validations propres.

## Interdictions maintenues

Ne pas importer d'historique réel sans stockage durable, ne pas modifier ou fermer la PR nº2 sans réconciliation, ne pas fusionner/retargeter la PR nº1, ne pas travailler sur `main`, ne pas créer de branche/PR, ne pas activer WTI/WTI Bench et ne pas déployer sans satisfaction des gates correspondants.
