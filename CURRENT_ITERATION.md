# Itération courante

```text
LOOP_ID: OF-LOOP-DATA-002
ITERATION: 001
TASK_ID: OF-DATA-002
STATUS: VERIFIED_COMPLETE
START_HEAD: 0a48c14999a5f173fa5ab3ce4b91109e24092c2c
VALIDATED_TECHNICAL_HEAD: 1fb49075abdfb958e152accf915c37ac86b9a54e
DATE: 2026-08-06
```

## Hypothèse et verdict

**Hypothèse :** les 143 colonnes physiques du cœur fonds peuvent être décrites
par une source d’authoring machine-readable unique, sans modifier le runtime ni
inventer le catalogue Openfunds.

**Verdict : confirmé.** Le paquet JSON gouverné se développe en 143 contrats de
36 attributs, réconciliés exactement avec la migration `015`. Les sorties JSON,
CSV `;` et Markdown sont reproductibles sur Python 3.11 et 3.12.

## Corrections de boucle

- alignement des empreintes du manifeste sur le générateur commité ;
- correction du test SQL afin de ne lire que les déclarations de colonnes au
  niveau top-level ;
- aucune réécriture d’historique et aucune modification SQL.

## Limite

Cette itération ne couvre pas D00–D17, les autres schémas, le mapping officiel
Openfunds, les historiques réels ou la production.
