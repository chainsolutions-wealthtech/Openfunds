# PR1 RECONCILIATION AND POPULATION PLAN

## OBJECTIF

Reconciler la PR #1 avec le socle canonique actuel sans regression, sans doublon de source de verite et sans confondre architecture prete, referentiels peuples, mappings de sources et historiques reellement collectes.

## REGLE DIRECTRICE

Le projet doit aboutir a une chaine complete :

PAYS / ZONE
-> RELATIONS GEOGRAPHIQUES ET DE MARCHE
-> DOMAINES D00-D17
-> DEFINITIONS CANONIQUES D INDICATEURS
-> APPLICABILITE PAYS OU ZONE
-> INSTITUTIONS ET SOURCES OFFICIELLES
-> SERIES FOURNISSEURS
-> COLLECTE ET ARTEFACTS SOURCES
-> OBSERVATIONS VALIDEES
-> CONVERSIONS LOCAL EUR USD
-> CATEGORIES ET SOUS CATEGORIES
-> GROUPES DE PAIRS
-> INDICES MARCHE PRINCIPAL ET SECONDAIRE
-> WTI
-> WTI BENCH
-> METRIQUES ET CLASSEMENTS
-> API ET VIEW MODELS ATOMIC DESIGN

## CE QUE SIGNIFIE PEUPLE

### NIVEAU 1 — REFERENTIEL PEUPLE

Les entites stables sont presentes et reliees :

- AFRICA ;
- cinq regions ;
- 54 pays ;
- devises ;
- UEMOA, CEMAC, CMA et autres zones retenues ;
- banques centrales, bourses, regulateurs et institutions ;
- relations pays-region-continent-devise-zone-marche.

Ce niveau ne contient pas encore tous les historiques economiques et financiers.

### NIVEAU 2 — CATALOGUE PEUPLE

Les 420 definitions D00-D17 sont documentees et chargeables :

- code canonique ;
- nom ;
- description ;
- type ;
- unite ;
- frequence ;
- traitement devise ;
- source prioritaire ;
- usage dans les ratios, indices, WTI, WTI Bench, metriques et API.

### NIVEAU 3 — MAPPING PAYS / ZONE PEUPLE

Pour chaque pays ou zone et chaque indicateur applicable :

- statut d applicabilite ;
- institution responsable ;
- serie fournisseur ;
- URL ou endpoint ;
- methode de collecte ;
- frequence reelle ;
- historique disponible ;
- statut de verification ;
- ruptures methodologiques.

La matrice logique contient 54 x 420 combinaisons potentielles, mais seules les relations utiles sont materialisees.

### NIVEAU 4 — HISTORIQUES PEUPLES

Les observations reelles sont collectees et validees :

- donnees macroeconomiques ;
- taux directeurs et monetaires ;
- adjudications ;
- courbes de taux ;
- prix et rendements obligataires ;
- indices actions ;
- VL, AUM et dividendes des fonds ;
- FX ;
- revisions ;
- provenance complete.

Ce niveau ne peut etre declare termine qu apres collecte effective des sources officielles. La PR #1 ne fournit pas, a elle seule, tous les historiques pour les 54 pays.

### NIVEAU 5 — PRODUITS CALCULES PEUPLES

Les series calculees sont disponibles et reconstructibles :

- versions LOCAL, EUR et USD ;
- categories nationales, regionales et AFRICA ;
- sous categories ;
- groupes de pairs ;
- indices marche principal et secondaire ;
- WTI ;
- WTI Bench ;
- performances ;
- volatilite ;
- Sharpe et Sortino ;
- drawdowns ;
- alpha et beta ;
- percentiles, quartiles et classements.

## RECONCILIATION DES REFERENTIELS

### SOURCE DE VERITE UNIQUE

Les fichiers suivants restent les referentiels canoniques :

- data/reference/AFRICA_REGIONS.csv ;
- data/reference/AFRICA_COUNTRIES.csv ;
- data/reference/MARKET_ZONES.csv ;
- data/reference/COUNTRY_RELATIONSHIPS.csv.

Le fichier african_countries_v0.1.csv de la PR doit etre traite comme une source de comparaison et non comme un deuxieme registre canonique.

### CONVENTION DE NOMMAGE

Les codes techniques suivent :

- MAJUSCULES ;
- SANS ACCENT ;
- SANS APOSTROPHE ;
- SEPARATEUR UNDERSCORE ;
- IDENTIFIANT STABLE.

Les noms d affichage et libelles sources restent separes et peuvent conserver les accents.

### ZONES COMMUNES

Les fonds restent lies au pays puis a la region et a AFRICA.

Les donnees de marche communes sont resolues par MARKET_SCOPE :

- pays UEMOA -> UEMOA -> BCEAO / BRVM ;
- pays CEMAC -> CEMAC -> BEAC / BVMAC ;
- autres pays -> marche national ou autre zone explicite.

## TAXONOMIE ET REGROUPEMENTS

A partir de PAYS + CLASSE D ACTIFS :

- CATEGORIE NATIONALE ;
- CATEGORIE REGIONALE ;
- CATEGORIE AFRICA.

A partir de PAYS + CLASSE + SOUS CLASSE :

- SOUS CATEGORIE NATIONALE ;
- SOUS CATEGORIE REGIONALE ;
- SOUS CATEGORIE AFRICA.

Chaque categorie et sous categorie possede un bloc de quatre roles :

1. INDICE MARCHE PRINCIPAL ;
2. INDICE MARCHE SECONDAIRE ;
3. WTI - [CATEGORIE OU SOUS CATEGORIE] ;
4. WTI BENCH - [CATEGORIE OU SOUS CATEGORIE].

Les regroupements servent simultanement a :

- definir les groupes de pairs ;
- construire les WTI ;
- calculer les classements ;
- calculer les metriques ;
- rattacher les references de marche ;
- produire les vues nationales, regionales et AFRICA.

## LOCAL EUR USD

Toute observation monetaire convertible conserve :

- valeur native ;
- devise source ;
- valeur EUR ;
- valeur USD ;
- observation FX exacte ;
- methode de conversion ;
- statut qualite.

Les niveaux regional et AFRICA sont recalcules a partir des series converties, et non par simple affichage ou moyenne de niveaux locaux.

## LIMITES ACTUELLES

A l issue de la reconciliation documentaire et schema :

- les referentiels et relations pourront etre complets ;
- le catalogue D00-D17 pourra etre complet ;
- les plans de benchmarks et regles qualite pourront etre complets ;
- les tables pourront etre pretes ;
- les categories et blocs pourront etre generes.

Mais tous les historiques de tous les pays ne seront pas automatiquement presents. Ils devront etre collectes, controles et historises source par source. La Tunisie constitue un pilote riche, mais ne vaut pas couverture complete de l Afrique.

## CRITERES DE FIN

Le projet ne doit etre declare pleinement peuple que lorsque, pour chaque pays ou zone :

- les sources prioritaires sont identifiees ;
- les endpoints sont verifies ;
- les historiques sont charges ou l indisponibilite est documentee ;
- les conversions EUR et USD sont calculables ;
- les categories et groupes de pairs sont peuples ;
- les indices de marche sont affectes ;
- les WTI sont calculables ;
- les WTI Bench sont calculables ;
- les metriques et classements sont reproductibles ;
- la provenance et la qualite sont auditables.

## ORDRE D EXECUTION

1. Rebaser et reconciler la PR #1 avec le socle actuel.
2. Eliminer les doublons de referentiels.
3. Aligner les codes canoniques.
4. Conserver les 420 definitions D00-D17.
5. Relier les definitions aux pays et zones.
6. Peupler institutions, sources et endpoints.
7. Charger progressivement les historiques officiels.
8. Produire LOCAL / EUR / USD.
9. Generer categories, sous categories et groupes de pairs.
10. Affecter les blocs de references.
11. Calculer WTI et WTI Bench.
12. Calculer metriques et classements.
13. Exposer les API et view models Atomic Design.
