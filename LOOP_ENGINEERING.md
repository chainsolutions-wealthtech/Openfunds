# Loop Engineering pour Openfunds

Loop Engineering transforme chaque intervention en boucle contrôlée et reproductible. Il relie Git, les décisions, les tâches, le code, les données, les tests, la CI et la mémoire persistante sans remplacer aucune de ces autorités.

## Boucle canonique

```text
DISCOVER
→ BASELINE
→ SELECT
→ IMPACT_ANALYSIS
→ IMPLEMENT_COMPATIBLY
→ VERIFY
→ REGRESSION_CHECK
→ CORRECT_IF_REQUIRED
→ VERIFY_AGAIN
→ PERSIST_STATE
→ COMMIT
→ VERIFY_REMOTE_STATE
→ SELECT_NEXT
```

L’ancien résumé `OBSERVE → FRAME → PLAN → CHANGE → VERIFY → LEARN → HANDOFF` reste conceptuellement compatible, mais la séquence ci-dessus est désormais le contrat opérationnel détaillé.

## 1. DISCOVER

Avant toute écriture :

- lire `00_START_HERE.md` et la chaîne d’autorité ;
- résoudre repository, branche, HEAD, PR et CI ;
- lire les derniers commits pertinents ;
- identifier les documents, schémas, tests et consommateurs concernés ;
- détecter les travaux concurrents ;
- ne rien inventer pour combler une information absente.

## 2. BASELINE

Enregistrer l’état réellement observé avant changement :

- HEAD de départ ;
- statut de la PR ;
- workflows/checks pertinents ;
- tests et défauts préexistants ;
- état documentaire ;
- compteurs métier pertinents ;
- limitations externes.

Une CI préexistante rouge reste un défaut préexistant et ne doit jamais être transformée en PASS documentaire.

## 3. SELECT

Choisir une unité de travail unique et bornée :

- `LOOP_ID` ;
- tâche `OF-*` ou décision correspondante ;
- objectif ;
- critères d’acceptation ;
- allowlist de fichiers lorsque pertinente ;
- conditions d’arrêt ;
- gates humains ou externes.

## 4. IMPACT_ANALYSIS

Avant implémentation, vérifier les impacts sur :

- données et migrations ;
- identifiants et compatibilité historique ;
- modèle canonique ;
- Openfunds et autres mappings ;
- sources/provenance ;
- calculs et méthodologies ;
- API/UI ;
- tests/CI ;
- sécurité ;
- documentation et exploitation.

Aucun impact non compris ne doit être masqué.

## 5. IMPLEMENT_COMPATIBLY

Priorité obligatoire :

```text
REUTILISER
→ CORRIGER
→ RENFORCER
→ ETENDRE
→ MIGRER COMPATIBLEMENT
```

Ne jamais créer une seconde autorité, réécrire un composant validé par préférence personnelle, supprimer un identifiant stable sans migration ou affaiblir un invariant pour simplifier l’implémentation.

Pour un comportement nouveau ou corrigé, utiliser RED → GREEN/TDD lorsque le type de changement s’y prête.

## 6. VERIFY

Exécuter les contrôles pertinents réellement disponibles :

- tests unitaires ;
- tests d’intégration ;
- validateurs de registres ;
- migrations sur environnement de test ;
- build/typecheck/lint selon la surface ;
- contrôles de génération déterministe ;
- CI GitHub ;
- contrôles de données et de provenance.

Ne jamais déclarer un contrôle exécuté sans preuve.

## 7. REGRESSION_CHECK

Comparer explicitement avec la baseline :

- aucun comportement historique non ciblé cassé ;
- aucun identifiant ou contrat supprimé silencieusement ;
- aucune donnée historique perdue ;
- aucune source de vérité concurrente créée ;
- aucune sortie non concernée modifiée sans justification ;
- aucun test supprimé/affaibli pour obtenir du vert ;
- documentation et statut honnêtes.

## 8. CORRECT_IF_REQUIRED

Si une régression ou un échec introduit par la boucle apparaît, corriger dans la même boucle lorsqu’il est sûr de le faire. Un défaut préexistant peut être laissé ouvert uniquement s’il est clairement identifié, documenté et hors périmètre de la boucle.

## 9. VERIFY_AGAIN

Après correction, rejouer les contrôles pertinents et vérifier que la correction n’a pas déplacé le problème vers une autre couche.

## 10. PERSIST_STATE

Avant de considérer la boucle terminée, synchroniser les autorités concernées :

- `STATUS.md` ;
- `TODO.md` ;
- `SUIVI.md` ;
- `NEXT_ACTION.md` ;
- `LOOP_STATE.md` ;
- `CURRENT_ITERATION.md` ;
- `WORK_LOG.md` ;
- `HANDOFF.md` ;
- `CHANGELOG.md` ;
- décisions/ADR et spécifications si concernées.

Tous ces fichiers ne doivent pas être modifiés mécaniquement à chaque micro-changement : seuls les propriétaires d’information concernés sont mis à jour. En revanche, une boucle ne doit jamais laisser volontairement l’état courant en contradiction avec Git.

## 11. COMMIT

Le commit doit être ciblé, descriptif et conforme à la branche autorisée. Aucune création de branche, PR, fusion, retargeting, force-push ou réécriture d’historique n’est implicite dans Loop Engineering.

## 12. VERIFY_REMOTE_STATE

Après écriture :

- résoudre de nouveau le HEAD distant ;
- vérifier que le commit attendu est bien dans la lignée ;
- comparer les fichiers modifiés à l’allowlist ;
- observer les workflows/checks déclenchés ;
- distinguer `PENDING`, `SUCCESS`, `FAILURE`, non déclenché et non observable ;
- ne jamais confondre commit créé et changement vérifié.

## 13. SELECT_NEXT

Fermer par une seule prochaine action déterministe, ou déclarer explicitement qu’un gate humain/externe bloque la suite.

## Contrat minimal d’une boucle

Chaque boucle possède, selon sa portée :

```text
LOOP_ID
TASK_ID
CONTROL_BRANCH
START_HEAD
BASELINE
OBJECTIVE
IMPACT_ANALYSIS
ACCEPTANCE_CRITERIA
FILE_ALLOWLIST_OR_SCOPE
TEST_EVIDENCE
REGRESSION_RESULT
END_HEAD
REMOTE_VERIFICATION
KNOWN_LIMITATIONS
STOP_CONDITIONS
NEXT_ACTION
```

## Règles permanentes

- amélioration uniquement ;
- zéro régression ;
- lecture avant création ;
- analyse du rôle des documents ;
- vérification avant et après écriture ;
- mémoire persistante dans Git ;
- aucune preuve inventée ;
- aucun statut plus avancé que la preuve disponible ;
- aucune conversation n’est une autorité canonique.

La Definition of Done détaillée est portée par `DEFINITION_OF_DONE.md`.
