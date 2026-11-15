# Targeted cost-failure diagnosis

Date: 2026-11-15. Run: 2026-11-15_costdiag_01. Source: the committed [16-cell / 20-scenario run](../../../calibrated_merger_v5/runs/2026-11-15_16cell_01/REPORT.md), commit d5fcf7c9b0c9cc44cdf382f634904e2082618669. This diagnosis uses saved parameters, quantities and baseline cost arrays. **No estimation, equilibrium solve, cost clipping, ownership change or product/market deletion ran.**

## What the diagnosis establishes

1. **Scott single rolls dominate the linear/AAC problem.** On the common numerical sample at rho zero, Scott accounts for 86.28% of package volume attached to negative manufacturer costs; five Scott UPCs account for 84.69%. P&G contributes another 12.48%. These are shares of negative-cost package volume, not fractions of manufacturers or markets.
2. **There is more than one mechanical channel.** In that cell, 29.11% of negative manufacturer-cost package volume already fails the singleton-own-elasticity check; 31.05% first fails when the manufacturer's portfolio is priced jointly; 39.84% has nonnegative effective cost but turns negative after the AAC-implied retailer wedge. These categories are ordered accounting comparisons, not causal estimates.
3. **Higher rho strengthens the portfolio effect even when own elasticities look stable.** For Scott white single-roll UPC 5400041500, the weighted portfolio markup grows from $0.582 to $1.013 across the linear/AAC rho grid, against a fixed weighted retail price of $0.525 and AAC of $0.478. Its singleton markup grows only from $0.520 to $0.574.
4. **Retailer assumptions alter manufacturer-cost interpretation much more than effective-cost feasibility here.** At linear/AAC rho zero on common markets, negative manufacturer-cost package incidence falls from 37.22% to 22.37% under percentage margins. Effective-cost incidence barely changes, from 22.39% to 22.37%. Percentage margins therefore do not repair the demand/portfolio-implied effective-cost failures.
5. **The common numerical sample hides a concentrated log-price tail.** All 18 full-sample log/AAC rho-zero manufacturer-cost-failing markets are excluded from the common 7,960-market intersection. Their category shares range from 68.29% to 99.986%. Raw movement and seven-day traffic reconciliation passes, so these are observed input patterns rather than a discrepancy introduced by the v5 pipeline. They raise a purchase-unit/market-size interpretation issue, without proving stockpiling or erroneous raw data.

The current model remains useful as a conditional sensitivity exercise. These findings narrow the mechanical explanation but do not validate an IV, identify rho, establish true manufacturer marginal costs, or select log price because its cost signs look better.

## Definitions and comparison samples

All package weights are baseline MOVE; they are not roll counts or expenditure. Cost diagnostics cover 44 UPCs belonging to six active manufacturers. Six private-label/generic UPCs have fixed prices and no inferred costs. Unless explicitly marked full input, the tables below use the same 7,960 numerically accepted markets across all 20 source scenarios. Full-input tables use all 7,996 markets, including numerical failures; baseline cost inversion remains an accounting diagnostic there, not an accepted merger equilibrium.

Let p be retail package price, q=1 under dollar margins or one minus the store/UPC median retailer percentage margin, and mu the manufacturer markup from the relevant FOCs. Effective cost is p-mu/q. Manufacturer cost is AAC-mu under dollar margins, or q*p-mu under percentage margins. For dollar margins, manufacturer cost equals effective cost minus (p-AAC). AAC is an acquisition-cost proxy, not observed manufacturer marginal cost.

With signed price derivative b (beta for linear price, beta/p for log price), h=1/(1-rho), S the inside share, and A=1+(h-1)/S, the hypothetical singleton retail-equivalent markup is -1/[b*(h-A*s_j)]=p/abs(own elasticity). This is a baseline derivative diagnostic holding shares fixed, not a newly solved market with changed ownership. The exact portfolio markup is independently reconstructed and checked against every saved active-product markup.

For negative manufacturer-cost rows, the ordered partition is: (i) singleton markup already exceeds retail price; (ii) singleton passes but portfolio markup/q exceeds retail price; (iii) portfolio effective cost passes but AAC-mu is negative. Category (iii) exists only for the dollar-rule manufacturer-cost diagnostic. Other assumptions interact, so the partition must not be described as identifying a unique economic cause. Negative recorded retailer margins can also rescue some negative effective costs; the tables retain this possibility rather than assuming p>=AAC.

## Manufacturer and UPC concentration

Linear price, AAC IV, rho zero, fixed dollar margins; common numerical sample. A sole-failing-owner count means all negative-cost products in that market belong to that owner. It is an attribution of failed screens, not a simulation deleting that firm.

| Manufacturer | Own packages with negative cost (%) | Share of all negative-cost packages (%) | Markets with a failure | Sole failing owner markets |
| --- | --- | --- | --- | --- |
| Fort Howard | 0.15 | 0.02 | 231 | 60 |
| Georgia-Pacific | 0.54 | 0.06 | 1 | 1 |
| James River | 0.0 | 0.0 | 0 | 0 |
| Kimberly-Clark | 7.44 | 1.17 | 20 | 7 |
| Procter & Gamble | 19.19 | 12.48 | 210 | 36 |
| Scott | 70.1 | 86.28 | 6911 | 6553 |

Top five UPCs by negative manufacturer-cost package volume in the same cell/sample:

| UPC | Description (single roll) | Within-UPC negative packages (%) | Share of all negative-cost packages (%) |
| --- | --- | --- | --- |
| 5400041500 | $SCOTT WHITE BATH TI | 90.83 | 33.57 |
| 5400046550 | $SCOTT BEIGE BATH TI | 92.5 | 14.53 |
| 5400046510 | $SCOTT PINK BATH TIS | 92.42 | 13.27 |
| 5400046520 | SCOTT SINGLE BATH TI | 92.14 | 12.73 |
| 5400046530 | $SCOTT YELLOW BATH T | 94.66 | 10.59 |

The five descriptions above are Scott single-roll products, not Cottonelle multipacks. The new v5 catalog already corrected their historical brand labels; this diagnosis does not change ownership or any catalog. All 44 active UPCs and six manufacturers are retained in [group_diagnostics.csv](group_diagnostics.csv), including full-input results.

## Why nesting magnifies costs

For linear price with dollar margins, all products of a given manufacturer in one market have the same implied dollar markup:

```text
mu_f = 1 / [abs(beta) * (h - A*S_f)]
     = (1 / (h*abs(beta))) / [1 - ((1-rho)*S_f + rho*S_f/S)].
```

As rho rises, the denominator increasingly uses the manufacturer's share within the tissue category. A manufacturer with many close substitutes internalizes more diversion. In the estimated linear/AAC grid the base term 1/(h*abs(beta)) barely changes; the portfolio denominator drives much of the increase. This is conditional on the saved shares and estimated beta at each calibrated rho, not a claim that rho was identified.

The following values are baseline-package-weighted means for Scott white UPC 5400041500 on common markets. Retail price is $0.5248 and AAC $0.4783 throughout. Means help explain magnitudes; row-level signs, not signs of means, determine failure rates.

| Cell | Base markup ($) | Singleton markup ($) | Portfolio markup ($) | Negative manufacturer-cost packages (%) |
| --- | --- | --- | --- | --- |
| linear__aac__rho00 | 0.4931 | 0.5196 | 0.5821 | 90.8285 |
| linear__aac__rho25 | 0.4916 | 0.5387 | 0.6707 | 99.8648 |
| linear__aac__rho50 | 0.4887 | 0.5583 | 0.8004 | 99.9644 |
| linear__aac__rho75 | 0.4801 | 0.5736 | 1.0134 | 99.9064 |

In log/AAC rho zero, the same UPC has a weighted singleton markup of $0.1021 and portfolio markup of $0.1162 on common markets. Log price makes the base markup proportional to the product price; linear price imposes a common dollar base. Its different estimated coefficient also matters. This comparison cannot isolate functional form from the fitted parameter or establish that log price is correct.


Ordered breakdown of negative manufacturer-cost package volume, dollar margins/common markets (%):

| Cell | Singleton already fails | Portfolio first crosses retail price | Retailer wedge only |
| --- | --- | --- | --- |
| linear__aac__rho00 | 29.11 | 31.05 | 39.84 |
| linear__aac__rho25 | 33.4 | 38.07 | 28.54 |
| linear__aac__rho50 | 34.06 | 50.33 | 15.61 |
| linear__aac__rho75 | 31.39 | 59.14 | 9.46 |
| linear__other_zone__rho00 | 41.32 | 25.02 | 33.66 |
| linear__other_zone__rho25 | 23.78 | 53.59 | 22.63 |
| linear__other_zone__rho50 | 14.64 | 62.49 | 22.87 |
| linear__other_zone__rho75 | 12.08 | 70.91 | 17.01 |

## Separating the retailer rules

At rho zero the exact difference in manufacturer costs is

```text
c_percentage - c_dollar = (q*p - AAC) + (mu_dollar - mu_percentage).
```

For linear/AAC common-market active packages, weighted mean manufacturer cost increases by $0.06760: the wholesale-level term is -$0.01776 and the markup term is +$0.08536. Weighted mean effective cost changes by only -$0.000022. Mean changes do not determine sign-transition rates because the changes vary across products/markets. These are algebraic effects of the maintained rules, not evidence that actual retailer behavior changed.

The 2x2 accounting table below holds saved markup vectors fixed while changing the wholesale-price input. Only the diagonal entries correspond to the two source structural scenarios. Off-diagonal hybrids are diagnostic arithmetic, not additional estimated or simulated models.

| Wholesale input | Markup vector | Negative packages (%) | Passing markets | Interpretation |
| --- | --- | --- | --- | --- |
| observed_AAC | dollar_FOC | 37.217 | 945 | saved scenario |
| observed_AAC | percentage_FOC | 18.852 | 5616 | accounting hybrid only; not a structural scenario |
| median_margin_qp | dollar_FOC | 35.855 | 1350 | accounting hybrid only; not a structural scenario |
| median_margin_qp | percentage_FOC | 22.368 | 5323 | saved scenario |

The full [retailer bridge](retailer_bridge.csv) reports transitions, mean components and effective-cost changes by UPC/manufacturer/pack for all four rho-zero pairs. The small aggregate effective-cost change does not establish exact equivalence of the rules, especially after Scott and Kimberly-Clark combine portfolios with different margins.

## Cost failures outside the common numerical sample

Manufacturer-negative package percentages among active products, dollar margins. Full-input and common-sample denominators differ. The reduction for log-price models is sample selection, not a correction of their full-input cost failures.

| Cell | Full input negative packages (%) | Common numerical negative packages (%) |
| --- | --- | --- |
| linear__aac__rho00 | 39.062 | 37.217 |
| linear__aac__rho25 | 43.841 | 42.152 |
| linear__aac__rho50 | 48.53 | 46.992 |
| linear__aac__rho75 | 54.697 | 53.36 |
| linear__other_zone__rho00 | 10.574 | 7.796 |
| linear__other_zone__rho25 | 18.031 | 15.497 |
| linear__other_zone__rho50 | 28.998 | 26.821 |
| linear__other_zone__rho75 | 40.742 | 38.948 |
| log__aac__rho00 | 1.704 | 0.0 |
| log__aac__rho25 | 2.009 | 0.0 |
| log__aac__rho50 | 2.833 | 0.114 |
| log__aac__rho75 | 5.866 | 2.949 |
| log__other_zone__rho00 | 1.704 | 0.0 |
| log__other_zone__rho25 | 2.143 | 0.0 |
| log__other_zone__rho50 | 3.151 | 0.332 |
| log__other_zone__rho75 | 7.478 | 4.612 |

All 18 log/AAC rho-zero manufacturer-cost-failing markets involve Scott. Eleven fail that scenario's numerical checks; seven pass its own numerical checks but fail the all-scenario intersection. Thus zero failures on the common sample must not be described as universal log-price cost consistency. The 18 markets occur in 12 stores and four weeks: seven in week 99 (1991-08-01), nine in week 110 (1991-10-17), and one each in weeks 117 and 149. Their category shares are 0.6829–0.99986, Scott accounts for 90.34%–97.26% of inside packages, and Scott weighted prices are about $0.339–$0.410.

Store 124/week 110 is particularly revealing: 29,209 tissue packages versus 29,213 shopping trips. Five Scott single-roll UPCs alone contribute 27,916 packages, all recorded at PRICE=$0.39 and QTY=1, with SALE=B. This is not a multi-buy QTY division discrepancy. It is consistent with pressure on the one-package-per-shopping-opportunity approximation; raw measurement error, multipackage purchasing and intertemporal substitution remain possibilities, not established explanations. One must not inflate traffic or delete these observations merely to make costs positive.

The raw audit reconciles every saved row's MOVE, PRICE/QTY, AAC and deal flag against wtti.csv, and every market's seven positive daily customer counts against ccount.dta. All checks pass. This validates provenance and arithmetic, not the accuracy of the underlying records or the interpretation of packages as choice probabilities. See [audit evidence](raw_input_audit.json), [all 18 weekly records](tail_weekly_audit.csv), [their source movement records](tail_movement_records.csv), and [daily traffic](tail_daily_traffic.csv). [Market exposure](market_exposure.csv) covers all 7,996 markets; [all-input examples](all_input_examples.csv) preserve extreme cases that the common sample excludes.

## Algebraic price-sensitivity thresholds

At fixed observed shares, rho, functional form and retailer q, every markup scales as 1/abs(beta). Thus a market's minimum multiplier on the saved abs(beta) for every active cost to become nonnegative is the maximum markup/relevant-price ratio across its products. For effective costs use mu/(q*p); for dollar-rule manufacturer costs use mu/AAC; for percentage-rule manufacturer costs use mu/(q*p).

These are accounting feasibility thresholds, not estimated parameters, confidence bounds, weak-IV tests or recommended coefficient adjustments. The 95% column weights markets by all baseline market packages and refers to passing whole markets, not 95% of individual product rows.

| Cell | Multiplier for 50% package coverage | Multiplier for 95% package coverage | Multiplier for every common market |
| --- | --- | --- | --- |
| linear__aac__rho00 | 1.053 | 1.735 | 4.344 |
| linear__aac__rho25 | 1.155 | 2.16 | 5.469 |
| linear__aac__rho50 | 1.292 | 2.885 | 7.373 |
| linear__aac__rho75 | 1.47 | 4.113 | 11.252 |

## Research assessment and next step

No discrepancy was found in the checked markup algebra, saved cost identities, group totals or raw-input reconstruction. The evidence instead locates a joint model-consistency problem: cheap single-roll prices, manufacturer portfolio substitution, the AAC/retailer mapping, and a concentrated high-purchase-share tail. It does not uniquely identify an invalid IV, incorrect ownership, stockpiling, or erroneous raw data.

Keep the existing matrix as a conditional exercise and its failures visible. Before another demand specification, the most focused question is whether a package-purchase model with traffic as the opportunity denominator is defensible for the identified Scott episodes and how its static price response should be interpreted. A subsequent bounded study could compare raw purchase/promotion patterns around weeks 99/110 and articulate an economically justified purchase-unit or availability assumption. Such work needs a stated estimand; aggregation, market deletion, arbitrary traffic inflation, relaxing costs, or selecting log price solely for positive costs would not establish identification. The retailer-cost interpretation should remain a separate sensitivity rather than being used to conceal effective-cost failures.

The targeted diagnosis is complete. It does not finish the broader research project or authorize a new estimation grid. Mac verification, counterfactual statistical uncertainty and instrument exclusion remain unresolved.

## Reproduction and preservation

[Scope](scope.json) was recorded before the primary diagnosis. [Validation](validation.json) reproduces all 20 saved markup/cost vectors within 3.70e-13, matches dense ownership-block inversions within 9.44e-15, checks the singleton identity and retailer bridge, and verifies that UPC/manufacturer/pack totals partition negative package volume. The source audit independently checks 259,986 raw movement rows and 7,996 weekly traffic totals. Supplements add fresh files, with source snapshots and their own preservation evidence.

All 303 pre-existing research files, including the complete committed v5 run and its code, remain byte-identical. [Preservation](preservation.json), [supplement validation](supplement_validation.json), [raw audit](raw_input_audit.json), and the [repository validation record](../../../../docs/validation/2026-11-15-cost-failure-diagnosis.md) document the checks. New analysis is local on codex/diag-001-cost-failures, based on d5fcf7c. The source run is already committed and was verified on origin/main; these new diagnosis files are not yet committed/pushed.
