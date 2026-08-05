# GOUVERNANCE DU PROJET OPENFUNDS

## 1. OBJECTIF

La gouvernance garantit que les données, schémas, méthodologies et documents peuvent évoluer sans perte d'historique, sans source de vérité concurrente et sans présentation trompeuse de l'avancement.

## 2. REFERENCES PERMANENTES

| Document | Fonction |
|---|---|
| `README.md` | comprendre le projet et son état réel |
| `TODO.md` | connaître les tâches et critères d'acceptation |
| `SUIVI.md` | reprendre le travail au point exact |
| `DECISIONS.md` | connaître les décisions et propositions |
| `DATA_DICTIONARY.md` | gouverner les champs |
| `OPENFUNDS_MAPPING.md` | gouverner les correspondances externes |
| `CHANGELOG.md` | suivre les changements |

## 3. ROLES DE GOUVERNANCE

Les rôles ci-dessous sont fonctionnels ; une même personne peut en exercer plusieurs au début du projet.

- **Product owner :** valide le périmètre et les priorités.
- **Data owner :** approuve la définition et l'usage d'un domaine.
- **Data steward :** tient le dictionnaire, les référentiels et la qualité.
- **Source reviewer :** vérifie l'autorité, l'URL, la série et la licence.
- **Methodology owner :** valide les transformations, indices et ratios.
- **Data engineer :** implémente collecte, transformation et chargement.
- **Quality reviewer :** contrôle règles, anomalies et preuves.
- **Release reviewer :** vérifie migrations, tests, documentation et non-régression.

Aucun rôle humain nominatif n'est imposé dans le dépôt tant que l'organisation n'est pas formalisée.

## 4. CYCLE DE VIE D'UNE DONNEE

```text
PROPOSED
→ SOURCE_IDENTIFIED
→ URL_LINKED
→ SPECIFICATION_DRAFTED
→ COLLECTION_TESTED
→ PARTIAL_HISTORY_LOADED
→ COMPLETE_HISTORY_LOADED
→ VALIDATED_FOR_PUBLICATION
```

Etats alternatifs :

```text
NOT_PUBLISHED
NOT_APPLICABLE
DISCONTINUED
REPLACED
REJECTED
BLOCKED
```

Une donnée ne change de statut qu'avec une preuve et des critères vérifiables.

## 5. CYCLE DE VIE D'UNE DECISION

```text
PROPOSE
→ ANALYSE D'IMPACT
→ ALTERNATIVES
→ VALIDATION
→ ADR ACCEPTE
→ IMPLEMENTATION
→ TEST
→ DOCUMENTATION
```

Un changement structurant doit :

1. citer la décision existante ;
2. expliquer le problème ;
3. proposer les alternatives ;
4. documenter l'impact sur données, API et migrations ;
5. obtenir une validation ;
6. mettre à jour `DECISIONS.md`.

## 6. GOUVERNANCE DES SOURCES

Pour chaque source officielle :

- organisation distincte de l'endpoint ;
- rôle et périmètre explicites ;
- URL vérifiée et datée ;
- conditions d'accès et licence documentées ;
- série fournisseur identifiée ;
- fréquence et unité réelles ;
- spécification de collecte versionnée ;
- artefact brut hashé ;
- run et parseur identifiables ;
- historique et ruptures documentés.

Une page d'accueil ne vaut pas automatiquement endpoint de série.

## 7. GOUVERNANCE DES REFERENTIELS

- une seule représentation maître doit être choisie ;
- les exports CSV/SQL/Markdown doivent être générés ou contrôlés ;
- les identifiants restent stables ;
- les lignes remplacées sont marquées, pas supprimées ;
- les dates inconnues ne sont pas fabriquées ;
- les valeurs autorisées sont versionnées ;
- chaque modification porte une justification.

Le choix du registre maître relève de `ADR-021`.

## 8. GOUVERNANCE DES MIGRATIONS

Avant production :

- migration numérotée et ordonnée ;
- préconditions explicites ;
- aucune destruction implicite ;
- conservation de la donnée existante ;
- test depuis base vide et base existante ;
- procédure de correction ;
- version de schéma enregistrée ;
- séparation entre migration et collecte.

Les fichiers SQL actuels mélangent propositions, schémas, seeds et migrations ; cette dette est suivie par `OF-ARCH-004`.

## 9. GOUVERNANCE GIT ET REVUE

- aucune modification directe de `main` ;
- branche dédiée ;
- PR en brouillon tant que les décisions critiques restent ouvertes ;
- commits ciblés et descriptifs ;
- tests avant revue ;
- aucune exposition de secret ;
- pas de déploiement implicite ;
- documentation mise à jour avec le code.

La PR #1 reste volontairement en brouillon jusqu'à la consolidation et la revue.

## 10. DOCUMENTATION OBLIGATOIRE APRES INTERVENTION

Mettre à jour au minimum :

- la tâche `OF-*` dans `TODO.md` ;
- les réalisations et le point de reprise dans `SUIVI.md` ;
- les ADR concernées ;
- `CHANGELOG.md` ;
- le dictionnaire ou mapping lorsque le modèle change ;
- les preuves de test lorsque la collecte ou un calcul change.

## 11. DEFINITION DE TERMINE

Un composant est terminé uniquement si :

- sa portée est définie ;
- les données ou comportements existent réellement ;
- les tests couvrent les critères ;
- la provenance est disponible ;
- les limites sont documentées ;
- les tâches et décisions sont mises à jour ;
- aucun statut plus avancé n'est revendiqué sans preuve.
