# Current project status

Updated 2026-11-15 after Fable's presentation review: delivery remains the priority, due November 23. Read the [latest handoff](handoffs/2026-11-15-yifan-presentation-revision.md), [workplan](WORKPLAN.md), [current presentation](../Presentation/2026-11-23/revision_02/README.md), and [original Chinese baseline](handoffs/2026-11-14-wenhan-baseline_zh.md).

## Presentation delivery

Yifan selected Codex to draft LaTeX/Beamer. Revision 02 has fifteen main slides and three backups, targeting 25.5 minutes of remarks plus questions. [PDF](../Presentation/2026-11-23/revision_02/presentation.pdf), [source](../Presentation/2026-11-23/revision_02/main.tex), [notes](../Presentation/2026-11-23/revision_02/SPEAKER_NOTES.md). Added demand and first-stage estimates with uncertainty, pack-size elasticities, a worked Scott cost example, calendar dates and price-variation summary. Scott joins the main price table; retailer, mixed-logit and welfare details move to backups. The talk explicitly connects large predicted effects to cost failures. Fresh preview sheets reflect this PDF; the original draft is preserved.

The diagnosis/review thread is closed and frozen. Negative costs are a result for the classroom argument, not a blocker requiring another model. No further estimation or solver retries are scheduled. Human review, agreement on speaking parts and a timed rehearsal remain outstanding. Proposed split: Wenhan industry/data/demand, Yifan supply/counterfactual; rough rehearsal by November 19. Yifan authorized the local delivery commit including accumulated work and will push it himself. Codex does not push or send the drafted email.

## Latest diagnosis

The user-authorized [cost-failure diagnosis](../Analysis/cost_failure_diagnosis/runs/2026-11-15_costdiag_01/REPORT.md) is complete. It uses all saved v5 scenarios without new estimation or equilibria and preserves all 303 pre-existing research files. Independent algebra/dense checks and raw movement/traffic reconciliation passed; see [validation](validation/2026-11-15-cost-failure-diagnosis.md).

In linear/AAC rho zero on common numerical markets, Scott accounts for 86.28% of negative manufacturer-cost package volume and five single-roll UPCs for 84.69%. REVIEW-004 confirms the numbers but corrects the exclusive-sounding accounting labels: singleton markup already exceeds AAC for 61.41% of that negative volume; the remaining 38.59% requires the portfolio increment at fixed inputs. Joint inequalities and both orders replace a causal reading of the earlier three-way split. Percentage manufacturer/effective signs agree by identity; the same-AAC percentage-markup diagnostic (18.85% negative volume) is reported alongside calibrated percentage costs (22.37%) and dollar costs (37.22%).

All 18 full-input log/AAC rho-zero manufacturer-cost-failing markets are excluded from the common numerical intersection; seven pass their own scenario's numerical checks. They involve very high Scott purchase shares, mostly in weeks 99/110. Every saved quantity/price/AAC/deal observation and all seven-day traffic totals match the raw sources. The extreme package/traffic ratios therefore remain a substantive issue for the one-package-per-shopping-opportunity interpretation, rather than a discrepancy introduced by the checked pipeline. No automatic data deletion or denominator adjustment was made.

The targeted diagnosis is finished; model credibility, identification, purchase-unit interpretation and uncertainty remain limitations for the presentation. The first complete presentation draft now exists.

## Feedback verification and reporting direction

[The independent feedback review](../Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_01/REPORT.md) reproduces Fable's main findings and adds the requested joint-cost, IV-moment and physical-volume tables. All 333 pre-existing research files remain unchanged. Four existing coefficients were reconstructed within 8.18e-14 from fixed full-sample residuals; no new demand specification or equilibrium ran.

The log/AAC cost improvement exists on full input (39.06% linear versus 1.70% log negative volume); common-sample selection only removes the remaining 1.70%. Discounted rows contribute 56.14% of log/AAC instrument-price cross-products, but descriptive complement ratios do not identify regular-price demand or show that all demand changes must fail. Rolls/trip and unflagged discounts reproduce; roll counts are physical units, not alternative choice shares. Broader-v1 and v5 weekly store counts differ and are now labeled explicitly.

Full-input negative manufacturer-cost incidence among Scott single-roll packages is 61.6–99.96% for linear/AAC, 21.3–80.1% for linear/other-zone and 3.05–15.62% for log price. REVIEW-005 removes the earlier accepted-sample exception: all four log/rho-zero scenarios accept exactly their nonnegative-effective-cost markets. Percentage manufacturer/effective signs agree by identity, so their accepted-sample zero is not independent evidence. Their 11 manufacturer-failing markets are all rejected; dollar cases have 18, with 11 rejected and seven retained. Largest pre-merger manufacturer share separates numerical acceptance/rejection in every scenario, although the code does not explicitly screen costs or firm shares. All rejections fail baseline reproduction and none fails saved curvature checks. [Evidence and solver qualifications](../Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_02/REPORT.md).

The appropriate claim remains conditional model consistency, not general impossibility of static manufacturer pricing. Finite diagnostics are complete; no additional estimation or open-ended episode audit is scheduled. Next is consolidated reporting with identification and measurement assumptions explicit.

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
| DIAG-001 | Saved cost attribution, retailer accounting bridge, high-share tail and full source reconciliation | [Diagnosis](../Analysis/cost_failure_diagnosis/runs/2026-11-15_costdiag_01/REPORT.md) |

Markets remain store-weeks, products UPCs, prices/sales per package, and market size store customer traffic. v1 inputs remain active dependencies; v5 reads v1, v3 instruments, v4 keys and the IO-free v2 estimator helper without changing them.

## Engineering and sharing

The shared uv lock pins Python 3.13.9 and the recorded dependency versions. Windows numerical tests and independent saved-output checks passed; see [validation](validation/2026-11-15-calibrated-merger.md). All 194 pre-existing research files remained byte-identical during the 21-minute research run. The final safe check passed 12 tests, four preparation audits and a saved-market prediction; all 298 inventoried research files were unchanged. It used a unique evidence directory to preserve prior logs. Native Mac runtime verification is still pending.

The inherited estimator had an unused log-price upward-slope reporting field that was wrong. The corrected derived table and audit preserve the raw output; actual demand derivatives, markups, simulated prices and welfare were unaffected. The current runner fixes this field for future runs. An initial independent-validation attempt was interrupted to eliminate repeated array decompression; unchanged numerical checks then passed, with both source versions recorded. No demand/supply rerun occurred.

The shared base is d5fcf7c9b0c9cc44cdf382f634904e2082618669; fetched origin/main remains there. The authorized local delivery commit on codex/deliv-001-beamer includes accumulated diagnosis, feedback review and presentation work. Yifan will push; no remote update by Codex. All earlier work was preserved. The presentation revision leaves all 369 historical research files and the first draft PDF unchanged. Historical manifests retain their original as-of-run sharing statements; the latest handoff describes the delivery commit.

## Open research and next step

IV exclusion, transformed-IV validity, deal exogeneity, actual availability/zero-sales selection, stockpiling, traffic-based market size, non-anchor ownership mapping and wholesale-cost interpretation remain limitations. First-stage strength, convergence and negative price signs do not resolve them. Five of six saved v4 joint tests reject; the cause is not uniquely identified and no mixed-logit rerun was performed.

Next: Yifan and Wenhan review the Beamer draft, Codex incorporates consolidated edits, and the presenters agree on speaking parts and rehearse before November 23. The existing analysis supports the assignment's six required parts. No additional estimation is needed for this delivery; optional aggregation is deferred until after a reviewed full draft and rehearsal, if time and an explicit research question justify it.
