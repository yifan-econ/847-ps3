# 2026-11-15: Verify Fable's cost-diagnosis feedback

Work ID: REVIEW-004. Yifan / Codex. Branch `codex/review-004-cost-feedback`, base `d5fcf7c9b0c9cc44cdf382f634904e2082618669`. Fetched origin; main remains at the base commit. Preserved all existing uncommitted DIAG-001 work. Source v5 results are committed/shared; diagnosis and review additions are local/uncommitted/unpushed.

## Executed checks

```sh
uv run --locked python Analysis/cost_failure_diagnosis/src/review_feedback.py --review-id 2026-11-15_fable_01
uv run --locked python Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_01/scope_supplement.py
```

Windows, existing Python 3.13.9/uv lock. Both scripts passed. Primary review completed in 7.38 seconds. No new demand specification, subgroup refit, uncertainty calculation or equilibrium solve ran. Reconstructed four existing rho-zero coefficients from full-sample fixed-effect/deal residual cross-products; maximum discrepancy from saved values 8.18e-14. The complement cross-product ratios are explicitly descriptive and do not re-absorb effects on a reduced sample.

| Feedback item | Independent result |
|---|---|
| Joint cost classification | Reproduces 29.11 / 22.28 / 10.02 / 8.77 / 29.82% for linear/AAC rho zero on common markets |
| Order dependence | Portfolio category 31.05→59.14% under original order, 38.59→42.66% under wedge-first order across rho 0→.75 |
| Retailer signs and mean identity | Percentage manufacturer/effective signs identical; general inverse-slope-weighted mean-q identity within 2.7e-15; package-q special case holds for linear price, not generally log price |
| Effective sign changes | 97 of 226,378 common active rows for linear/AAC rho zero |
| Common-AAC percentage-markup diagnostic | 18.8524% negative package volume versus 37.2173% for dollar markup; calibrated percentage cost gives 22.3682% |
| Modal discount definition | Below 95% of store/UPC mode, lowest-price tie break, full v5 sample; 60,446 rows / 23.2497% |
| Log/AAC discount contributions | 56.1442% of instrument–price sum; 66.1305% of instrument–outcome sum |
| Weeks 99/110 | 1.8336% of rows; 15.4388% of log/AAC instrument–price sum |
| Single-roll own elasticity, common sample | Package-weighted -1.0294 linear/AAC versus -5.2441 log/AAC |
| Rolls per trip | Median 0.44917; 325 markets >1; 2,900 >0.5; physical units, not choice shares |
| Unflagged price discounts | 12.4875% of full-input packages below 95% of mode have deal=0 |
| Weekly store counts | Fable's 76/78 reproduce in broader v1; v5 keys have 73/75 stores in weeks 99/110 |
| Universal-failure wording (corrected by REVIEW-005) | Every saved scenario has some full-input Scott-single negative costs; accepted-sample zeros are not independent validation because log/rho-zero numerical acceptance equals effective-cost nonnegativity and percentage cost signs agree by identity. Report full-input magnitudes instead; [follow-up](2026-11-15-numerical-selection.md) |
| Preservation | All 333 pre-existing research files unchanged, including prior diagnosis outputs |

Evidence: [review report](../../Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_01/REPORT.md), [verification](../../Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_01/verification.json), [scope](../../Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_01/scope.json), [preservation](../../Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_01/preservation.json). Original feedback and exact code snapshots are retained in that review directory.

## Interpretation corrections and limits

Accept Fable's main numerical criticism and show joint inequalities/both accounting orders. Do not use “retailer wedge only” as an exclusive explanation. The like-for-like AAC diagnostic deserves prominence alongside calibrated percentage costs, not replacement of the equilibrium calibration. The full-input log-price improvement is much larger than the sample-selection effect.

Do not infer a causal promotion effect or a general impossibility result from fixed-residual covariance splits. Modal-price discounts are a proxy and do not prove sale-flag errors. Rolls per trip are not choice probabilities, and cannot identify buyers, units per buyer or inventory payback. Post-week-110 summaries also depend on the later week-117 spike; no identified “recoupment” rate is claimed. Existing source reconciliation does not verify the truth of customer counts. No new model or valid causal instrument has been selected.

Final documentation/numerical review passed: Git whitespace, all local targets in 40 Markdown files, joint classifications against prior negative-volume totals, both order totals and scope-specific Scott cost claims. Final SHA-256 recheck: 333 protected files unchanged. [Evidence](../../Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_01/final_checks.json).
