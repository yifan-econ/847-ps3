# 003: Execute the isolated 16-cell calibrated merger design

Date: 2026-11-15. Status: accepted for this exploratory run. Work IDs: RUN-001, ENG-002, RES-002, RES-004, CF-001.

## Authorization and scope

The user explicitly requested proceeding with the corrected 16-cell design in WORKPLAN, isolating all new outputs, preserving existing results, and documenting findings. Yifan / Codex implements this round on `codex/run-001-calibrated-merger`, base `14254a5f4177177fd2d9f0b14c598c299b219096`. The 11 pre-existing uncommitted review documents are preserved.

Use the existing v4 all-pack complete-market keys, 1991–1992, and a hypothetical Scott/Kimberly-Clark merger. Run the prespecified two IVs by two price forms by four fixed rho values, plus percentage-margin sensitivity in the four rho-zero cells. All fit and simulation results are conditional on maintained instrument, static-demand, ownership, and conduct assumptions. This accepts a research design, not any final specification or causal merger estimate.

## Implementation choices fixed before estimation

- New code and run roots live in `Analysis/calibrated_merger_v5/`; the default run directory cannot already exist. Existing analysis/data locations are read-only.
- Correct Scott labels only in the new derived catalog. Map six portfolios through brand evidence and UPC-prefix groups; private-label/generic prices are fixed. Retain limitations of inferred non-anchor brand mapping.
- Log-price cells use log IVs and explicitly assume the corresponding moment restriction. No sample changes or parameter sign constraints are introduced to obtain favorable results.
- Percentage margins use store/UPC medians from the full 1991–1992 positive-sales window; implied wholesale `q*p` calibrates manufacturer costs. Observed AAC is reported separately. Dollar margins recover effective costs for prediction and AAC-proxy manufacturer costs for diagnostics.
- Prespecify damped markup iteration, two starts, FOC/baseline tolerances and local-curvature checks as documented in the [v5 guide](../../Analysis/calibrated_merger_v5/README.md). Record failures without additional cells or result-driven starts.
- All outputs, source snapshots, sample/corrected catalog, manifests, failures, and preservation evidence stay in the unique run directory. Hash all 194 pre-existing research files. Do not rewrite any legacy fit, code, report, input, or failed attempt.
- Report all-cell estimates and both individual/common cost screens, baseline-weighted price changes, category elasticities, diversion, and linear-price welfare. Do not present calibrated rho ranges as confidence intervals.

## Consequences

The plan's former unexecuted/proposed labels are superseded only for this authorized run. No expansion to joint demographic models, new instruments, aggregation, or automatic retries is authorized by this design. Mac runtime verification remains separate. Final documentation must distinguish numerical success, cost/conduct consistency, and identification credibility.
