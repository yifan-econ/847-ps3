# 2026-11-15: Research review and documentation validation

Work ID: REVIEW-001. Platform: Windows-11-10.0.26300-SP0. Python: 3.13.9.
Branch: `codex/review-001-research-workplan`; base `14254a5f4177177fd2d9f0b14c598c299b219096`; documentation changes uncommitted.

## Checks

| Command or check | Outcome / evidence |
|---|---|
| `git fetch origin`, then `git rev-list --left-right --count HEAD...origin/main` | Fetch succeeded; `0 0`. Initial fetch needed sandbox escalation to write `.git/FETCH_HEAD`. Starting tree was clean. |
| `uv sync --locked` | Passed; resolved 15 packages, checked 14; no dependency-file changes. |
| `uv run --locked python scripts/check_environment.py` | Passed in 28.85 seconds. Six disposable tests; four preparation combinations matched saved audits; no estimation. |
| Saved-result prediction within that check | `all_packs__household__aac`, market `100_100`, 32 products; maximum share error `6.938893903907228e-18`. |
| Read-only CSV checks with `uv run --locked python -` | One-to-one join of six v4 estimates and independent diagnostics; all six converged; five joint-moment p-values below 0.05; all four income p-values below 0.001. |
| Paired elasticity calculation from saved CSV | `100 * (abs(other_zone median) / abs(aac median) - 1)`: 25.0% all-pack household, 32.5% all-pack income, 37.6% multipack income. No formal difference test. |
| Assignment extraction with `uv run --locked python -` and bundled `pypdf` | Read both pages; page 1 footnote allows omitting supply for a demand-only counterfactual; presentation length is 30 minutes. Used bundled pure-Python PDF dependencies through a process-local import path; project dependencies unchanged. |
| Static code review | Confirmed `run_mixed.py` writes shared demographic type files despite `--tag`; `validate_results.py` computes fixed-parameter 31-point shares and writes the legacy validation CSV. Neither script was executed as an estimator/validator in this round. |
| `git diff --check` and read-only documentation/path/hash check via `uv run --locked python -` | Passed. Seven Markdown-only changes under `docs/`; all 52 relative links in changed/new documents resolve; final research inventory still matches all 194 pre-check SHA256 hashes. |

Environment used by the safe check: NumPy 2.4.6, pandas 2.3.3, SciPy 1.18.1, PyBLP 1.2.0, statsmodels 0.14.6, filelock 3.32.7. Full ephemeral check output is in ignored `.local/validation/report.json` with before/after manifests and test output; this shared record contains the substantive evidence without requiring those local files.

## Sources and preservation

Research sources: [v2 estimates](../../Analysis/cost_iv_v2/results/estimates.csv), [v3 estimates](../../Analysis/paper_iv_v3/results/estimates.csv), [v4 estimates](../../Analysis/mixed_logit_v4/results/estimates.csv), [independent diagnostics](../../Analysis/mixed_logit_v4/results/independent_validation.csv), [final status](../../Analysis/mixed_logit_v4/results/final_status.json), [zero-sales audit](../../Archive/ps3_reference_update/Results/zero_and_elasticity_audit.json), [original baseline](../handoffs/2026-11-14-wenhan-baseline_zh.md), and [assignment](../../ps3.pdf). Both multipack household `rejected_fit.json` records were read.

All 194 files under the safe check's protected research inventory were byte-identical before/after. No estimations or counterfactuals ran. Baseline CSVs, saved models, inputs, PDFs, and failed fits were preserved. This is a documentation review, not a fresh independent re-estimation or a replication of all historical diagnostics.

## Limits and follow-up

- Joint-moment test interpretation uses the saved diagnostics and reviewed implementation; the six tests were not recomputed here. Conventional p-values do not prove instrument validity or strong identification.
- The safe check predicts one saved market; it does not establish new income quadrature/optimizer stability or validate all demand derivatives for a counterfactual.
- No native Mac or CI runtime check was performed. No new literature search or historical ownership research was performed.
- No final specification or counterfactual scope was selected. Claude feedback has not been received. Proposed deliverables are in [WORKPLAN.md](../WORKPLAN.md).
