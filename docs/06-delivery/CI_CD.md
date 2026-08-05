# CI/CD

La CI valide les changements selon les chemins concernés : Python, PostgreSQL, collecteurs live, registres et migrations. Chaque run est rattaché à un SHA. Les échecs externes sont distingués des régressions. Aucun CD ni déploiement production n’est configuré ou autorisé par OF-DOC-003. Toute future promotion exige environnement, approbation, secrets et rollback.
