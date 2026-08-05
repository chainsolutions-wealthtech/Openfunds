# MATRICE DES ECARTS — CONVERSATION, DECISIONS ET DEPOT

## 1. REGLE DE LECTURE

Cette matrice confronte les demandes et décisions fonctionnelles exprimées pour Openfunds à l'état réellement observé dans la branche `architecture/africafunds-country-indicators-v0.1`.

Statuts utilisés :

- `VALIDE` : décision formellement acceptée ;
- `DOCUMENTE` : décrit dans le dépôt sans implémentation complète ;
- `PARTIELLEMENT_IMPLEMENTE` : une partie fonctionnelle est exécutable ;
- `IMPLEMENTE_TESTE` : code exécuté et contrôlé ;
- `ABSENT` : aucun livrable opérationnel correspondant ;
- `A_ARBITRER` : décision structurante encore nécessaire.

## 2. MATRICE

| ID | Sujet | Demande ou décision issue du projet | Etat observé dans le dépôt | Ecart | Action nécessaire | Priorité |
|---|---|---|---|---|---|---|
| GAP-001 | Modèle canonique | Construire un modèle interne plus riche qu'Openfunds | Architecture hybride et modèles de domaine documentés | Le modèle complet n'est pas encore migré ni peuplé | Stabiliser les domaines, identifiants et migrations | P0 |
| GAP-002 | Rôle d'Openfunds | Utiliser Openfunds comme couche de mapping, pas comme schéma unique | Principe accepté dans l'ADR | Aucun mapping officiel champ par champ | Créer `OPENFUNDS_MAPPING.md` et un fichier structuré versionné | P0 |
| GAP-003 | Fonds / compartiment / classe | Séparer Fund, SubFund et ShareClass | SQL actuel contient Fund et ShareClass | Objet SubFund incomplet ou absent | Arbitrer la structure juridique puis migrer | P0 |
| GAP-004 | Identifiants canoniques | Identifiant stable pour chaque objet | UUID et codes canoniques présents dans plusieurs schémas | Politique globale d'identifiant non centralisée | Formaliser les namespaces, règles et immutabilité | P1 |
| GAP-005 | Alias et noms historiques | Conserver anciens noms et alias | Décision documentée, source tunisienne analysée | Pas de tables canoniques complètes d'alias fonds | Ajouter identité, dénomination et alias historisés | P1 |
| GAP-006 | Evénements fonds | Gérer fusion, absorption, scission, liquidation, transfert, changement de gestionnaire | Besoin documenté dans la conversation | Aucun modèle opérationnel complet dans la branche | Créer modèle événementiel fonds et tests | P1 |
| GAP-007 | Historisation | Conserver validité métier et connaissance système | ADR bitemporel accepté | Application inégale selon les schémas | Définir convention temporelle commune | P0 |
| GAP-008 | Provenance cellule/page | Tracer jusqu'au fichier, feuille, ligne, cellule et page PDF | Modèle pays propose source_document et extraction_record | Aucun pipeline fonds ne le remplit dans ce dépôt | Créer modèle commun et intégration pays | P1 |
| GAP-009 | Donnée brute | Ne jamais écraser les fichiers et valeurs sources | Principe accepté, artefacts FX hashés | Stockage permanent absent | Configurer object storage immuable | P0 |
| GAP-010 | Corrections | Corriger sans supprimer l'ancienne observation | Chargeur FX versionne et supersède | Non généralisé aux autres domaines | Créer politique de révision commune | P1 |
| GAP-011 | Pays africains | Couvrir 54 pays et 5 régions | Référentiels présents | Validation institutionnelle et historique incomplète | Vérifier officiellement chaque relation | P1 |
| GAP-012 | UEMOA/CEMAC | Conserver géographie et zone de marché en parallèle | Modèle et relations présents | Certaines preuves restent `PENDING` dans les CSV | Réconcilier CSV et seeds SQL | P0 |
| GAP-013 | Devises | Produire local, EUR et USD | 44 devises et 84 paires requises | Routes officielles absentes pour la majorité des devises | Peupler sources FX et fallbacks | P1 |
| GAP-014 | BCEAO FX | Collecter et transformer XOF | Implémenté et testé live | Historique durable absent | Activer persistance puis backfill | P1 |
| GAP-015 | BEAC FX | Collecter et transformer XAF | Implémenté et testé live | Historique durable absent | Activer persistance puis backfill | P1 |
| GAP-016 | Organisations | Banques centrales, bourses, régulateurs, statistiques, finances et dette par pays | 40 organisations et 70 rôles de portée | Couverture limitée à quelques pays et zones | Compléter les 54 pays | P1 |
| GAP-017 | Endpoints | URL, API et fichiers officiels vérifiés | 43 endpoints de travail | Plusieurs sont génériques ou `PENDING` | Vérifier, dater et versionner | P1 |
| GAP-018 | Catalogue indicateurs | Référentiel complet d'indicateurs pays | 18 domaines et environ 420 définitions documentées | Pas de catalogue machine-readable complet | Centraliser les 420 définitions | P0 |
| GAP-019 | Mapping pays-indicateur-source | Relier chaque point de donnée à son fournisseur | 55 mappings initiaux | Loin de la couverture 54 × 420 | Générer l'applicabilité puis renseigner progressivement | P1 |
| GAP-020 | Séries fournisseurs | Identifier code, fréquence, unité et historique | 50 lignes initiales | Codes et URL exacts souvent vides | Vérifier chaque série | P1 |
| GAP-021 | Spécifications collecte | Rendre chaque import reproductible | 17 spécifications/templates | Seules BCEAO/BEAC FX sont exécutables | Implémenter source par source | P1 |
| GAP-022 | Base Tunisie | Intégrer la base CMF riche et auditable | Analyse documentaire présente | Fichier SQLite et chargeur absents du dépôt | Importer par processus gouverné et conserver la source | P1 |
| GAP-023 | Nigeria SEC | Fiabiliser les archives hebdomadaires, fonds, VL, AUM et événements | Besoin connu et mappings SEC présents | Extracteur complet Nigeria absent | Créer projet d'ingestion auditable | P1 |
| GAP-024 | Taxonomie fonds | Classes Actions, Obligations, Diversifié, Monétaire et sous-classes | Modèle accepté et SQL de brouillon | Référentiels non seedés | Valider puis peupler | P1 |
| GAP-025 | Catégories multi-niveaux | Générer national, régional et Afrique | Modèle documenté | Aucune catégorie générée | Créer générateur déterministe et tests | P2 |
| GAP-026 | Bloc de quatre références | Primary Market Index, Secondary Market Index, WTI, WTI Bench | Décision acceptée | Aucun bloc peuplé | Générer après validation taxonomique | P2 |
| GAP-027 | WTI | Performance moyenne observée des fonds éligibles | Méthode documentée | Aucun moteur de calcul | Implémenter après historique NAV fiable | P2 |
| GAP-028 | WTI Bench | Benchmark indépendant, versionné et réplicable | Principes et premières allocations documentés | Méthodes monétaires/flexibles incomplètes | Produire méthodologies par classe | P2 |
| GAP-029 | Indices obligataires | Courbes, instruments, coupons, pondérations et total return | Chaîne conceptuelle documentée | Pas d'univers instrument ni moteur | Modéliser titres et courbes | P2 |
| GAP-030 | Indices actions | All Share et Total Return officiels par marché | Plan de sources présent | Codes et historiques non confirmés | Vérifier chaque bourse | P2 |
| GAP-031 | Performances et risques | YTD, 1/3/5 ans, vol, drawdown, Sharpe, Sortino, alpha, beta, VaR | Besoins connus | Aucun moteur général dans ce dépôt | Définir calculs versionnés | P2 |
| GAP-032 | Portefeuille | Holdings, expositions, look-through | Ressources API envisagées | Modèle et ingestion absents | Concevoir domaine portefeuille | P3 |
| GAP-033 | Frais | Frais courants, gestion, souscription, performance | Famille fonctionnelle retenue | Dictionnaire et modèle incomplets | Ajouter entités et périodes de validité | P2 |
| GAP-034 | Réglementaire | EMT, EPT, EET, TPT et statuts | Vision fonctionnelle connue | Aucun mapping structuré | Concevoir après dictionnaire canonique | P3 |
| GAP-035 | ESG | Données et classifications ESG | Domaine envisagé | Non modélisé opérationnellement | Définir périmètre et standards | P3 |
| GAP-036 | Documents | Prospectus, KID, factsheets, décisions et bulletins | Besoin fort dans les pilotes | Modèle source générique seulement | Créer registre documentaire fonds | P1 |
| GAP-037 | API-first | Exposer toutes les ressources canoniques | ADR accepté | Aucun serveur ou OpenAPI | Définir contrats après stabilisation du modèle | P3 |
| GAP-038 | Atomic Design | Construire pages réutilisables à partir des API | Principes documentés | Aucun view model ni composant | Créer contrats UI après API | P3 |
| GAP-039 | Qualité | Unicité, conflits, fraîcheur, provenance et niveaux de confiance | Règles initiales présentes | Pas de moteur transversal | Créer règles exécutables et reporting | P1 |
| GAP-040 | Gouvernance | Décisions, validation, versionnement et non-régression | Plusieurs principes dispersés | Pas de fichiers racines de continuité avant consolidation | Maintenir README, TODO, SUIVI, DECISIONS, CHANGELOG | P0 |
| GAP-041 | Migrations | Déployer sans régression | Scripts numérotés et tests partiels | Pas de migration runner ni registre appliqué | Choisir et documenter la stratégie | P0 |
| GAP-042 | Persistance production | Historiser les observations quotidiennes | Chargeur testé sur PostgreSQL éphémère | Secret et base persistante absents | Configurer environnement de production | P1 |
| GAP-043 | Couverture historique | Distinguer collecte, historique partiel et complet | Statuts bien définis | Une seule date FX validée par zone | Créer vue couverture et backfill | P1 |
| GAP-044 | Sécurité | Ne pas exposer de secrets et contrôler les accès | Workflows utilisent des secrets optionnels | Modèle d'accès API absent | Définir politique avant API/production | P2 |
| GAP-045 | Documentation permanente | Permettre la reprise sans relire la conversation | Documentation de domaine riche | README/TODO/SUIVI absents ou incomplets avant ce travail | Finaliser et maintenir les documents racines | P0 |

## 3. ECARTS STRUCTURANTS NECESSITANT UNE VALIDATION

### 3.1 Fund / SubFund / ShareClass

Décision fonctionnelle attendue : séparation stricte.

Etat SQL actuel : `fund.fund` et `fund.share_class` seulement.

Validation nécessaire : définir si `fund.fund` désigne la structure légale racine, le compartiment investissable, ou les deux selon le type juridique. Une migration ne doit pas être écrite avant cet arbitrage.

### 3.2 Date métier inconnue

Décision existante : ne pas inventer `1900-01-01` ou une date de début artificielle.

Etat SQL : plusieurs tables imposent `valid_from NOT NULL`.

Validation nécessaire : introduire une distinction entre date d'effet connue, date de collecte et statut d'incertitude.

### 3.3 Registre canonique des sources

Etat actuel : CSV de gouvernance + seeds SQL opérationnels.

Validation nécessaire : déterminer si les CSV génèrent les seeds, si la base génère les exports CSV, ou si un outil de synchronisation gouverné est retenu. La double saisie manuelle ne doit pas continuer.

### 3.4 Catalogue des champs

Etat actuel : définitions dispersées dans les documents, SQL et CSV.

Validation nécessaire : choisir un format canonique machine-readable avant d'étendre les 420 définitions ou le mapping Openfunds.

## 4. REGLE DE CONTINUITE

Chaque future intervention doit :

1. citer la tâche `OF-*` correspondante dans `TODO.md` ;
2. vérifier les décisions `ADR-*` dans `DECISIONS.md` ;
3. mettre à jour `SUIVI.md` ;
4. ajouter une entrée à `CHANGELOG.md` lorsqu'un livrable change ;
5. mettre à jour cette matrice lorsqu'un écart est fermé ou lorsqu'un nouvel écart est découvert.
