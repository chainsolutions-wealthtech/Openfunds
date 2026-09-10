# Journal de travail Loop Engineering

## Boucle OF-LOOP-DOC-003-RECONCILIATION-20260910 — 2026-09-10

```text
TASK_ID: OF-DOC-003
START_HEAD: eeaa07194fcb46fa0cf0859d5061a30ffc5602c0
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
MODE: DOCUMENTARY_GOVERNANCE_RECONCILIATION
STATUS: PERSISTED / REMOTE_FINAL_VERIFICATION_PENDING
PR_1: DRAFT / OPEN / UNMERGED
GITHUB_RULESETS: NONE_OBSERVED
PRODUCTION_DEPLOYED: NO
```

### Discovery / baseline

Les autorités racines, la branche existante, la PR #1, les workflows récents, les règles GitHub observables et le socle Regulatory de référence ont été relus avant écriture. Openfunds possédait déjà un socle important ; la décision a donc été de renforcer l'existant et non de recopier ou remplacer son architecture documentaire.

Baseline de départ : `eeaa07194fcb46fa0cf0859d5061a30ffc5602c0`.

La CI récente est devenue observable. Le run `OF-MAP-002 Mapping Registry` `32541124896` sur `275ec7a10658cfc5a9f5822eb2315bf01138fc10` est rouge : l'intégration officielle/canonique passe, les jobs unitaires Python 3.11 et 3.12 échouent parce que le contrat Batch 07 attend `NO_PARENT_CURRENCY_INFERENCE` dans `NOTES`.

### Implémentation documentaire

- `00_START_HERE.md` réconcilié ;
- `SOURCE_OF_TRUTH.md` renforcé ;
- `LOOP_ENGINEERING.md` complété ;
- `DEFINITION_OF_DONE.md` ajouté ;
- `STATUS.md`, `NEXT_ACTION.md`, `LOOP_STATE.md`, `CURRENT_ITERATION.md`, `TODO.md`, `SUIVI.md`, `HANDOFF.md` et `CHANGELOG.md` synchronisés ;
- rapport `docs/00_PROJECT/OF_DOC_003_GOVERNANCE_RECONCILIATION_20260910.md` ajouté.

### Non-régression par périmètre

Aucun code métier, migration, mapping, donnée d'outcome, test, workflow, `main`, branche supplémentaire, PR supplémentaire, retargeting, merge, force-push, production ou donnée réelle n'a été modifié par cette tranche.

Aucune règle métier du dépôt Regulatory n'a été transposée.

### Gaps ouverts

```text
OF_MAP_002_CI: FAILURE_KNOWN
GITHUB_NATIVE_RULESET: NONE_OBSERVED
PERSISTENT_PRODUCTION_DB: NOT_CONFIGURED
IMMUTABLE_RAW_STORE: NOT_CONFIGURED
PRODUCTION: NOT_DEPLOYED
```

### Prochaine action

Réconcilier le contrat Batch 07 de `OF-MAP-002` sans affaiblir les tests, obtenir la preuve CI Python 3.11/3.12 + intégration, puis reprendre Task 4 review outcomes.

---

## Boucle OF-LOOP-DATA-001 — 2026-08-05

```text
TASK_ID: OF-DATA-001
START_HEAD: e79c735b2cda8cc40a237b7deb3e379cc42bf1d9
VALIDATED_TECHNICAL_HEAD: 8ab1e75b2fd94566f9c0538ca33460140787c6bf
STATUS: VERIFIED_COMPLETE
```

Le modèle Fund/SubFund/ShareClass, la migration `015`, les fixtures Maroc/Tunisie/Nigeria et les contrôles PostgreSQL 16 ont été validés. Le commit intermédiaire ayant ajouté `NONEXISTENT` a été corrigé par un descendant sans force-push ni réécriture.

---

## Boucle OF-LOOP-DATA-002 — 2026-08-06

```text
TASK_ID: OF-DATA-002
START_HEAD: 0a48c14999a5f173fa5ab3ce4b91109e24092c2c
INITIAL_TECHNICAL_HEAD: 2d4c8c860aedce30a25cfc9ffcda1ab6ec820a43
MANIFEST_ALIGNMENT_HEAD: ecb2713c6b7ba591bc86b977ca7d35c455465174
VALIDATED_TECHNICAL_HEAD: 1fb49075abdfb958e152accf915c37ac86b9a54e
STATUS: VERIFIED_COMPLETE
```

### Audit

Le HEAD, la PR nº 1, `DATA_DICTIONARY.md`, ADR-024, la migration `015`, le manifeste de migrations et les conventions de gouvernance ont été lus avant écriture. Aucun catalogue officiel Openfunds versionné n’était présent.

### Implémentation

- paquet JSON gouverné en neuf fichiers ;
- dix tables et 143 colonnes ;
- 36 attributs par champ ;
- JSON Schema logique ;
- manifeste SHA-256 ;
- bibliothèque et générateur déterministes ;
- JSON expansé, CSV UTF-8 `;` et Markdown ;
- sept tests contractuels ;
- workflow Python 3.11/3.12 avec artefacts.

### Corrections transparentes

Le run initial a révélé deux empreintes de sortie provenant d’une variante locale. Le manifeste a été aligné sur le générateur commité au commit `ecb2713c...`. Le run suivant a révélé que le test SQL lisait une ligne `references` comme colonne ; l’extracteur a été limité au niveau top-level au commit `1fb49075...`. Aucun SQL ou contenu métier n’a changé.

### Validation

```text
31113488180 — Canonical Field Dictionary — SUCCESS
31113488273 — Collector Tests — SUCCESS
```

Les artefacts Python 3.11 et 3.12 ont le digest identique `sha256:a237c13e85fc486dcab515b3508fd92479596438acdb327679920d442596b67f`.

### Sortie

`OF-DATA-002` est fermé. Aucun historique réel, mapping officiel Openfunds, merge, déploiement ou démarrage de `OF-DATA-003` n’a été réalisé.

---

## Boucle OF-LOOP-DATA-003 — 2026-08-11

```text
TASK_ID: OF-DATA-003
START_HEAD: 145461e04ba9affd2b11fedaf56ed4ad49171b5d
VALIDATED_TECHNICAL_HEAD: 0777afffad950e779234ef09f3f2b9031ec41ce7
STATUS: VERIFIED_COMPLETE
```

### Audit et décision

Les sept sources Markdown D00–D17 ont été relues et comptées avant écriture : 18 domaines / 420 définitions. L’utilisateur a validé l’Option A `MIRROR_FIRST` : aucune donnée absente n’est inventée et la classification canonique est séparée de la nature source.

### TDD et implémentation

- `623afd1b…` RED puis `d7a5cb39…` GREEN : contrat legacy strict ;
- `c707f295…` RED puis `d60c494a…` GREEN : paquet machine-readable ;
- `98396915…` : bootstrap des 19 fichiers d’authoring ;
- `89321886…` RED puis `daab85c8…` / `01d9db78…` : classification gouvernée ;
- `0652758e…` RED puis `7369e34d…` / `ab4d1f06…` : vues déterministes, manifeste et SQL frozen ;
- `7527263b…` RED puis `e91079ed…` : migration gouvernée `016` ;
- `d8b3a2d6…` : correction de l’autorité d’authoring CI ;
- `0777afffad950e779234ef09f3f2b9031ec41ce7` : invariant fonds découplé de la position globale de migration.

### Validation

```text
COUNTRY_INDICATOR_CATALOG_RUN: 31484468846 — SUCCESS
MIGRATION_RUNNER_RUN: 31484586710 — SUCCESS
```

Le runner PostgreSQL 16 applique deux fois les 16 migrations, vérifie 18 domaines / 420 définitions, les comptes 298/85/7/30, l’absence de statut historique inventé et le scénario d’adoption sans ledger.

### Sortie

`OF-DATA-003` est fermé. Aucun historique réel, mapping officiel Openfunds, merge, déploiement, nouvelle branche ou nouvelle PR n’a été réalisé. La prochaine tâche candidate est `OF-SOURCE-002` en audit lecture seule.

---

## Boucle OF-LOOP-SOURCE-002 — Vague 01 — 2026-08-12

```text
TASK_ID: OF-SOURCE-002
WAVE: 01
AUDIT_START_HEAD: ddeee85042d37803bd27bc9cda81cc2e67856c57
WAVE_DATA_HEAD: 1f85c0df1878743f4a2ac322c2087b0b1a549641
STATUS: VERIFIED_COMPLETE_WAVE / GLOBAL_TASK_EN_COURS
```

### Audit read-only

Le dépôt a été relu depuis `00_START_HERE.md`, `AGENTS.md`, `SOURCE_OF_TRUTH.md`, les états de boucle et ADR-021. La lignée du HEAD a été vérifiée avant écriture. La baseline institutionnelle était :

```text
54 pays
40 organisations = 20 VALIDATED + 20 PENDING
7 / 54 pays avec au moins une organisation country-scoped
70 relations organisation-rôle = 26 VALIDATED + 44 PENDING
43 endpoints = 20 VALIDATED + 23 PENDING
```

Les actifs de recherche de la PR nº2 ont été exploités en lecture seule et chaque candidat a été réconcilié avec les codes existants. Une allowlist a ensuite été établie à partir de preuves institutionnelles officielles primaires.

### TDD

- test contractuel écrit avant intégration ;
- run `31592435103` RED sur Python 3.11/3.12 : validateur, organisations et rôles attendus absents ;
- validateur `scripts/validate_institutional_registry.py` ajouté ;
- run `31592516832` : invariants historiques et validateur verts, allowlist toujours rouge comme attendu ;
- 15 organisations et 22 relations de rôle ajoutées ;
- run final `31592700354` GREEN sur Python 3.11/3.12, 4/4 tests.

### Organisations intégrées

```text
BOTSWANA: BOB, NBFIRA, BSE, STATISTICS_BOTSWANA
NAMIBIE: BON, NAMFISA, NSX, NSA_NAMIBIA
ETHIOPIE: NBE, ECMA, ESX, ESS_ETHIOPIA
UEMOA: AMF_UMOA, UMOA_TITRES
CEMAC: COSUMAF
```

`FMDQ` est volontairement resté hors allowlist en attente d’un arbitrage sur le rôle canonique exact.

### État après vague 01

```text
55 organisations = 35 VALIDATED + 20 PENDING
10 / 54 pays avec au moins une organisation country-scoped
44 pays sans organisation country-scoped
92 relations organisation-rôle = 48 VALIDATED + 44 PENDING
43 endpoints inchangés
```

### Limites et sortie

Aucun endpoint spécialisé, provider series, collection specification, SQL runtime, historique, base persistante, branche, PR, merge, retargeting ou déploiement n’a été créé par cette vague. Les CSV restent des inventaires de découverte/revue conformément à ADR-021.

`OF-SOURCE-002` reste `EN_COURS`. La vague 02 démarre en lecture seule sur les 44 pays non couverts et les rôles manquants des 10 pays présents.

---

## Boucle OF-LOOP-SOURCE-002 — Vague 02 — 2026-08-12

```text
TASK_ID: OF-SOURCE-002
WAVE: 02
AUDIT_HEAD: 8e38c99d3e8ab224228bf9e1a628afb68878ba42
WAVE_DATA_HEAD: 2216ff00406e3ee40b0f8ef70ff8710f5c928d34
STATUS: VERIFIED_COMPLETE_WAVE / GLOBAL_TASK_EN_COURS
```

### Audit et allowlist

Quatre nouveaux pays ont été audités sur sources officielles primaires : Algérie, Maurice, Rwanda et Tanzanie. Seize organisations et vingt-deux relations de rôle ont été autorisées. Les rôles assurance/pension n'ont pas été ajoutés en Algérie ou Tanzanie faute de preuve correspondant exactement au rôle combiné canonique.

### TDD

```text
RED_RUN: 31594066287
RED_HEAD: 39b5f3a04df4c5f69d9ac4300c5a21e4f5728749
INTERMEDIATE_RUN: 31594256827
INTERMEDIATE_HEAD: 8a057200682773b09f61e898e55ca2f3537422f2
GREEN_RUN: 31594503714
GREEN_HEAD: 2216ff00406e3ee40b0f8ef70ff8710f5c928d34
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
TESTS: 6 / 6 PASS
```

Le RED initial conservait les quatre tests antérieurs verts et faisait échouer uniquement les deux tests de vague 02. Après ajout des organisations, cinq tests sur six passaient ; après ajout des relations, la suite complète était verte.

### Organisations intégrées

```text
ALGERIE: BANQUE_ALGERIE, COSOB, SGBV, ONS_ALGERIE
MAURICE: BOM, FSC_MAURITIUS, SEM, STATISTICS_MAURITIUS
RWANDA: NBR, CMA_RWANDA, RSE, NISR
TANZANIE: BOT, CMSA_TANZANIA, DSE, NBS_TANZANIA
```

### État après vague 02

```text
71 organisations = 51 VALIDATED + 20 PENDING
14 / 54 pays avec au moins une organisation country-scoped
40 pays sans organisation country-scoped
114 relations organisation-rôle = 70 VALIDATED + 44 PENDING
43 endpoints inchangés
```

Le workflow général `Collector Tests` a été déclenché sur le commit volontairement RED du contrat et a échoué pour cette raison ; il n'a pas été présenté comme vert au HEAD de données final. Le workflow `Institutional Registry`, gouvernant directement cette surface, est vert au HEAD final.

---

## Boucle OF-LOOP-SOURCE-002 — Vague 03 — 2026-08-12

```text
TASK_ID: OF-SOURCE-002
WAVE: 03
WAVE_DATA_HEAD: 5024a9767b1b9aecf8a6cd52d315ccfbf8384389
STATUS: VERIFIED_COMPLETE_WAVE / GLOBAL_TASK_EN_COURS
```

### Audit et protections

Le lot Ouganda, Zambie, Zimbabwe et Malawi a été audité sur sources officielles primaires. Deux risques ont été explicitement bloqués :

- `SEC_ZAMBIA` n'a pas été intégré car la racine du domaine historique officiel retournait lors de l'audit un contenu de paris non institutionnel ;
- `RBM/FUND_REGULATOR` n'a pas été intégré car les preuves primaires contrôlées ne démontraient pas assez explicitement la compétence CIS/OPC.

Pour l'Ouganda, les fonctions assurance et retraite étant séparées entre IRA et URBRA, aucune relation combinée `INSURANCE_PENSION_REGULATOR` n'a été inventée.

### TDD

```text
RED_RUN: 31595214746
RED_HEAD: c7169584b582760a26c708c701c63e77799ff3d8
INTERMEDIATE_RUN: 31595412831
INTERMEDIATE_HEAD: f74a482eb375e819419c77697d89c9d74676da2f
GREEN_RUN: 31595575537
GREEN_HEAD: 5024a9767b1b9aecf8a6cd52d315ccfbf8384389
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
TESTS: 8 / 8 PASS
```

Le RED conservait six tests existants verts et faisait échouer uniquement les deux nouveaux tests. Après ajout des seize organisations, sept tests sur huit passaient. Après ajout des vingt relations, les huit tests passaient. Les tests négatifs protègent également l'absence de `SEC_ZAMBIA` et de `RBM/FUND_REGULATOR`.

### Organisations intégrées

```text
OUGANDA: BOU, CMA_UGANDA, USE_UGANDA, UBOS
ZAMBIE: BOZ, LUSE, ZAMSTATS, PIA_ZAMBIA
ZIMBABWE: RBZ, SEC_ZIMBABWE, ZSE, ZIMSTAT, IPEC
MALAWI: RBM, MSE_MALAWI, NSO_MALAWI
```

### État après vague 03

```text
87 organisations = 67 VALIDATED + 20 PENDING
18 / 54 pays avec au moins une organisation country-scoped
36 pays sans organisation country-scoped
134 relations organisation-rôle = 90 VALIDATED + 44 PENDING
43 endpoints inchangés
```

### Sortie

Les vagues 01 à 03 n'ont ajouté aucun endpoint spécialisé, provider series, collection specification, SQL runtime, historique, base persistante, branche, PR, merge, retargeting ou déploiement. Les CSV restent des inventaires de découverte/revue conformément à ADR-021.

`OF-SOURCE-002` reste `EN_COURS`. La vague 04 est ouverte uniquement en audit lecture seule sur un nouveau lot contrôlé parmi les 36 pays restants.
