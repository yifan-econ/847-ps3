# Storyboard and speaker notes

Presentation date: November 23, 2026. Fifteen main slides, thirty-minute target including transitions and brief discussion. These are timing allocations, not a completed rehearsal. Proposed speaking split: Yifan slides 1–8, Wenhan slides 9–15, subject to their agreement. Codex owns draft production and revisions; neither collaborator has yet accepted a speaking allocation.

| Slide | Minutes | Required assignment part | Main point / transition |
|---|---:|---|---|
| 1 | 1 | Counterfactual | We use a merger exercise to learn where static demand and supply can support a prediction. |
| 2 | 2 | Counterfactual | Merge Scott/Kimberly-Clark at the observed earlier-period conditions; no efficiencies or historical prediction. |
| 3 | 2 | Industry | Show manufacturer portfolios and sample package shares. These are chain/sample shares, not national shares. Explain brand and pack-size differentiation, promotions, and the fixed fringe. |
| 4 | 2 | Assumptions / data | Explain UPC/store-week, package versus roll, weekly shopping trips, outside option and positive-sales selection. Brand aggregation would erase pack/variant substitution; store-week preserves local price schedules. Neither choice solves inventory behavior. |
| 5 | 2 | Summary / typical market | Walk through one ordinary market's small product shares and large outside option. Selection uses median inside share and assortment size, not favorable counterfactual outcomes. |
| 6 | 2 | Industry / price variation | Follow the same UPC within one store over time. Temporary drops and volume spikes remain after persistent store-product differences are accounted for. Do not infer causality from this picture. |
| 7 | 3 | Estimator / assumptions | Explain log-share inversion, fixed effects, residual price endogeneity, and 2SLS. The calibrated nesting term moves to the left; one instrument cannot identify two endogenous coefficients. Rho changes substitution; it does not vary market size. |
| 8 | 2 | Identification | Explain cost versus other-zone instrument relevance and their distinct exclusion threats. Wald statistics are not effective F statistics. Price and instrument are both logged in log cells; levels orthogonality does not imply log orthogonality. |
| 9 | 2 | Supply / assumptions | Explain portfolio markups, retailer mapping and fixed costs after inversion. There is no estimated parametric marginal-cost equation: each baseline product-market cost is recovered from the FOCs. AAC is a wholesale proxy, not manufacturer marginal cost. |
| 10 | 2 | Results | Read category and K–C effects in one row, then compare price form and retailer rules. Rho-zero is the presentation anchor, not a selected model. |
| 11 | 3 | Interpretation / sensitivity | Nesting has the largest matched effect over the tested grid; price form follows. This ranking is grid-dependent. Category price changes span about 0.2–3.4%, K–C about 1–24% across all saved scenarios. Explain why internalizing diversion matters. |
| 12 | 2 | Results / interpretation | Negative costs are a result about jointly maintained assumptions. Full-input Scott single-roll volume is the denominator; this differs from all-product cost incidence. Show the simple contrast rather than retelling the review history. |
| 13 | 2 | Interpretation | Cheap single rolls and functional form produce very different markups. The discount moment statistic is a signed covariance contribution, not a causal promotion coefficient. Quantity choice and inventories are possible missing mechanisms. |
| 14 | 2 | Interpretation / identification | Connect the findings to the assignment's goal of understanding challenges of static counterfactuals. Earlier mixed logit: eight attempted fits, six converged; five of six saved joint tests reject. These tests do not isolate the cause or make the conditional logit exercise invalid as an illustration. |
| 15 | 1 | Interpretation / discussion | Close on predictions, sensitivity and economic consistency; invite a concrete alternative measurement or identifying assumption. |

Total: 30 minutes. Suggested handoff after slide 8: “These are the demand assumptions. Wenhan will show how we translate them into manufacturer pricing and what happens when ownership changes.” The proposed split gives Yifan sixteen minutes and Wenhan fourteen; adjust after rehearsal.

## Sources and numerical definitions

- Assignment: [ps3.pdf](../../ps3.pdf), page 1. Required parts are counterfactual, industry, assumptions, estimator, identification, results/interpretation. Data summaries and typical markets are advised.
- Data and charts: [saved v5 inputs/results](../../Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01/REPORT.md); chart CSVs and [build_figures.py](build_figures.py) retain exact values and selection rules. The same-price-rule comparison changes only one design dimension at a time; nesting/price-form/instrument comparisons use dollar margins, retailer comparisons rho zero.
- Ownership: [v5 catalog documentation](../../Analysis/calibrated_merger_v5/README.md), which cites [Hausman–Leonard](../../Paper/Hausman_Leonard_2002_public_earlier_version.pdf). Portfolio labels are historical analytical mappings, with non-anchor prefix grouping maintained.
- Historical transaction: [SEC administrative proceeding](https://www.sec.gov/enforcement-litigation/administrative-proceedings/34-45653) states that the merger occurred in December 1995. [DOJ settlement announcement](https://www.justice.gov/archive/atr/public/press_releases/1995/0486.htm) describes the required facial-tissue and baby-wipes divestitures. Our bathroom-tissue simulation does not represent those remedies or estimate their effects.
- Cost and elasticity slides: [frozen feedback review](../../Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_01/REPORT.md) and [closed numerical-selection review](../../Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_02/REPORT.md). No new cost diagnosis, fit or equilibrium was run for the presentation.

## Rehearsal checklist

Yifan and Wenhan should confirm the split, run the entire talk with a timer, record actual segment times, and cut detail before reducing font sizes. Check legibility on the classroom display. Prioritize explaining the share denominator, excluded instrument and matched assumption comparison. Keep technical accounting and solver algebra in the linked reports for questions. Rehearsal and collaborator approval are still pending.
