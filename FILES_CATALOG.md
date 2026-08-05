# Catalogue des fichiers Loop Engineering

```text
TASK_ID: OF-DOC-003
LOOP_ID: OF-LOOP-DOC-003
KIT_VERSION: 1.0.0
KIT_MARKDOWN_PATHS: 176
CANONICAL_HISTORICAL_DOCUMENTS_PRESERVED: YES
```

## Catalogue par domaine

| Domaine | Chemins | Fonction |
|---|---:|---|
| Racine et mémoire | 47 | contexte, statut, boucle, sécurité, backlog et handoff |
| `.github` Markdown | 6 | templates et adaptateur Copilot |
| Gouvernance | 11 | décisions, ownership, exceptions et critères |
| Produit | 8 | vision, use cases, validation et release |
| Architecture | 10 | index, flux, composants, contrats et dette |
| Développement | 12 | Git, code, dépendances, migrations et revue |
| Qualité | 12 | tests, gates, non-régression et validation |
| Livraison | 10 | build, CI, environnements, release et rollback |
| Opérations | 10 | runbooks, monitoring, incidents et sauvegardes |
| Sécurité | 7 | accès, secrets, menaces et vulnérabilités |
| Boucle | 14 | itérations, dérive, expériences, leçons et arrêt |
| IA | 11 | gouvernance, outils, autonomie et handoff |
| Modèles | 9 | tâches, PR, specs, incidents et rétrospectives |
| Optionnels | 13 | données, conformité, production et services tiers |
| ADR | 2 | index et modèle de décision |

## Autorité

La liste chemin par chemin, sa correspondance, son action, son canonique et son statut sont dans `DOCUMENT_INTEGRATION_MATRIX.md`. Ce catalogue ne duplique pas ces 176 lignes.

## Règles

- les documents racine historiques restent canoniques ;
- les chemins redondants sont des index ou adaptateurs ;
- `CONDITIONAL_NOT_ACTIVE` ne prouve aucune capacité ;
- aucun fichier ne doit rester vide ;
- toute création, suppression ou changement d’autorité met à jour ce catalogue, `MANIFEST.md` et la matrice.
