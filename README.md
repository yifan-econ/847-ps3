# ECON 847 PS3: Bathroom Tissue Demand

Wenhan and Yifan's collaborative demand-estimation project using Dominick's toilet-paper data and Python.

## Start here

**Current priority:** the November 23 classroom presentation. The current deck is [revision 03](Presentation/2026-11-23/revision_03/README.md): PDF, editable source, tables, figures, previews and speaker notes. [Revision 02](Presentation/2026-11-23/revision_02/README.md) is preserved. Diagnosis is frozen; presenter agreement and a timed rehearsal are next. See [WORKPLAN](docs/WORKPLAN.md).

1. Start with the [collaboration hub](docs/README.md) and [current project status](docs/STATUS.md).
2. Read the [latest handoff](docs/handoffs/README.md) and [Wenhan's Chinese research baseline](docs/handoffs/2026-11-14-wenhan-baseline_zh.md).
3. Follow the [environment and execution guide](docs/SETUP.md) before running code.
4. Consult the [assignment](ps3.pdf) for course requirements.

The latest work completes an isolated [16-cell conditional merger exercise](Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01/REPORT.md), with 20 supply scenarios and linear-price welfare. Strong substitution, functional-form and cost-screen sensitivity prevents selecting a single credible merger estimate. Earlier mixed-logit results and all original research files are preserved.

The [cost-failure diagnosis](Analysis/cost_failure_diagnosis/runs/2026-11-15_costdiag_01/REPORT.md) traces Scott single-roll failures, separates retailer and demand assumptions, and reconciles high-share episodes to raw inputs. The research assessment remains conditional; no further model was estimated.

The latest [Fable feedback verification](Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_01/REPORT.md) corrects the accounting labels, verifies discount-related IV moments and physical-volume patterns, and narrows the reporting claim. Earlier result files are preserved; no additional demand specification was estimated.

The [numerical-selection follow-up](Analysis/cost_failure_diagnosis/reviews/2026-11-15_fable_02/REPORT.md) corrects the accepted-sample exception: cost-screen success on numerically accepted log/rho-zero markets is not independent validation. Report full-input failure magnitudes and the overlap with solver rejection. All historical numerical results remain preserved; no new estimation or equilibrium solve ran.

## Project map

| Location | Contents |
|---|---|
| [Data/](Data/README.md) | Original Dominick's data and codebook |
| [Paper/](Paper/README.md) | Reference papers |
| [Archive/](Archive/README.md) | Original v1 analysis and diagnostics; includes inputs still used by current code |
| [Analysis/](Analysis/README.md) | v2 cost IV, v3 pricing-zone IV, and v4 demographic mixed logit |
| [Conditional merger v5](Analysis/calibrated_merger_v5/README.md) | Calibrated nesting, retailer-margin scenarios, isolated runs and diagnostics |
| [Cost diagnosis](Analysis/cost_failure_diagnosis/README.md) | UPC/manufacturer attribution, retailer accounting and raw-input checks |
| [docs/](docs/README.md) | Status, workplan, dated handoffs, decisions, validation, and templates |
| [AGENTS.md](AGENTS.md) | Instructions for agents working on this repository |

Analysis versions keep code in `src/`, generated outputs in `results/`, and prepared inputs in `data/` where applicable. Directory names used by scripts have been retained. Large files use Git LFS; see [setup](docs/SETUP.md).

## Safe environment check

```sh
uv sync --locked
uv run --locked python scripts/check_environment.py
```

The check tests portability, prepares data read-only, predicts one market at saved parameters, and verifies that research files remain unchanged. It does not rerun estimation. Python and dependencies are pinned in `.python-version`, `pyproject.toml`, and `uv.lock`.
