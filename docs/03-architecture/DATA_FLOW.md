# Flux de données

```text
OFFICIAL_SOURCE → RAW_ARTIFACT → EXTRACTION → NORMALIZATION → VALIDATION → POSTGRESQL_CANONICAL → CALCULATION → API → UI
```

Chaque transition conserve identifiants, dates, SHA-256, version du parseur, règle de transformation et décision qualité. Les flux actifs sont limités aux pilotes documentés. Toute extension nécessite un mapping source, une spécification, des tests et une politique de rétention.
