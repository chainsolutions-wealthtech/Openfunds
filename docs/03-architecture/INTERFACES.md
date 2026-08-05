# Interfaces internes

Les interfaces séparent collecteurs, normalisation, validation, loaders, calculs et consommateurs. Une interface documente types, identifiants, temporalité, erreurs, idempotence et provenance. Les fichiers fournisseurs ne doivent pas devenir des contrats internes. Les API et view models futurs consommeront les ressources canoniques, jamais les tables ou fichiers bruts directement.
