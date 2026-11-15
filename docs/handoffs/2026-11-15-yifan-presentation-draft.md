# 2026-11-15: Yifan / Codex — presentation delivery

Work ID DELIV-001. User confirmed November 23 and chose Codex to draft LaTeX/Beamer. Branch `codex/deliv-001-beamer`, base `d5fcf7c9b0c9cc44cdf382f634904e2082618669`; fetched origin/main remains at base. All earlier diagnosis/review work preserved. No commit or push. Recommend sharing the accumulated work before Wenhan reviews remotely; Yifan has not authorized that action yet.

## Direction and deliverables

Fable closed the technical review and urged delivery. Adopted that direction: cost diagnosis frozen, no new reviews or model runs. The assignment's six parts are covered by the existing conditional exercise; negative costs belong in its interpretation.

Added `Presentation/2026-11-23/`: fifteen-slide Beamer source/PDF, six saved-data figures with CSVs and editable generation script, descriptive summary statistics, a matched-assumption comparison, speaker notes/storyboard and preservation evidence. Rewrote the WORKPLAN opening and Next work as delivery tasks with owner, dates, effort and acceptance conditions; updated STATUS, README, indexes and changelog.

Main table shows four rho-zero demand cells under both retailer rules. Nesting sensitivity has a separate chart. The largest matched price change over the grid comes from nesting, followed by price functional form. This is a reporting comparison, not another identification or cost-diagnosis exercise. Notes distinguish conditional model assumptions, sample/weight denominators and the historical merger.

Codex owns drafting/revisions. Yifan and Wenhan's review and speaking roles are proposed, not accepted. Timing allocations total thirty minutes; no human timed rehearsal has occurred. Proposed split: Yifan first eight slides, Wenhan remaining seven. Targets: joint feedback by November 18, revisions by November 20, rehearsal by November 21, final display check November 22. Deadline November 23 is user-confirmed; intermediate dates are proposals.

## Checks and sharing

Read assignment page one; generated figures only from frozen inputs/results. All 369 existing research files remained unchanged. No estimators or equilibrium solvers ran; no lockfile/project dependency changes. Built with the local TeX Live alias and visually inspected all slides; corrected table input and image paragraph/footline layout during drafting. Matplotlib was supplied through an isolated uv `--with` environment. Native Mac build not tested.

See [validation](../validation/2026-11-15-presentation-draft.md), [draft](../../Presentation/2026-11-23/README.md), [notes](../../Presentation/2026-11-23/SPEAKER_NOTES.md). Next is collaborator feedback and rehearsal, not another review round or optional aggregation estimate. All post-base changes remain local/uncommitted/unpushed.
