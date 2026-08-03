# Africa Macro Indicator Usage Map — v0.1

## 1. Purpose

This document explains how country-level observations are combined into macroeconomic ratios, market benchmarks, fund analytics and API view models. Calculated indicators never replace the underlying official series.

## 2. Real economy

- Nominal GDP is the denominator for debt/GDP, deficit/GDP, credit/GDP, AUM/GDP and market-capitalisation/GDP.
- Real GDP and sector value added feed growth trends, sector contributions and country-cycle classification.
- Population and employment feed GDP per capita, employment ratios and household-demand context.

## 3. Inflation and real returns

- CPI year-on-year is used for real policy rate, real money-market rate and real fund returns.
- The CPI index, not only the published percentage, is retained for cumulative inflation and purchasing-power comparisons.
- Core, food and energy inflation explain dispersion and policy transmission.

## 4. Fiscal and sovereign debt

- Revenue, expenditure, interest and balances feed overall balance/GDP, primary balance/GDP, interest/revenue and fiscal impulse.
- Debt stock, maturity, rate type, currency and redemption profile feed refinancing walls, FX risk and sustainability scores.
- Auction yields and outstanding amounts feed marginal funding cost and index eligibility.

## 5. Monetary and banking

- Policy rates, overnight rates, T-Bills and liquidity operations determine the local risk-free hierarchy.
- M2 and private credit feed money growth, credit/GDP and financial-depth indicators.
- NPLs, capital, profitability and loan/deposit ratios feed banking-risk components of the country score.

## 6. External sector and FX

- Official EUR and USD FX series convert NAV, AUM, dividends, prices, indices and flows. Each converted value references the exact FX observation.
- Reserves and imports feed months of import cover.
- Current account and trade data feed external-balance ratios and vulnerability analysis.
- REER and NEER support competitiveness analysis but are not substitutes for spot conversion rates.

## 7. Yield curves and sovereign indices

The preferred hierarchy is observed secondary prices, official evaluated prices, official yield curve, then documented synthetic valuation. Primary auction yields alone are insufficient for a daily Total Return index.

Segment products include 0–1Y, 1–3Y, 3–5Y, 5–7Y, 7–10Y, 10Y+ and global sovereign indices. Total Return includes clean-price movement, accrued interest, coupons and principal repayments. Constituents, weights, exclusions and rebalancing are historised.

## 8. Funds, WTI and WTI Bench

- Fund NAV and distributions produce adjusted fund returns.
- WTI represents the observed performance of eligible peer funds. It may be equal-weighted or AUM-weighted according to the category methodology.
- WTI Bench is an independent market or strategic-allocation benchmark.
- Primary Market Index and Secondary Market Index remain separate reference roles.
- No missing NAV is silently interpolated. Eligibility and survivorship are historised.

## 9. Country score

The country score is a versioned analytical product combining growth, inflation, fiscal, debt, monetary, banking, external and governance components. Inputs, normalisation, weights, missing-data policy and methodology version are stored. A score is not published if critical components are silently imputed.

## 10. API and UI uses

| View model | Required domains |
|---|---|
| Country overview | D01–D09, D16 |
| Monetary conditions | D04, D07, D08 |
| Sovereign debt dashboard | D05, D06, D10 |
| Yield-curve page | D10 |
| Equity market page | D09, D11, D17 |
| Fund page | D09, D12, D17 |
| Fund comparison | D07, D09, D12, D17 |
| Country risk page | D03–D09, D16, D17 |
| Local/EUR/USD performance | D09, D11/D12, D17 |

## 11. Calculation lineage

Every calculated observation records methodology version, calculation run, input observation identifiers, FX observation identifiers, calendar, parameters, exclusions and quality status. This lineage must be retrievable from APIs and view models.
