# OF-ARCH-005 completion record — frozen generated migration 012

```text
DATE: 2026-08-05
TASK: OF-ARCH-005
LOOP: OF-LOOP-ARCH-005
ADR: ADR-029
STATUS: VERIFIED_COMPLETE
START_HEAD: d81f78942c18f4f908da8e8500f83d1280eea570
VALIDATED_TECHNICAL_HEAD: ec5a2fd2efe89f008c05d4443001790450090523
```

## 1. Problème fermé

Le manifeste exécutait auparavant le générateur de `012` avant le calcul du checksum. Une évolution du CSV actif pouvait donc modifier le contenu historique attendu sous le même ID et le même chemin, même si le ledger échouait ensuite de manière fermée.

## 2. Modèle final

```text
data/reference/VALIDATED_FX_REFERENCE_REGISTRY.csv
= authoring actif gouverné

migrations/sources/012_validated_fx_reference_registry.csv
= snapshot historique immuable

schemas/reference/012_validated_fx_reference_registry.sql
= migration historique immuable

PostgreSQL ledger
= checksum de l’artefact appliqué
```

Le manifeste appelle maintenant le générateur uniquement avec `--check`, une source figée et une sortie figée. Toute évolution crée un nouveau couple snapshot/SQL numéroté et une migration forward.

## 3. Artefact figé

```text
PATH
schemas/reference/012_validated_fx_reference_registry.sql

LINES
49

SHA256
fb1e82536717082092e762706f29d51dd834dd5b2f0ea1b10193665f9f48bda0

SOURCE SNAPSHOT
migrations/sources/012_validated_fx_reference_registry.csv
```

Le SQL conserve uniquement les pilotes BCEAO/XOF et BEAC/XAF au statut `COLLECTION_TESTED`; il ne revendique ni historique partiel/complet, ni production.

## 4. Commits

```text
a5796821904fd9ca8178b5579a3da44bfe1c3465
commit intermédiaire accidentel d’un README d’un mot

b07c3153cb3d6d5c5270760b3b00e600bbcbc4f5
bootstrap du snapshot, du générateur et du workflow ponctuel

54284d83bcee537b559dfbfd057ad23e39776844
commit bot de l’artefact SQL exact

ec5a2fd2efe89f008c05d4443001790450090523
politique définitive, garde read-only, manifest, tests et ADR
```

L’entrée intermédiaire incorrecte a été corrigée au commit suivant sans force-push ni réécriture. Le workflow ponctuel avec permission `contents: write` a été remplacé au HEAD technique par `Frozen Migration 012 Guard` avec `contents: read`.

## 5. CI du HEAD technique

| Workflow | Run | Résultat | Preuves principales |
|---|---:|---|---|
| Reference Registry Synchronization | 30989910122 | SUCCESS | compilation, 6 tests, checksum stable, PostgreSQL, double application |
| Governed Migration Runner | 30989910488 | SUCCESS | tests, plan, base vide, second apply, verify, contrat runtime, adoption sans ledger |
| Frozen Migration 012 Guard | 30989910399 | SUCCESS | reproductibilité read-only et SHA exact |
| Collector Tests | 30989909622 | SUCCESS | non-régression globale des collecteurs/tests |

## 6. Critères d’acceptation

```text
FROZEN_SQL_COMMITTED: YES
FROZEN_SOURCE_SNAPSHOT_COMMITTED: YES
HISTORICAL_REGENERATION_DURING_MANIFEST_LOAD: NO
CHECK_ONLY_REPRODUCIBILITY: PASSED
REWRITE_012_REJECTED: TESTED
FORWARD_CREATE_ONLY: TESTED
SQL_SHA_FIXED: PASSED
EMPTY_POSTGRESQL_16: PASSED
DOUBLE_APPLY: PASSED
LEDGER_VERIFY: PASSED
EXISTING_DB_WITHOUT_LEDGER: PASSED
PRODUCTION_DEPLOYMENT: NO
```

## 7. Statuts

```text
OF-ARCH-004 VERIFIED_COMPLETE
OF-ARCH-005 VERIFIED_COMPLETE
OF-DATA-001 NOT_STARTED
```

## 8. Risques résiduels

- aucun advisory lock global ne sérialise l’ensemble du plan ;
- les topologies legacy partiellement initialisées ou structurellement incompatibles ne sont pas toutes simulées ;
- aucune politique de déploiement production ou base persistante n’est activée.

Ces sujets ne rouvrent pas le blocker de l’artefact `012`, mais restent des travaux de hardening distincts.

## 9. Opérations non réalisées

Aucune nouvelle branche ou PR, aucun travail sur `main`, aucune fusion, aucun retargeting, aucune fermeture de PR, aucun force-push, aucune suppression de branche et aucun déploiement.
