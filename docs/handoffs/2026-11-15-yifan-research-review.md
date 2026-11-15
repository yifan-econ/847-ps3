# 2026-11-15: Yifan / Codex — research progress and workplan review

- Work ID: REVIEW-001; proposed follow-up REVIEW-002 and SCOPE-001.
- Human/account: Yifan's workspace/session; agent: Codex. Claude feedback requested by the user, not yet received.
- Starting branch/base: `main` at `14254a5f4177177fd2d9f0b14c598c299b219096`.
- Working branch: `codex/review-001-research-workplan`, same base commit.
- Starting state: clean working tree. `git fetch origin` succeeded after the initial sandbox write restriction; fetched `origin/main` and HEAD had zero commits of divergence.
- Sharing state: local, uncommitted, not pushed. No messages sent to Claude or another account. The user can share the workplan for feedback.

## Scope and changes

The user requested a progress review, assessment of whether the research direction is promising, and an update to `docs/WORKPLAN.md` for subsequent Claude feedback.

- `docs/WORKPLAN.md`: added evidence-based assessment, counterfactual scope options, priorities, dependencies, concrete outputs, model-selection conditions, and questions for Claude. Preserved existing work IDs and added REVIEW-001/002, SCOPE-001, RES-005, CF-001, and DELIV-001. New research tasks remain unassigned.
- `docs/STATUS.md`: recorded review interpretation, fresh safe-check evidence, and actual branch/sharing state.
- `docs/handoffs/2026-11-15-yifan-research-review.md` and `docs/handoffs/README.md`: this round and index entry.
- `docs/validation/2026-11-15-research-review.md` and `docs/validation/README.md`: checks, source provenance, and limitations.
- `docs/CHANGELOG.md`: review entry.

No analysis code, data, baseline estimates, historical reports, dependency definitions, or lockfiles changed. No new accepted modeling decision was made; the new priorities and scope alternatives await review, so no numbered modeling decision was added.

## Evidence

Read the project entry/workflow files, latest portability handoff, original Chinese baseline, assignment (both pages), v2–v4 reports, saved result tables, zero-sales audit, rejected-fit records, and v4 preparation/estimation/validation code. Numerical claims were checked against saved CSV/JSON rather than inferred from prose alone.

`uv sync --locked` passed. `uv run --locked python scripts/check_environment.py` passed on Windows/Python 3.13.9: six tests, all four preparation combinations, a 32-product saved-market prediction with maximum share error `6.938893903907228e-18`, and 194 protected files unchanged. No estimation ran. A separate read-only CSV check verified the rejection counts and computed paired elasticity sensitivity. See [validation](../validation/2026-11-15-research-review.md) for commands and limits.

Final documentation checks passed: `git diff --check`, all 52 relative links in seven changed/new Markdown files, and a second comparison of the full 194-file research inventory against the pre-check hashes. All changes are confined to `docs/`.

## Research interpretation

The project is promising as a focused PS3 structural-demand exercise. Data preparation, controlled comparisons, preserved failed attempts, and numerical checks are substantial assets. The limiting steps are the economic interpretation of the sample, instrument exclusion (especially demographic interactions), and the intended counterfactual, rather than simply the number of fitted models.

Five of six retained v4 joint-moment tests reject at 5%; the all-pack household/AAC p-value of 0.090 is not validation. Across otherwise paired fits, switching from AAC to other-zone IV changes absolute median elasticity by 25.0%–37.6%. This is descriptive sensitivity; no formal cross-estimator difference test was performed. Income quadrature remains a numerical question distinct from identification. Neighborhood demographic weights, static inventories/promotions, and zero-sales selection remain unresolved.

The assignment explicitly allows a demand-only counterfactual. A prespecified posted-price exercise could reduce supply-side scope, while retaining demand-side caveats. Manufacturer merger analysis requires a defensible vertical pricing model and historical ownership; merely supplying manufacturer IDs at observed retail prices is insufficient. Both routes remain proposals.

## Open work and next action

1. User/Claude review SCOPE-001 and the proposed same-sample identification matrix; record disagreements and accepted changes in REVIEW-002.
2. Agree ownership and a bounded run plan. No work is assigned to Wenhan or Claude by this review.
3. Implement ENG-002 before new research runs; read-only sample/identification review and the Mac environment check can proceed independently.
4. Keep counterfactual execution gated by a documented reporting-model decision; do not conceal unresolved identification by selecting the one non-rejected fit.

Mac runtime and CI evidence remain unverified in this round. Existing historical reports retain their original context; in particular, v3's then-missing Romeo full-text note was superseded by v4 and the Chinese baseline. Read the current records before interpreting older recommendations.
