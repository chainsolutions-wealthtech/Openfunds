# Politique de migrations

Autorité : ADR-028, `migrations/manifest.json` et `migrations/README.md`. Les migrations sont ordonnées, forward-only, atomiques avec leur ledger et contrôlées par SHA-256. Aucun fichier appliqué ne doit être modifié. Blocker ouvert : la migration générée 012 n’est pas encore figée historiquement. Ce document ne corrige ni n’autorise ce changement.
