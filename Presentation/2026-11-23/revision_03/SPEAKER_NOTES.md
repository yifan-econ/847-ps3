# Speaker notes, revision 03

Thirteen main slides and five backups. Wenhan presents slides 1–7, Yifan slides 8–13. About 13 minutes each, 4 minutes for questions. The split is Wenhan's proposal; nobody has rehearsed this version yet.

## Wenhan: slides 1–7 (13 minutes)

| Slide | Min | Say | Likely question and answer |
|---|---:|---|---|
| 1 Title | 0.5 | We ask what a Scott–Kimberly-Clark merger would have done to bathroom tissue prices at Dominick's in 1991–1992. | |
| 2 Question and answer | 1.5 | One ownership change, everything else fixed. Prices rise in every specification. The size depends on how closely tissue products substitute for each other, and on whether price enters in dollars or in logs. | *Is this the real 1995 merger?* No. The firms did merge in 1995. We simulate the merger under 1991–1992 conditions, without the divestitures. |
| 3 Industry | 1.5 | Scott sells 43% of packages, Kimberly-Clark 5%. Kleenex bath tissue is new in 1991. A small firm merging with a large one: the small firm's prices move most. | *Are these national shares?* No, one Chicago chain. |
| 4 Prices and promotions | 2 | Almost all price variance is between products, mostly pack size. After store–UPC and week fixed effects, what identifies the price coefficient is the 1.9% that moves within a store and UPC over time, and that is mostly temporary price cuts. | *Then why not aggregate over time?* Averaging over weeks removes exactly the variation we use. The cost is that weekly price cuts also invite stockpiling, which a static model ignores. |
| 5 Market and product | 2 | Market: store-week. Product: UPC. Share: packages sold divided by shopping trips. Outside option: a trip with no tissue purchase, 87% of trips in the median market. | *Why trips as market size?* Each trip is one chance to buy. It makes the outside share large; ρ later controls how much that matters. |
| 6 Logit and instruments | 3 | Logit with store–UPC and week effects, estimated by 2SLS. Two instruments, used one at a time. AAC is the wholesale cost. The other-zone price is the same UPC's price in Dominick's other pricing zones. Both are strong. Both share one weakness: chain-wide promotions move the instrument and demand together. | *The other-zone first stage is 1.05 with R² 0.7–0.8. Is that not just the price?* Nearly. Dominick's sets prices chain-wide, so zones move together. The instrument only helps if demand shocks are local to a store, and chain-wide promotions break that. That is why we show AAC as well. |
| 7 Logit results | 2.5 | Price coefficients are negative and precisely estimated. With price in dollars, elasticity is proportional to price: −1.0 for a single roll, −5.8 for large packs. With log price it is about −5.2 for every pack size. Remember the −1.0: it is where the cost problem comes from. | *Which price form is right?* Yifan's cost check answers that. |

Handoff line: "So the two price forms disagree most for cheap single rolls. Yifan will show what that does to costs and to the merger."

## Yifan: slides 8–13 (13 minutes)

| Slide | Min | Say | Likely question and answer |
|---|---:|---|---|
| 8 Nested logit | 2.5 | Plain logit sends a lost buyer to every other option in proportion to its share, and the outside option has 87%. One nest for all tissue fixes that. ρ = 0 is plain logit; higher ρ keeps more lost buyers inside tissue. We do not estimate ρ: its regressor is endogenous and we have one instrument. We set it to four values. | *Why not estimate ρ?* It needs a second instrument that moves a product's share of tissue sales without moving its demand shock. The usual choice is the number of rival products in the market. We did not have one we trusted, so we set ρ and show how the answer moves with it. |
| 9 Nested results | 2 | Own-price elasticity does not move with ρ. Category elasticity falls, and diversion from Kimberly-Clark to Scott rises from 5% to 29%. Diversion is what a merger internalizes. | *Why does β fall as ρ rises?* The own elasticity is pinned by the data; a higher ρ needs a smaller β to give the same elasticity. |
| 10 Supply | 2.5 | The lecture's multiproduct formula. The manufacturer's price is the wholesale price; the retailer adds a fixed dollar margin. Markup comes from demand and ownership. Cost is AAC minus markup, one number per product, store and week. The merger changes the ownership matrix and nothing else. | *Is the retailer passive?* Yes, by assumption. The backup shows a percentage margin instead; the merger effects barely change. |
| 11 Implied costs | 2.5 | Read the first paragraph. Then the example: price 52 cents, wholesale 48 cents, markup 58 cents, so cost is −10 cents. With price in dollars almost all Scott single rolls fail. With log price few do. | *Why is Scott's markup 58 cents and not 49?* 49 cents is for a firm with a tiny share. Scott's share raises it: 1 / (|β|(1 − S)). |
| 12 Merger | 2.5 | What changes, what is re-solved, what is fixed. Kimberly-Clark's prices rise most because its buyers divert to Scott, which the merged firm now keeps. Higher ρ, larger effect. | *Why is the category effect small?* Kimberly-Clark is 5% of packages and Scott's own prices rise by at most 5%. |
| 13 Conclusion | 1 | Prices rise. The log-price model passes the cost check, so we believe its range: 1% to 11% for Kimberly-Clark. The dollar-price model's larger effects rest on markups that cannot be real. What remains uncertain is ρ. | *Is the log-price model right, then?* It passes the one check we have. Its elasticities still come largely from temporary price cuts, and both models are static. |

## Backups

- B1 typical market. B2 the store-week where packages sold equal shopping trips. B3 dollar versus percentage retailer margin. B4 mixed logit. B5 consumer surplus.

## Where each number comes from

- Sample counts, first stages, estimates, elasticities, diversion, price effects, cost check, consumer surplus, store 124: `tables/`, written by `prepare_tables.py` from the saved run `Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01`.
- Scott white example (price \$0.52, AAC \$0.48, markup \$0.58 and \$1.01): `Analysis/cost_failure_diagnosis/runs/2026-11-15_costdiag_01/REPORT.md`.
- Chart on slide 11: `Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_01/scott_cost_claim_check.csv`.
- Mixed logit counts: `Analysis/mixed_logit_v4/REPORT_zh.md`.
- Lecture notation (λ, Ω ⊙ D, the logit markup): course slides `02Demand_Lecture.pdf` and `03Supply_Lecture.pdf`.
