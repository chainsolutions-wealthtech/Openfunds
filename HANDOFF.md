# Handoff Loop Engineering

```text
LOOP_ID: OF-LOOP-DATA-001
TASK_ID: OF-DATA-001
STATUS: IMPLEMENTATION_IN_PROGRESS
CONTROL_BRANCH: architecture/africafunds-country-indicators-v0.1
START_HEAD: e79c735b2cda8cc40a237b7deb3e379cc42bf1d9
TECHNICAL_HEAD: PENDING
```

## Modèle retenu

```text
STANDALONE FUND -> SHARE_CLASS
UMBRELLA FUND -> SUBFUND -> SHARE_CLASS
```

Identité, états, profils, noms, identifiants, relations et événements sont
séparés. Le brouillon historique reste exclu ; la migration runtime candidate est
`015_FUND_SUBFUND_SHARECLASS_CORE`.

## Fichiers principaux

- `schemas/fund/015_fund_subfund_shareclass_core.sql` ;
- `docs/01_ARCHITECTURE/ADR-030_FUND_SUBFUND_SHARECLASS_CANONICAL_MODEL.md` ;
- `docs/02_DOMAIN_MODEL/FUND_SUBFUND_SHARECLASS_MODEL_V1.md` ;
- `tests/test_fund_domain_model.py` ;
- `tests/sql/fund_domain_model_assert.sql`.

## Validation attendue

PostgreSQL 16 vide, double apply, ledger, adoption sans ledger, chemins Maroc /
Tunisie / Nigeria, unicité ISIN, parent structurel unique et interdiction d’une
classe directe sous un umbrella.

## Limites

Aucun fonds réel, historique, NAV, document, mandat de service, mapping
Openfunds, API ou déploiement n’est inclus dans cette boucle.
