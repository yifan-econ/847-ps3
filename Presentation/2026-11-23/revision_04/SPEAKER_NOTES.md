# Speaker notes, version 4

A title page and fourteen slides, no backups. Slide numbers are the ones printed on the slides; the PDF page is one higher. Wenhan presents slides 1–8 from his own file; these notes cover Yifan's slides 9–14 (slides 8–13 of revision 03, unchanged). About 13 minutes for Yifan's part. Nobody has rehearsed this version.

## Say at the handover, before slide 9

Wenhan's slides and Yifan's come from different runs, and three things on slides 9–14 are not introduced by slides 1–8. One or two sentences each:

- **Log price.** Wenhan's logit has price in dollars. Slides 9–14 also use log price: "We estimate every model twice, with price in dollars and with log price. f(p) in the formula is one or the other."
- **Sample.** Wenhan reports 8,508 store-weeks and 277,363 observations. The merger slides use 7,996 store-weeks and 259,986 observations: store-weeks need seven days of traffic counts and both instruments for every product. That is why the ρ = 0 row on slide 10 (−2.03, elasticity −2.33) is close to, but not the same as, Wenhan's AAC column (−2.107, −2.42).
- **Second instrument.** Wenhan's is the price of the same UPC in other stores. The charts on slides 12 and 13 say "other zone": the same UPC's price in Dominick's other pricing zones. Same idea, different construction.

Two symbols change meaning. μ is the store–UPC effect on Wenhan's slide 5 and the markup on slides 11–13. D is the deal flag on his slides and the matrix of share derivatives on slide 11.

## Yifan: slides 9–14

| Slide | Min | Say | Likely question and answer |
|---|---:|---|---|
| 9 Nested logit | 2.5 | Plain logit sends a lost buyer to every other option in proportion to its share, and the outside option is most of the market. One nest for all tissue fixes that. ρ = 0 is plain logit; higher ρ keeps more lost buyers inside tissue. We do not estimate ρ: its regressor is endogenous, each regression uses one instrument, and both of ours are shifters of the product's own price. We set it to four values. | *Why not estimate ρ?* Each regression uses one instrument, and both of ours are shifters of the product's own price. Identifying ρ needs something that moves a product's share of tissue sales with its own price held fixed, such as rivals' costs or the number of rival products. We did not build one, so we set ρ and show how the answer moves with it. |
| 10 Nested results | 2 | Own-price elasticity barely moves with ρ: about −2.3 with price in dollars, −5.4 to −5.6 with log price. The price coefficient shrinks to keep it there. Category elasticity falls, and diversion from Kimberly-Clark to Scott rises from 5% to 29%. Diversion is what a merger internalizes. | *Why does β fall as ρ rises?* The own elasticity barely moves with ρ; the coefficient shrinks to keep it there. |
| 11 Supply | 2.5 | The lecture's multiproduct formula, written for the wholesale price w. The retail price p is w plus the retailer's fixed dollar margin m. Markup comes from demand and ownership. AAC is our measure of w, so implied manufacturer cost c is AAC minus markup, one number per product, store and week. The simulation holds c and m fixed, which is the same as holding retail price minus markup fixed. The merger changes the ownership matrix and nothing else. | *Is the retailer passive?* Yes, by assumption. We also ran a percentage margin; the merger effects barely change (Kimberly-Clark +1.03% against +1.13% at ρ = 0, log price, AAC). |
| 12 Implied costs | 2.5 | Read the first paragraph. Then the example: price 52 cents, wholesale 48 cents, markup 58 cents, so cost is −10 cents. With price in dollars almost all Scott single rolls fail. With log price few do. | *Why is Scott's markup 58 cents and not 49?* 49 cents is for a firm with a tiny share. Scott's share raises it: 1 / (\|β\|(1 − S)). |
| 13 Merger | 2.5 | What changes, what is re-solved, what is fixed. The algorithm works in retail prices: cost plus the retailer's margin plus the markup. A market is kept if observed prices are reproduced under the old ownership and two starting points agree; 7,960 of 7,996 are. Kimberly-Clark's prices rise most because its buyers divert to Scott, which the merged firm now keeps. Higher ρ, larger effect. | *Why is the category effect small?* Kimberly-Clark is 5% of packages and Scott's own prices rise by at most 5%. |
| 14 Conclusion | 1 | Prices rise. The log-price model passes the cost check, so we believe its range: 1% to 11% for Kimberly-Clark. The dollar-price model's larger effects rest on markups that cannot be real. What remains uncertain is ρ. | *Is the log-price model right, then?* It passes the one check we have. Its elasticities still come largely from temporary price cuts, and both models are static. |

## If asked about what the backups covered

- **Mixed logit.** Eight specifications, six converged, five of those reject the joint test of their moment conditions.
- **Consumer surplus.** With price in dollars, the loss is 0.03 to 0.34 cents per shopping trip.
- **Store 124, week of October 17, 1991.** 29,209 packages sold against 29,213 shopping trips; a one-package-per-trip model does not describe that week.

The backup slides themselves are in [revision 03](../revision_03/presentation.pdf), pages 14–18.

## Where each number comes from

Slides 9–14 are unchanged from revision 03, whose [check script](../revision_03/check_deck.py) compares every number with the saved run `Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01`. Wenhan's numbers come from his saved v1–v3 outputs, as his source file states; they were not rechecked here.
