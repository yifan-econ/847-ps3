# Current project status

Updated 2026-11-15 after the authorized conditional merger run. Read the [latest handoff](handoffs/2026-11-15-yifan-calibrated-merger.md), [workplan](WORKPLAN.md), [results report](../Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01/REPORT.md), and [original Chinese baseline](handoffs/2026-11-14-wenhan-baseline_zh.md).

## Current research result

The corrected 16-cell demand design and 20 supply scenarios are complete in run 2026-11-15_16cell_01. All use the same v4 all-pack sample: 259,986 observations, 7,996 store-weeks, 83 stores, 50 UPCs. The run retains 94.31% of full-panel 1991–1992 packages and corrects 10 Scott labels in its separate catalog. Original data, code and results are preserved.

This is a hypothetical Scott/Kimberly-Clark merger at 1991–1992 conditions. Price form (linear/log), IV family (AAC/other-zone) and calibrated rho (0/.25/.5/.75) define the 16 demand cells. Fixed dollar margins apply throughout; four rho-zero cells add percentage-margin sensitivity. Six manufacturer portfolios optimize and private-label/generic prices remain fixed. See [methods and ownership](../Analysis/calibrated_merger_v5/README.md) and [decision 003](decisions/003-calibrated-merger-design.md).

- All price coefficients are negative; rho is calibrated, not identified or estimated. Four distinct first stages are reported, with conditional store/month clustered uncertainty and zero overidentification degrees of freedom.
- Each scenario passes the numerical criteria in 7,960–7,985 markets. The common numerical sample is 7,960 markets, representing 97.08% of baseline packages. Failed candidates are retained. Checks establish local stationary profit maxima, not global equilibrium uniqueness.
- On the common numerical sample, category-wide price increases range from 0.157% to 3.374%, and Kimberly-Clark increases from 1.028% to 24.345%. These ranges include negative-cost cases and are not confidence intervals.
- Only 538 common markets, 5.61% of baseline packages, have nonnegative effective costs in every scenario. No common market passes every manufacturer-cost screen. Three linear/AAC nested cells have zero manufacturer-cost-admissible markets. Log-price models pass far more cost screens; this does not validate their IV assumptions.
- Own elasticities change little with rho within a price form/IV, while category elasticity and diversion change substantially. The exercise is promising as an explicit sensitivity analysis, but there is no defensible single headline merger prediction yet.
- Consumer surplus is reported only for linear-price cells. No additional cells, aggregation, market-size grid, mixed-logit refinement or result-driven solver restarts were added.

## Completed stages

| Stage | Scope | Read first |
|---|---|---|
| v1 | Cleaning, simple logit, package and zero-sales diagnostics | [Original README](../Archive/ps3_v1/README.md) |
| v2 | 14 cost-instrument specifications | [Report](../Analysis/cost_iv_v2/REPORT_zh.md) |
| v3 | 12 AAC/other-zone comparisons | [Report](../Analysis/paper_iv_v3/LITERATURE_AND_RESULTS_zh.md) |
| v4 | Eight demographic mixed-logit attempts: six converged, two rejected | [Report](../Analysis/mixed_logit_v4/REPORT_zh.md) |
| v5 | 16 conditional demand fits, 20 merger scenarios, cost/coverage diagnostics and linear welfare | [Run report](../Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01/REPORT.md) |

Markets remain store-weeks, products UPCs, prices/sales per package, and market size store customer traffic. v1 inputs remain active dependencies; v5 reads v1, v3 instruments, v4 keys and the IO-free v2 estimator helper without changing them.

## Engineering and sharing

The shared uv lock pins Python 3.13.9 and the recorded dependency versions. Windows numerical tests and independent saved-output checks passed; see [validation](validation/2026-11-15-calibrated-merger.md). All 194 pre-existing research files remained byte-identical during the 21-minute research run. The final safe check passed 12 tests, four preparation audits and a saved-market prediction; all 298 inventoried research files were unchanged. It used a unique evidence directory to preserve prior logs. Native Mac runtime verification is still pending.

The inherited estimator had an unused log-price upward-slope reporting field that was wrong. The corrected derived table and audit preserve the raw output; actual demand derivatives, markups, simulated prices and welfare were unaffected. The current runner fixes this field for future runs. An initial independent-validation attempt was interrupted to eliminate repeated array decompression; unchanged numerical checks then passed, with both source versions recorded. No demand/supply rerun occurred.

Changes are local, uncommitted and unpushed on codex/run-001-calibrated-merger, base 14254a5f4177177fd2d9f0b14c598c299b219096. Prior research/Fable review documents are retained. Git LFS attributes cover new compressed inputs, market tables and simulation arrays. Other collaborators do not receive these files until they are explicitly shared.

## Open research and next step

IV exclusion, transformed-IV validity, deal exogeneity, actual availability/zero-sales selection, stockpiling, traffic-based market size, non-anchor ownership mapping and wholesale-cost interpretation remain limitations. First-stage strength, convergence and negative price signs do not resolve them. Five of six saved v4 joint tests reject; the cause is not uniquely identified and no mixed-logit rerun was performed.

Next: review the common-sample sensitivity and cost failures with Wenhan/Fable, then build the 30-minute presentation around conditional conclusions and explicit assumptions. The bounded prototype is finished. Any new model, sample, market-size or instrument exercise needs a separately specified scope; no additional estimation is scheduled here.
