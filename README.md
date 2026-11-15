# ECON 847 PS3: Bathroom Tissue Demand

Wenhan and Yifan's collaborative demand-estimation project using Dominick's toilet-paper data and Python.

## Start here

1. Start with the [collaboration hub](docs/README.md) and [current project status](docs/STATUS.md).
2. Read the [latest handoff](docs/handoffs/README.md) and [Wenhan's Chinese research baseline](docs/handoffs/2026-11-14-wenhan-baseline_zh.md).
3. Follow the [environment and execution guide](docs/SETUP.md) before running code.
4. Consult the [assignment](ps3.pdf) for course requirements.

The latest work completes an isolated [16-cell conditional merger exercise](Analysis/calibrated_merger_v5/runs/2026-11-15_16cell_01/REPORT.md), with 20 supply scenarios and linear-price welfare. Strong substitution, functional-form and cost-screen sensitivity prevents selecting a single credible merger estimate. Earlier mixed-logit results and all original research files are preserved.

## Project map

| Location | Contents |
|---|---|
| [Data/](Data/README.md) | Original Dominick's data and codebook |
| [Paper/](Paper/README.md) | Reference papers |
| [Archive/](Archive/README.md) | Original v1 analysis and diagnostics; includes inputs still used by current code |
| [Analysis/](Analysis/README.md) | v2 cost IV, v3 pricing-zone IV, and v4 demographic mixed logit |
| [Conditional merger v5](Analysis/calibrated_merger_v5/README.md) | Calibrated nesting, retailer-margin scenarios, isolated runs and diagnostics |
| [docs/](docs/README.md) | Status, workplan, dated handoffs, decisions, validation, and templates |
| [AGENTS.md](AGENTS.md) | Instructions for agents working on this repository |

Analysis versions keep code in `src/`, generated outputs in `results/`, and prepared inputs in `data/` where applicable. Directory names used by scripts have been retained. Large files use Git LFS; see [setup](docs/SETUP.md).

## Safe environment check

```sh
uv sync --locked
uv run --locked python scripts/check_environment.py
```

The check tests portability, prepares data read-only, predicts one market at saved parameters, and verifies that research files remain unchanged. It does not rerun estimation. Python and dependencies are pinned in `.python-version`, `pyproject.toml`, and `uv.lock`.
