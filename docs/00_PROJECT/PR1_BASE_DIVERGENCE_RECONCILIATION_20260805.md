# Réconciliation de la divergence entre la PR nº 1 et sa base

```text
DATE: 2026-08-05
PR: 1
STATE: OPEN
DRAFT: TRUE
MERGED: FALSE
MERGEABLE: FALSE
BASE_BRANCH: architecture/canonical-model-v1-bootstrap
BASE_BRANCH_HEAD: 136abf71f0825075361f8c7446e19c6f6476a3a5
HEAD_BRANCH: architecture/africafunds-country-indicators-v0.1
HEAD_SHA: 202f23d5a5be961d6f8338984b04655eda336a6b
MERGE_BASE_SHA: 23ce7c7f00206f37eeec50dfccf03fa2cb7505ea
AHEAD_BY: 183
BEHIND_BY: 7
ACTION_PERFORMED: NONE
```

## 1. Les sept commits propres au bootstrap

| Ordre | SHA | Message |
|---:|---|---|
| 1 | `fd1ee4bcd686cad76096b7aa5fa6a4848ec5c45a` | `feat(reference): add canonical Africa regions` |
| 2 | `bd4b0f460e422ffb0904437c662955b15997a3e5` | `feat(reference): add monetary and common market zones` |
| 3 | `f7743bc59e0621facc7542410d87d1200ac1442b` | `feat(reference): add 54-country Africa canonical seed` |
| 4 | `d6c70249c60f6465aa046f0977b7b6cfdfcfae0a` | `docs: define pan-African country relationship model` |
| 5 | `14c7f4b839acd59862455d50fd9c2f7d8502077b` | `schema: add historized country relationship model` |
| 6 | `80165a8e9452176260a0bdaffeefc524e7a2b2ed` | `Add explicit country relationship matrix for 54 African countries` |
| 7 | `136abf71f0825075361f8c7446e19c6f6476a3a5` | `Document validation rules for country relationship matrix` |

Ces commits ajoutent exactement sept chemins après le merge-base.

## 2. Comparaison fichier par fichier

| Fichier | Blob base | Blob head | Identique | Head superset | Conflit sémantique | Risque Git | Contenu à préserver | Action future |
|---|---|---|---|---|---|---|---|---|
| `data/reference/AFRICA_COUNTRIES.csv` | `1c5d025e1b1b6a874cec54ae0a02ac369aea3b0c` | `1c5d025e1b1b6a874cec54ae0a02ac369aea3b0c` | YES | EQUAL | NO | LOW | blob commun | conserver une copie |
| `data/reference/AFRICA_REGIONS.csv` | `047f06bd1cc2bed0e3dfdb40e9481614bda51e96` | `047f06bd1cc2bed0e3dfdb40e9481614bda51e96` | YES | EQUAL | NO | LOW | blob commun | conserver une copie |
| `data/reference/COUNTRY_RELATIONSHIPS.csv` | `56dd5061489b8f6d4e9df644a809a31ad4b014d4` | `56dd5061489b8f6d4e9df644a809a31ad4b014d4` | YES | EQUAL | NO | LOW | blob commun | conserver une copie |
| `data/reference/MARKET_ZONES.csv` | `d8dde508028afdfeb4e290cb450052ea9910e5ba` | `d8dde508028afdfeb4e290cb450052ea9910e5ba` | YES | EQUAL | NO | LOW | blob commun | conserver une copie |
| `docs/04_GEOGRAPHY/COUNTRY_RELATIONSHIPS_VALIDATION.md` | `85d50ae755990f336ce83dcfe0586466ad23c562` | `85d50ae755990f336ce83dcfe0586466ad23c562` | YES | EQUAL | NO | LOW | blob commun | conserver une copie |
| `docs/04_GEOGRAPHY/COUNTRY_RELATIONSHIP_MODEL.md` | `5505d477bf54a427931b62138e65d6d11fce3fd0` | `5505d477bf54a427931b62138e65d6d11fce3fd0` | YES | EQUAL | NO | LOW | blob commun | conserver une copie |
| `schemas/reference/002_country_relationships.sql` | `394ee892c9d41e1ca038b1b7b411dbbdc990bb54` | `7bf9ef709bc4129be9c95880567741c637e042dd` | NO | YES | NO, intentional evolution | HIGH add/add | version head avec création monotone de vue | résoudre explicitement en faveur du head |

## 3. Cause exacte de `mergeable=false`

Les deux branches ont ajouté indépendamment les sept mêmes chemins après leur
merge-base.

Six additions ont le même blob et ne portent aucun conflit de contenu.

Le septième chemin possède deux blobs différents :

```text
schemas/reference/002_country_relationships.sql
```

La version bootstrap utilise `CREATE OR REPLACE VIEW`. La version AfricaFunds
conserve le même schéma historique mais crée la vue seulement si elle est
absente. Cette évolution est nécessaire pour ne pas retirer les colonnes
ajoutées par une migration ultérieure lors de l’adoption d’une base existante.

La cause fonctionnelle de `mergeable=false` est donc un conflit add/add sur ce
fichier. Le contenu AfricaFunds doit être préservé.

## 4. Stratégie A — réconcilier le bootstrap dans AfricaFunds

### Bénéfices

- conserve la cible actuelle de la PR ;
- rattache explicitement les sept commits du bootstrap ;
- résout le conflit dans la branche de travail.

### Risques

- crée un commit de merge ou une résolution dédiée ;
- ajoute du bruit historique pour six blobs déjà identiques ;
- risque de choisir par erreur l’ancien SQL `002`.

### Effet sur les conflits et la revue

- conflit manuel sur `002` ;
- nouvelle revue complète des résultats de fusion ;
- workflows à relancer.

### Garanties nécessaires

- six blobs inchangés ;
- blob head de `002` conservé ;
- tests business-date et migration runner verts ;
- aucune activation de modèles de proposition.

### Recommandation

```text
VIABLE_BUT_NOT_PREFERRED
```

## 5. Stratégie B — retargeter ultérieurement la PR nº 1 vers main

### Bénéfices

- évite les sept commits bootstrap redondants ;
- évite le conflit add/add avec le bootstrap ;
- présente directement la branche complète face à la branche stable minimale ;
- correspond à la recommandation historique.

### Risques

- change substantiellement la comparaison de la PR ;
- nécessite une nouvelle revue de périmètre ;
- la PR reste très volumineuse ;
- exige une autorisation explicite de retargeting.

### Effet sur l’historique et la revue

- conserve les 183 commits de la branche AfricaFunds ;
- ne fusionne pas la lignée bootstrap séparée ;
- réinitialise l’analyse de mergeabilité contre `main`.

### Garanties nécessaires

- main résolu dynamiquement ;
- contrôle que les actifs bootstrap utiles sont déjà présents ;
- CI déterministe verte au nouveau diff ;
- description PR actualisée ;
- blocker `012` résolu avant déclaration « prête à fusionner ».

### Recommandation

```text
PREFERRED_STRATEGY_AFTER_EXPLICIT_AUTHORIZATION
```

Le HEAD de `main` observé lors de cet audit est
`946145e4b33a6289eb340a16bf5c651cb9bbee7c`. Ce SHA est une observation, pas un
alias permanent.

## 6. Stratégie C — nouvelle PR propre vers main

### Bénéfices

- nouvelle narration d’intégration ;
- possibilité de curer les commits ou de présenter un squash contrôlé ;
- PR nº 1 conservée comme historique.

### Risques

- duplication de revue ;
- fragmentation des discussions et preuves ;
- risque de divergence entre l’ancienne et la nouvelle PR ;
- plus de travail de préparation.

### Garanties nécessaires

- source unique de la nouvelle branche/PR ;
- comparaison complète avec PR nº 1 ;
- aucun actif perdu ;
- CI et revue indépendantes.

### Recommandation

```text
FALLBACK_IF_RETARGETING_IS_REJECTED
```

## 7. Verdict

```text
CURRENT_RECOMMENDATION: STRATEGY_B
EXECUTION_AUTHORIZED: NO
CONFLICTING_FILES: 1
FILE_TO_PRESERVE: schemas/reference/002_country_relationships.sql FROM HEAD
MERGE_PERFORMED: NO
REBASE_PERFORMED: NO
RETARGETING_PERFORMED: NO
```
