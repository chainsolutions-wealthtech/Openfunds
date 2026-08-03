# Tunisia Country Data Pilot — v0.1

## 1. Purpose

Use Tunisia as a country-data pilot complementary to the Morocco market pilot. Tunisia validates macroeconomic series mapping, OPCVM data, source lineage, category indices, government-security modelling and connection of official institutions.

## 2. Official source roles identified

| Role | Institution / portal | Main data families |
|---|---|---|
| Central bank | Banque Centrale de Tunisie / GOSDMX | rates, money, banking, FX, reserves, balance of payments, external debt |
| Statistics office | Institut National de la Statistique | CPI, GDP, employment, industry and trade |
| Finance ministry | Ministère des Finances | budget, debt, BTCT, BTA, BTZc, auctions |
| Securities and fund regulator | Conseil du Marché Financier | fund NAVs, monthly OPCVM market files, prospectuses, bulletins and events |
| Stock exchange | Bourse des Valeurs Mobilières de Tunis | TUNINDEX, TUNINDEX20, securities, prices, volumes and corporate actions |
| Yield-curve platform | CMF / Tunisia Yield Curve | zero-coupon, par and sector curves |

## 3. Initial collection scope

### Funds

- canonical fund and management-company identity;
- published name and aliases;
- category and legal form;
- NAV, bid and offer prices when distinct;
- AUM and units;
- subscriptions, redemptions and net flows when published;
- prospectus, factsheet and financial statements;
- renaming, management transfer, merger, liquidation and distribution events.

### Macro and external

- CPI headline, core, food and energy;
- GDP and growth;
- employment and unemployment;
- exports, imports and trade coverage;
- policy and money-market rates;
- M1/M2/M3 and credit;
- EUR/TND and USD/TND;
- reserves and balance of payments.

### Government securities

- BTCT 13, 26 and 52 weeks;
- BTA and BTZc security master;
- auction dates, amounts, prices and yields;
- coupon schedules, outstanding amounts and maturities;
- historical and current yield curves.

## 4. Candidate benchmarks

- `AF_TUN_CASH`: TMM or preferred official short reference according to frequency and methodology;
- `AF_TUN_TBILL_13W_ROLL_TR`: rolling 13-week BTCT benchmark;
- sovereign Total Return segments 0–1Y, 1–3Y, 3–5Y, 5–7Y, 7–10Y and global;
- TUNINDEX and TUNINDEX20 Price/Total Return references;
- category WTI equal-weighted and AUM-weighted;
- independent WTI Bench per category.

## 5. Key implementation issues

- resolve and version BCT GOSDMX endpoints and provider series codes;
- connect the 2007–2017 CMF curve archive to the current curve platform without hiding method breaks;
- locate post-2018 auction continuity;
- obtain secondary or evaluated prices for true daily Total Return indices;
- audit each monthly OPCVM workbook sheet and layout;
- preserve fund events and aliases across publications;
- store exact file, sheet, row and cell lineage.

## 6. Acceptance criteria

The pilot is complete when official sources and endpoints are registered, mappings cover the priority indicator set, at least one reproducible historical window is loaded, fund/AUM totals reconcile, government securities are identifiable across events, benchmark calculations are versioned, and API-ready country, fund, curve and benchmark projections can be produced.
