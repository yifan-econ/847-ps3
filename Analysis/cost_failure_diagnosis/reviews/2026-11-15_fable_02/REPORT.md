# REVIEW-005: numerical selection and cost claims

Yifan / Codex, 2026-11-15. Branch `codex/review-005-numerical-selection`, base `d5fcf7c9b0c9cc44cdf382f634904e2082618669`; fetched origin/main remains at that base. All inherited local changes preserved; this round is uncommitted/unpushed. This report supersedes the accepted-sample exception in REVIEW-004. No estimation or equilibrium solve ran.

## Assessment

Fable is right that the earlier accepted-sample exception is not independent evidence of cost consistency. All four log-price/rho-zero scenarios accept exactly the markets with nonnegative effective costs. Under percentage margins, manufacturer and effective cost signs agree by identity. Thus their zero accepted-sample manufacturer failures add no evidence beyond the observed selection pattern. This does not undo the much larger full-input improvement from linear to log price.

There are two qualifications to Fable's wording. First, the numerical screen does **not explicitly test cost signs**: the runner combines convergence, baseline reproduction, two-start agreement and local curvature. The cost overlap is an empirical equality in these saved scenarios, not a general logical guarantee of the algorithm. Second, the dollar-margin log/rho-zero scenarios have 18 Scott-single manufacturer-cost-failing markets each; numerical screening excludes 11 and retains seven. Only the percentage-margin cases exclude all 11 of their manufacturer-cost-failing markets. Therefore “excludes those same markets” is too broad if applied to all manufacturer failures.

## Independent checks of saved arrays and market flags

The new [verification script](verify.py) reads all 20 saved market files and simulation arrays, independently recomputes cost-sign flags on active products, and reconciles Scott-single package-weighted incidence with REVIEW-004. [Scenario results](scenario_crosschecks.csv), [environment and verification](verification.json).

| Scenarios | Rejected markets per scenario | Rejected with nonnegative effective cost | Accepted with negative effective cost | Largest firm share: accepted maximum / rejected minimum |
|---|---:|---:|---:|---|
| Log, rho 0 (4) | 11 | 0 | 0 | .771756 / .811914 |
| Log, rho .25–.75 (6) | 11–18 | 0 | 1–42 | At rho .75: .710133 / .726216 |
| Linear, rho 0 (4) | 14 | 0 | 173–2,672 | .743922 / .762462 |
| Linear, rho .25–.75 (6) | 16–36 | 0 | 598–7,422 | At rho .75: .579576 / .583831 |

For each of the 20 scenarios individually, the largest pre-merger active manufacturer share strictly separates accepted from rejected markets. Share here is the sum of product shares relative to shopping opportunities, not the manufacturer's fraction of inside purchases. This is a descriptive separation in these data; it is not an implemented cutoff or a proven universal acceptance rule.

Every rejected market fails baseline convergence and the baseline-price reproduction tolerance; none fails the saved pre- or post-curvature flag. Baseline costs come from closed-form inversion at observed prices, so cost signs can and should be reported on all 7,996 input markets regardless of solver acceptance. Failure to return to the calibrated baseline does not establish equilibrium nonexistence. Conversely, saved curvature flags do not prove global optimality or uniqueness; post-curvature evaluations at unsuccessful candidates do not certify equilibria.

## Solver interpretation

Fable's single-product, rho-zero algebra checks out. Hold rivals' prices fixed, write beta = -a, a > 0, and let s be that product's share at the calibrated stationary point. Locally the positivity safeguard is inactive. For the iteration T(p) = [p + c/q + mu(p)/q]/2:

- Linear price: mu/q = 1/[a(1-s)] and T'(p) = (1-2s)/[2(1-s)]. Local contraction requires s < 3/4.
- Log price: mu/q = p/[a(1-s)] and T'(p) = (1 + 1/a - 2s)/[2(1-s)]. For a > 1, local contraction requires s < (3 + 1/a)/4. Nonnegative effective cost instead requires s <= 1 - 1/a.

Using the two saved log/rho-zero coefficients, contraction thresholds are .796400 (AAC) and .798225 (other-zone), versus cost thresholds .814401 and .807099. These are distinct thresholds. They support a solver-instability explanation, but the actual system has multiple products, simultaneous manufacturer updates and, in other cells, nesting. We have not derived its full iteration spectrum or re-solved rejected markets. Threshold columns in the CSV are rho-zero single-product benchmarks using each saved beta, not nested-model thresholds.

## Replacement reporting claim

> On the full input sample, negative implied manufacturer costs attach to 61.6–99.96% of Scott single-roll package volume under linear price/AAC, 21.3–80.1% under linear price/other-zone, and 3.05–15.62% under log price. At log price and rho zero, percentage-margin failures occur in 11 high-share store-weeks per scenario, all numerically rejected; dollar-margin failures occur in 18, of which 11 are rejected and seven accepted. Accepted-sample cost results are not an independent validation. These are conditional model-consistency findings, not proof that static manufacturer pricing fails in general.

These percentages use Scott single-roll packages as their denominator. They differ from the earlier all-active-product 39.06% versus 1.70% linear/log AAC comparison. Linear/AAC percentage/rho-zero is 61.65%, dollar/rho-zero 92.70%, and nested dollar cases 99.88–99.96%. Log/rho-zero percentage values are 3.05% and 3.15%; both dollar cases are 4.64%. Keep magnitudes, retailer assumptions and denominators explicit.

The stale retailer paragraph is also corrected: near-equality of effective-cost incidence in the linear/AAC comparison is an observed result for that cell, not a general inability of retailer assumptions to change cost signs. The same-AAC markup diagnostic (18.85%), calibrated percentage costs (22.37%) and dollar costs (37.22%) remain the appropriate separate comparisons on common numerical markets.

## Sample coverage and preservation

The smaller sample claim reproduces: v5 omits 512 broader-v1 store-weeks, including 15 of 79 stores in week 105. Using broader-v1 product coverage for both kept and omitted markets, omitted versus kept median packages/trip are .12168 versus .13259, and median rolls/trip .42644 versus .44917. Pooled rolls/trip are .50219 versus .50312. These summaries do not suggest higher typical volume among omitted markets, but do not prove selection is unrelated to promotions or otherwise innocuous. [Coverage table](sample_coverage.csv), [summary](sample_summary.json).

The check completed with all 358 pre-existing research files byte-identical. Subsequently, only the prose in REVIEW-004's REPORT.md was intentionally corrected, with its exact pre-edit version archived as `prior_review_report.md.txt` here; all historical numerical results and code remain unchanged. The final check records this sole research-document amendment. Fable's supplied message is preserved as `fable_feedback.txt`. No dependencies, source inputs, solver, estimates or saved simulation arrays were changed.

Reproduce the numerical check by copying `verify.py` into a new sibling review directory and running it with `uv run --locked python PATH_TO_COPY`; it refuses to overwrite its output files. No further estimation is scheduled. Consolidate the conditional findings for the written/presentation argument; model identification and measurement limitations remain unresolved.
