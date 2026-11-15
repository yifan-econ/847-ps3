# 2026-11-15: Yifan / Codex — isolated conditional merger matrix

- Work IDs: RUN-001, SCOPE-001, ENG-002, RES-001/002/004/005, CF-001.
- Human/account and agent: Yifan / Codex; user explicitly authorized the corrected 16-cell design, isolation and documentation.
- Branch: `codex/run-001-calibrated-merger`; base `14254a5f4177177fd2d9f0b14c598c299b219096`.
- Sharing: local, uncommitted, unpushed. No new commit ID exists. Fetching origin succeeded before branching; no remote work was overwritten.
- Starting state: retained the 11 uncommitted documents from the prior research/Fable reviews on `codex/review-001-research-workplan`.

## Scope and changes

Implemented a new IO-free single-nest demand/supply engine and an isolated runner under `Analysis/calibrated_merger_v5/src/`. The runner uses the existing IO-free v2 fit helper but never calls a legacy writing entry point. It snapshots code and environment, refuses an existing run directory, and inventories the 194 original research files before/after.

Run `2026-11-15_16cell_01` estimates linear/log package-price models with AAC/other-zone IVs conditional on rho 0/.25/.5/.75. All 16 use dollar retailer margins; the four rho-zero cells add percentage-margin scenarios. The same v4 all-pack keys are used for demand and supply. Separate catalog corrections and ownership evidence appear in the new guide and run artifacts. Scott and Kimberly-Clark merge hypothetically at 1991–1992 conditions, with four rivals reoptimizing and private-label/generic prices fixed.

New meaningful tests cover derivatives, exact markup inversion, independent equilibrium roots, profit curvature, welfare derivatives, market batching and retailer-rule divergence. Saved-output validation uses independent dense calculations and numerical differentiation. The report generator preserves raw artifacts and writes derived reporting tables.

Changed paths: the new v5 directory; `tests/test_calibrated_merger.py`; `scripts/check_environment.py` (optional fresh evidence directory, preserving earlier validation logs); `.gitattributes` for simulation-array LFS handling; root README; `docs/SETUP.md`, `docs/STATUS.md`, `docs/WORKPLAN.md`, `docs/CHANGELOG.md`; decision 003 and its index; this handoff and index; validation record and index. Earlier review documents remain in the working tree. No original research path was migrated or overwritten.

## Evidence and findings

Execution and validation completed successfully; evidence is recorded in the [validation record](../validation/2026-11-15-calibrated-merger.md) and [run report](../../Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01/REPORT.md). The [manifest](../../Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01/design.json) records actual branch/base, Python/dependencies, frozen implementation and numerical tolerances. Unlike the earlier read-only review rounds, this round **does estimate demand and simulate counterfactuals** in its new run directory.

The run completed all 16 fits and 20 scenarios in 21.0 minutes, preserving all 194 original research files. Independent dense checks passed across 240 scenario-market cases. The final Windows safe check passed 12 tests, all four preparation audits and a saved-market prediction, with all 298 then-existing research files unchanged. See the validation record for commands, exact residuals, the reporting-only slope correction and the interrupted/repaired validation attempt.

Final review: Git whitespace checks passed; local link targets in 35 Markdown files all resolve (the historical UTF-16 README was read in its original encoding). A final SHA-256 recheck confirmed all 194 original research files unchanged. The completed run contains 104 files, including archived environment evidence; no commit or push was made.

The common numerical sample is 7,960 markets, but the common effective-cost sample is only 538 markets / 5.61% of packages and the common manufacturer-cost sample is empty. Common-sample category price increases span 0.157%–3.374%, including negative-cost scenarios. The direction is useful for a conditional sensitivity presentation; no credible single headline merger estimate is selected. Numerical success, positive-cost coverage and identification remain separate claims.

## Open work and next action

Review the completed matrix and its cost/conduct limitations before choosing presentation claims. No final causal model is selected. Identification of rho, IV validity, availability/zero-sales selection, stockpiling, traffic-based market size, global equilibrium uniqueness and counterfactual sampling uncertainty are not established by the numerical checks. Mac runtime verification remains pending. No extra cells or legacy re-estimation are planned in this round.

## Documentation

[Decision 003](../decisions/003-calibrated-merger-design.md) records accepted scope. [STATUS](../STATUS.md) and [WORKPLAN](../WORKPLAN.md) distinguish the completed conditional prototype from unresolved research credibility. The repository record is intended to stand alone for Wenhan/Fable without chat access; it remains local until explicitly shared.
