# Workplan

Updated 2026-11-15 after executing the user-authorized corrected 16-cell design. The bounded run is complete; no preferred causal specification has been selected. Earlier review proposals are superseded for this run by [decision 003](decisions/003-calibrated-merger-design.md).

## Findings and assessment

The direction is useful for a transparent PS3 exercise about conditional merger predictions and their sensitivity. It does not yet support a credible single manufacturer-merger estimate. The [complete results report](../Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01/REPORT.md) contains all 16 demand cells and 20 supply scenarios, with failed markets retained.

- All 16 conditional price coefficients are negative. Four first-stage Wald statistics range from 44.59 to 3,245.69; these are not effective-F statistics and establish neither exclusion nor identification of rho. Rho remains calibrated.
- Individual scenarios accept 7,960–7,985 of 7,996 markets numerically. The common numerical intersection has 7,960 markets and 97.08% of baseline packages. Thirty-six markets fail at least one scenario; 320 scenario-market combinations fail. Numerical acceptance includes baseline reproduction, two starts, FOCs and local profit curvature, not global uniqueness.
- On that common numerical sample, category-wide baseline-package-weighted price increases span 0.157%–3.374% across the 20 scenarios. Kimberly-Clark increases span 1.028%–24.345%. These are conditional scenario ranges, not confidence intervals, and include negative-cost cases.
- Cost consistency is the main obstacle to a headline merger conclusion. The common nonnegative effective-cost intersection has only 538 markets (6.73% of markets, 5.61% of baseline packages). The common nonnegative manufacturer-cost intersection is empty. Three linear/AAC nested cells have no markets passing the manufacturer-cost screen. Do not substitute changing cell-specific screens for a common-sample comparison.
- Own-price elasticities are relatively stable across rho within each IV/price form, while category elasticity and substitution change substantially. Scott-to-Kimberly-Clark baseline-package-weighted diversion rises from 0.638% at rho zero to about 3.40% at rho .75. Thus stable own elasticities do not establish counterfactual robustness.
- Log-price cells have much better cost coverage; this is a functional-form result, not independent evidence that their instruments are valid. Dollar/percentage margins also change merging-firm predictions at rho zero. Percentage costs are calibrated from q*p; AAC remains a separate proxy.
- Linear-price consumer-surplus changes are reported; log-price dollar welfare is deferred. No market-size robustness, availability correction, stockpiling model or counterfactual sampling uncertainty is claimed.

Run 2026-11-15_16cell_01 used 259,986 observations, 7,996 store-weeks, 83 stores and 50 UPCs, retaining 94.31% of packages in the full 1991–1992 positive-sales panel. The isolated catalog corrects 10 Scott UPC labels present in this sample. All 194 pre-existing research files remain byte-identical. See [validation](validation/2026-11-15-calibrated-merger.md) and [handoff](handoffs/2026-11-15-yifan-calibrated-merger.md).

## Accepted and executed design

The following bounded design was accepted by the user's explicit instruction to proceed. All 16 demand cells and four additional percentage-margin scenarios were executed once; no extra specifications or result-driven restarts were added.

- Use the saved v4 all-pack complete-market keys: 259,986 rows, 7,996 store-weeks, 83 stores. Estimate and simulate on identical product-market keys. Correct labels in a separate derived catalog; source the six main corporate portfolios and explicitly identify the fixed-price fringe.
- Prespecify 16 conditional 2SLS cells: AAC versus other-zone IV, linear versus log package price, and calibrated `rho` in `{0, 0.25, 0.5, 0.75}`. Subtract `rho * log(s_j / S)` from the log-share-ratio dependent variable. Each cell estimates the price coefficient **conditional on rho**, not rho itself. Use store-by-UPC/week fixed effects and the maintained exogeneity of deal. There are only four distinct price first stages because rho changes the dependent variable, not the first stage.
- State the exclusion assumption for each chosen IV transformation. `E[z * xi] = 0` alone does not imply `E[log(z) * xi] = 0`; log-IV cells need a stronger conditional-exogeneity argument or their own explicit moment assumption. Check positivity without silently changing the common sample. Use a signed coefficient `beta_price` in estimation and `a = -beta_price > 0` in downward-demand markup formulas.
- Use fixed dollar retailer margins for all cells; percentage margins only for `rho = 0` as the executed sensitivity. For dollar margins, retail-equivalent cost inversion is sufficient for price prediction given demand and conduct; interpreting manufacturer costs using AAC is a separate diagnostic. For percentage margins, set `q_j = 1 - median_margin_store_upc`, baseline wholesale price `w_j = q_j * p_j`, and manufacturer cost `c_j = w_j - mu_j`. Report `AAC_j - mu_j` separately as an observed-cost-proxy diagnostic; do not substitute it for the calibrated cost and expect exact baseline reproduction when `AAC_j != q_j * p_j`.
- The percentage/dollar equivalence condition must hold within each **post-merger** portfolio as well as before merger. Different uniform margins at Scott and Kimberly-Clark become within-owner dispersion after merger. Do not assume the two simulations coincide merely because pre-merger owners each had uniform margins.
- Use the demand Jacobian for the actual price form and rho in every cost/FOC calculation. The simple-logit closed-form markups apply only at `rho = 0`. State fixed fringe prices as an additional conduct assumption, not a consequence of a passive retailer. Hold market size, non-price utility (including recovered unobservables), deal, product set, retailer rule, and manufacturer costs fixed within each simulation.
- Validate baseline ownership reproduction and scaled FOC residuals with documented units/tolerances and two starts; check economically admissible solutions and local profit-maximization conditions, not just stationary roots. For negative/wrong-sign demand or failed equilibria, preserve and label the failed cell; do not force acceptance. Report cost diagnostics by pack size, category elasticity, diversion, and price changes weighted by **baseline** packages.
- Report full-sample diagnostic coverage and invalid-cell counts. If showing results for cost-admissible markets, state whether the screen concerns retail-equivalent or manufacturer costs and report retained market/package shares. Use a common retained-market intersection for cross-cell comparisons as well as any cell-specific screen. Changing screened samples must not masquerade as parameter sensitivity.
- Report consumer surplus only for linear-price cells with the correctly normalized nested-logit welfare formula. Defer log-price dollar welfare absent a specified income-compensation model. Variation across rho tests **substitution sensitivity at fixed market size**, not sensitivity to the traffic denominator. No market-size grid or aggregation is included in this round.

Stop after the prespecified cells and diagnostics; preserve failures and avoid adding cells after inspecting results. No further mixed-logit refinement or store-deletion exercise is needed for this prototype. Remaining IV assumptions are documented limitations, not a promise to prove exclusion or identify a unique source of the joint rejection.

## Work register

Ownership records accepted work only. Complete below refers to the bounded deliverable, not validation of the economic assumptions.

| ID | Work item | Owner | Status | Evidence / remaining dependency |
|---|---|---|---|---|
| ENG-001 | Shared uv environment and portable locking | Yifan / Codex | Complete on Windows; Mac pending | Locked environment and safe check; no Mac runtime claim |
| COLLAB-001 | Repository handoffs and decisions | Yifan / Codex | Complete | [Workflow](COLLABORATION.md) |
| REVIEW-001 | Evaluate saved research progress | Yifan / Codex | Complete | [Original review](validation/2026-11-15-research-review.md) |
| REVIEW-002 | Verify Fable's first feedback | Yifan / Codex | Complete | [First feedback evidence](validation/2026-11-15-fable-review.md) |
| REVIEW-003 | Correct nesting identification and retailer assumptions | Yifan / Codex | Complete | [Second response](validation/2026-11-15-fable-response.md) |
| CHECK-001 | Native Mac safe check | Unassigned | Proposed | Actual Mac evidence required; off the research critical path |
| SCOPE-001 | Fix estimand and bounded matrix | Yifan / Codex | Complete | [Decision 003](decisions/003-calibrated-merger-design.md): hypothetical Scott/Kimberly-Clark merger at 1991–1992 conditions |
| ENG-002 | Isolate every new research output | Yifan / Codex | Complete | Unique run root, code/environment snapshots, preservation manifests; safe-check logs also isolated |
| RUN-001 | Execute the corrected 16-cell design | Yifan / Codex | Complete | 16 demand fits, 20 supply scenarios; all failures preserved |
| RES-001 | Product, choice-set and market-size audit | Yifan / Codex (bounded audit) | In progress | Common keys, package retention and label correction complete; true availability, zero-sales selection, detailed exclusion decomposition and traffic sensitivity unresolved |
| RES-002 | Conditional identification assumptions and four first stages | Yifan / Codex | Complete for bounded matrix | Report documents transformed-IV assumptions, fixed rho, inference limits and same-sample sensitivities; exclusion remains unproven |
| RES-003 | Additional mixed-logit numerical refinement | Unassigned | Proposed / deferred | Only if a mixed-logit specification is reused; no automatic retries |
| RES-004 | Corrected catalog, period ownership and retailer rules | Yifan / Codex | Complete for prototype | Six portfolios and explicit fixed fringe; non-anchor brands grouped by prefix remain a maintained mapping limitation |
| RES-005 | Decide how to report the bounded matrix | Yifan / Codex | Complete for this round | Report all scenarios and coverage; no final causal model selected and no p-value/cost-screen selection |
| CF-001 | Conditional merger prototype and diagnostics | Yifan / Codex | Complete | Baseline/two-start/FOC/local-curvature checks, cost screens, price changes and linear welfare; credible final policy interpretation remains unresolved |
| DELIV-001 | 30-minute presentation and final claims | Unassigned | Proposed | Use the report and explicit limitations; instructor/collaborator review before presenting a single headline estimate |

## Next work, in order

1. Review the common-sample matrix with Wenhan/Fable. Focus on the linear/AAC single-roll cost failures, functional-form sensitivity and the empty common manufacturer-cost sample. Treat these as challenges to the maintained demand/conduct/cost-proxy combination; the current evidence does not uniquely locate the problem.
2. Prepare the presentation around the conditional question, units/sample exclusions, IV assumptions, calibrated substitution, retailer mapping, diagnostics and sensitivity. Keep v2/v3 and failed v4 fits as historical evidence. The assignment requires a counterfactual and a 30-minute presentation; it does not require a validated manufacturer-merger prediction.
3. If a new research round is agreed, specify one bounded economic question and its acceptance/coverage criteria before running anything. Potential issues include availability/zero sales, traffic-based market size, and wholesale-cost interpretation. Do not expand rho grids, drop stores, aggregate markets or search for a non-rejected model automatically.
4. Complete native Mac verification separately when the collaborator receives these local changes. Follow [SETUP](SETUP.md); never infer Mac runtime success from Windows or portability code alone.

The broader identification concerns from the [original Chinese baseline](handoffs/2026-11-14-wenhan-baseline_zh.md) and review remain. Five of six saved v4 joint tests reject; that does not identify lognormal income as the cause. A single excluded IV cannot jointly estimate price and within-nest share coefficients. The fixed-rho design addresses that rank problem by conditioning on rho, not by identifying it.

No further estimation is scheduled under RUN-001. Changes are local and uncommitted/unpushed on codex/run-001-calibrated-merger, base 14254a5f4177177fd2d9f0b14c598c299b219096. Follow the handoff for exact paths and checks.
