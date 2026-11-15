# 2026-11-15: numerical selection feedback verification

REVIEW-005, Yifan / Codex. Branch `codex/review-005-numerical-selection`, base `d5fcf7c9b0c9cc44cdf382f634904e2082618669`. Fetched origin/main remains at that commit. Existing uncommitted work preserved; new work local/uncommitted/unpushed.

Executed on Windows with the shared locked uv environment:

```sh
uv run --locked python Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_02/verify.py
```

Passed independent reconciliation of all 20 saved market cost flags to product-level arrays, Scott-single full-input volume fractions to REVIEW-004, and the numerical/cost cross-tabs. No estimation or equilibrium solver was called. [Code, results and interpretation](../../Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_02/REPORT.md), [machine evidence](../../Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_02/verification.json).

- All four log/rho-zero scenarios reject 11 markets and accept exactly those with nonnegative effective costs. Percentage manufacturer/effective cost signs agree by identity. Accepted-sample zeros are not independent validation.
- Every scenario's largest pre-merger active manufacturer share separates numerical acceptance and rejection. Every rejection fails baseline convergence/reproduction; no rejected market fails either saved curvature flag. Cost signs are not explicitly part of numerical acceptance.
- Correct Fable's proposed wording: log/rho-zero dollar cases have 18 Scott manufacturer-failing markets each, with 11 rejected and seven accepted; percentage cases have 11, all rejected.
- Full-input Scott-single negative-cost package fractions: linear/AAC 61.6488–99.9608%; linear/other-zone 21.2679–80.1492%; log 3.0528–15.6160%. These denominators differ from all-active-product cost incidence.
- Single-product/rho-zero derivative algebra confirms local 0.5-damped iteration thresholds .75 for linear price and (3+1/abs(beta))/4 for log price. The latter is .796400/.798225, distinct from cost thresholds .814401/.807099. This is not a full multiproduct/nested stability proof; no re-solving was attempted.
- Broader-v1 coverage: 512 omitted markets, including 15 of 79 stores in week 105. Omitted markets have lower median packages/trip and rolls/trip; this does not establish selection exogeneity.

The numerical check preserved all 358 inventoried pre-existing research files. Documentation correction then amended only REVIEW-004 REPORT.md within that inventory; its exact original text is archived in the new review directory. Historical estimates, arrays, tables, scripts and raw inputs are unchanged. Current WORKPLAN/STATUS, prior review wording and navigation records are corrected. See [final checks](../../Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_02/final_checks.json) for hashes, Git whitespace and local-link validation.

No native Mac runtime claim, new identification result or solver-repair claim is made. Numerical acceptance remains a computational diagnostic; full-input cost inversion remains separately reportable.
