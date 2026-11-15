# 2026-11-15: Saved cost-failure diagnosis

Work ID: DIAG-001. Human/account: Yifan / Codex. Branch: `codex/diag-001-cost-failures`. Base/source commit: `d5fcf7c9b0c9cc44cdf382f634904e2082618669`. Windows 11, Python 3.13.9, existing locked uv environment. Source commit was verified on local main and remote origin/main; the starting worktree was clean. New diagnosis work remains local/uncommitted/unpushed.

## Commands and observed checks

```sh
uv sync --locked
uv run --locked python Analysis/cost_failure_diagnosis/src/diagnose.py --run-id 2026-11-15_costdiag_01
uv run --locked python Analysis/cost_failure_diagnosis/src/supplement.py --run-id 2026-11-15_costdiag_01
uv run --locked python Analysis/cost_failure_diagnosis/src/audit_inputs.py --run-id 2026-11-15_costdiag_01
uv run --locked python Analysis/cost_failure_diagnosis/src/report.py --run-id 2026-11-15_costdiag_01
```

All four scripts completed successfully. The primary diagnosis took 22.78 seconds. No estimation or equilibrium solve ran. These checks are specific to the new diagnostics; the earlier twelve-test Windows environment result remains historical evidence and was not represented as rerun here.

| Check | Observed result |
|---|---|
| Independent exact block inversion vs saved active-product markups, all 20 scenarios | Maximum absolute difference 3.70e-13 |
| Reconstructed effective/manufacturer costs vs saved values | Maximum absolute difference 3.70e-13 |
| Independent dense inversion in four deterministic markets per scenario | Maximum markup difference 9.44e-15 |
| Singleton markup / price equals inverse absolute own elasticity | Maximum discrepancy 6.66e-16 |
| Dollar/percentage manufacturer and effective cost bridges | Maximum discrepancy 1.33e-15 |
| Cost-sign market masks | Exactly reproduce source masks and per-scenario numerical/cost counts |
| UPC/manufacturer/pack grouping | Each partitions the all-active negative-package total |
| Sample | 259,986 observations; 7,996 markets; 44 active-manufacturer UPCs; common numerical intersection 7,960 markets |
| Raw source reconciliation | All 259,986 MOVE, PRICE/QTY, AAC and deal records matched |
| Price/AAC arithmetic | Maximum discrepancies 1.11e-16 / 8.88e-16 |
| MOVE and deal | Zero quantity difference; zero deal mismatches |
| Raw customer counts | All 7,996 traffic totals match; seven valid dates each; zero traffic difference |
| Preservation | All 303 pre-existing research files byte-identical after primary diagnosis and supplements |

Evidence: [primary validation](../../Analysis/cost_failure_diagnosis/runs/2026-11-15_costdiag_01/validation.json), [scope](../../Analysis/cost_failure_diagnosis/runs/2026-11-15_costdiag_01/scope.json), [preservation](../../Analysis/cost_failure_diagnosis/runs/2026-11-15_costdiag_01/preservation.json), [tail supplement](../../Analysis/cost_failure_diagnosis/runs/2026-11-15_costdiag_01/supplement_validation.json), and [raw reconciliation](../../Analysis/cost_failure_diagnosis/runs/2026-11-15_costdiag_01/raw_input_audit.json). Exact source snapshots are stored beside these files. The report's numerical statements are drawn from the saved diagnostic tables.

## Interpretation and limits

The arithmetic partition separates singleton-demand, portfolio and retailer-wedge crossings; it is ordered and is not a causal decomposition. Both full-input and common numerical samples are retained. The supplementary all-input audit was added after the primary tables revealed that the common intersection excludes all 18 log/AAC rho-zero manufacturer-cost-failing markets; it adds no model, equilibrium or sample restriction.

The raw audit confirms observed source records rather than reconstructing unobserved customers or inventory. Extreme package/traffic ratios remain economically problematic for a one-package model despite passing arithmetic checks. Threshold multipliers are algebraic feasibility calculations, not estimates or recommendations to tune beta. Numerical failures and negative costs remain preserved. No owner map, retailer parameter, demand coefficient or protected artifact was modified. No native Mac runtime claim is made.

## Final documentation review

The final link/whitespace and preservation checks are recorded in the [handoff](../handoffs/2026-11-15-yifan-cost-failure-diagnosis.md). The [report](../../Analysis/cost_failure_diagnosis/runs/2026-11-15_costdiag_01/REPORT.md) documents all findings and table denominators.

Final observed outcome: whitespace check passed; all local targets in 37 Markdown files resolve; saved decomposition totals and retailer bridges reconcile; all 303 protected files remain unchanged. [Machine-readable final review](../../Analysis/cost_failure_diagnosis/runs/2026-11-15_costdiag_01/final_review.json).
