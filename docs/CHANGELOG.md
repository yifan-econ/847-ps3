# Collaboration changelog

## 2026-11-15

- RUN-001 / ENG-002 / RES-002/004/005 / CF-001: executed the user-authorized 16-cell conditional demand design and 20 supply scenarios in a unique v5 run. Added corrected catalog, ownership/retailer documentation, numerical engine, independent validation, cost/common-sample diagnostics and linear welfare. All 194 original research files are unchanged. Common numerical coverage is 7,960 markets, but common effective-cost coverage is 538 and manufacturer-cost coverage is empty; no causal model selected. See [handoff](handoffs/2026-11-15-yifan-calibrated-merger.md), [validation](validation/2026-11-15-calibrated-merger.md), and [report](../Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01/REPORT.md). Added isolated safe-check evidence paths and LFS attributes. Changes remain local/uncommitted/unpushed.

- REVIEW-003: checked Fable's second response and recorded a proposed 16-cell conditional-rho matrix. Reproduced single-roll cost diagnostics and clarified percentage-margin baseline calibration and post-merger margin dispersion. Closed unique attribution of old joint rejection as unresolved; no project estimation or empirical merger equilibrium ran. See [handoff](handoffs/2026-11-15-yifan-fable-response.md) and [verification](validation/2026-11-15-fable-response.md).
- REVIEW-002: independently checked user-supplied Fable feedback. Confirmed descriptive evidence, Scott/Cottonelle mapping bug, and income/AAC restart history; qualified rejection attribution, nested-logit identification, and cost interpretation. Revised WORKPLAN to allow an early conditional merger prototype alongside diagnostics. See [handoff](handoffs/2026-11-15-yifan-fable-review.md) and [evidence](validation/2026-11-15-fable-review.md). No estimation or equilibrium simulation ran; local documentation changes remain uncommitted/unpushed.
- REVIEW-001: assessed saved research progress and expanded WORKPLAN with priorities, completion evidence, counterfactual scope options, and questions for Claude; no final model selected. Updated STATUS and added [review handoff](handoffs/2026-11-15-yifan-research-review.md) and [validation evidence](validation/2026-11-15-research-review.md). Safe Windows check passed again; all 194 protected research files unchanged; no estimation ran. Local review changes are uncommitted and unpushed.
- ENG-001: replaced direct fcntl use with FileLock; added a pinned uv project and a read-only preparation path.
- Added disposable locking tests and a research-file preservation check.
- COLLAB-001: introduced status, workplan, handoff, decision, validation, and template structure.
- See [the round handoff](handoffs/2026-11-15-yifan-portability.md) and [Windows evidence](validation/2026-11-15-windows-portability.md).

## 2026-11-14

- Organized project entry notes, retained analysis/data paths, and added folder guides.
- Preserved [Wenhan's research baseline](handoffs/2026-11-14-wenhan-baseline_zh.md) and [older entry notes](history/README.md).
