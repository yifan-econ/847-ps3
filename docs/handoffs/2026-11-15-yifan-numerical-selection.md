# 2026-11-15: Yifan / Codex — numerical selection review

- Work ID: REVIEW-005, responding to user-supplied Fable feedback.
- Branch `codex/review-005-numerical-selection`; base `d5fcf7c9b0c9cc44cdf382f634904e2082618669`. Fetched origin/main remains at base.
- Inherited uncommitted DIAG-001/REVIEW-004 work preserved. No commit or push; Wenhan's agent needs these files committed/shared before relying on them remotely.

## Findings and corrections

Fable's core criticism is correct. The prior accepted-sample exception is not independent evidence of cost consistency: log/rho-zero numerical acceptance exactly equals effective-cost nonnegativity, and percentage manufacturer/effective signs agree by identity. Full-input Scott-single package incidence is 61.6–99.96% linear/AAC, 21.3–80.1% linear/other-zone, 3.05–15.62% log. All 20 scenarios exhibit strict separation by largest pre-merger manufacturer share between accepted/rejected markets. Rejections all fail baseline reproduction, none saved curvature checks.

Qualify two claims: numerical acceptance does not explicitly test costs or firm shares, so these are empirical coincidences rather than universal rules. Fable's proposed “same markets” wording is incomplete for dollar-margin log/rho-zero cases: 18 manufacturer-failing markets, 11 rejected and seven retained. Percentage cases have 11, all rejected. His single-product stability algebra reproduces, but the full multiproduct/nested iteration has not been analyzed or re-solved.

Corrected current WORKPLAN/STATUS, stale retailer wording, REVIEW-004 report/validation/handoff, root README and indexes/changelog. The exact old REVIEW-004 report is archived before its prose correction. No existing numerical results, scripts or inputs changed.

## Evidence and paths

New isolated review: `Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_02/`. Contains the supplied message, independent `verify.py`, all-20 scenario crosschecks, broader-v1 kept/omitted coverage, environment/hash evidence, original prior report text and the current report. No estimation or equilibrium calls.

`uv run --locked python Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_02/verify.py` passed on Windows. All 358 pre-existing research files were unchanged during the check. The final inventory allows only the intentionally amended prior report and verifies its archived original against the pre-check hash. [Validation](../validation/2026-11-15-numerical-selection.md), [report](../../Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_02/REPORT.md), [final checks](../../Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_02/final_checks.json).

## Next action

Consolidate the conditional written/presentation claim with full-input cost magnitudes, explicit retailer assumptions and dependent numerical selection. No further estimation or solver retries are scheduled. Model identification, purchase-unit interpretation and other research limitations remain open; this review does not establish equilibrium nonexistence or a preferred causal model.
