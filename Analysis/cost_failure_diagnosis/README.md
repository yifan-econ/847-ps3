# Targeted diagnosis of saved cost failures

This is a diagnosis of the committed v5 results, not a new demand model or merger run. Read the [findings report](runs/2026-11-15_costdiag_01/REPORT.md), [workplan](../../docs/WORKPLAN.md), and [validation record](../../docs/validation/2026-11-15-cost-failure-diagnosis.md).

## Reproduce in a new directory

```sh
uv sync --locked
uv run --locked python Analysis/cost_failure_diagnosis/src/diagnose.py --run-id YYYY-MM-DD_costdiag_unique
uv run --locked python Analysis/cost_failure_diagnosis/src/supplement.py --run-id YYYY-MM-DD_costdiag_unique
uv run --locked python Analysis/cost_failure_diagnosis/src/audit_inputs.py --run-id YYYY-MM-DD_costdiag_unique
uv run --locked python Analysis/cost_failure_diagnosis/src/report.py --run-id YYYY-MM-DD_costdiag_unique
```

The primary runner refuses an existing directory. Supplements/report refuse existing target files. Every write is confined to the new run root; each program is snapshotted there. No estimator or equilibrium solver is imported. Source parameters, shares, prices, ownership, q and cost arrays remain unchanged. All pre-existing files in Analysis/Archive/Data/Paper are hashed, excluding only this new diagnosis directory and disposable bytecode. The first run protected 303 files, including all v5 code and results.

The reporting script narrates this fixed source run; it is not a generic report template for different estimated designs. The original source is `Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01/`, committed at d5fcf7c9b0c9cc44cdf382f634904e2082618669.

## Outputs and units

| Output | Interpretation |
|---|---|
| group_diagnostics.csv | All 20 scenarios, effective/manufacturer costs, manufacturer/UPC/pack/all-active groups, both full-input and common numerical samples |
| failure_decomposition.csv | Ordered singleton/portfolio/retailer-wedge accounting partition of negative package volume |
| retailer_bridge.csv | Exact manufacturer-cost difference between saved dollar and percentage rules, separated into wholesale-price and markup terms |
| retailer_accounting_2x2.csv | Two saved rho-zero scenarios plus two explicitly labeled arithmetic hybrids; no new equilibria |
| coefficient_thresholds.csv | Conditional inverse-sensitivity feasibility thresholds; not estimates, uncertainty intervals or tuning recommendations |
| case_examples.csv | Lowest-cost and highest-package-exposure negative rows from common markets |
| market_exposure.csv | Every source market's quantities, traffic, inside/Scott shares, prices, deals and saved numerical/cost flags |
| all_input_examples.csv | Extreme negative-cost rows including markets outside the common numerical sample |
| tail_movement_records.csv / tail_daily_traffic.csv / tail_weekly_audit.csv | Source reconciliation for all 18 log/AAC rho-zero manufacturer-cost-failing markets |
| scope.json / validation.json / preservation.json / raw_input_audit.json | Scope, algebra/dense checks, preservation and full-sample source reconciliation |

All package fractions use baseline MOVE, not rolls, revenue or post-merger quantities. Group-specific negative fractions divide by that group's package volume. Shares of all negative packages divide by the active-manufacturer negative volume in the same cell/rule/scope/cost definition. When the latter is zero, CSV composition fields use zero as an empty-set convention, not a substantive composition estimate. Fringe rows are excluded from cost diagnostics. Their quantities remain in market-share denominators and market package-coverage weights.

Full input means 7,996 markets, including numerical failures; common numerical means the fixed 7,960-market intersection across all source scenarios. Neither is a cost-screened sample. Sole-failing-group counts indicate that every negative-cost product in a market belongs to that group; they do not represent dropping products and recomputing demand.

## Accounting versus economic interpretation

Let S be total inside share, S_f the sum of product shares belonging to manufacturer f, h=1/(1-rho), A=1+(h-1)/S, and b the signed derivative of mean utility with respect to retail price. The scalar singleton effective markup is `-1/[b*(h-A*s_j)]`. With the existing portfolio ownership, independent block inversion reproduces saved markups. For linear price/dollar margins, `mu_f=1/[abs(beta)*(h-A*S_f)]`: an owner has the same dollar markup across its products in one market.

The three failure categories hold observed shares and demand parameters fixed. They separate where a cost sign crosses in an ordered comparison; they do not identify a causal contribution or solve an alternative ownership equilibrium. Percentage manufacturer and effective costs have the same sign because q is positive. Under dollar margins the retailer wedge p-AAC can cause additional manufacturer-cost failures, or occasionally rescue effective failures when recorded retailer margins are negative.

The exact retailer bridge is `c_percentage-c_dollar=(q*p-AAC)+(mu_dollar-mu_percentage)`. Off-diagonal 2x2 accounting hybrids are not maintained structural models. Mean cost differences and fractions crossing zero need not move together.

The raw audit independently reconstructs MOVE, PRICE/QTY, AAC, deal flags and seven-day traffic for all saved keys. It confirms arithmetic/provenance, not actual availability, raw-data accuracy, instrument exclusion, stockpiling or the one-package-per-shopping-opportunity approximation. No rows are deleted or repaired.
