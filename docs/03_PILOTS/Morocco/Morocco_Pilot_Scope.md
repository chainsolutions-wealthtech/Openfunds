# Morocco Pilot — Canonical Fund Categories, Bond Indices and Platform Benchmarks

## Status

Approved pilot country: Morocco.

## Purpose

Morocco is the first country used to validate the full national methodology for:

- national asset-class categories;
- national sub-asset-class categories;
- official market indices;
- platform-calculated fund benchmarks;
- synthetic bond indices built from historical rates;
- full daily calculation lineage;
- reproducible base-100 series.

## National classification hierarchy

Country -> National Category -> National Subcategory -> Fund -> Share Class.

For Fixed Income in Morocco:

- Morocco Fixed Income;
  - Morocco Short-Term Fixed Income;
  - Morocco Medium-Term Fixed Income;
  - Morocco Long-Term Fixed Income.

## Bond market indices built from rates

The platform must create:

1. Morocco Short-Term Bond Market Index;
2. Morocco Medium-Term Bond Market Index;
3. Morocco Long-Term Bond Market Index;
4. Morocco Global Bond Market Index.

These indices are independent from fund performance. They are built from official Moroccan rate and bond-market data, including as available:

- Treasury bill and bond quotations;
- sovereign yield-curve points;
- auction results;
- secondary-market quotations;
- central-bank or Treasury publications.

## Platform fund benchmarks

The platform must create:

1. Morocco Short-Term Fixed Income Platform Benchmark;
2. Morocco Medium-Term Fixed Income Platform Benchmark;
3. Morocco Long-Term Fixed Income Platform Benchmark;
4. Morocco Global Fixed Income Platform Benchmark.

Each subcategory benchmark is calculated from the daily returns of eligible funds belonging to that Moroccan national subcategory and having a calculable new valuation for the calculation date.

The global platform benchmark is calculated according to the methodology approved for the national Morocco Fixed Income category.

## Benchmark attachment for a Moroccan short-term bond fund

A Moroccan short-term fixed-income fund is attached to:

- National Category: Morocco Fixed Income;
- National Subcategory: Morocco Short-Term Fixed Income;
- Morocco Short-Term Bond Market Index;
- Morocco Short-Term Fixed Income Platform Benchmark;
- Morocco Global Bond Market Index;
- Morocco Global Fixed Income Platform Benchmark;
- the fund-declared prospectus benchmark, when one exists.

## Initial source families

The source inventory must cover at least:

- Bank Al-Maghrib;
- Morocco Ministry of Economy and Finance — Debt Office;
- AMMC;
- Casablanca Stock Exchange;
- official Treasury auction and E-Bond publications.

## Required outputs

- source inventory and endpoint history;
- maturity matrix;
- normalized historical rate observations;
- daily yield curves;
- synthetic bond constituents;
- daily constituent valuations;
- CT, MT, LT and global bond-index levels;
- national category and subcategory memberships;
- CT, MT, LT and global platform benchmark levels;
- contribution and exclusion details;
- methodology versions and audit trail;
- SQL schema, JSON schemas, API-ready contracts and tests.

## Non-negotiable principles

- A rate average is not treated as a bond performance index.
- Market indices and fund platform benchmarks remain distinct.
- Every daily level must be reproducible.
- Every interpolation, carry-forward, correction and exclusion must be explicit.
- Original files and publications must remain traceable.
- Regional and continental benchmarks are outside this pilot phase and will be designed later in EUR and/or USD.
