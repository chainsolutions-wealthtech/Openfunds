# Sources de vérité Openfunds

```text
STATUS: ACTIVE
OWNER: PROJECT_GOVERNANCE
LAST_VERIFIED: 2026-08-05
TASK_ID: OF-DOC-003
```

## Hiérarchie d’autorité

| Sujet | Autorité | Rôle | Ne constitue pas |
|---|---|---|---|
| État Git | GitHub sur `architecture/africafunds-country-indicators-v0.1` résolu dynamiquement | commits, arbres, PR et CI | une mémoire conversationnelle |
| Décisions | `DECISIONS.md` et ADR acceptés | décisions structurantes | une proposition non acceptée |
| Tâches | `TODO.md` | identifiants, statut et critères | un simple commentaire |
| Continuité | `SUIVI.md`, `WORK_LOG.md`, `HANDOFF.md` | historique et reprise | un état runtime |
| Architecture | `ARCHITECTURE.md` | architecture canonique historique | l’index `docs/03-architecture/ARCHITECTURE.md` |
| Modèle | `DATA_MODEL.md` | modèle canonique historique | le brouillon SQL Fund |
| Pilotes FX validés | `data/reference/VALIDATED_FX_REFERENCE_REGISTRY.csv` | autorité d’authoring compacte | historique complet |
| SQL généré | représentation dérivée | synchronisation additive | nouvelle source d’authoring |
| PostgreSQL | vérité runtime après migration vérifiée | état appliqué | vérité d’authoring Git |
| `research_queue` | recherche non canonique | candidats et preuves à examiner | source canonique |
| Excel | export dérivé de revue | contrôle humain | source canonique |
| openfunds | couche de mapping et d’échange | import/export versionné | schéma physique interne |
| Artefacts bruts | stockage immuable par SHA-256 | preuve source | valeur canonique validée |

## Règle de conflit

En cas de contradiction, ne choisir ni la valeur la plus récente en apparence ni
celle d’un assistant. Ouvrir une décision tracée, conserver les deux preuves et
appliquer l’autorité ci-dessus.

## Blocker maintenu

`OF-ARCH-004` reste `IMPLEMENTED_WITH_OPEN_GOVERNANCE_BLOCKER` : la migration
générée `012` n’est pas figée comme artefact historique. Cette mission ne la
modifie pas et ne masque pas ce blocker.

## Mise à jour

Ce fichier change uniquement lorsqu’une décision acceptée modifie une autorité.
Toute évolution exige une entrée dans `DECISIONS.md`, `TODO.md`, `SUIVI.md` et
`CHANGELOG.md`.
