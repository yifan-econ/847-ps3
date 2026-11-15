# 2026-11-15: Verification of Fable's research assessment

Work ID: REVIEW-002. Reviewer: Codex in Yifan's session. Input: user-pasted Fable review, which reported read-only post-processing and recommended simple/nested-logit merger analysis. Fable's temporary scripts were not supplied; checks below were independently reconstructed.

Branch/base: `codex/review-001-research-workplan` at `14254a5f4177177fd2d9f0b14c598c299b219096`, with the seven existing review documentation changes preserved. This round adds documentation and ignored local audit artifacts only. No estimation or counterfactual equilibrium was run.

## Verdict

Fable's descriptive work is substantially reproducible, and its recommendation to attempt a bounded merger prototype is useful. The initial workplan was too restrictive about sequencing and the need for a developed vertical model. An explicit passive-retailer rule is a legitimate classroom assumption, not a result established by firm IDs alone.

Several stronger conclusions are unsupported: interaction-heavy test loadings do not identify the lognormal distribution as the source of rejection; one excluded IV cannot identify both endogenous coefficients in nested logit; and cost comparisons require distinguishing manufacturer cost from retail-equivalent cost. The proposed 2%/0.5% price effects and the claim that market-size uncertainty dominates IV uncertainty remain unverified back-of-envelope claims.

## Reproduced numerical evidence

Read-only commands used `uv sync --locked` and inline `uv run --locked python -` scripts. Python/package versions match the preceding [Windows/research validation](2026-11-15-research-review.md). The moment audit loaded six trusted repository pickles one at a time with `pyblp.Problem.solve` patched to raise, and never called estimation or result-writing scripts.

| Specification | Joint statistic | Chi-square(1) p | F(1,23) reference p | Base-IV loading in saved moment coordinates |
|---|---:|---:|---:|---:|
| all-pack household/AAC | 2.875099 | 0.089959 | 0.103456 | 0.110030 |
| all-pack household/other-zone | 5.607109 | 0.017888 | 0.026674 | 0.061877 |
| all-pack income/AAC | 12.650852 | 0.000375 | 0.001678 | -0.068812 |
| all-pack income/other-zone | 12.814244 | 0.000344 | 0.001587 | -0.040636 |
| multipack income/AAC | 13.739989 | 0.000210 | 0.001162 | -0.079698 |
| multipack income/other-zone | 12.084102 | 0.000509 | 0.002043 | -0.043284 |

All six moment Jacobians have shape 4 by 3; the tested null-space direction has dimension one. Statistics match [saved diagnostics](../../Analysis/mixed_logit_v4/results/independent_validation.csv) to floating-point precision. The two-way statistic is the smallest of the independently checked store-only, month-only, and two-way alternatives for all six fits. That numerical ordering is not a general guarantee of conservative inference. An F reference with 23 denominator degrees of freedom is a sensitivity calculation, not a validated two-way few-cluster correction; household/other-zone still rejects at 5% under that reference.

The income interaction-instrument correlations after fixed effects range from -0.9533 to -0.9551. The weighted income-type mean/variance correlation across stores is -0.954330. These confirm Fable's collinearity observation, but not the attribution of rejection to the distributional assumption.

The separate descriptive audit uses the v1 positive-share panel restricted by `date_start` to 1991–1992: **277,363 rows, 8,508 store-weeks, 86 stores**. This differs from both the v3 common-IV sample and v4 complete-market sample.

| Quantity | Independently computed value |
|---|---:|
| Median outside share, one observation per market | 0.868042 |
| Median product count per market | 33 (Fable said about 32) |
| Fraction of rows marked deal | 25.0239% |
| Share of packages sold on deal | 47.9176% |
| Median recorded retail gross margin | 16.75% |
| UPC-week group-mean share of residual price sum of squares | 75.3110% |
| Same statistic for AAC | 94.0120% |
| Incremental partial R-squared from adding UPC-week FE, price / AAC | 75.8127% / 94.6105% |
| Single-roll packages with Scott descriptions | 88.4573% |
| Scott-described packages sold as single rolls | 94.7714% |

Variation calculation: residualize price and AAC on store-by-UPC and week effects using the read-only `absorb` helper from `Analysis/cost_iv_v2/src/estimator.py`. Divide the sum of squares of UPC-week group means (expanded to the observation level) by residual sum of squares. The alternative partial R-squared compares the residual sum of squares after store-by-UPC plus UPC-week absorption with that after store-by-UPC plus week absorption. Fable's rounded 75%/94% numbers reproduce under the first definition.

The [v3 coefficient table](../../Analysis/paper_iv_v3/results/coefficients_first_stages.csv) confirms an all-pack 1991–1992 other-zone first-stage coefficient of 1.049169; the [estimate table](../../Analysis/paper_iv_v3/results/estimates.csv) gives partial R-squared 0.693722. Its AAC conventional 95% intervals contain the other-zone point estimates for both package samples. Neither this containment nor the descriptive IV gap is a formal difference test.

Revenue shares grouped by zero-padded UPC prefix reproduce the provisional major portfolios: `054000` 32.278%, `037000` 30.080%, `042000` 18.508%, `036000` 5.257%. They are sample revenue shares, not national shares or purchase-probability shares. Prefixes and descriptions support an initial ownership mapping, not a complete dated corporate-ownership audit.

## What the joint test can and cannot establish

Let `G` be the saved moment Jacobian, `m` the saved moment vector, `L = null_space(G.T)`, and `Ssum` the sum-of-cluster-scores covariance with store + month - store/month components and cluster-count corrections. The code tests:

`T = (L.T @ m).T @ inv(L.T @ Ssum @ L / N**2) @ (L.T @ m)`.

This is a first-order parameter-estimation-orthogonal moment contrast under the maintained regularity/identification and covariance assumptions. It does not require treating the one-step objective as Hansen's J. Orthogonality reduces sensitivity to small parameter-estimation/optimization errors; it does not justify arbitrary nonstationary or inconsistent estimates.

For all-pack income/AAC, saved-coordinate loadings are approximately `(-0.0688, 0.5823, 0.8100, -0.00143)`. Multiplying only the base moment by 0.001 and transforming the Jacobian/covariance consistently changes its normalized loading magnitude to **0.999895**, while the statistic remains **12.650852**. The same invariance check passed for all six fits. Thus a small raw loading is not a coordinate-invariant measure of which economic assumption failed. Even standardized interaction loadings cannot distinguish conditional IV invalidity, omitted local demand heterogeneity, demographic measurement error, and income functional form. Similar rejection statistics across related specifications also do not identify a unique cause.

## Brand and optimization findings

Confirmed bug: [run_logit.py](../../Archive/ps3_v1/src/run_logit.py), lines 153–154, checks `COTT` before `SCOTT`. All 11 Scott-described UPCs in the 1991–1992 panel (57,813 rows) are labeled Cottonelle. `product_id` remains the UPC; the main UPC estimates are not changed by this label. The brand/pack/variant aggregation is affected. A parent-company mapping needs separate verification: Cottonelle and ScotTissue both belonged to Scott, so a correctly dated parent map need not change despite the brand error. Correct a new derived catalog and add targeted regression coverage when implementing the fix; do not regenerate archived results in place.

Confirmed restart history: [original income/AAC log](../../Analysis/mixed_logit_v4/results/all_packs__income__aac.log) reports optimization failure; [refinement log](../../Analysis/mixed_logit_v4/results/all_packs__income__aac_refinement.log) records zero optimizer iterations at the identical parameters and objective. Its gradient norm is 0.000745390, below the declared 0.001 threshold, with positive reported Hessian eigenvalues and accurate shares. The saved `converged: true` is accurate for that restart and tolerance. Report it as an accepted restart with an initial failure, not a clean independent convergence or a seventh fit.

## Counterfactual and supply assessment

**Merger feasibility:** The local [Hausman–Leonard early version](../../Paper/Hausman_Leonard_2002_public_earlier_version.pdf), pp.30–31, explicitly derives retail-equivalent manufacturer first-order conditions under fixed retailer margins. This supports Fable's general feasibility argument and warrants relaxing the original plan's sequencing. It does not establish that the assumption holds in this sample. The same paper studies Kleenex Bath Tissue; its introduction is therefore a relevant counterfactual precedent.

**Nested logit:** The estimating equation adds endogenous `log(s_j / s_inside)` alongside endogenous price. Keeping deal exogenous, the proposed separate single-AAC and single-other-zone regressions each lack an excluded instrument for the second endogenous regressor. Additional defensible instruments and rank/relevance checks are needed; jointly using both candidates imposes both exclusion restrictions. A fixed nesting grid is an alternative conditional sensitivity, not estimation of nesting. The [official PyBLP tutorial](https://pyblp.readthedocs.io/en/stable/_notebooks/tutorial/logit_nested.html) explicitly instruments within-nest shares; its product-count example cannot be imported uncritically when observed product counts depend on positive sales.

**Retailer rule and cost units:** Under fixed additive margins, write `p_j = w_j + r_j`. If `w_j = AAC_j` is maintained and `mu_j` is the manufacturer markup implied by demand, then manufacturer cost is `c_j = AAC_j - mu_j`. Inverting retail-price FOCs gives `c_eff,j = p_j - mu_j = c_j + r_j`. Comparing `c_eff` directly with AAC is not the same as checking manufacturer cost below wholesale price. Fixed percentage margins require a different transformation and suitable assumptions about margins across jointly owned products.

As an **illustrative diagnostic, not a fitted supply model**, apply the saved v3 all-pack 1991–1992 price coefficients to the broader v1 panel above, provisionally grouping UPC prefixes as portfolios. Homogeneous logit gives `mu_j = 1 / (alpha * (1 - S_f))`, where `S_f` sums product purchase shares for that portfolio in that market. All 277,363 rows have AAC. Results:

| Saved price coefficient source | Negative retail-equivalent cost rows | Negative manufacturer cost rows under fixed additive margins | Package share on rows with negative manufacturer cost |
|---|---:|---:|---:|
| AAC, alpha=2.070537 | 6.79% | 15.51% | 34.67% |
| Other-zone, alpha=2.703845 | 0.37% | 3.80% | 12.09% |

These diagnostics depend on the provisional ownership and sample mismatch and are not final estimates. They show why supply consistency and the wholesale/retail distinction deserve early scrutiny; neither instrument should be selected simply because it yields fewer negative costs. No negative costs were clipped, no prices solved, and no back-of-envelope merger percentage was validated.

**Promotions, aggregation, and sensitivity:** Shared UPC-week variation need not be exclusively promotions; common costs, advertising, and other demand shocks can also generate it. The diagnostics make stockpiling and common shocks important risks but do not prove a specific bias or its sign here. Monthly/zone aggregation needs a new market/share/price/IV construction and changes the economic approximation. It is not an automatic inventory correction. Large outside share makes substitution assumptions worth investigating, but does not establish that market size dominates IV sensitivity without actual comparable exercises. A small exogenous posted-price change and a merger do not generally have identical sensitivity to alpha; in simple logit, calibrated merger dollar changes can scale inversely with alpha while fixed-price quantity responses generally increase in magnitude with alpha.

## Historical checks and limits

- The [SEC record](https://www.sec.gov/enforcement-litigation/administrative-proceedings/34-45653) dates completion of the Kimberly-Clark/Scott merger to December 12, 1995. The [DOJ settlement announcement](https://www.justice.gov/archive/atr/public/press_releases/1995/0486.htm) concerns facial tissue and baby wipes; do not mistake its concentration figures for bathroom tissue. A 1991–1992 exercise is a hypothetical earlier merger under that period's conditions.
- The v1 panel first records Kleenex/KLNX descriptions on July 11, 1991; this is first observed positive sales, not proof of availability or an exact universal launch date. The local Hausman–Leonard paper, p.5, supports the major pre-merger brand affiliations and its KBT subject.
- Three `036000` UPCs with Cottonelle descriptions first appear in 1996, but UPC `3600061115` already appears on April 1, 1993 with the static catalog description `KLEENEX/CNTL 4DBL RL`. The joined UPC description is not time-varying, so the apparent prefix/name transition cannot independently date ownership. [GS1](https://www.gs1us.org/who-we-are/membership/mergers-acquisitions) also documents identifier transfer through ownership changes. Do not infer contemporaneous corporate ownership from a prefix alone.
- No complete historical UPC ownership table, nested-logit rank/weak-IV analysis, new demand estimate, merger equilibrium, bootstrap, or Mac/CI verification was completed. Fable's throwaway scripts were unavailable, so the exact original weighting choices are known only where independently reproduced.

## Preservation and artifacts

The pre-check SHA256 inventory covers the same 194 research files under `Analysis/`, `Archive/`, `Data/`, and `Paper/`, excluding disposable bytecode. Ignored `.local/fable-review/` holds `before.json`, `descriptives.json`, `moment-audit.json`, and `provisional-cost-audit.json`; the substantive calculations and their assumptions are recorded above for collaborators. Final preservation and documentation checks are recorded in the round handoff.

Final outcome: all 194 protected files byte-identical; `git diff --check` passed; all 69 relative links in the nine changed/new Markdown documents resolved. The nine documents include the seven pre-existing review changes. No historical estimate, analysis source, or data file changed.
