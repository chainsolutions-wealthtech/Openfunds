# Gestion des secrets

Secrets uniquement dans un gestionnaire ou les secrets GitHub, jamais dans Git, logs, captures ou fichiers de configuration. Rotation après exposition, portée minimale, environnements séparés et audit des accès. Les variables `OPENFUNDS_DATABASE_URL`, `DATABASE_URL` et `PGPASSWORD` sont fournies à l’exécution et masquées.
