# Revue indépendante des risques du migration runner

```text
DATE: 2026-08-05
AUDITED_HEAD: 202f23d5a5be961d6f8338984b04655eda336a6b
VALIDATED_TECHNICAL_SHA: 5a6ed3da39571e331e8317e3759cd7068165c66d
WORKFLOW_RUN: 30965690163
WORKFLOW_RESULT: completed / success
AUDIT_MODE: NO_TECHNICAL_MODIFICATION
```

## 1. Composants examinés

- `migrations/manifest.json`
- `scripts/run_migrations.py`
- `scripts/generate_validated_fx_reference_sql.py`
- `data/reference/VALIDATED_FX_REFERENCE_REGISTRY.csv`
- chemin déclaré `schemas/reference/012_validated_fx_reference_registry.sql`
- `docs/01_ARCHITECTURE/ADR-028_GOVERNED_MIGRATION_RUNNER.md`
- workflow `Governed Migration Runner`
- tests du runner

## 2. Contrôles réellement présents

Le manifeste contient exactement 14 entrées, avec ordre strictement croissant
de 10 à 140. Les IDs, ordres et chemins sont contrôlés comme uniques.

Le ledger est :

```text
openfunds_migration.schema_migration
```

Il conserve :

- ID ;
- ordre ;
- chemin ;
- SHA-256 ;
- timestamp ;
- utilisateur ;
- version du runner.

Le runner :

- exécute seulement les entrées du manifeste ;
- rejette les chemins dangereux ;
- rejette les commandes psql et transactions imbriquées dans les SQL ;
- compare ordre, chemin et checksum aux lignes du ledger ;
- bloque les entrées inconnues ;
- applique le SQL et insère la ligne de ledger dans une transaction ;
- utilise `lock_timeout = 15s` et `statement_timeout = 5min` ;
- expose `plan`, `apply`, `verify`.

## 3. Point critique : migration générée 012

### 3.1 Observation factuelle

L’entrée `012_VALIDATED_FX_REFERENCE_REGISTRY` déclare un générateur.

À chaque chargement du manifeste avec le comportement par défaut, le runner :

1. exécute `scripts/generate_validated_fx_reference_sql.py` ;
2. écrit ou remplace
   `schemas/reference/012_validated_fx_reference_registry.sql` ;
3. calcule ensuite le SHA-256 du fichier matérialisé ;
4. compare ce SHA au ledger.

Au HEAD audité, le fichier SQL `012` n’est pas présent comme blob Git. Seuls le
CSV source, le générateur et la déclaration du manifeste sont versionnés.

### 3.2 Réponses obligatoires

#### Une modification future du CSV peut-elle modifier rétroactivement 012 ?

```text
YES
```

Le même ID et le même chemin `012` sont régénérés à partir de l’état courant du
CSV. Une modification du CSV produit donc un nouveau contenu sous l’identité
historique `012`.

#### Le comportement respecte-t-il réellement `IMMUTABLE_AFTER_APPLICATION` ?

```text
NO — NOT AS AN ARTIFACT GOVERNANCE RULE
```

Le ledger protège la base déjà migrée en provoquant un checksum mismatch. C’est
un bon comportement fail-closed, mais cela ne rend pas l’artefact historique
immuable : le contenu attendu de `012` a déjà été régénéré avant la comparaison.

#### Quelle doit être la règle future ?

```text
1. OLD GENERATED SQL IS COMMITTED AND FROZEN FOREVER.
2. --check ONLY VERIFIES REPRODUCIBILITY OF THAT FROZEN ARTIFACT.
3. A NEW REGISTRY CHANGE CREATES A NEW FORWARD MIGRATION:
   015, 016, ...
4. AN APPLIED MIGRATION ID, PATH AND CONTENT ARE NEVER REGENERATED.
```

#### Le runner peut-il provoquer un drift involontaire avant `verify` ?

```text
YES
```

`verify` appelle le même chargement de manifeste qui exécute le générateur avant
le calcul du checksum.

#### La documentation actuelle suffit-elle ?

```text
NO
```

ADR-028 indique que les migrations générées sont matérialisées avant hashing et
affirme des checksums immuables. Il n’explique pas la règle de gel du SQL généré
ni la création obligatoire d’une nouvelle migration pour toute évolution du CSV.

### 3.3 Verdict

```text
MIGRATION_012_IMMUTABILITY:
NOT_DEMONSTRATED

OF_ARCH_004_STATUS:
IMPLEMENTED_WITH_OPEN_GOVERNANCE_BLOCKER
```

Aucun fichier technique n’est corrigé par cette revue.

## 4. Concurrence

Aucun verrou global PostgreSQL ou advisory lock n’est acquis avant la lecture du
ledger et l’application de la série.

Deux runners peuvent :

- lire simultanément le même état incomplet ;
- tenter la même migration ;
- se bloquer sur les DDL ou l’unicité du ledger ;
- provoquer le rollback de l’un des deux.

L’atomicité évite normalement une ligne de ledger sans sa migration, mais elle ne
sérialise pas les runners et n’empêche pas la contention.

```text
GLOBAL_RUNNER_LOCK: NOT_COVERED
CONCURRENT_RUNNERS: PARTIALLY_COVERED
```

Recommandation future : advisory lock global, acquis avant lecture du ledger et
conservé jusqu’à la fin du plan d’application.

## 5. Adoption des bases existantes

Le workflow vert teste :

```text
EMPTY_DATABASE
→ APPLY
→ APPLY AGAIN
→ VERIFY
→ DROP ONLY THE LEDGER SCHEMA
→ REPLAY ALL MIGRATIONS
→ VERIFY
```

Il démontre l’adoption d’une base qui possède déjà le résultat complet des 14
migrations mais plus son ledger.

Il ne démontre pas exhaustivement :

- une base avec seulement certaines migrations déjà matérialisées ;
- une base contenant des objets de même nom mais de structure incompatible ;
- un ledger partiel ;
- des données historiques déclenchant une contrainte nouvelle ;
- une base dérivée d’une ancienne branche avec divergence de schéma.

```text
EXISTING_DATABASE_ADOPTION: PARTIALLY_COVERED
```

Le runner échoue fermé sur plusieurs incompatibilités, mais ne possède pas de
mode d’inspection/adoption explicite par migration.

## 6. Matrice des risques

| Risque | Classement | Preuve / limite |
|---|---|---|
| Deux runners concurrents | `PARTIALLY_COVERED` | transactions et timeouts, sans sérialisation globale |
| Absence de verrou global | `NOT_COVERED` | aucun advisory lock dans le runner |
| Base partiellement initialisée sans ledger | `PARTIALLY_COVERED` | rejeu possible si tout est idempotent, scénario non exhaustif |
| Objets existants incompatibles | `PARTIALLY_COVERED` | échec fermé probable, absence de préflight structuré |
| Certaines migrations présentes seulement | `PARTIALLY_COVERED` | le workflow teste seulement l’état complet sans ledger |
| Ajout futur au manifeste | `COVERED` | ordre et unicité contrôlés ; migration forward possible |
| Modification d’une entrée appliquée | `COVERED` | dérive ordre/chemin/checksum bloquée |
| Suppression d’une entrée appliquée | `COVERED` | devient une entrée inconnue du ledger |
| Déplacement d’un SQL | `COVERED` | fichier manquant ou dérive de chemin |
| Générateur d’une ancienne migration | `NOT_COVERED` | `012` est rematérialisée avant checksum |
| Transaction DDL PostgreSQL | `COVERED` | SQL et ledger dans le même `BEGIN/COMMIT` |
| Timeout et rollback | `COVERED` | lock 15 s, statement 5 min, erreur psql non ignorée |
| Repair exceptionnel | `PARTIALLY_COVERED` | procédure documentaire, pas de mécanisme contrôlé dédié |
| Reproductibilité du plan | `PARTIALLY_COVERED` | déterministe pour un CSV donné, mutable dans le temps |
| Promotion accidentelle d’un SQL de proposition | `PARTIALLY_COVERED` | propositions exclues aujourd’hui, aucune interdiction sémantique permanente |
| Déploiement production | `OUT_OF_SCOPE` | aucun déploiement effectué ou testé |

## 7. Workflow validé

Le run `30965690163` valide le commit technique :

```text
5a6ed3da39571e331e8317e3759cd7068165c66d
```

Étapes réussies :

- tests unitaires ;
- plan du manifeste ;
- PostgreSQL 16 vide ;
- première application ;
- deuxième application ;
- verify ;
- assertions du contrat runtime ;
- adoption d’une base initialisée sans ledger.

Le commit `202f23d5...` est documentaire. Il n’est pas un nouveau run technique.

## 8. Procédure de réparation

La règle documentée « nouvelle migration forward » est correcte.

Le repair manuel exceptionnel doit rester soumis à :

- incident enregistré ;
- approbation explicite ;
- SQL transactionnel revu ;
- sauvegarde vérifiée ;
- preuve avant/après ;
- nouvelle migration forward décrivant l’état final.

Le runner ne doit jamais offrir un override silencieux de checksum.

## 9. Recommandations sans implémentation

1. Figer et committer le SQL historique `012`.
2. Transformer le générateur en vérificateur de reproductibilité pour `012`.
3. Produire toute évolution sous une nouvelle migration.
4. Ajouter un advisory lock global.
5. Ajouter des fixtures de bases partiellement initialisées et incompatibles.
6. Ajouter un préflight d’adoption en lecture seule.
7. Rendre l’exclusion des propositions indépendante d’une simple liste éditable.
8. Documenter précisément la matrice d’adoption et de repair.

Ces recommandations nécessitent une nouvelle phase explicitement autorisée.
