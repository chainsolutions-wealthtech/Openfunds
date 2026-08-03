# Africa Country Indicator Framework — v0.1

## Status

Draft extension aligned with the accepted Country-Centric Market Universe and the Fund Relationship Information Model.

## Scope

- 54 African countries;
- monetary unions represented separately from sovereign countries;
- 18 canonical domains;
- 420 indicator, metadata, event and calculated-product definitions;
- official-source preference, provenance, revisions, quality and bitemporal history;
- links from raw country series to macro ratios, risk scores, market indices, WTI and WTI Bench.

## Canonical hierarchy

```text
Country
  -> Domain
  -> Canonical indicator definition
  -> Country-indicator relationship
  -> Provider series mapping
  -> Source endpoint
  -> Collection specification
  -> Source document and extraction record
  -> Validated canonical observation
  -> Calculated observation / benchmark / API view model
```

The catalogue is not a 420-column country table. Definitions are shared. Country-specific applicability, provider labels, units, frequency, method breaks and source mappings are relationships.

## Domains

- [D00 — Gouvernance et traçabilité](indicator_catalog/D00_gouvernance_et_traçabilite.md)
- [D01 — Identité pays et institutions](indicator_catalog/D01_identite_pays_et_institutions.md)
- [D02 — Démographie, emploi et revenus](indicator_catalog/D02_demographie,_emploi_et_revenus.md)
- [D03 — Comptes nationaux et activité](indicator_catalog/D03_comptes_nationaux_et_activite.md)
- [D04 — Prix et inflation](indicator_catalog/D04_prix_et_inflation.md)
- [D05 — Finances publiques](indicator_catalog/D05_finances_publiques.md)
- [D06 — Dette publique et soutenabilité](indicator_catalog/D06_dette_publique_et_soutenabilite.md)
- [D07 — Politique monétaire et liquidité](indicator_catalog/D07_politique_monetaire_et_liquidite.md)
- [D08 — Monnaie, crédit et banques](indicator_catalog/D08_monnaie,_credit_et_banques.md)
- [D09 — Change, réserves et secteur extérieur](indicator_catalog/D09_change,_reserves_et_secteur_exterieur.md)
- [D10 — Titres publics et courbes de taux](indicator_catalog/D10_titres_publics_et_courbes_de_taux.md)
- [D11 — Marché actions](indicator_catalog/D11_marche_actions.md)
- [D12 — OPCVM et gestion d’actifs](indicator_catalog/D12_opcvm_et_gestion_dactifs.md)
- [D13 — Assurance, retraite et institutionnels](indicator_catalog/D13_assurance,_retraite_et_institutionnels.md)
- [D14 — Immobilier et crédit immobilier](indicator_catalog/D14_immobilier_et_credit_immobilier.md)
- [D15 — Secteurs réels et matières premières](indicator_catalog/D15_secteurs_reels_et_matieres_premieres.md)
- [D16 — Risque souverain, réglementation et ESG](indicator_catalog/D16_risque_souverain,_reglementation_et_esg.md)
- [D17 — Indices, benchmarks et analytiques](indicator_catalog/D17_indices,_benchmarks_et_analytiques.md)

## Application states

A country-indicator relationship may be: required, source not identified, source identified, URL linked, collection tested, partial history loaded, complete history loaded, not published, not applicable, discontinued or replaced. Method breaks create explicit historical segments.

## Minimum operational coverage

A country is operationally covered when identity and institutions, GDP/growth, inflation, public finance, public debt, policy and money-market rates, money and credit, FX and reserves, government securities, yield curve or valuation fallback, equity index where applicable, fund regulator/fund master/NAVs where applicable, lineage, quality and freshness are available or explicitly documented as unavailable.

## Reference files

The machine-readable catalogue and coverage templates live under `data/reference/`. CSV encoding is UTF-8 and separator is `;`.
