
# Sources de vérité Openfunds

```text
STATUS: ACTIVE
OWNER: PROJECT_GOVERNANCE
LAST_VERIFIED: 2026-08-11
CURRENT_HEAD_POLICY: RESOLVE_DYNAMICALLY
```

## Hiérarchie d’autorité

| Sujet | Autorité | Rôle | Ne constitue pas |
|---|---|---|---|
| État Git | GitHub sur la branche de contrôle résolue dynamiquement | commits, arbres, PR et CI | mémoire conversationnelle |
| Décisions | `DECISIONS.md` et ADR acceptés | décisions structurantes | proposition non acceptée |
| Tâches | `TODO.md` | identifiants, statut et critères | simple commentaire |
| Continuité | `SUIVI.md`, `WORK_LOG.md`, `HANDOFF.md` | historique et reprise | état runtime |
| Fund core dictionary | `data/dictionary/spec_v1/` | authoring des 143 champs physiques `fund.*` | catalogue D00–D17 |
| D00–D17 | `data/indicator_catalog/v1/` | authoring des 420 définitions pays-indicateurs | preuve de collecte/historique |
| Markdown D00–D17 historiques | `docs/04_DATA_GOVERNANCE/indicator_catalog/` | bootstrap et audit de fidélité | source d’authoring après bootstrap |
| SQL D00–D17 | `schemas/reference/016_country_indicator_catalog.sql` | migration frozen générée | source d’authoring |
| Migrations | `migrations/manifest.json` + ledger runtime | ordre et intégrité d’application | autorisation de production |
| Pilotes FX validés | `data/reference/VALIDATED_FX_REFERENCE_REGISTRY.csv` | authoring compact des pilotes validés | historique complet |
| PostgreSQL | vérité runtime après migration vérifiée | état appliqué | vérité d’authoring Git |
| `research_queue` | recherche non canonique | candidats et preuves | source canonique |
| Openfunds | couche de mapping/échange | import/export versionné | schéma physique interne |
| Artefacts bruts | stockage immuable par SHA-256 | preuve source | valeur canonique validée |

## Règle de conflit

En cas de contradiction, ne choisir ni la valeur la plus récente en apparence ni celle d’un assistant. Conserver les preuves, ouvrir une décision tracée et appliquer la hiérarchie ci-dessus.

## État vérifié

`OF-ARCH-004`, `OF-DATA-001`, `OF-DATA-002` et `OF-DATA-003` sont vérifiés complets dans leur périmètre. Le runner de migrations est validé en PostgreSQL 16 éphémère jusqu’à la migration `016`. Cela ne signifie pas qu’une base persistante de production est configurée ou migrée.

Toute évolution d’une autorité exige ADR/décision, tâche, SUIVI et CHANGELOG.
