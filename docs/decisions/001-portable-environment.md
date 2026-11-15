# 001: Portable Python environment and locking

Date: 2026-11-15. Status: accepted for this implementation. Work item: ENG-001.

## Context

The user requested Windows and macOS support (clarified that “iOS” meant Mac), uv setup, and checks without rerunning estimation or overwriting Wenhan's results. The mixed-logit entry point imported Unix-only fcntl, preventing import on Windows.

## Decision

- Use FileLock around the entire per-specification execution, including the cache check, at the existing run.lock path. A context manager releases the lock on return or exception.
- Preserve blocking acquisition behavior. Native OS locking releases on process exit; an old lock filename is not by itself an active lock.
- Pin Python 3.13.9 and Wenhan's recorded NumPy 2.4.6, pandas 2.3.3, SciPy 1.18.1, and PyBLP 1.2.0 in project configuration. Resolve all dependencies in uv.lock.
- Use filelock as a dependency rather than maintaining separate platform-specific locking code. See the [official platform documentation](https://py-filelock.readthedocs.io/en/latest/).
- Use `uv sync --locked` and `uv run --locked`; these reject stale lock metadata rather than silently resolving a different environment. See [uv's documentation](https://docs.astral.sh/uv/concepts/projects/sync/).
- Make preparation validation read-only by default; retain explicit --write-artifacts for intentional regeneration.

## Limits

The lock coordinates a local specification directory. It does not coordinate separate Git clones or all shared type-file writes. Native Windows runtime evidence is recorded separately; actual macOS execution still needs confirmation. Matching package versions does not establish numerical equivalence of a full optimization across platforms.
