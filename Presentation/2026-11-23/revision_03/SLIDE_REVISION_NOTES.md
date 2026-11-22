# Slide revision notes for the PS3 deck

Written November 22, 2026 for the session that will revise the slides.
Deck reviewed: `D:\dev\Documents\UNC\847-ps3\Presentation\2026-11-23\revision_02\` (`main.tex`, 15 main + 3 backup slides).

## Ground rules

- Build the new deck in a new folder (`revision_03`). Leave `revision_02` and the first draft untouched.
- Every number below already exists in the saved results. No new estimation and no new price solves are needed.
- Target: **13 main slides**, Wenhan 7 (including the title), Yifan 6. Backups do not count.
- Time: about 13 minutes each, 4 minutes for questions.

## The split Wenhan proposed

| Speaker | Topics |
|---|---|
| Wenhan | Overview; industry and summary statistics; market and product definition; data cleaning and instruments; logit model; logit results |
| Yifan | Nested logit specification; nested logit results; cost recovery; merger |

The current deck does not fit this split. The nested logit is one bullet inside the demand slide (slide 7) and one caption (slide 12).
It needs its own two slides, because it is now the opening of Yifan's half.

## Proposed 13-slide order

| New | Speaker | Content | Built from current slide |
|---:|---|---|---|
| 1 | Wenhan | Title | 1 |
| 2 | Wenhan | Question and answer preview | 2 |
| 3 | Wenhan | Industry: who sells what | 3 |
| 4 | Wenhan | Prices and promotions: where price variation comes from | 6 (figure) plus the variance split |
| 5 | Wenhan | Market, product, share, outside option, what is dropped | 4 |
| 6 | Wenhan | Logit model and instruments, with the first-stage table | 7 (without the ρ term) and 8 |
| 7 | Wenhan | Logit results: coefficients and elasticities by pack size | 9 |
| 8 | Yifan | Nested logit: equation, what ρ does, why it is set and not estimated | new, from the last bullet of 7 |
| 9 | Yifan | Nested logit results | new table, values below |
| 10 | Yifan | Supply: pricing rule and how cost is backed out | 10 |
| 11 | Yifan | Implied costs: the Scott single-roll example and why | 13 and 14 merged |
| 12 | Yifan | Merger results | 11 and 12 merged |
| 13 | Yifan | Conclusion | 15 |
| B1 | backup | Typical market | 5 |
| B2 | backup | Store 124, week of October 17, 1991 | second half of 14 |
| B3 | backup | Retailer margin rules | 16 |
| B4 | backup | Mixed logit attempts | 17 |
| B5 | backup | Consumer surplus | 18 |

## New slide 8: nested logit specification

Title: "Nested logit lets tissue products be closer substitutes for each other".

Content:

- The equation, with the nesting term on the right-hand side as the lecture writes it:
  `log(s_jt / s_0t) = α_{j,store} + τ_t + β f(p_jt) + γ Deal_jt + ρ log(s_jt / S_t) + ξ_jt`,
  where `S_t` is the total share of all tissue products in the market, so `s_jt / S_t` is the product's share of tissue sales.
- One nest holds all tissue products. The outside option is alone in its own nest.
- `ρ = 0` is the plain logit. As `ρ` rises, a buyer who leaves one tissue product is more likely to pick another tissue product and less likely to buy nothing.
- `ρ` is not estimated. `log(s_jt / S_t)` is endogenous, so estimating `ρ` needs a second instrument that moves a product's share of tissue sales without moving its demand shock. We have one instrument. We set `ρ` to 0, 0.25, 0.5, 0.75 and estimate `β` at each value.
- One short line for the audience: "ρ here is 1 − λ in the lecture's notation."

## New slide 9: nested logit results

Title: "Nesting leaves own-price elasticities alone and changes where lost buyers go".

Table, linear price with the AAC instrument (source: `Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01/REPORT.md`
and `Presentation/2026-11-23/revision_02/diversion_backup.csv`):

| ρ | Price coefficient (SE) | Median own elasticity | Median category elasticity | Diversion, K-C to Scott |
|---:|---:|---:|---:|---:|
| 0 | −2.03 (0.32) | −2.33 | −1.87 | 5% |
| 0.25 | −1.53 (0.24) | −2.32 | −1.41 | 13% |
| 0.50 | −1.02 (0.16) | −2.32 | −0.95 | 21% |
| 0.75 | −0.52 (0.08) | −2.35 | −0.48 | 29% |

Two lines under the table:

- The data fix the own-price elasticity at about −2.3 for every ρ. ρ decides how the lost buyers split between other tissue and the outside option.
- Diversion is the share of buyers leaving a Kimberly-Clark product who switch to a Scott product. It is what the merger internalizes.

Log-price row values, if there is room for a second small table (log price, AAC): coefficients −5.39, −4.07, −2.75, −1.43;
own elasticity −5.4 throughout; category elasticity −4.67, −3.53, −2.38, −1.24. Diversion is the same as above because it depends only on shares and ρ.

## Issues that change content

Ordered by how much they matter in the room.

1. **Nested logit has no slide.** See new slides 8 and 9.

2. **Slide 10 defines one cost and then talks about another.** The equation defines `c_eff = p − μ`.
   The bullet says "manufacturer cost is AAC minus implied markup". The audience cannot connect the two. Say it in this order:
   - Retail price = wholesale price + the retailer's margin. The retailer's margin is a fixed dollar amount per package.
   - AAC is our measure of the wholesale price.
   - The manufacturer's first-order condition gives its markup `μ`. Implied manufacturer cost = AAC − μ.
   - Drop `c_eff` from the main slide. If it stays, define it as "manufacturer cost plus the retailer's margin".

3. **Slide 10 never shows the markup formula.** The class knows it from the supply lecture. Put it on the slide:
   `p = c − (Ω ∘ D)^{-1} s`, and for the plain logit with price in dollars, `μ_f = 1 / (|β| (1 − S_f))`, where `S_f` is the firm's total share of the market.
   Then one line: the merger changes `Ω` and nothing else.

4. **The reason for negative costs is not stated in one sentence anywhere.** It is this:
   with price in dollars, the logit gives every product nearly the same dollar markup, about `1/|β|` = \$0.49.
   A 52-cent roll with a 48-cent wholesale price cannot carry a 49-cent markup, so its implied cost is below zero.
   With log price the markup is the same percentage of price for every product, about 19%, so the problem goes away.
   Put this on new slide 11 above the Scott example. The elasticity formula on current slide 14 can go to the spoken explanation.

5. **Slide 10 does not say what marginal cost is.** The assignment asks for the cost functional form and cost shifters.
   Add one line: "Marginal cost is constant in quantity. We do not estimate a cost function. Cost is the residual `p − markup`, one number per product, store and week."

6. **The conclusion argues against the cost check that the course teaches.** Slide 15 says credible instruments matter more than
   "choosing the specification with the nicest cost signs". The lecture lists "costs cannot be negative" as a valid way to reject a model.
   The log-price model passes that check for 93% to 98% of packages, depending on ρ, and the dollar-price model fails it for most Scott single rolls. The conclusion should use this:
   - "The log-price model gives sensible costs. In it the merger raises Kimberly-Clark prices by 1% to 11% and category prices by 0.2% to 1.7%, depending on ρ."
   - "The dollar-price model predicts larger effects, and those come from markups that are too large to be real."
   This changes the message of the last slide, so Wenhan should agree to it.

7. **Slide 6 states the weakest point of the data choice without answering it.** The caption says 98.1% of price variance is across store-UPC averages and 1.9% is within a store-UPC over time.
   The fixed effects remove the 98.1%. The estimate uses the 1.9%. The assignment says that little price variation over weeks is a reason to aggregate, so this will be asked.
   The slide should say: "After fixed effects, the price coefficient is identified from week-to-week price changes within a store and UPC. These are mostly temporary price cuts."
   Also say that most of the 98.1% is pack size (a 12-pack costs more than a single roll), so it says little about differences between stores.

8. **Slide 8: the other-zone instrument is nearly the price itself.** A first-stage slope of 1.05 with a partial R² of 0.69 to 0.79 means the IV estimate is close to OLS.
   The slide's title presents this as good news. Retitle to what each instrument assumes, one line each:
   - AAC: the wholesale cost moves the retail price and is unrelated to this week's demand shock in this store.
   - Other-zone price: the same UPC's price in Dominick's other pricing zones moves with common costs and is unrelated to this store's demand shock.
   - Weakness of both: promotions are planned by the chain and funded by manufacturers, so they move the instrument and demand together.

9. **Slide 8: the "Wald χ²" column and its footnote.** With one instrument the cluster-robust first-stage F is the squared t-statistic, and it equals the Wald χ² shown (101, 1316, 45, 3246).
   In this one-instrument case the robust F and the effective F are the same statistic. Label the column "First-stage F" and delete "Wald is not an effective-F statistic".

10. **Slide 14 says "linear demand".** The demand is logit. What is linear is price inside utility. Write "with price in dollars" and "with log price" throughout.

11. **Merged merger slide (new 12) should list what is held fixed and what moves.** The assignment asks for it by name.
    - Changes: ownership. Scott and Kimberly-Clark products get one owner.
    - Re-solved: prices of the six manufacturers' products, and all shares.
    - Held fixed: marginal costs, non-price utility (fixed effects, deal flags, demand shocks), market size, the product set, the retailer's dollar margin, private-label prices.
    - Algorithm, one line: start from observed prices and repeat `p ← ½p + ½(c + markup(p))` until prices stop moving.

12. **Slide 13 mixes two samples.** The worked example uses the 7,960 solved markets and the chart uses all 7,996. Keep both, but shorten the caption to
    "Chart: share of Scott single-roll packages with negative implied cost."

13. **Backup welfare slide: the numbers cannot be read.** −\$0.000423 per shopping trip means nothing to an audience.
    Show cents per trip (0.04 to 0.34 cents) and the total over the sample (\$66 thousand to \$528 thousand over two years in 83 stores). Both are in the saved results.

## Wording to change

Remove labels the class has never seen and footnotes that only defend the authors.

| Where | Now | Change to |
|---|---|---|
| Title slide | "a conditional merger exercise" | "What would a Scott–Kimberly-Clark merger do to bathroom tissue prices?" |
| 2, title | "with a fragile supply interpretation" | "The merger raises prices; how much depends on substitution within the category" |
| 2 | "Across maintained scenarios" | "Across our specifications" |
| 2, footnote | "The scenario ranges are not confidence intervals." | Delete. Say it aloud once. |
| 3, footnote | whole footnote | "Shares of packages sold at Dominick's, 1991–1992." |
| 4 | "Single-roll sales volume 37.7%" | "Single rolls, share of packages sold: 37.7%" |
| 4, footnote | "Positive-price/share observations and complete traffic weeks; ... Availability and units per buyer are not observed." | "259,986 observations; 94% of packages sold in 1991–1992." |
| 5, footnote | "without consulting merger predictions" | Delete. |
| 7 | "Deal is maintained exogenous." | "The deal dummy is treated as exogenous." |
| 7, footnote | "it does not prove a recording error" | Delete the clause. |
| 8, footnote | "each needs its own E[z̃ξ]=0 restriction" | "The instrument is in dollars when price is in dollars and in logs when price is in logs." |
| 9, footnote | "Coefficient units differ by price form." | Keep. Delete the rest. |
| 10, title | "Portfolio markups determine implied costs" | "Each manufacturer sets prices for all its products; cost is price minus markup" |
| 10 | "damped markup fixed-point iteration" | "fixed-point iteration on prices" |
| 11, footnote | "Same 7,960 store-weeks with valid numerical solutions in every scenario ... Negative-cost cases remain included." | "Percent, weighted by packages sold. 7,960 of 7,996 store-weeks." |
| 12, footnote | "Nesting moves predictions most over this grid." | Delete. The figure shows it. |
| 13, title | "the markup exceeds the wholesale proxy" | "For a Scott single roll, the implied markup is larger than the wholesale price" |
| 14, title | "expose the static model's limitations" | Slide is merged into new 11. |
| 14 | "plausible missing mechanisms, not identified explanations from these aggregates" | Delete. |
| 15, title | "The exercise shows why counterfactual assumptions matter" | "What we conclude" |
| 16, footnote | "Comparing retailer rules does not validate AAC as manufacturer marginal cost." | Delete. |
| 17 | "This is not evidence that heterogeneity cannot help. ... See source notes ..." | Delete the footnote. |
| 18, footnote | "These are model outputs, not causal welfare estimates." | Delete. |

## Small layout points

- Slide 13 chart: the y-axis label and the legend are too small to read from the back of a room.
- Slide 7 equation: `S_t` is never defined on the slide.
- Keep one caption line per slide at most.

## Not checked

- I did not rebuild the PDF or test any of these changes in LaTeX.
- The split and the change to the conclusion (issue 6) need Wenhan's agreement.
