# 2026-11-15: Check of Fable's second response

Work ID: REVIEW-003. Reviewer: Codex in Yifan's session. Branch/base: `codex/review-001-research-workplan` at `14254a5f4177177fd2d9f0b14c598c299b219096`. User supplied Fable's response withdrawing estimated nesting with one IV, correcting cost units, and proposing 16 conditional-rho cells. Nine existing uncommitted documentation files were preserved. No project demand model or empirical merger equilibrium was estimated in this check.

## Assessment

The proposed calibrated grid is a workable specification plan, conditional on the stated IV assumptions. It resolves the order-condition problem by fixing rho and estimating only the price coefficient (plus exogenous controls/FE). The transformed dependent variable is correct. See the [official nested-logit equation](https://pyblp.readthedocs.io/en/stable/_notebooks/tutorial/logit_nested.html). Label results as sensitivity to calibrated substitution, not estimated nesting or variation in market size.

The grid is not a confidence set for rho or a guarantee that any listed value is empirically credible. Log package and log per-roll prices differ by a UPC-specific constant when package count is fixed, so their coefficients coincide with the stated fixed effects. This does not resolve the separate package-quantity/shopping-opportunity interpretation of market shares.

For the next prototype, close the attempt to uniquely attribute the old mixed-logit joint rejection. Keep the first-stage and identifying-assumptions memo as a finite deliverable. Scope recommendations are more concrete now; the proposed matrix was not executed or treated as user approval to estimate.

## Independently checked claims

Inline `uv run --locked python -` calculations read the existing v1 panel, v3 instruments, and saved v4 all-pack product keys. The v1 cost checks use 277,363 positive-share rows in 1991–1992, matching the earlier review rather than the narrower proposed estimation sample.

- Median margins: single rolls **10.53%**, 2–4 rolls **20.00%**. Median single-roll AAC **0.494533 dollars/package**.
- Dollar-margin negative manufacturer-cost incidence reproduces **15.5147%** at `a=2.070537` and **3.8001%** at `a=2.703845`. Single rolls comprise **97.5553%** and **95.3416%** of those negative-cost rows, respectively.
- With `q = 1 - median(PROFIT)/100` by store/UPC and the rho-zero linear-price percentage-margin markup formula, the diagnostic `AAC - mu` is negative on **6.6555%** and **0.4528%** of rows. Single rolls comprise **97.9686%** and **85.8280%** of those rows. These reproduce Fable's rounded 6.66%/0.45% and 98%/86% figures.
- The internally calibrated percentage-model manufacturer cost is instead `q*p - mu`; its negative incidence is **6.7428%** and **0.3753%**. This distinction matters when period-median margins do not reproduce weekly AAC. Using weekly margins gives yet another diagnostic; do not mix definitions across tables.

These findings establish concentration of the negative-cost issue in single rolls. They do not prove which demand, cost-measurement, or conduct assumption is wrong, nor prove the direction of bias in incremental merger effects. The earlier statement that costs say nothing about instruments is too absolute: the screen rejects combinations of maintained assumptions; it cannot separately diagnose instrument validity. Its incidence is mechanically decreasing in a with fixed shares/ownership under the dollar-margin simple-logit formula.

## Rank versus validity

Fable's prediction that two IVs will give weak conditional identification is plausible but not established by the response. On the proposed 259,986 v4 all-pack rows, residualize `[price, log(s_j/S), AAC, other_zone_price, deal]` on store-by-UPC/week FE using the repository's read-only `absorb`, then partial out residualized deal and standardize each remaining column. The sample matrix `Z.T @ X / N` is:

```text
              price        log within share
AAC           0.353313     -0.127707
other-zone    0.832724     -0.403626
```

Its singular values are **0.998079** and **0.036332**, and its numerical rank is **2**, not exactly one. This indicates an ill-conditioned direction but is not a Sanderson–Windmeijer conditional F test or evidence of valid exclusion. It neither proves strong identification nor warrants saying both IVs can only identify price by construction. The proposed calibrated grid avoids the need to estimate rho, without settling this broader question.

Demographic interactions do not have an intrinsic rule that they identify alpha but never rho; identification depends on the relevant derivatives/rank and valid moment assumptions. Likewise, the claim that every rival index is absorbed relies on a common fixed product set and a time-only total; actual store-specific totals need not satisfy that identity. None of this establishes a usable additional instrument in this dataset.

For log-IV cells, `E[z*xi]=0` alone does not imply `E[log(z)*xi]=0`. State conditional exogeneity or the transformed moment restriction explicitly. Fixed rho repairs the count of moments, not their economic validity. Keep the estimated signed price coefficient distinct from the positive magnitude used in markup formulas.

## Retailer-rule correction and synthetic check

Fable's dollar- and percentage-margin FOCs and rho-zero markup formulas are correct when `a>0` denotes the magnitude of the negative price coefficient. Its log-price dollar-margin markup formula is also correct for rho zero. At positive rho, use the nested-demand Jacobian; these simple-logit formulas cannot be reused unchanged.

The claim that uniform margins within each owner give identical predictions needs the condition to hold **after merger** too. Different uniform pre-merger margins become dispersion inside the merged firm.

A synthetic two-product counterexample was solved using `scipy.optimize.root` via `uv run --locked python -`; this was an algebra check, not a project-data simulation:

- Baseline prices `(2, 2.5)`, shares `(0.2, 0.15)`, outside share `0.65`, `a=2`.
- Each pre-merger firm owns one product, so its margins are trivially uniform. Fixed percentage margins are `m=(0.1, 0.3)`; write `q=1-m`.
- Set `delta = log(s/s0) + a*p`, `mu0 = 1/[a*(1-s)]`, retail-equivalent cost `c_eff=p-mu0`, and percentage-rule manufacturer cost `c=q*c_eff`. Both rules reproduce the same pre-merger baseline.
- Post-merger dollar-rule FOC is `s + J.T@(p-c_eff)=0`; percentage-rule FOC is `q*s + J.T@(q*p-c)=0`, with `J=-a*(diag(s)-s*s.T)`.
- Dollar-rule post-merger prices: **(2.092124, 2.628889)**.
- Percentage-rule post-merger prices: **(2.072507, 2.665702)**.
- Percentage-rule residual at the dollar solution: approximately **(-0.006364, 0.006364)**.

Both solvers succeeded. Thus equality is not guaranteed by uniform margins within pre-merger owners. This strengthens the case for retaining the proposed percentage sensitivity, rather than dropping it.

Under fixed dollar margins, observed AAC is not needed directly by the price-equilibrium calculation once demand and retail-equivalent costs are given; AAC may still affect predictions through estimation of demand. Under the percentage sensitivity with median margins, use `w0=q*p0` for internally consistent baseline calibration and report observed AAC comparisons separately. Fixed fringe prices are an additional supply assumption, not implied by a passive retailer.

## Qualifications to the proposed diagnostics

- A nesting grid changes substitution at fixed baseline shares/market size; it does not directly test the market-size denominator. Do not call its spread a test that market size dominates instrument choice.
- Low FOC residuals and two starts do not alone establish a profit maximum or uniqueness. State residual units, use a scale-aware criterion, and check local profit curvature/admissibility. Preserve failed cells.
- Cost-screened output can change the market population across cells. Report excluded markets/package volume, distinguish manufacturer and retail-equivalent cost screens, and include a common-market comparison. Do not select price form or IV merely by favorable cost incidence.
- The statement that the same statistic is equivalent to testing **any** extra parameter is too broad without an identified extension and an asymptotic testing argument. The orthogonal contrast does not uniquely diagnose an omitted parameter or guarantee equality to arbitrary finite-sample Wald/LR tests.
- Fable's fixed-parameter store-deletion results were not independently reproduced in this round because the scripts and influence-selection details were not supplied. They are descriptive sensitivity, not re-estimated restricted-sample tests or a bootstrap. A reported increase from 5.6 to 11.1 also does not itself overturn a rejection at 5%.
- Fable's 0.39 pass-through regression was not independently reproduced here. A within-FE association between price and inventory-weighted AAC is not, without identification, a causal pass-through estimate that validates or rejects either retailer rule.
- Fort Howard/prefix ownership remains to be sourced; it was not established by the previously checked Hausman–Leonard p.5 text. Major revenue coverage does not eliminate the need to specify every remaining product's owner or fixed-price status.

## Preservation

Research files were read only. No legacy report generator/validator or estimation entry point ran. The synthetic algebra example did not use project results as an empirical counterfactual. Final hashes and documentation checks are recorded in the round handoff.

Final outcome: all 194 protected research files unchanged; whitespace/diff check passed; 77 relative links in 11 changed/new Markdown documents resolve. The 11-file count includes nine pre-existing changes. No research implementation was modified.
