# Dictionnaire canonique des champs — Fund core v1

```text
TASK: OF-DATA-002
SCOPE: CANONICAL_FUND_CORE
STATUS: IMPLEMENTED_AWAITING_CI
FIELD_COUNT: 143
ENTITY_COUNT: 10
AUTHORITATIVE_PACKAGE: data/dictionary/spec_v1/
```

Le paquet JSON gouverné couvre les 143 colonnes physiques des dix tables créées
par la migration `015`. Le générateur produit les vues complètes JSON, CSV `;` et
Markdown sous `build/dictionary/`. GitHub Actions publie ces trois vues comme
artefacts de revue sur Python 3.11 et 3.12.

## Tables couvertes

| Table | Champs |
|---|---:|
| `fund.entity` | 5 |
| `fund.entity_state` | 15 |
| `fund.fund_profile` | 18 |
| `fund.subfund_profile` | 16 |
| `fund.share_class_profile` | 19 |
| `fund.entity_event` | 11 |
| `fund.event_participant` | 6 |
| `fund.entity_name` | 18 |
| `fund.entity_identifier` | 18 |
| `fund.structure_relationship` | 17 |
| **Total** | **143** |

## Règles

- `FIELD_ID` est stable et suit `OF_<DOMAIN>_<ENTITY>_<FIELD>` ;
- chaque champ expansé possède 36 attributs ;
- le paquet est la seule source d’authoring ;
- les vues de build ne sont pas modifiées manuellement ;
- aucun identifiant Openfunds n’est inventé ;
- `NULL`, `UNKNOWN` et `NOT_APPLICABLE` restent distincts ;
- la concordance avec la migration `015` est contrôlée en CI.

## Limites

Le statut de complétude ne couvre pas `ref.*`, `source.*`, `market.*`, D00–D17,
les objets métier non encore présents dans le runtime, ni le mapping officiel
Openfunds.
