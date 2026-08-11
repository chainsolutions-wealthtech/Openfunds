#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-11"
TECHNICAL_HEAD = "0777afffad950e779234ef09f3f2b9031ec41ce7"
LOOP_START_HEAD = "145461e04ba9affd2b11fedaf56ed4ad49171b5d"
COUNTRY_RUN = "31484468846"
MIGRATION_RUN = "31484586710"

EXPECTED_DOC_PATHS = [
    "00_START_HERE.md",
    "AGENTS.md",
    "SOURCE_OF_TRUTH.md",
    "STATUS.md",
    "LOOP_STATE.md",
    "CURRENT_ITERATION.md",
    "WORK_LOG.md",
    "NEXT_ACTION.md",
    "HANDOFF.md",
    "TODO.md",
    "SUIVI.md",
    "CHANGELOG.md",
    "DECISIONS.md",
    "docs/04_DATA_GOVERNANCE/Africa_Country_Indicator_Framework_v0.1.md",
    "docs/superpowers/plans/2026-08-11-of-data-003-country-indicator-catalog.md",
    "docs/01_ARCHITECTURE/ADR-032_COUNTRY_INDICATOR_CATALOG_MIRROR_FIRST.md",
    "docs/04_DATA_GOVERNANCE/COUNTRY_INDICATOR_CATALOG_V1.md",
    "docs/00_PROJECT/OF_DATA_003_COMPLETION_20260811.md",
]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.rstrip() + "\n", encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one anchor, found {count}")
    return text.replace(old, new, 1)


def append_once(path: str, marker: str, block: str) -> None:
    text = read(path)
    if marker in text:
        return
    write(path, text.rstrip() + "\n\n" + block.strip() + "\n")


def set_task_status(text: str, task_id: str, status: str) -> str:
    pattern = re.compile(
        rf"(?ms)(^## {re.escape(task_id)} —.*?^- \*\*Statut :\*\* )([^\n]+)"
    )
    match = pattern.search(text)
    if not match:
        raise RuntimeError(f"TODO: task/status not found for {task_id}")
    return text[: match.start(2)] + status + text[match.end(2) :]


def update_todo() -> None:
    path = "TODO.md"
    text = read(path)
    text = replace_once(
        text,
        "Dernière mise à jour : `2026-08-03`.",
        "Dernière mise à jour : `2026-08-11`.",
        "TODO last update",
    )
    for task_id in (
        "OF-ARCH-001",
        "OF-SOURCE-001",
        "OF-ARCH-002",
        "OF-ARCH-003",
        "OF-ARCH-004",
        "OF-DATA-001",
        "OF-DATA-002",
        "OF-DATA-003",
    ):
        text = set_task_status(text, task_id, "TERMINE")

    text = replace_once(
        text,
        "- **Etat actuel :** structure obligatoire documentée dans `DATA_DICTIONARY.md`, catalogue non peuplé.",
        "- **Etat actuel :** `OF-DATA-002` vérifié complet : paquet JSON gouverné `data/dictionary/spec_v1/`, 10 tables, 143 champs, 36 attributs par champ et CI Python 3.11/3.12 verte.",
        "TODO OF-DATA-002 state",
    )
    data003_anchor = "- **Livrables :** catalogue structuré, import SQL et tests d'unicité."
    data003_replacement = data003_anchor + "\n- **Date de fin :** 2026-08-11\n- **Résultat vérifié :** 18 domaines, 420 codes uniques, paquet d’authoring JSON v1, classification gouvernée 298 `RAW` / 85 `METADATA` / 7 `EVENT` / 30 `CALCULATED`, vues JSON/CSV `;`/Markdown/SQL déterministes, migration `016` et double application PostgreSQL 16 en CI.\n- **Preuve :** `docs/00_PROJECT/OF_DATA_003_COMPLETION_20260811.md`."
    text = replace_once(text, data003_anchor, data003_replacement, "TODO OF-DATA-003 closeout")

    sync_marker = "## Synchronisation des statuts — 2026-08-11"
    if sync_marker not in text:
        anchor = "Priorités : `P0_CRITIQUE`, `P1_HAUTE`, `P2_MOYENNE`, `P3_BASSE`."
        sync = anchor + "\n\n## Synchronisation des statuts — 2026-08-11\n\nLes statuts de `OF-ARCH-001`, `OF-SOURCE-001`, `OF-ARCH-002`, `OF-ARCH-003`, `OF-ARCH-004`, `OF-DATA-001`, `OF-DATA-002` et `OF-DATA-003` sont alignés sur les boucles vérifiées et les preuves CI. Les descriptions historiques restent conservées ; le statut `TERMINE` n’implique ni déploiement de production ni chargement d’historiques réels."
        text = replace_once(text, anchor, sync, "TODO status sync")
    write(path, text)


def update_suivi() -> None:
    path = "SUIVI.md"
    text = read(path)
    text = replace_once(
        text,
        "Dernière mise à jour : `2026-08-03`  ",
        "Dernière mise à jour : `2026-08-11`  ",
        "SUIVI last update",
    )
    replacements = {
        "CATALOGUE D00-D17                        DOCUMENTE, NON CENTRALISE": "CATALOGUE D00-D17                        CENTRALISE JSON / TESTE / MIGRATION 016",
        "MODELE FUND/SUBFUND/SHARECLASS           A ARBITRER": "MODELE FUND/SUBFUND/SHARECLASS           VERIFIED_COMPLETE",
        "DICTIONNAIRE MACHINE-READABLE            NON PEUPLE": "DICTIONNAIRE MACHINE-READABLE            FUND CORE + D00-D17 GOUVERNES",
    }
    for old, new in replacements.items():
        text = replace_once(text, old, new, f"SUIVI summary {old[:20]}")
    write(path, text)
    append_once(
        path,
        "## MISE A JOUR DU 11 AOUT 2026 — OF-DATA-003 VERIFIED COMPLETE",
        f"""
## MISE A JOUR DU 11 AOUT 2026 — OF-DATA-003 VERIFIED COMPLETE

```text
TASK_ID: OF-DATA-003
LOOP_ID: OF-LOOP-DATA-003
LOOP_START_HEAD: {LOOP_START_HEAD}
VALIDATED_TECHNICAL_HEAD: {TECHNICAL_HEAD}
CURRENT_HEAD_POLICY: RESOLVE_DYNAMICALLY
PRODUCTION_DEPLOYED: NO
REAL_COUNTRY_HISTORY_LOADED: NO
```

### Résultat

- les sept Markdown D00–D17 historiques ont été figés comme sources de bootstrap et de fidélité ;
- `data/indicator_catalog/v1/` est la source d’authoring logique gouvernée ;
- 18 domaines et exactement 420 codes canoniques uniques sont présents ;
- les absences restent `null` / `NOT_AUTHORED` au lieu d’être inventées ;
- `source_nature` reste distinct de `canonical_nature` ;
- la classification gouvernée `OF-DATA-003-A` compte 298 `RAW`, 85 `METADATA`, 7 `EVENT` et 30 `CALCULATED` ;
- `target_history` reste une exigence et tous les `history_status` restent `NOT_ASSERTED_BY_DEFINITION_CATALOGUE` ;
- JSON expansé, CSV UTF-8 `;`, Markdown et SQL sont générés déterministement ;
- la migration `016_COUNTRY_INDICATOR_CATALOG` crée uniquement `ref.indicator_domain` et `ref.indicator_definition` ;
- aucune observation, série pays, historique réel, secret, base persistante ou production n’a été chargé.

### Preuves

```text
COUNTRY_INDICATOR_CATALOG_RUN: {COUNTRY_RUN} — SUCCESS
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
MIGRATION_RUNNER_RUN: {MIGRATION_RUN} — SUCCESS
POSTGRESQL_16_DOUBLE_APPLY: SUCCESS
POSTGRESQL_16_VERIFY: SUCCESS
RUNTIME_COUNTS: 18 DOMAINS / 420 DEFINITIONS
```

Le run de migrations valide aussi les fixtures Fund/SubFund/ShareClass et le scénario d’adoption d’une base déjà initialisée sans ledger.

### Correction transparente de boucle

La CI a révélé qu’une étape réappliquait la classification dans son workspace avant de figer le manifeste. Le SQL était identique, mais la phrase de métadonnées rendait le hash JSON différent. La cause a été corrigée au commit `d8b3a2d697e9bfdad9a022ba8379494fcaa17608` : le paquet JSON commité est désormais strictement autoritaire et la CI le vérifie sans le réécrire. Un test fonds supposait ensuite à tort que la migration `015` devait rester la dernière migration globale ; le commit `{TECHNICAL_HEAD}` a recentré l’invariant sur l’unicité de la migration canonique du domaine `fund`.

### Prochaine porte

`OF-MAP-001` reste bloqué tant qu’un catalogue Openfunds officiel, versionné et licencié n’est pas archivé. La prochaine tâche non bloquée de priorité haute est `OF-SOURCE-002` : compléter les institutions des 54 pays. La reprise doit commencer en lecture seule par un audit de couverture et de preuve ; aucune donnée réelle ne doit être inventée ou déclarée complète sans source vérifiée.
""",
    )


def update_changelog() -> None:
    path = "CHANGELOG.md"
    text = read(path)
    old_decide = """### A décider

- source de vérité des référentiels CSV/SQL ;
- modèle canonique d'endpoint ;
- traitement des dates métier inconnues ;
- stratégie de migrations ;
- modèle final Fund/SubFund/ShareClass ;
- format maître du dictionnaire ;
- version officielle openfunds à intégrer."""
    new_decide = """### A décider

- version officielle Openfunds à intégrer et sa licence ;
- PostgreSQL persistant et stockage brut immuable ;
- complétude des institutions et mappings sources des 54 pays ;
- méthodologies WTI Bench, risque sans risque et MAR encore ouvertes."""
    text = replace_once(text, old_decide, new_decide, "CHANGELOG open decisions")
    marker = "## [2026-08-11] — OF-DATA-003 CATALOGUE D00-D17 GOUVERNE"
    if marker not in text:
        anchor = "## [2026-08-03] — CONSOLIDATION DOCUMENTAIRE"
        block = f"""
## [2026-08-11] — OF-DATA-003 CATALOGUE D00-D17 GOUVERNE

### Décidé

- Option A `MIRROR_FIRST` : les sept Markdown historiques restent des sources de bootstrap/audit et le paquet JSON `data/indicator_catalog/v1/` devient l’autorité d’authoring ;
- les valeurs absentes restent `null` avec statut explicite ;
- `source_nature` et `canonical_nature` sont séparés ;
- la classification `RAW / METADATA / EVENT / CALCULATED` est une décision de gouvernance versionnée, pas une assertion fournisseur ;
- `target_history` ne prouve jamais qu’un historique est chargé.

### Ajouté

- 19 fichiers d’authoring (`00_metadata.json` + D00 à D17) ;
- JSON Schema du catalogue ;
- générateur déterministe JSON/CSV `;`/Markdown/SQL ;
- manifeste SHA-256 ;
- migration gouvernée `016_COUNTRY_INDICATOR_CATALOG` ;
- tests contractuels et workflow Python 3.11/3.12 ;
- ADR-032, documentation de gouvernance et rapport de clôture.

### Vérifié

- 18 domaines / 420 codes uniques ;
- 298 `RAW`, 85 `METADATA`, 7 `EVENT`, 30 `CALCULATED` ;
- aucun historique chargé revendiqué ;
- run catalogue `{COUNTRY_RUN}` : `SUCCESS` ;
- run migrations `{MIGRATION_RUN}` : `SUCCESS` ;
- double application PostgreSQL 16, vérification runtime et scénario d’adoption sans ledger : `SUCCESS`.

### Corrigé

- suppression d’une mutation CI du paquet d’authoring avant génération du manifeste ;
- découplage du test Fund/SubFund/ShareClass de la position globale de la migration `015`.

### Non réalisé

- aucune production persistante ;
- aucune observation ou histoire pays chargée ;
- aucun mapping officiel Openfunds inventé ;
- aucun merge, retargeting, nouvelle branche, nouvelle PR ou déploiement.

"""
        text = replace_once(text, anchor, block + anchor, "CHANGELOG OF-DATA-003 insert")
    write(path, text)


def update_decisions() -> None:
    append_once(
        "DECISIONS.md",
        "## ADR-032 — CATALOGUE D00-D17 MIRROR-FIRST",
        """
## ADR-032 — CATALOGUE D00-D17 MIRROR-FIRST

- **Statut :** ACCEPTE
- **Date :** 2026-08-11
- **Tâche :** `OF-DATA-003`
- **Décision détaillée :** `docs/01_ARCHITECTURE/ADR-032_COUNTRY_INDICATOR_CATALOG_MIRROR_FIRST.md`.
- **Décision :** les sept Markdown historiques D00–D17 sont des sources de bootstrap et de fidélité ; le paquet JSON `data/indicator_catalog/v1/` est l’unique autorité d’authoring de la v1 du catalogue pays-indicateurs.
- **Règle d’absence :** aucune valeur manquante n’est inventée ; `null`, `NOT_AUTHORED`, `UNKNOWN`, `NOT_APPLICABLE` et zéro restent distincts.
- **Nature :** `source_nature` est préservée ; `canonical_nature` est une classification de gouvernance distincte et versionnée selon `OF-DATA-003-A`.
- **Historique :** `target_history` est un objectif de couverture ; il ne prouve ni collecte ni chargement. Le catalogue ne peut pas attribuer un statut historique chargé.
- **Runtime :** la migration générée/frozen `016_COUNTRY_INDICATOR_CATALOG` matérialise uniquement les définitions sous `ref.*` ; elle n’importe aucune observation pays.
- **Effet sur ADR-024 :** ADR-024 est remplacé pour le périmètre D00–D17 par ADR-032. ADR-031 reste l’autorité du dictionnaire `CANONICAL_FUND_CORE`.
- **Limites :** aucun catalogue officiel Openfunds n’est intégré, aucune donnée réelle n’est chargée et aucun déploiement de production n’est autorisé par cette décision.
""",
    )


def update_framework() -> None:
    path = "docs/04_DATA_GOVERNANCE/Africa_Country_Indicator_Framework_v0.1.md"
    text = read(path)
    old = "## Status\n\nDraft extension aligned with the accepted Country-Centric Market Universe and the Fund Relationship Information Model."
    new = "## Status\n\nFramework retained. The D00–D17 definition catalogue is governed as v1 under ADR-032; country coverage, provider mappings and loaded histories remain separate evidence layers."
    text = replace_once(text, old, new, "framework status")
    write(path, text)
    append_once(
        path,
        "## Governed authoring authority — 2026-08-11",
        """
## Governed authoring authority — 2026-08-11

The canonical D00–D17 definition catalogue is authored under:

```text
data/indicator_catalog/v1/
```

The seven files in `docs/04_DATA_GOVERNANCE/indicator_catalog/` remain frozen bootstrap/audit inputs. Generated JSON, CSV, Markdown and SQL views are derived representations and must not become competing authoring sources.

The v1 catalogue contains exactly 18 domains and 420 unique canonical codes. `source_nature` preserves what the legacy source stated; `canonical_nature` is a separate governed classification under decision `OF-DATA-003-A`. Missing source semantics remain explicit `null` / `NOT_AUTHORED`.

The catalogue does not claim country-series availability, successful collection, historical completeness or active calculations. `target_history` is a requested coverage horizon and `history_status` remains `NOT_ASSERTED_BY_DEFINITION_CATALOGUE`. Country/zone mappings, provider series and observations stay relationally separate.
""",
    )


def update_plan() -> None:
    path = "docs/superpowers/plans/2026-08-11-of-data-003-country-indicator-catalog.md"
    text = read(path)
    text = text.replace("- [ ]", "- [x]")
    text = replace_once(
        text,
        "- Create: `data/indicator_catalog/v1/00_metadata.json`\n- Create: `data/indicator_catalog/v1/catalog.json`\n- Create: `data/indicator_catalog/country-indicator-catalog-v1.schema.json`",
        "- Create: `data/indicator_catalog/v1/00_metadata.json`\n- Create: `data/indicator_catalog/v1/D00.json` … `D17.json`\n- Create: `data/indicator_catalog/country-indicator-catalog-v1.schema.json`",
        "plan authoring files",
    )
    text = replace_once(
        text,
        "Type consistency: `catalog.json` est l’unique authoring authority après bootstrap ; toutes les sorties et le SQL dérivent de ce fichier.",
        "Type consistency: `data/indicator_catalog/v1/` est l’unique paquet logique d’authoring après bootstrap ; toutes les sorties et le SQL dérivent de ses 19 fichiers gouvernés.",
        "plan type consistency",
    )
    if "## Implementation record" not in text:
        text += f"""

## Implementation record

```text
LOOP_START_HEAD: {LOOP_START_HEAD}
VALIDATED_TECHNICAL_HEAD: {TECHNICAL_HEAD}
COUNTRY_INDICATOR_CATALOG_RUN: {COUNTRY_RUN} — SUCCESS
MIGRATION_RUNNER_RUN: {MIGRATION_RUN} — SUCCESS
POSTGRESQL_16_DOUBLE_APPLY: SUCCESS
PRODUCTION_DEPLOYED: NO
REAL_COUNTRY_DATA_LOADED: NO
```

Implementation deviation intentionally accepted: instead of a single monolithic `catalog.json`, the authoring authority is partitioned into `00_metadata.json` plus D00–D17 domain files. This keeps one logical authority while making review and domain ownership tractable.
"""
    write(path, text)


def write_current_state_docs() -> None:
    write("00_START_HERE.md", f"""
# Openfunds — point d’entrée obligatoire

```text
STATUS: ACTIVE
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
CURRENT_HEAD_POLICY: RESOLVE_DYNAMICALLY
DOCUMENTARY_BASELINE_END: 59f6475102b8a0c5b1274060afc412db787f2caf
LATEST_VERIFIED_TECHNICAL_HEAD: {TECHNICAL_HEAD}
LAST_VERIFIED: 2026-08-11
```

## Finalité

Ce fichier est le premier document à lire pour toute intervention humaine ou IA. Il ne remplace pas les documents historiques : il ordonne les autorités à consulter avant toute écriture.

## Lecture obligatoire

1. `AGENTS.md` ;
2. `SOURCE_OF_TRUTH.md` ;
3. `STATUS.md` ;
4. `NEXT_ACTION.md` ;
5. `LOOP_STATE.md` et `CURRENT_ITERATION.md` ;
6. `TODO.md`, `SUIVI.md`, `DECISIONS.md` ;
7. le rapport de clôture le plus récent sous `docs/00_PROJECT/` ;
8. les ADR liés à la tâche candidate.

## Contrôle Git obligatoire

Résoudre dynamiquement le HEAD de la branche de contrôle, vérifier la lignée depuis la baseline documentaire et inventorier tout commit postérieur au dernier HEAD technique validé. Arrêter en cas de divergence non comprise ou d’intervention concurrente sur les mêmes fichiers.

## Gates techniques vérifiés

```text
OF-ARCH-001   VERIFIED_COMPLETE
OF-SOURCE-001 VERIFIED_COMPLETE
OF-ARCH-002   VERIFIED_COMPLETE
OF-ARCH-003   VERIFIED_COMPLETE
OF-ARCH-004   VERIFIED_COMPLETE
OF-DATA-001   VERIFIED_COMPLETE
OF-DATA-002   VERIFIED_COMPLETE
OF-DATA-003   VERIFIED_COMPLETE
```

## Interdictions permanentes

Ne pas travailler directement sur `main`, créer une branche/PR, force-push, fusionner ou retargeter une PR, déployer ou charger des données réelles sans une porte explicite. `COLLECTION_TESTED` ne signifie jamais `HISTORY_LOADED` et une définition de catalogue n’est jamais une observation.
""")

    write("AGENTS.md", """
# Règles communes pour tous les agents et assistants

```text
STATUS: ACTIVE
AUTHORITY: COMMON_AI_AND_HUMAN_ENTRY_POINT
TASK_POLICY: RESOLVE_FROM_STATUS_AND_NEXT_ACTION
LOOP_POLICY: RESOLVE_FROM_LOOP_STATE
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
BASELINE_END_SHA: 59f6475102b8a0c5b1274060afc412db787f2caf
```

## Ordre d’amorçage

Tout agent doit lire `00_START_HERE.md`, ce fichier, `SOURCE_OF_TRUTH.md`, `STATUS.md`, `NEXT_ACTION.md`, `TODO.md`, `SUIVI.md`, `DECISIONS.md`, puis les audits/rapports datés les plus récents avant de proposer une écriture.

## Vérification dynamique obligatoire

1. résoudre le HEAD courant de la branche de contrôle ;
2. vérifier la lignée depuis la baseline documentaire ;
3. inventorier les commits ajoutés depuis le dernier HEAD technique validé ;
4. vérifier les PR nº 1 et nº 2 avant toute opération les concernant ;
5. rechercher toute collision d’identifiant `OF-*` et `OF-LOOP-*` ;
6. arrêter en cas de divergence non comprise ou de modification concurrente.

## Branche et PR

- seule branche d’écriture autorisée sans nouvelle décision : `architecture/africafunds-country-indicators-v0.1` ;
- ne jamais travailler directement sur `main` ;
- ne créer aucune branche ou PR sans autorisation explicite ;
- ne pas modifier, fermer, fusionner ou retargeter la PR nº 2 ;
- ne pas fusionner ou retargeter la PR nº 1 ;
- commits fast-forward uniquement, sans réécriture d’historique.

## Non-régression métier

Préserver PostgreSQL comme vérité runtime, Openfunds comme couche de mapping, les couches raw/normalisé/validé/canonique/analytique/API/UI, la bitemporalité, la provenance, Fund/SubFund/ShareClass, identité/noms/alias, pays/région/zone de marché, XOF/XAF, native/EUR/USD, observé/calculé, catégorie/peers/WTI/benchmark/WTI Bench/RFR/MAR, `NULL != 0` et l’absence de date inventée.

## Frontières de statut

```text
STRUCTURE_PREFILLED != PRODUCTION_ACTIVE
NOT_ACTIVE != CALCULATED_PRODUCT_AVAILABLE
METHODOLOGY_TO_VALIDATE != VALIDATED_METHODOLOGY
COLLECTION_TESTED != HISTORY_LOADED
PROPOSED_SQL != PRODUCTION_MIGRATION
RESEARCH_CANDIDATE != CANONICAL_SOURCE
IMPLEMENTED != VERIFIED_COMPLETE
DEFINITION_PRESENT != OBSERVATION_AVAILABLE
TARGET_HISTORY != HISTORY_LOADED
```

## Preuves et transmission

Toute affirmation doit pointer vers un commit, diff, test, workflow, artefact, document daté ou état d’environnement observé. Mettre à jour `LOOP_STATE.md`, `CURRENT_ITERATION.md`, `WORK_LOG.md`, `NEXT_ACTION.md`, `STATUS.md` et `HANDOFF.md`. Le rapport final sépare fait, preuve, limite, risque, décision et prochaine action.
""")

    write("SOURCE_OF_TRUTH.md", f"""
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
""")

    write("STATUS.md", f"""
# État vérifié du projet

```text
STATUS_DATE: 2026-08-11
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
CURRENT_HEAD_POLICY: RESOLVE_DYNAMICALLY
VALIDATED_TECHNICAL_HEAD: {TECHNICAL_HEAD}
TASK_ID: OF-DATA-003
LOOP_ID: OF-LOOP-DATA-003
LOOP_STATUS: VERIFIED_COMPLETE
PRODUCTION_DEPLOYED: NO
REAL_COUNTRY_DATA_LOADED: NO
```

## Gates

```text
OF-ARCH-001   VERIFIED_COMPLETE
OF-SOURCE-001 VERIFIED_COMPLETE
OF-ARCH-002   VERIFIED_COMPLETE
OF-ARCH-003   VERIFIED_COMPLETE
OF-ARCH-004   VERIFIED_COMPLETE
OF-DATA-001   VERIFIED_COMPLETE
OF-DATA-002   VERIFIED_COMPLETE
OF-DATA-003   VERIFIED_COMPLETE
```

## Catalogue D00–D17

```text
AUTHORITATIVE_PACKAGE: data/indicator_catalog/v1/
DOMAIN_COUNT: 18
INDICATOR_COUNT: 420
RAW: 298
METADATA: 85
EVENT: 7
CALCULATED: 30
CSV_DELIMITER: ;
HISTORY_STATUS: NOT_ASSERTED_BY_DEFINITION_CATALOGUE
MIGRATION: 016_COUNTRY_INDICATOR_CATALOG
```

## Preuves CI

```text
COUNTRY_INDICATOR_CATALOG_RUN: {COUNTRY_RUN} — SUCCESS
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
MIGRATION_RUNNER_RUN: {MIGRATION_RUN} — SUCCESS
POSTGRESQL_16_DOUBLE_APPLY: SUCCESS
POSTGRESQL_16_RUNTIME_ASSERTIONS: SUCCESS
ADOPTION_WITHOUT_LEDGER: SUCCESS
```

## Limites conservées

Aucun historique pays/fonds, NAV, AUM, dividende ou portefeuille n’est chargé par cette boucle. Aucun PostgreSQL persistant, stockage objet permanent, catalogue officiel Openfunds, mapping officiel, API, UI, merge ou déploiement n’est réalisé.

## Prochaine tâche candidate

```text
NEXT_CANDIDATE: OF-SOURCE-002
TITLE: Compléter les institutions des 54 pays
INITIAL_MODE: READ_ONLY_AUDIT
WRITE_GATE: VERIFY_COVERAGE_AND_EVIDENCE_FIRST
OF-MAP-001: BLOCKED_OFFICIAL_OPENFUNDS_CATALOGUE_UNAVAILABLE
```
""")

    write("LOOP_STATE.md", f"""
# État de la boucle

```text
LOOP_ID: OF-LOOP-DATA-003
TASK_ID: OF-DATA-003
LOOP_TYPE: COUNTRY_INDICATOR_CATALOG
STATUS: VERIFIED_COMPLETE
START_HEAD: {LOOP_START_HEAD}
VALIDATED_TECHNICAL_HEAD: {TECHNICAL_HEAD}
BRANCH: architecture/africafunds-country-indicators-v0.1
SCOPE: D00_D17_DEFINITION_CATALOG
PRODUCTION_DEPLOYED: NO
REAL_COUNTRY_DATA_LOADED: NO
POSTGRESQL_VALIDATION: EPHEMERAL_CI_ONLY
```

## Résultat

Le paquet JSON `data/indicator_catalog/v1/` est l’autorité d’authoring v1 des 18 domaines et 420 définitions D00–D17. Les sept Markdown historiques restent des sources de bootstrap/audit. Les sorties JSON, CSV `;`, Markdown et SQL sont déterministes ; la migration `016` matérialise uniquement les définitions sous `ref.*`.

## Preuves

```text
COUNTRY_INDICATOR_CATALOG_RUN: {COUNTRY_RUN} — SUCCESS
MIGRATION_RUNNER_RUN: {MIGRATION_RUN} — SUCCESS
PYTHON: 3.11 SUCCESS / 3.12 SUCCESS
POSTGRESQL_16_DOUBLE_APPLY: SUCCESS
RUNTIME: 18 DOMAINS / 420 DEFINITIONS
```

## Sortie

Boucle fermée. La prochaine boucle candidate est `OF-SOURCE-002`, à démarrer par un audit en lecture seule. `OF-MAP-001` reste bloqué faute de catalogue Openfunds officiel versionné/licencié.
""")

    write("CURRENT_ITERATION.md", f"""
# Itération courante

```text
LOOP_ID: OF-LOOP-DATA-003
ITERATION: 001
TASK_ID: OF-DATA-003
STATUS: VERIFIED_COMPLETE
START_HEAD: {LOOP_START_HEAD}
VALIDATED_TECHNICAL_HEAD: {TECHNICAL_HEAD}
DATE: 2026-08-11
```

## Hypothèse et verdict

**Hypothèse :** les 420 définitions D00–D17 peuvent être centralisées sans réécrire leurs sources, inventer les champs absents ni transformer des exigences de couverture en historiques chargés.

**Verdict : confirmé.** Un paquet JSON gouverné unique développe 18 domaines / 420 codes, conserve la provenance legacy, sépare `source_nature` de `canonical_nature`, génère quatre vues déterministes et alimente une migration additive testée sur PostgreSQL 16.

## Corrections de boucle

- TDD RED/GREEN pour le parseur, le paquet authoring, la classification, les sorties et la migration ;
- correction de la mutation CI du paquet d’authoring avant gel du manifeste ;
- correction d’un test funds qui supposait à tort que la migration `015` devait être la dernière migration globale ;
- aucun force-push ni réécriture d’historique.

## Limite

Cette itération ne charge aucune donnée réelle et ne valide ni disponibilité pays, ni historique complet, ni mapping Openfunds, ni calcul actif, ni production.
""")

    write("NEXT_ACTION.md", """
# Prochaine action autorisée

```text
CURRENT_LOOP: OF-LOOP-DATA-003_COMPLETED
CURRENT_TASK: OF-DATA-003_VERIFIED_COMPLETE
NEXT_CANDIDATE: OF-SOURCE-002
STATUS: READY_FOR_READ_ONLY_AUDIT
WRITE_GATE: VERIFY_COVERAGE_AND_EVIDENCE_FIRST
```

## Phase candidate

Compléter les institutions des 54 pays sans confondre organisation connue, rôle supposé, endpoint identifié, endpoint vérifié et collecte testée.

## Audit préalable obligatoire

1. résoudre dynamiquement le HEAD ;
2. inventorier les 54 pays et les rôles institutionnels attendus ;
3. comparer `ORGANIZATIONS`, `ORGANIZATION_SCOPE_ROLES`, `SOURCE_ENDPOINTS` et les mappings ;
4. mesurer la couverture par pays et rôle ;
5. séparer `VERIFIED`, `SOURCE_IDENTIFIED`, `PENDING`, `NOT_PUBLISHED` et `NOT_APPLICABLE` ;
6. ne promouvoir aucune URL ou institution sans preuve officielle ;
7. définir une allowlist avant toute écriture.

## Gate externe maintenu

`OF-MAP-001` reste bloqué tant qu’un catalogue Openfunds officiel, versionné, licencié et archivé n’est pas disponible. Aucun identifiant Openfunds ne doit être inventé.

## Interdictions maintenues

Ne pas importer d’historique réel, modifier la PR nº 2, fusionner/retargeter la PR nº 1, travailler sur `main`, créer branche/PR, activer WTI/WTI Bench ou déployer sans porte explicite.
""")

    write("HANDOFF.md", f"""
# Handoff Loop Engineering

```text
LOOP_ID: OF-LOOP-DATA-003
TASK_ID: OF-DATA-003
STATUS: VERIFIED_COMPLETE
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
START_HEAD: {LOOP_START_HEAD}
VALIDATED_TECHNICAL_HEAD: {TECHNICAL_HEAD}
CURRENT_HEAD_POLICY: RESOLVE_DYNAMICALLY
NEXT_CANDIDATE: OF-SOURCE-002
```

## Résultat canonique

```text
AUTHORING_SOURCE: data/indicator_catalog/v1/
DOMAINS: 18
DEFINITIONS: 420
RAW: 298
METADATA: 85
EVENT: 7
CALCULATED: 30
MIGRATION: 016_COUNTRY_INDICATOR_CATALOG
HISTORY_LOADED: NO
PRODUCTION_DEPLOYED: NO
```

## Entrées principales

- `docs/01_ARCHITECTURE/ADR-032_COUNTRY_INDICATOR_CATALOG_MIRROR_FIRST.md` ;
- `docs/04_DATA_GOVERNANCE/COUNTRY_INDICATOR_CATALOG_V1.md` ;
- `data/indicator_catalog/v1/` ;
- `data/indicator_catalog/COUNTRY_INDICATOR_CATALOG_MANIFEST_V1.json` ;
- `data/indicator_catalog/country-indicator-catalog-v1.schema.json` ;
- `scripts/country_indicator_catalog.py` ;
- `scripts/generate_country_indicator_catalog.py` ;
- `tests/test_country_indicator_catalog.py` ;
- `schemas/reference/016_country_indicator_catalog.sql` ;
- `docs/00_PROJECT/OF_DATA_003_COMPLETION_20260811.md`.

## Preuves finales

```text
COUNTRY_INDICATOR_CATALOG_RUN: {COUNTRY_RUN} — SUCCESS
MIGRATION_RUNNER_RUN: {MIGRATION_RUN} — SUCCESS
POSTGRESQL_16_DOUBLE_APPLY: SUCCESS
POSTGRESQL_16_ADOPTION_WITHOUT_LEDGER: SUCCESS
```

## Point de reprise

Résoudre le HEAD dynamiquement, vérifier la clôture documentaire puis commencer `OF-SOURCE-002` uniquement par un audit de couverture institutionnelle en lecture seule. Ne pas transformer une source identifiée en source vérifiée, ni une définition en historique chargé.
""")


def update_work_log() -> None:
    append_once(
        "WORK_LOG.md",
        "## Boucle OF-LOOP-DATA-003 — 2026-08-11",
        f"""
---

## Boucle OF-LOOP-DATA-003 — 2026-08-11

```text
TASK_ID: OF-DATA-003
START_HEAD: {LOOP_START_HEAD}
VALIDATED_TECHNICAL_HEAD: {TECHNICAL_HEAD}
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
- `{TECHNICAL_HEAD}` : invariant fonds découplé de la position globale de migration.

### Validation

```text
COUNTRY_INDICATOR_CATALOG_RUN: {COUNTRY_RUN} — SUCCESS
MIGRATION_RUNNER_RUN: {MIGRATION_RUN} — SUCCESS
```

Le runner PostgreSQL 16 applique deux fois les 16 migrations, vérifie 18 domaines / 420 définitions, les comptes 298/85/7/30, l’absence de statut historique inventé et le scénario d’adoption sans ledger.

### Sortie

`OF-DATA-003` est fermé. Aucun historique réel, mapping officiel Openfunds, merge, déploiement, nouvelle branche ou nouvelle PR n’a été réalisé. La prochaine tâche candidate est `OF-SOURCE-002` en audit lecture seule.
""",
    )


def create_new_docs() -> None:
    write("docs/01_ARCHITECTURE/ADR-032_COUNTRY_INDICATOR_CATALOG_MIRROR_FIRST.md", """
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
""")

    write("docs/04_DATA_GOVERNANCE/COUNTRY_INDICATOR_CATALOG_V1.md", f"""
# Country Indicator Catalogue v1 — Gouvernance

```text
TASK: OF-DATA-003
STATUS: VERIFIED_COMPLETE
AUTHORING_AUTHORITY: data/indicator_catalog/v1/
DOMAIN_COUNT: 18
INDICATOR_COUNT: 420
CLASSIFICATION_DECISION: OF-DATA-003-A
```

## Autorité et fidélité

Les sept Markdown sous `docs/04_DATA_GOVERNANCE/indicator_catalog/` sont les sources historiques de bootstrap/audit. Le paquet JSON v1 est l’autorité d’authoring. Les sorties sous `build/indicator_catalog/` sont dérivées et ne doivent pas être éditées comme une deuxième source de vérité.

## Répartition gouvernée

| Nature canonique | Nombre |
|---|---:|
| RAW | 298 |
| METADATA | 85 |
| EVENT | 7 |
| CALCULATED | 30 |
| **Total** | **420** |

La nature canonique est une décision de gouvernance séparée de `source_nature`.

## Contrats essentiels

- code canonique unique `Dnn.CODE` ;
- domaine D00–D17 ;
- libellé source français conservé ;
- absence de traduction non sourcée = `null` / `NOT_AUTHORED` ;
- définition source absente = `null` / `NOT_AUTHORED` ;
- fréquence, unité, source préférée, usages, benchmark, priorité et horizon cible conservés quand présents ;
- provenance par fichier legacy et SHA-256 ;
- statuts `definition`, `source_mapping`, `collection_spec`, `collection_test`, `history`, `calculation` indépendants ;
- `history_status` ne peut pas être promu par le catalogue de définitions.

## Génération et contrôle

```text
python scripts/generate_country_indicator_catalog.py --check-authoring
python scripts/generate_country_indicator_catalog.py --generate-derived
python scripts/generate_country_indicator_catalog.py --check-derived
python -m unittest -v tests.test_country_indicator_catalog
python scripts/generate_country_indicator_catalog.py --check \
  --source data/indicator_catalog/v1/00_metadata.json \
  --output schemas/reference/016_country_indicator_catalog.sql
```

Les sorties générées sont :

```text
build/indicator_catalog/COUNTRY_INDICATOR_CATALOG_V1.json
build/indicator_catalog/COUNTRY_INDICATOR_CATALOG_V1.csv
build/indicator_catalog/COUNTRY_INDICATOR_CATALOG_V1.md
build/indicator_catalog/COUNTRY_INDICATOR_CATALOG_V1.sql
```

Le manifeste commité est `data/indicator_catalog/COUNTRY_INDICATOR_CATALOG_MANIFEST_V1.json`. Le SQL frozen commité est `schemas/reference/016_country_indicator_catalog.sql`.

## Empreintes v1

```text
JSON: 1d19a2d612b4d34e6d83f96100c6b073acd3791f96418aaca7cf1a097ad58184
CSV: 7d0f549684bdf91164ad98b7d912510784c8a2f07b4a8d0d86ecdc3e4a34ee94
MARKDOWN: a2044c0ebff3ba90a839eb7ee30ff388952b53a8380360f7cf7d8d15bb3f4730
SQL: fa00298ca8371cf1f95e20d809cc82b97774ea3cf0bf8fa2945cf269d0982432
```

## Preuves

```text
COUNTRY_INDICATOR_CATALOG_RUN: {COUNTRY_RUN} — SUCCESS
MIGRATION_RUNNER_RUN: {MIGRATION_RUN} — SUCCESS
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
POSTGRESQL_16_DOUBLE_APPLY: SUCCESS
```

## Limites

Cette v1 centralise des définitions, pas des historiques. Elle ne prouve ni disponibilité d’une série pour un pays, ni endpoint vérifié, ni collecte testée, ni couverture complète, ni produit analytique actif. Aucun identifiant Openfunds officiel n’est inventé.
""")

    write("docs/00_PROJECT/OF_DATA_003_COMPLETION_20260811.md", f"""
# OF-DATA-003 — Rapport de clôture du catalogue D00–D17

```text
DATE: 2026-08-11
TASK_ID: OF-DATA-003
LOOP_ID: OF-LOOP-DATA-003
STATUS: VERIFIED_COMPLETE
BRANCH: architecture/africafunds-country-indicators-v0.1
START_HEAD: {LOOP_START_HEAD}
VALIDATED_TECHNICAL_HEAD: {TECHNICAL_HEAD}
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
2. un test Fund/SubFund/ShareClass supposait que `015` devait être la dernière migration globale. `{TECHNICAL_HEAD}` vérifie désormais le vrai invariant : `015` reste l’unique migration canonique du domaine `fund`, indépendamment des migrations de référence ultérieures.

## 9. Preuves finales

### Country Indicator Catalog

```text
RUN_ID: {COUNTRY_RUN}
CONCLUSION: SUCCESS
PYTHON_3_11: SUCCESS
PYTHON_3_12: SUCCESS
```

Les deux jobs valident le paquet commité, régénèrent les quatre sorties, exécutent les tests contractuels, vérifient l’identité octet pour octet et publient des artefacts de revue.

### Governed Migration Runner

```text
RUN_ID: {MIGRATION_RUN}
HEAD_SHA: {TECHNICAL_HEAD}
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
""")


def verify() -> None:
    for path in EXPECTED_DOC_PATHS:
        if not (ROOT / path).is_file():
            raise RuntimeError(f"missing expected closeout file: {path}")
    status = read("STATUS.md")
    for token in ("OF-DATA-003   VERIFIED_COMPLETE", "DOMAIN_COUNT: 18", "INDICATOR_COUNT: 420"):
        if token not in status:
            raise RuntimeError(f"STATUS missing {token}")
    next_action = read("NEXT_ACTION.md")
    if "NEXT_CANDIDATE: OF-SOURCE-002" not in next_action:
        raise RuntimeError("NEXT_ACTION candidate drift")
    if "OF-DATA-003 — Centraliser" not in read("TODO.md") or "**Statut :** TERMINE" not in read("TODO.md"):
        raise RuntimeError("TODO closeout missing")
    if "ADR-032 — CATALOGUE D00-D17 MIRROR-FIRST" not in read("DECISIONS.md"):
        raise RuntimeError("DECISIONS missing ADR-032")
    plan = read("docs/superpowers/plans/2026-08-11-of-data-003-country-indicator-catalog.md")
    if "- [ ]" in plan:
        raise RuntimeError("implementation plan still contains unchecked steps")


def main() -> None:
    update_todo()
    update_suivi()
    update_changelog()
    update_decisions()
    update_framework()
    update_plan()
    write_current_state_docs()
    update_work_log()
    create_new_docs()
    verify()
    print("OF-DATA-003 documentation closeout prepared and verified")
    for path in EXPECTED_DOC_PATHS:
        print(path)


if __name__ == "__main__":
    main()
