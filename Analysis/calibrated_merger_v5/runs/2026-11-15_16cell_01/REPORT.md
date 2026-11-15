# Conditional merger results: 2026-11-15_16cell_01

Completed the authorized 16 demand cells and 20 supply scenarios on 259,986 observations, 7,996 store-weeks, 83 stores and 50 UPCs. All demand coefficients are negative. This is a conditional hypothetical Scott/Kimberly-Clark merger at 1991–1992 conditions. Rho is calibrated, not estimated. No preferred causal model is selected.

Run time: 21.0 minutes. All 194 pre-existing research files are byte-identical. [Manifest](design.json), [status](status.json), [preservation](preservation.json), [sample audit](sample_audit.json), and [methods/ownership](../../README.md) record provenance and assumptions.

The sample retains 94.31% of packages in the full 1991–1992 positive-sales panel. Its median outside share is 86.74%; fixed-price fringe accounts for 9.25% of baseline packages. The separate catalog corrects 10 Scott UPC labels present in this sample. Missing zero sales and actual availability remain unresolved.

## First stages and conditional demand

Only four first stages are distinct. Wald chi-square is not a KP/effective-F statistic and does not establish exclusion. Level/log instrument transformations require their own valid moment assumptions. Deal exogeneity, common demand shocks across zones, AAC endogeneity, static purchase behavior and only 24 month clusters remain limitations. Standard errors are conditional on rho and use the existing two-way store/month sandwich; no counterfactual uncertainty is propagated.


| form | iv | first_stage_wald_chi2 | first_stage_partial_r2 |
| --- | --- | --- | --- |
| linear | aac | 101.4494 | 0.1248 |
| linear | other_zone | 1315.5675 | 0.6934 |
| log | aac | 44.5856 | 0.1105 |
| log | other_zone | 3245.6933 | 0.7879 |

Price coefficients and SE have different units across linear/log forms. Own/category elasticities are medians; diversion is baseline Scott-package weighted.

| model | beta_price | se_price | median_own_elasticity | category_elasticity_median | scott_to_kc_diversion_packages |
| --- | --- | --- | --- | --- | --- |
| linear__aac__rho00 | -2.028 | 0.319 | -2.3257 | -1.8732 | 0.0064 |
| linear__aac__rho25 | -1.5256 | 0.2391 | -2.3205 | -1.4091 | 0.0152 |
| linear__aac__rho50 | -1.0232 | 0.1591 | -2.3217 | -0.9451 | 0.0244 |
| linear__aac__rho75 | -0.5208 | 0.0794 | -2.3498 | -0.481 | 0.034 |
| linear__other_zone__rho00 | -2.6893 | 0.1642 | -3.0841 | -2.484 | 0.0064 |
| linear__other_zone__rho25 | -2.0155 | 0.1231 | -3.0657 | -1.8616 | 0.0152 |
| linear__other_zone__rho50 | -1.3418 | 0.0821 | -3.0446 | -1.2393 | 0.0244 |
| linear__other_zone__rho75 | -0.668 | 0.0411 | -3.0144 | -0.617 | 0.034 |
| log__aac__rho00 | -5.3879 | 0.5582 | -5.3762 | -4.6736 | 0.0064 |
| log__aac__rho25 | -4.0682 | 0.4167 | -5.3934 | -3.5288 | 0.0152 |
| log__aac__rho50 | -2.7486 | 0.2761 | -5.4467 | -2.3841 | 0.0244 |
| log__aac__rho75 | -1.4289 | 0.1394 | -5.6432 | -1.2394 | 0.034 |
| log__other_zone__rho00 | -5.184 | 0.2085 | -5.1727 | -4.4967 | 0.0064 |
| log__other_zone__rho25 | -3.8857 | 0.1561 | -5.1514 | -3.3705 | 0.0152 |
| log__other_zone__rho50 | -2.5873 | 0.1036 | -5.1273 | -2.2443 | 0.0244 |
| log__other_zone__rho75 | -1.289 | 0.0513 | -5.0908 | -1.1181 | 0.034 |

## Counterfactuals on a common numerical sample

Common intersection across all 20 scenarios: **7,960 markets**. The intersections additionally requiring all active effective costs or manufacturer costs nonnegative contain **538** and **0** markets, respectively. An empty intersection is reported as empty, never replaced by a favorable cell-specific sample.


Baseline-package-weighted percentage price changes, common numerical sample (negative costs permitted and disclosed):

| cell | retailer | Scott | Kimberly-Clark | rivals | fringe | all |
| --- | --- | --- | --- | --- | --- | --- |
| linear__aac__rho00 | dollar | 0.5465 | 2.8179 | 0.0013 | 0.0 | 0.3762 |
| linear__aac__rho00 | percentage | 0.4939 | 3.1237 | 0.0013 | 0.0 | 0.3705 |
| linear__aac__rho25 | dollar | 1.558 | 7.9254 | 0.0242 | 0.0 | 1.0757 |
| linear__aac__rho50 | dollar | 2.9779 | 14.9836 | 0.085 | 0.0 | 2.0643 |
| linear__aac__rho75 | dollar | 4.8235 | 24.3446 | 0.1988 | 0.0 | 3.3744 |
| linear__other_zone__rho00 | dollar | 0.4121 | 2.125 | 0.001 | 0.0 | 0.2837 |
| linear__other_zone__rho00 | percentage | 0.3724 | 2.3556 | 0.001 | 0.0 | 0.2794 |
| linear__other_zone__rho25 | dollar | 1.1793 | 5.999 | 0.0183 | 0.0 | 0.8142 |
| linear__other_zone__rho50 | dollar | 2.2708 | 11.4258 | 0.0648 | 0.0 | 1.5742 |
| linear__other_zone__rho75 | dollar | 3.7601 | 18.9775 | 0.155 | 0.0 | 2.6305 |
| log__aac__rho00 | dollar | 0.2585 | 1.0284 | 0.001 | 0.0 | 0.162 |
| log__aac__rho00 | percentage | 0.2345 | 1.125 | 0.0009 | 0.0 | 0.1571 |
| log__aac__rho25 | dollar | 0.7407 | 3.0542 | 0.0219 | 0.0 | 0.4782 |
| log__aac__rho50 | dollar | 1.3996 | 5.8782 | 0.0782 | 0.0 | 0.9254 |
| log__aac__rho75 | dollar | 2.129 | 9.2678 | 0.1762 | 0.0 | 1.4499 |
| log__other_zone__rho00 | dollar | 0.2711 | 1.0786 | 0.001 | 0.0 | 0.1699 |
| log__other_zone__rho00 | percentage | 0.246 | 1.1799 | 0.001 | 0.0 | 0.1648 |
| log__other_zone__rho25 | dollar | 0.7853 | 3.2362 | 0.0234 | 0.0 | 0.507 |
| log__other_zone__rho50 | dollar | 1.5148 | 6.352 | 0.0856 | 0.0 | 1.0014 |
| log__other_zone__rho75 | dollar | 2.4392 | 10.5796 | 0.2057 | 0.0 | 1.6608 |

## Numerical and cost coverage

Counts below are out of 7,996 markets. Cost screens require **every active manufacturer product** in a market to pass. Package coverage fractions use all baseline sample packages. These screens are model diagnostics, not model-selection tests. Failure counts and candidate prices remain saved.

| cell | retailer | numerically_valid | effective_nonnegative | manufacturer_nonnegative | effective_package_coverage | manufacturer_package_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| linear__aac__rho00 | dollar | 7982 | 5310 | 945 | 0.5628 | 0.0805 |
| linear__aac__rho00 | percentage | 7982 | 5323 | 5323 | 0.5639 | 0.5639 |
| linear__aac__rho25 | dollar | 7980 | 3397 | 0 | 0.3651 | 0.0 |
| linear__aac__rho50 | dollar | 7978 | 1440 | 0 | 0.1613 | 0.0 |
| linear__aac__rho75 | dollar | 7960 | 538 | 0 | 0.0561 | 0.0 |
| linear__other_zone__rho00 | dollar | 7982 | 7809 | 7549 | 0.917 | 0.8646 |
| linear__other_zone__rho00 | percentage | 7982 | 7807 | 7807 | 0.9166 | 0.9166 |
| linear__other_zone__rho25 | dollar | 7980 | 7382 | 6872 | 0.8299 | 0.7481 |
| linear__other_zone__rho50 | dollar | 7978 | 6044 | 4856 | 0.6617 | 0.5151 |
| linear__other_zone__rho75 | dollar | 7960 | 4161 | 2440 | 0.439 | 0.2578 |
| log__aac__rho00 | dollar | 7985 | 7985 | 7978 | 0.9889 | 0.9831 |
| log__aac__rho00 | percentage | 7985 | 7985 | 7985 | 0.9889 | 0.9889 |
| log__aac__rho25 | dollar | 7985 | 7984 | 7974 | 0.9884 | 0.9796 |
| log__aac__rho50 | dollar | 7985 | 7975 | 7958 | 0.9809 | 0.9699 |
| log__aac__rho75 | dollar | 7978 | 7948 | 7870 | 0.9649 | 0.9361 |
| log__other_zone__rho00 | dollar | 7985 | 7985 | 7978 | 0.9889 | 0.9831 |
| log__other_zone__rho00 | percentage | 7985 | 7985 | 7985 | 0.9889 | 0.9889 |
| log__other_zone__rho25 | dollar | 7985 | 7983 | 7971 | 0.9875 | 0.9778 |
| log__other_zone__rho50 | dollar | 7985 | 7973 | 7952 | 0.9792 | 0.9667 |
| log__other_zone__rho75 | dollar | 7978 | 7936 | 7817 | 0.9593 | 0.92 |

[All six reporting scopes and groups](counterfactual_summary.csv) include full numerical coverage, cell-specific screens and common intersections. [Equilibrium diagnostics](equilibrium_diagnostics.csv) report maxima over **all attempted markets**, including failures; those maxima are not residuals of accepted solutions. [Per-market files](cells/) identify convergence, reproduction, start agreement and curvature failures separately.


## Cost diagnostics by package size

Below: fraction of baseline packages attached to negative-cost active products, before numerical or market-level cost screens. Dollar-rule manufacturer costs use AAC as wholesale proxy; percentage-rule manufacturer costs use calibrated q*p. They are distinct assumptions. [Full cost table](cost_diagnostics.csv) also includes counts, medians and AAC-proxy costs.

| cell | retailer | 2_to_4 | 5_plus | all | single |
| --- | --- | --- | --- | --- | --- |
| linear__aac__rho00 | dollar | 0.0937 | 0.0001 | 0.3906 | 0.927 |
| linear__aac__rho00 | percentage | 0.0382 | 0.0001 | 0.2468 | 0.6165 |
| linear__aac__rho25 | dollar | 0.1337 | 0.0001 | 0.4384 | 0.9988 |
| linear__aac__rho50 | dollar | 0.2207 | 0.0001 | 0.4853 | 0.9996 |
| linear__aac__rho75 | dollar | 0.3358 | 0.0014 | 0.547 | 0.9992 |
| linear__other_zone__rho00 | dollar | 0.0395 | 0.0 | 0.1057 | 0.2303 |
| linear__other_zone__rho00 | percentage | 0.0035 | 0.0 | 0.08 | 0.2127 |
| linear__other_zone__rho25 | dollar | 0.0607 | 0.0 | 0.1803 | 0.4025 |
| linear__other_zone__rho50 | dollar | 0.1234 | 0.0001 | 0.29 | 0.6096 |
| linear__other_zone__rho75 | dollar | 0.211 | 0.0003 | 0.4074 | 0.8015 |
| log__aac__rho00 | dollar | 0.0 | 0.0 | 0.017 | 0.0464 |
| log__aac__rho00 | percentage | 0.0 | 0.0 | 0.0112 | 0.0305 |
| log__aac__rho25 | dollar | 0.0 | 0.0 | 0.0201 | 0.0547 |
| log__aac__rho50 | dollar | 0.0004 | 0.0 | 0.0283 | 0.0766 |
| log__aac__rho75 | dollar | 0.0167 | 0.0 | 0.0587 | 0.1354 |
| log__other_zone__rho00 | dollar | 0.0 | 0.0 | 0.017 | 0.0464 |
| log__other_zone__rho00 | percentage | 0.0 | 0.0 | 0.0116 | 0.0315 |
| log__other_zone__rho25 | dollar | 0.0 | 0.0 | 0.0214 | 0.0583 |
| log__other_zone__rho50 | dollar | 0.0021 | 0.0 | 0.0315 | 0.0827 |
| log__other_zone__rho75 | dollar | 0.0325 | 0.0 | 0.0748 | 0.1562 |

## Consumer surplus

Linear-price only; traffic-weighted dollars per shopping opportunity on the common numerical sample. Total dollars sum modeled opportunities across retained store-weeks; they are not a consumer panel or a forecast of the actual 1995 merger. Values are scenario outputs, not confidence intervals.

| cell | retailer | welfare_per_opportunity | welfare_total_dollars |
| --- | --- | --- | --- |
| linear__aac__rho00 | dollar | -0.000423 | -65514.63336 |
| linear__aac__rho00 | percentage | -0.000426 | -65906.034358 |
| linear__aac__rho25 | dollar | -0.001182 | -183057.006881 |
| linear__aac__rho50 | dollar | -0.002181 | -337732.224793 |
| linear__aac__rho75 | dollar | -0.003408 | -527840.418603 |
| linear__other_zone__rho00 | dollar | -0.000319 | -49405.941876 |
| linear__other_zone__rho00 | percentage | -0.000321 | -49701.105474 |
| linear__other_zone__rho25 | dollar | -0.000895 | -138561.074345 |
| linear__other_zone__rho50 | dollar | -0.001663 | -257539.797037 |
| linear__other_zone__rho75 | dollar | -0.002657 | -411470.306113 |

## Validation and limits

Accepted markets require baseline reproduction, two post-merger starts, absolute/scaled FOC checks and local negative-definite profit Hessians. Local checks do not prove global Nash equilibrium or uniqueness. Negative costs are never clipped. Log-price dollar welfare is deliberately absent. Rho variation changes substitution at fixed market size; no traffic-denominator robustness is claimed. Saved markup/cost arrays are meaningful only for firm > 0; fixed-price fringe entries are unused placeholders, not inferred costs.

The raw estimator emits an irrelevant upward-slope diagnostic using signed log prices. [Corrected demand table](estimates_corrected.csv) fixes only that reporting field, with [audit](reporting_correction.json); original estimates remain preserved. Actual demand derivatives, simulations and reported own elasticities already use the correct formulas.

No extra cells, data-dependent restarts, mixed-logit refinement or aggregation were added after inspecting results. [Independent validation](independent_validation.json) checks saved outputs without new estimation; [repository validation record](../../../../docs/validation/2026-11-15-calibrated-merger.md) records runtime evidence and limitations.
