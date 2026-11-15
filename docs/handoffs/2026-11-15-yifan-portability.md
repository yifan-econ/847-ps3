# 2026-11-15: Yifan / Codex — portability and collaboration setup

- Work IDs: ENG-001, COLLAB-001; follow-up CHECK-001.
- Account/collaborator: Yifan; agent: Codex.
- Branch/base: main at a5f6632.
- Delivery branch: main, shared at Yifan's request. This handoff accompanies the implementation commit; use `git log -1 -- docs/handoffs/2026-11-15-yifan-portability.md` to identify it after pulling.
- Starting state: the prior organization round already had uncommitted documentation moves and new folder guides. Those changes were preserved.

## Request and implementation

The user requested Windows and “iOS” support, clarified to macOS, a uv environment, non-destructive checks, and structured docs for collaboration with Wenhan's Astra/Sol sessions.

- Analysis/mixed_logit_v4/src/run_mixed.py: replaced direct fcntl import/locking with FileLock and a context-managed run_locked boundary. Retained the existing lock location and blocking behavior; estimation math is unchanged.
- Analysis/mixed_logit_v4/src/validate_preparation.py: moved work behind a main guard, made validation callable and read-only by default, and retained explicit --write-artifacts for intentional regeneration.
- pyproject.toml, .python-version, uv.lock: established the shared environment; local .venv is installed. The v4 requirements file also includes filelock.
- tests/test_portability.py: six disposable lock/cache/default-behavior tests.
- scripts/check_environment.py: read-only data preparation, saved-result prediction, and before/after research-file hashing.
- .github/workflows/portability.yml: Windows/macOS unit/import checks, with no LFS data download or estimation.
- docs/: added a collaboration hub, current status/workplan, dated handoffs, decisions, validation records, and templates. Old handoff filenames redirect; the original Chinese content remains in the dated baseline.
- AGENTS.md and README.md: current workflow and environment entry points.

## Evidence and research status

[Windows validation](../validation/2026-11-15-windows-portability.md) passed. Six tests, four preparation combinations, and one saved-parameter market prediction succeeded. All 194 files covered by the preservation check stayed unchanged. No estimation ran.

Scientific-package versions match Wenhan's recorded v4 environment. No research specification, instrument, ownership assumption, or final model was selected. All prior identification and numerical caveats remain.

## Next concrete actions

1. Pull main after preserving any local work. Start with AGENTS.md and docs/README.md, then read this handoff and docs/STATUS.md.
2. On Wenhan's Mac, run uv sync --locked and uv run --locked python scripts/check_environment.py. Add a dated Mac validation record and update CHECK-001. Check GitHub Actions for the separate Windows/macOS CI results; they were not evaluated in this handoff.
3. Before a new estimation round, implement full output isolation (ENG-002). The existing --tag option still writes shared demographic type files.
4. Agree ownership of the research-review work in WORKPLAN.md. Do not silently treat the engineering fixes as model validation.

## 给 Wenhan 的 ChatGPT：接手检查

先读根目录 `AGENTS.md`、`docs/README.md`、本交接文件，以及 `docs/STATUS.md`。本轮只整理协作文档、修复跨平台文件锁、配置 uv 环境并做只读核验；没有重新估计模型，也没有覆盖原有结果。原中文研究交接保存在 `docs/handoffs/2026-11-14-wenhan-baseline_zh.md`。

在 Mac 上依次运行 `uv sync --locked` 和 `uv run --locked python scripts/check_environment.py`。完整数据核验需要 Git LFS 文件已下载。请将实际 Mac 核验结果写入新的 `docs/validation/` 记录，并更新 `CHECK-001`；不要运行全量 batch、`--force` 或 `--write-artifacts`。后续新估计需先解决完整输出隔离（ENG-002）。

## Durable decisions

- [001: portable environment and locking](../decisions/001-portable-environment.md)
- [002: baseline preservation and repository handoffs](../decisions/002-baseline-and-handoffs.md)
