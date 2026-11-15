# Collaboration workflow

Applies to Yifan, Wenhan, Codex, and Astra/Sol sessions using this repository. Decisions and evidence belong in Git-accessible files, not only in account-specific chats.

## Before work

- Read the root AGENTS.md, docs/STATUS.md, docs/WORKPLAN.md, and the latest dated handoff.
- Inspect `git status --short` and the current branch/commit. Preserve pre-existing local changes.
- Record the work ID, human collaborator/account, agent if useful, and intended scope in the next handoff. Assign work only when someone has accepted it.
- Prefer a separate branch per work item. For Codex-created branches, use `codex/<work-id>-<topic>`. Wenhan may use a distinct personal prefix.
- Fetch/reconcile shared changes before editing overlapping files. Do not reset or overwrite another collaborator's work to obtain a clean tree.

## Protect the research record

Existing v1–v4 outputs are the baseline. Portability checks and environment work must not rerun estimation or rewrite those outputs.

- The standard safe check is `uv run --locked python scripts/check_environment.py`. It hashes research files before/after, tests locks in temporary folders, prepares data read-only, and predicts one market using saved parameters.
- Preparation validation is read-only by default. Its `--write-artifacts` flag is an explicit write operation.
- Other existing scripts are not automatically read-only. In particular, v2/v3 estimation, v4 batch execution, validate_results.py, and report generators can write tracked files.
- Plan new research runs with a unique run ID and separate output location before execution. The current runner still defaults to legacy result paths; `--force` can overwrite them. A v4 `--tag` isolates specification output but does NOT isolate all shared data/type files.
- Preserve failed attempts and explain why a fit was rejected. Do not replace a baseline estimate just because a new result looks more plausible.
- Do not remove an OS lock file while another process may hold it. The lock coordinates processes on one machine, not two separate Git clones.

## Record the outcome

1. Update STATUS.md with new facts, clearly separating checked behavior from research interpretation.
2. Update the relevant WORKPLAN row and dependencies.
3. Add a dated file in handoffs/ from the template. Include changed paths, exact checks, result-preservation evidence, open issues, and the next concrete action.
4. Add a numbered decision when a durable modeling or engineering choice changes. Supersede old decisions explicitly.
5. Add a validation record for consequential changes; distinguish runtime testing from planned or CI-only checks.
6. Add links to the indexes and CHANGELOG.md. Use relative links so both machines can open them.

## Sharing and integration

Review the diff and run appropriate checks before sharing commits. Update dependencies through pyproject.toml and uv.lock together; use `uv sync --locked` on the receiving machine.

Git sharing is the handoff boundary: local files are not visible from the other account until committed and pushed or otherwise explicitly transferred. Record base commit/branch and whether changes were shared. Do not fabricate a commit ID for uncommitted work.

Do not change raw data or rewrite Git history as routine collaboration cleanup. Preserve conflicting research interpretations in the handoff and resolve them through an explicit decision.
