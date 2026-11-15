# 2026-11-15: Yifan / Codex — second Fable response

- Work ID: REVIEW-003; user supplied Fable's follow-up without requesting execution of the proposed estimation matrix.
- Human/account: Yifan's session; agent: Codex.
- Branch/base: `codex/review-001-research-workplan`, `14254a5f4177177fd2d9f0b14c598c299b219096`.
- Starting state: nine uncommitted documentation files from prior reviews; preserved and extended. Fetch succeeded; HEAD and fetched origin/main had zero divergence.
- Sharing: local, uncommitted, unpushed; no communication sent to Fable or another account.

Fable withdrew estimated nested logit with one IV, accepted the cost-unit correction, and withdrew the unique functional-form interpretation of the joint rejection. It proposed 16 demand fits conditional on calibrated rho, dollar-margin simulations and a rho-zero percentage sensitivity, on the common v4 all-pack sample.

The [verification](../validation/2026-11-15-fable-response.md) reproduces the new cost percentages and single-roll concentration, checks the joint-IV sample rank without estimating demand, and supplies a synthetic counterexample to an overly broad retailer-rule equivalence claim. It distinguishes median-margin model-implied wholesale prices from observed AAC, and substitution sensitivity from market-size sensitivity. Fable's new influence/deletion and pass-through calculations were not fully replicated and remain qualified.

Changed files this round: `docs/WORKPLAN.md`, `docs/STATUS.md`, `docs/CHANGELOG.md`, the handoff and validation indexes, this new handoff, and `docs/validation/2026-11-15-fable-response.md`. The plan now records the proposed bounded matrix, defers mixed-logit causal diagnosis/refinement and aggregation, and clarifies finite deliverables. The demand-only option is a fallback rather than the recommended next run. No model or merger outcome was accepted, and no numbered modeling decision was added.

Checks used inline `uv run --locked python -` scripts, read-only data summaries/projections, and a synthetic two-product `scipy.optimize.root` calculation. No project demand estimation or empirical merger equilibrium ran. Existing research data/code/results were preserved; final verification is recorded below.

Next concrete action: finalize the scope and ownership note and implementation ownership for the proposed matrix. Any implementation should isolate all outputs and implement the actual nested-demand Jacobian, consistent cost calibration, baseline/FOC/profit diagnostics, and explicit handling of failed cells. Do not treat this feedback exchange as execution of the run proposal.

Final checks: `git diff --check` passed; all 194 protected research files still match the prior SHA256 inventory; all 77 relative links across the 11 changed/new Markdown documents resolve. Eleven is cumulative, including the nine pre-existing documentation changes.
