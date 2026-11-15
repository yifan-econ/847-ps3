# 2026-11-15: Yifan / Codex — revise presentation and commit accumulated work

DELIV-001 continuation. User supplied Fable's review, requested revision and a local commit, and reserved the push for himself. Wenhan has made no changes since the shared baseline, per Yifan. Branch `codex/deliv-001-beamer`; fetched base/origin-main `d5fcf7c9b0c9cc44cdf382f634904e2082618669`.

This handoff is included in the authorized local delivery commit, together with the accumulated diagnosis/review work and both presentation drafts. Identify the containing commit through Git history; its parent is the shared baseline. No push or email transmission by Codex. Historical run manifests retain their original uncommitted statements as records of when those runs occurred.

## Revision

New isolated directory `Presentation/2026-11-23/revision_02/` preserves the first draft. The revised PDF has fifteen main slides, three backups and a 25.5-minute remarks target. Demand estimates/SEs/median elasticities and first-stage regression/results now precede supply. Pack-size elasticities and a Scott-white cost example explain why costs fail. Scott is added to the main price table; percentage margins move to backup with mixed-logit history and welfare. Clean product labels, dated promotions, a raw price-variance split, readable captions and fresh PDF previews improve presentation use.

The main talk connects the high-effect scenarios to negative Scott costs. It retains the distinction between manufacturer and retail-equivalent costs. No OLS comparison on an unmatched sample is inserted. Clarify that −5.8 is the six-plus-roll elasticity, not all multipacks. The checked paper supports entry in 1991 without establishing July; strong cross-zone comovement does not prove promotions cause it. These are presentation corrections, not a reopened cost review.

Proposed speaking split now gives Wenhan slides 1–9 and Yifan slides 10–15, subject to their agreement. Review by November 18, rough timed run by November 19, revision November 20, final rehearsal/display check before November 23. No actual rehearsal yet.

## Paths and validation

Updated current README, STATUS, WORKPLAN, indexes and changelog; added this handoff and [validation](../validation/2026-11-15-presentation-revision.md). Added the revised source/PDF, figures/CSVs, exact saved-table extracts, derivation scripts, notes, supplied feedback, current previews and numerical/build evidence. [Current entry point](../../Presentation/2026-11-23/revision_02/README.md).

All 369 pre-existing research files and the first-draft PDF remain unchanged. No model fit or equilibrium solve ran. The revised PDF compiles and all eighteen pages were visually reviewed. Captions/table values were checked against frozen inputs and estimates; PDF encryption is false. A scoped .gitattributes rule disables newline normalization for the new diagnosis directory so its archived byte hashes survive Git checkout. No project lock or dependency changes. The optional matplotlib environment is isolated through uv. Native Mac execution and classroom projection remain untested.

Next: Yifan pushes the delivery branch; Wenhan fetches and reviews the current draft, especially the demand/identification story. Agree on speaking parts and rehearse. No new estimation or cost-review round is scheduled.
