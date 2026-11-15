# 2026-11-15: Windows portability and preservation

Work item: ENG-001. Platform: Windows 11, x86-64 (10.0.26300).
Python: CPython 3.13.9. uv: 0.12.19.
At validation time, the base commit was a5f6632 on main and the organization/portability changes were uncommitted. This record accompanies their subsequent delivery commit.
Machine-readable evidence: [report JSON](2026-11-15-windows-portability.json).

uv.lock SHA-256: `109bd104a40de51727091b381c029c90d40b92d506e71023a121be3e7b4ca9b2`.

## Environment

| Package | Installed |
|---|---|
| numpy | 2.4.6 |
| pandas | 2.3.3 |
| scipy | 1.18.1 |
| pyblp | 1.2.0 |
| statsmodels | 0.14.6 |
| filelock | 3.32.7 |

Python and the four recorded scientific-package versions match Wenhan's v4 environment record. The new lockfile also records transitive packages; the original environment record did not list all of those.

## Checks performed

| Command/check | Observed outcome |
|---|---|
| uv sync (initial creation) | Python downloaded, .venv created, 14 dependencies installed |
| uv pip check | All 14 installed packages compatible |
| uv lock --check --offline | Lock consistent with project metadata |
| uv run --locked --offline --no-sync python Analysis/mixed_logit_v4/src/run_mixed.py --help | CLI imports and exits successfully on Windows |
| uv run --locked --offline --no-sync python scripts/check_environment.py | Passed in 29.09 seconds |
| Disposable subprocess tests | Six passed: mutual exclusion/reacquisition, abrupt-exit release, stale marker, cached runner preservation, exception release, read-only validator default |
| Preparation | All four combinations matched existing sample_audit.csv |
| Saved PyBLP object | Loaded all_packs__household__aac; market 100_100, 32 products, maximum share error 6.94e-18 |
| Documentation/source checks | 94 local links resolved; original Chinese handoff text preserved apart from notice/link relocation; eight Python files compiled without execution; git diff --check passed |

Preparation counts: all packs 259,986 rows / 7,996 markets; multipacks 204,170 rows / 8,062 markets; 83 stores in each. Household/income agent counts matched the saved audit.

## Preservation

No estimator or optimizer was run. The environment checker prohibits calls to PyBLP Problem.solve, uses temporary lock/cache fixtures, and evaluates saved parameters only.

SHA-256 inventories before and after covered 194 files under Analysis, Archive, Data, and Paper (excluding Python bytecode caches). No files in that inventory changed, disappeared, or were added during the check. Full inventories and test output are local under .local/validation/. The three intended analysis changes were the runner lock, preparation-validator behavior, and filelock dependency declaration; existing result/data files were not edited.

## Limits

No native Mac runtime was available in this session. macOS support uses FileLock's platform backend and the shared lockfile, which includes Mac wheels; this is not Mac runtime evidence. The added Windows/macOS CI workflow has not executed yet.

This is an engineering/compatibility check, not a reproduction of all six fits, a full-estimation timing test, a test of every multiprocessing path, or validation of identification assumptions. Other legacy scripts can still overwrite outputs.
