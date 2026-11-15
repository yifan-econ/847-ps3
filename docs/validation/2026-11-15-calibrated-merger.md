# 2026-11-15: Conditional merger matrix validation

Work IDs: RUN-001, ENG-002, RES-002/004, CF-001. Platform: Windows 11, Python 3.13.9. Locked dependencies: NumPy 2.4.6, pandas 2.3.3, SciPy 1.18.1, PyBLP 1.2.0, FileLock 3.32.7. Branch `codex/run-001-calibrated-merger`, base `14254a5f4177177fd2d9f0b14c598c299b219096`, uncommitted/unpushed.

## Commands and scope

```sh
uv sync --locked
uv run --locked python -m unittest discover -s tests -p test_calibrated_merger.py -v
uv run --locked python Analysis/calibrated_merger_v5/src/run_design.py --run-id 2026-11-15_16cell_01
uv run --locked python Analysis/calibrated_merger_v5/src/validate_run.py --run-id 2026-11-15_16cell_01
uv run --locked python Analysis/calibrated_merger_v5/src/report_run.py --run-id 2026-11-15_16cell_01
uv run --locked python scripts/check_environment.py --output-dir .local/validation/2026-11-15_16cell_01
```

The six new synthetic tests passed before estimation. They verify demand derivatives against finite differences, ownership-block markups against dense inversion, an independently solved merger equilibrium and Hessian, linear welfare derivatives, market independence and a retailer-margin counterexample. The frozen run has a maximum of 600 damped iterations per solve, two post-merger starts and one unchanged-ownership reproduction solve; failures are preserved.

The safe environment checker now accepts a new evidence directory and refuses to overwrite it. Its isolated scratch evidence is copied into the run after the preservation check finishes; writing it directly into Analysis during the check would change the inventory being verified. Prior `.local/validation/` evidence remains untouched.

## Output checks

All commands completed successfully. The research run finished in 1,257.23 seconds (21.0 minutes), with 16 estimated demand cells, 20 supply scenarios, zero wrong-sign demand rejections and no run error. No additional cells or result-driven restarts ran.

| Check | Observed outcome |
|---|---|
| Six new synthetic tests before estimation | All passed |
| Saved-output validation | Passed all 20 scenarios; 12 deterministic accepted markets per scenario for independent dense/numerical checks |
| Largest dense markup discrepancy | 1.71e-14 dollars |
| Largest baseline/post dense FOC residual | 1.39e-16 / 1.53e-12 |
| Largest finite-difference Jacobian discrepancy | 6.00e-10 |
| Largest sampled firm-Hessian eigenvalue | -1.67e-5; all sampled Hessians negative definite |
| Largest independent share discrepancy | 1.11e-16 |
| Largest aggregate price-summary discrepancy | 5.55e-17 percentage points |
| Final safe environment check | Passed 12 tests, four read-only preparation combinations and one saved 32-product PyBLP prediction |
| Saved-market prediction discrepancy | 6.94e-18 |
| Final safe-check preservation | All 298 inventoried research files unchanged; 30.97 seconds; no estimation inside this check |
| Git whitespace check and shared-document links | Passed; all local targets in 35 Markdown files resolve; final 194-file SHA-256 recheck unchanged |

[Independent evidence](../../Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01/independent_validation.json) includes the SHA-256 of the exact [validator source](../../Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01/independent_validation_code.py). An earlier validation attempt was interrupted because arrays were being decompressed repeatedly in its market loop. Caching each array once fixed runtime without changing checks/tolerances. Both sources and the [attempt record](../../Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01/validation_attempts.json) are retained. No demand or simulation result was rerun or replaced.

The validator checks every scenario's saved acceptance flags, cost identities/screens, fringe prices and aggregate summaries. Independent dense FOC/markup and numerical derivative/Hessian checks cover 240 scenario-market cases, not every market independently. Saved full-sample FOC thresholds remain part of the runner's acceptance rule. [Environment evidence](../../Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01/environment_check/report.json) was copied into the run only after its check finished; those archival copies were therefore not part of its 298-file inventory.

## Findings and reporting correction

All scenarios share 7,960 numerically accepted markets (97.08% of baseline packages). Thirty-six markets fail at least one scenario, comprising 320 failed scenario-market combinations. The intersection additionally requiring every active effective cost nonnegative has 538 markets (5.61% of packages); requiring all manufacturer costs nonnegative leaves zero. These are distinct cost assumptions, not tests that identify the true model. See the [report](../../Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01/REPORT.md) for all cell-specific screens, pack diagnostics and price/welfare results.

The inherited fit helper computed its unused upward-slope reporting field from signed log price, incorrectly marking 37.8355% of rows in each log-price cell. Actual derivative formulas were correct and all 16 cells have downward demand. [Corrected estimates](../../Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01/estimates_corrected.csv) change only that derived field; the [correction audit](../../Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01/reporting_correction.json) preserves original values. Coefficients, standard errors, own elasticities, costs, equilibria and welfare are unchanged. The frozen execution source remains under code/; current source fixes the field for future runs.

## Preservation and limits

All new run products are under [the unique run root](../../Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01/). All 194 pre-existing v1–v4 outputs, code, data and PDFs are byte-identical under SHA-256 comparison. Negative costs and failed candidate equilibria remain saved; no clipping or favorable-result replacement is allowed. Code snapshots distinguish the implementation actually executed from subsequent reporting-only changes.

Numerical acceptance is conditional: it checks local profit curvature, not global Nash equilibrium or uniqueness. Rho is not estimated; 16 conditional fits have zero overidentification degrees of freedom. First-stage strength does not establish instrument exclusion. Cost screens use different meanings under dollar versus percentage margins. Log-price dollar welfare is absent. Runtime evidence here applies to Windows only.

Failed solver paths are never accepted or included in equilibrium summaries. If a path becomes numerically invalid, the engine may reset its saved prices to baseline solely to finish other markets; those flagged rows are placeholders, not recovered equilibria. No global best-response or uniqueness proof is claimed.
