# 2026-11-15: Yifan / Codex — check Fable's assessment

- Work ID: REVIEW-002.
- Human/account: Yifan's workspace/session; agent: Codex. Feedback author was identified by the user as Fable.
- Branch/base: `codex/review-001-research-workplan`, `14254a5f4177177fd2d9f0b14c598c299b219096`.
- Starting state: seven uncommitted documentation changes from REVIEW-001; preserved and extended. `git fetch origin` succeeded; HEAD and fetched `origin/main` had zero divergence.
- Sharing state: local, uncommitted, unpushed; no messages sent to another account.

## Request and outcome

The user supplied Fable's assessment and asked to check it. Fable proposed abandoning further mixed-logit refinement in favor of simple/nested-logit merger analysis and identified data-label and convergence-history issues.

Independent read-only checks reproduced all six joint-moment statistics, income-moment collinearity, promotion shares, chain-wide variation measures, broad prefix portfolio revenue shares, and the two code/log findings. The [verification record](../validation/2026-11-15-fable-review.md) contains methods, numerical results, qualifications, and primary-source links.

Agree with attempting an early conditional merger prototype, keeping all-pack goods for a Scott merger, and removing unused v4 refinement from the critical path. The local Hausman–Leonard paper explicitly permits fixed retailer margins, so the earlier plan overstated the practical barrier to a classroom merger exercise.

Do not accept the inference that interaction-heavy null-space loadings identify lognormal income as the rejection's cause. A rescaling check changes the apparent base-moment loading to nearly one without changing the statistic. Also, nested logit with both price and within-nest share endogenous needs more identification than either proposed base IV alone. Cost checks must specify how retail-equivalent costs map to manufacturer costs. An illustrative saved-coefficient cost screen found substantial negative manufacturer costs under one explicit passive-retailer rule; it is a diagnostic, not a new fitted supply model.

## Changed paths

- `docs/WORKPLAN.md`: reconciled Fable feedback, corrected the counterfactual/refinement circularity, distinguished an early prototype from final reporting, moved ownership/catalog work earlier, and narrowed output-isolation work to the selected runner. No final model selected.
- `docs/STATUS.md`: recorded verified brand bug and restart history; updated feedback status and latest handoff.
- `docs/validation/2026-11-15-fable-review.md`: detailed verification and limitations.
- `docs/handoffs/2026-11-15-yifan-fable-review.md`: this handoff.
- `docs/validation/README.md`, `docs/handoffs/README.md`, `docs/CHANGELOG.md`: index and outcome records.

No historical analysis file, raw input, reference paper, fit, or failed attempt was rewritten. The Scott label bug is identified but intentionally not patched as part of this review. No new accepted modeling decision was made, so no numbered decision record was added.

## Checks and next steps

`uv sync --locked` passed. Inline `uv run --locked python -` scripts performed data summaries, fixed-effect projections, saved-result moment tests, rescaling checks, and an analytic cost screen. The moment audit patched `pyblp.Problem.solve` to reject accidental estimation. No estimator/report generator or legacy writing validator ran. The scripts wrote only ignored `.local/fable-review/` evidence.

Next: agree the hypothetical merger scope, create a corrected derived UPC/ownership table, state an explicit retailer-price rule, and define an isolated bounded simple-logit prototype. Do not add nested-logit fits until the second endogenous regressor has an identification plan or is handled as an explicitly calibrated sensitivity. Do not use the preliminary cost screen to select the preferred IV mechanically.

The scope remains proposed; no implementation ownership is assigned to Wenhan or Fable. Native Mac and CI verification remain pending and are independent of this research review.

Final checks passed: `git diff --check`; all 69 relative links across the nine changed/new Markdown documents resolve; all 194 protected research files are byte-identical to the pre-review inventory. Nine is the cumulative documentation count including the seven pre-existing changes. Evidence is summarized here and in the validation record; local preservation output is in `.local/fable-review/preservation.json`.
