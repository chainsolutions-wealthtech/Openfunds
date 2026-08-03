# CHANGELOG OPENFUNDS

Toutes les modifications importantes du projet sont consignées ici. Les commits Git restent la source détaillée des changements fichier par fichier.

## [UNRELEASED]

### A décider

- source de vérité des référentiels CSV/SQL ;
- modèle canonique d'endpoint ;
- traitement des dates métier inconnues ;
- stratégie de migrations ;
- modèle final Fund/SubFund/ShareClass ;
- format maître du dictionnaire ;
- version officielle openfunds à intégrer.

### Limites connues

- PR #1 non fusionnée ;
- branche `main` minimale ;
- PostgreSQL persistant non configuré ;
- stockage brut permanent absent ;
- historique FX limité à un snapshot validé par zone ;
- mapping openfunds absent ;
- API, catégories, WTI et WTI Bench non implémentés.

## [2026-08-03] — CONSOLIDATION DOCUMENTAIRE

### Ajouté

- audit complet des 95 fichiers de la branche ;
- matrice de 45 écarts entre conversation, décisions et dépôt ;
- `TODO.md` avec tâches `OF-*`, dépendances et critères d'acceptation ;
- `SUIVI.md` avec réalisations, décisions, risques et point exact de reprise ;
- `DECISIONS.md` avec ADR-001 à ADR-025 ;
- `ARCHITECTURE.md` ;
- `DATA_MODEL.md` ;
- `DATA_DICTIONARY.md` ;
- `OPENFUNDS_MAPPING.md` ;
- `GOVERNANCE.md` ;
- `QUALITY_RULES.md` ;
- `SOURCE_REGISTRY.md` ;
- `ROADMAP.md` ;
- `CHANGELOG.md`.

### Modifié

- remplacement du README minimal par un guide complet ;
- documentation des commandes réellement utilisées par les workflows ;
- distinction explicite entre architecture, référentiel, mapping, collecte, historique, calcul et production.

### Corrigé

- clarification que les 420 définitions ne sont pas 420 séries historiques par pays ;
- clarification que les pilotes FX sont `COLLECTION_TESTED` et non des historiques complets ;
- identification des divergences CSV/SQL et des modèles d'endpoints concurrents ;
- documentation transparente de la PR #3 accidentelle, immédiatement fermée sans fusion ni modification de fichier.

## [2026-08-03] — PIPELINE QUOTIDIEN FX

### Ajouté

- `pipelines/fx_daily.py` ;
- orchestration BCEAO_XOF et BEAC_XAF ;
- manifeste de couverture par source ;
- persistance PostgreSQL optionnelle ;
- workflow `Daily Africa FX Staging` ;
- politique de staging et persistance ;
- tests unitaires de l'orchestrateur.

### Validé

- collecte double source ;
- quatre paires canoniques : XOF_EUR, XOF_USD, XAF_EUR, XAF_USD ;
- statut honnête `STAGING_ONLY_DATABASE_NOT_CONFIGURED` sans secret de production ;
- artefacts temporaires GitHub Actions.

## [2026-08-03] — BEAC FX

### Ajouté

- collecteur BEAC ;
- parsing des blocs `div.taux_de_change` ;
- fallback tableau ;
- profil de chargement `BEAC_XAF` ;
- seed CEMAC/BEAC ;
- migration parseur 0.2.0 ;
- migration de validation live ;
- workflow live et fixture réaliste.

### Validé

- 13 paires observées ;
- date de valeur ;
- SHA256 ;
- buy et sell distincts ;
- XAF_EUR et XAF_USD calculés ;
- six observations PostgreSQL ;
- double chargement idempotent ;
- absence de mélange XOF/XAF.

### Corrigé

- adaptation du parseur après inspection de l'artefact réel ;
- correction documentaire du taux XAF_USD.

## [2026-08-03] — BCEAO FX

### Ajouté

- collecteur BCEAO ;
- parsing HTML, dates françaises et nombres localisés ;
- transformation canonique XOF ;
- seed UEMOA/BCEAO ;
- workflow live ;
- preuve de collecte.

### Validé

- date de valeur ;
- SHA256 ;
- EUR/USD présents ;
- XOF_EUR et XOF_USD ;
- chargement PostgreSQL idempotent.

## [2026-08-03] — CHARGEUR ET SCHEMAS DE SOURCES

### Ajouté

- chargeur PostgreSQL multi-profils ;
- tables de runs, artefacts, séries et spécifications ;
- lignée FX observée/calculée ;
- vues d'observations courantes ;
- tests PostgreSQL 16 ;
- migration de réconciliation des endpoints.

### Corrigé

- suppression robuste d'une ancienne contrainte unique tronquée par PostgreSQL ;
- compatibilité des deux ordres de création 003/004 ;
- endpoint `PENDING` autorisé sans URL vérifiée ;
- conflits de types et de colonnes détectés par les tests.

## [2026-08-03] — REFERENTIELS AFRICAINS

### Ajouté

- 54 pays ;
- 1 continent et 5 régions ;
- UEMOA, CEMAC et CMA ;
- 266 relations pays ;
- 44 devises ;
- 84 paires locale→EUR/USD ;
- organisations, rôles et périmètres initiaux ;
- endpoints, mappings, séries et spécifications initiaux ;
- cadre D00-D17 ;
- pilotes Maroc et Tunisie ;
- modèle relationnel pays-indicateur.

### Documentation

- règles de conversion quotidienne ;
- modèles organisations/sources ;
- workflow de collecte ;
- plans de benchmarks et règles qualité.

## [2026-07-31] — FONDATION ARCHITECTURALE

### Décidé

- modèle canonique interne plus riche qu'openfunds ;
- PostgreSQL comme source de vérité ;
- API-first ;
- Atomic Design comme présentation ;
- historisation bitemporelle ;
- provenance complète ;
- séparation raw/validation/canonique/calcul/API/UI ;
- quatre rôles de référence ;
- WTI distinct du WTI Bench ;
- niveaux national, régional et Afrique.
