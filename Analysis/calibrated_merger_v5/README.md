# Conditional nesting and merger exercise (v5)

Authorized on 2026-11-15 by Yifan after the Fable/Codex review. See [decision 003](../../docs/decisions/003-calibrated-merger-design.md). This is a hypothetical Scott/Kimberly-Clark merger under 1991–1992 conditions, not a prediction of the actual 1995 transaction.

The first run is `2026-11-15_16cell_01`: read its [results report](runs/2026-11-15_16cell_01/REPORT.md), [design manifest](runs/2026-11-15_16cell_01/design.json), and [validation record](../../docs/validation/2026-11-15-calibrated-merger.md). Frozen execution sources live inside that run's `code/`; subsequent reporting sources are preserved separately in `postprocessing_code/`.

## Reproduction and preservation

```sh
uv sync --locked
uv run --locked python -m unittest discover -s tests -p test_calibrated_merger.py -v
uv run --locked python Analysis/calibrated_merger_v5/src/run_design.py --run-id YYYY-MM-DD_16cell_unique
uv run --locked python Analysis/calibrated_merger_v5/src/validate_run.py --run-id YYYY-MM-DD_16cell_unique
uv run --locked python Analysis/calibrated_merger_v5/src/report_run.py --run-id YYYY-MM-DD_16cell_unique
```

The runner refuses an existing run directory. Every generated file, including the design, environment, source snapshots, corrected catalog, input keys, fit summaries, cost diagnostics, candidate equilibria, failed-market flags, and preservation inventory, stays under `runs/<run-id>/`. It reads the archived cleaned panel, v3 cross-zone IVs, and saved v4 sample keys. It imports only the IO-free v2 estimator helpers, never legacy writing entry points. It hashes all pre-existing research files before/after, excluding this new v5 directory and disposable bytecode. Failed runs and cells are retained.

Validation/reporting also refuse to overwrite their existing outputs. For the first run only, the inherited estimator's unused `share_upward_sloping` field was wrong in log-price cells because it multiplied by signed log price. `estimates_corrected.csv` repairs that one derived reporting field while preserving the raw results and recording the discrepancy. Actual demand derivatives, simulation markups, costs, elasticities and welfare were already computed by the correct demand engine. The current runner fixes the diagnostic for future runs; it was not rerun to replace the first record.

## Demand and design

Sixteen just-identified 2SLS cells: two price forms (linear/log), two IV families (AAC/other-zone), four calibrated rho values (0, .25, .5, .75). For fixed rho the dependent variable is `log(s/s0) - rho*log(s/S)`. Price and IV are logged together in log-price cells. Instruments in levels versus logs impose distinct moment assumptions; neither is established by the first stage. Store-by-UPC and week FE, exogenous deal, store/month two-way sandwich with cluster and absorbed-FE count corrections follow the existing estimator. Only 24 months support approximate inference. There is no overidentification test with positive degrees of freedom. First-stage Wald is not an effective F/KP statistic.

Demand uses one inside nest and a singleton outside option. All cells use the same complete-market v4 all-pack sample. All original product shares and the traffic denominator are retained. Non-price utilities, including recovered unobservables and deal, are fixed in simulation. These are static package-purchase models; zero-sales selection and stockpiling remain unresolved. Rho is calibrated, not estimated; the grid is not a confidence interval and does not vary market size.

## Ownership and conduct

The new catalog corrects Scott brand labels without touching v1. Zero-padded UPC prefixes are linked to observed brand descriptions and historical company evidence; this is an explicit analytical mapping, not a claim that prefixes themselves establish ownership for all dates:

| Prefix | 1991–1992 portfolio / conduct | Evidence |
|---|---|---|
| 054000 | Scott (ScotTissue, Cottonelle) | Hausman–Leonard, p.5 |
| 036000 | Kimberly-Clark (Kleenex, Delsey) | Kleenex affiliation in Hausman–Leonard, p.5; Delsey grouped by same prefix in UPC catalog |
| 037000 | P&G (Charmin, White Cloud) | Charmin affiliation in Hausman–Leonard, p.5; White Cloud grouped by prefix |
| 042000 | James River (Northern) | Hausman–Leonard, p.5 |
| 030400 | Georgia-Pacific (Angel Soft, Coronet) | Angel Soft affiliation in Hausman–Leonard, p.5; Coronet grouped by prefix |
| 073310 | Fort Howard (Green Forest, Soft N Gentle) | University of Wisconsin–Green Bay Fort Howard archive, product labels; FTC-hosted 1992 Green Forest advertising record |
| 038281, 070524, 075725 | Dominick's private label / generic fringe; prices fixed | Catalog descriptions; fixed-price conduct is a maintained assumption, not inferred supplier ownership |

[Hausman–Leonard local early version](../../Paper/Hausman_Leonard_2002_public_earlier_version.pdf); [Fort Howard corporate archive](https://www.uwgb.edu/UWGBCMS/media/Archives-and-ARC/files/Fort-Howard-company-records.pdf); [FTC-hosted advertising record, Green Forest case dated April 1, 1992](https://www.ftc.gov/sites/default/files/documents/public_comments/guides-use-environmental-marketing-claims-534743-00035/534743-00035.pdf). Historical prefix grouping of non-anchor brands remains a maintained mapping limitation, recorded rather than silently asserted to be a complete trademark-title audit.

Scott and Kimberly-Clark become one portfolio; four named rivals reoptimize and fringe prices stay observed. Fixed fringe prices are an additional assumption. No efficiencies, product exits, entry, assortment changes, or dynamic inventories are modeled.

## Retail margins, numerical checks, and reporting

Dollar margins apply to all 16 cells. FOCs recover retail-equivalent costs `p - markup`; manufacturer cost `AAC - markup` is a diagnostic under the wholesale-proxy assumption. Four rho-zero cells additionally use fixed percentage margins. Let `q=1-m`, where `m` is the store/UPC median recorded margin in the full 1991–1992 positive-sales window. Percentage-rule baseline wholesale prices are `q*p`, manufacturer costs are `q*p-markup`, and `AAC-markup` is a separate proxy diagnostic. Differing margins across merging portfolios matter after merger.

Interpret saved markup/cost arrays only where `firm > 0` in `product_inputs.csv.gz`. Fixed-price fringe rows contain vectorized placeholders (including zero calibrated costs); these are neither inferred fringe costs nor used in cost screens or profit optimization. Price/share arrays still cover every product.

The single-nest Jacobian admits an exact ownership-block inverse. We use it for markup iteration with damping .5, at most 600 iterations, two post-merger starts (observed prices and 10% higher), and a baseline reproduction solve from 2% higher prices. Prices remain positive through step shortening; costs are never clipped. Accepted markets require baseline prices within 1e-8 dollars, scaled and absolute FOCs below 1e-8, starts agreeing within 1e-7 dollars, and negative-definite firm profit Hessians at baseline/post-merger stationary points. This checks local optimality, not global equilibrium uniqueness. Candidate prices and failures are saved even when excluded from reported equilibria.

Price changes use baseline package weights. Report all numerically valid markets, cell-specific cost-admissible samples, and common intersections across all 20 retailer/demand scenarios, with market/package coverage. Manufacturer and retail-equivalent cost screens are distinct. No IV or price form is chosen by a favorable cost screen. Welfare is the change in the correctly normalized nested inclusive value divided by positive price sensitivity for linear-price cells only, per shopping opportunity and multiplied by market traffic; no dollar welfare is reported for log-price cells. Scenario spreads are not sampling confidence intervals.

## Implemented equations

For one market, let `S=sum(s)`, `h=1/(1-rho)`, `A=1+(h-1)/S`, and `b_j=beta` for linear price or `beta/p_j` for log price. The Jacobian has rows for shares and columns for prices:

```text
J_jk = b_k * [h*s_j*1(j=k) - A*s_j*s_k].
```

For owner f, retail-coordinate profit is `sum_j (q_j*p_j-c_j)*s_j`. Under dollar margins, `q=1` and c is retail-equivalent cost; under percentage margins, `q=1-m` and c is manufacturer cost. Multiplying by fixed market traffic does not affect its optimum. The FOC is `q*s + J_f'*(q*p-c)=0`. Let `mu=q*p-c`, `u_j=-q_j/(h*b_j)`, and `S_f=sum_f s`. Its exact block solution is

```text
C_f = sum_f(s_j*u_j) / [1-(A/h)*S_f]
mu_j = u_j + (A/h)*C_f.
```

Costs are inverted at observed prices and held fixed. The post-merger fixed point updates prices toward `(c+mu(p))/q` for active manufacturers. Fixed fringe products enter all demand sums but their FOCs are not imposed.

Baseline mean utilities are `delta_j=log(s_j/s_out)-rho*log(s_j/S)`. At counterfactual prices add `beta*(p_j-p0_j)` or `beta*log(p_j/p0_j)` to delta. Write `L=logsumexp(h*delta)`. Inside share is `logistic(L/h)` and within-inside shares are `softmax(h*delta)`. Linear-price consumer surplus change is `[log(1+exp(L_post/h))-log(1+exp(L_pre/h))]/(-beta)`. This normalization includes the outside option; no additional factor of `1-rho` belongs outside that outer log.
