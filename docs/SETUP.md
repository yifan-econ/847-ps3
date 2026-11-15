# Environment and safe execution

Targets: Windows and macOS. The user clarified that “iOS” meant a Mac. Run commands from the repository root; no virtual-environment activation is required.

## Install and synchronize

Install uv if needed using its [official instructions](https://docs.astral.sh/uv/getting-started/installation/), then:

```sh
uv sync --locked
```

The project pins Python 3.13.9 in .python-version. pyproject.toml pins NumPy 2.4.6, pandas 2.3.3, SciPy 1.18.1, and PyBLP 1.2.0 to Wenhan's [recorded environment](../Analysis/mixed_logit_v4/results/environment.json). uv.lock pins all resolved dependencies, including filelock 3.32.7 and statsmodels 0.14.6.

The project is a script collection, not an installable Python package. The root uv project is authoritative; per-analysis requirements files remain for historical compatibility.

The first sync may download Python and packages. uv 0.12.19 was used for the Windows setup. The local interpreter was downloaded under ignored .uv-python/ because this session's filesystem permissions required project-local storage; collaborators can let uv use its usual managed-Python location. Never copy .venv between machines or operating systems.

The [uv documentation](https://docs.astral.sh/uv/concepts/projects/sync/) explains --locked: it fails if project metadata and the lockfile disagree rather than silently updating the lock.

## Data checkout

The full data check requires actual Git LFS objects, not pointer files:

```sh
git lfs install
git lfs pull
```

The small portability tests below do not need LFS data.

## Safe checks

```sh
uv pip check
uv run --locked python -m unittest discover -s tests -v
uv run --locked python Analysis/mixed_logit_v4/src/run_mixed.py --help
uv run --locked python scripts/check_environment.py
```

The full environment check:

- hashes the research files before and after;
- tests inter-process exclusion, crash/exception release, stale lock files, and cached execution using disposable directories;
- prepares all four sample/demographic combinations without writing saved artifacts and compares them to the saved sample audit;
- loads one trusted repository PyBLP result and predicts one market at saved parameters;
- writes evidence only to ignored .local/validation/.

No estimation runs. The current Windows check passed; see [the validation record](validation/2026-11-15-windows-portability.md). Run the same commands on Wenhan's Mac and add a new record for CHECK-001.

For preparation alone:

```sh
uv run --locked python Analysis/mixed_logit_v4/src/validate_preparation.py
```

This is now read-only by default. --write-artifacts intentionally overwrites the legacy audit/manifest files. Avoid Python's -O mode because preparation validation uses assertions.

After installation, --offline --no-sync can be added to uv run for local checks without resolving or installing packages.

## Platform behavior

The runner uses [FileLock](https://py-filelock.readthedocs.io/en/latest/) at the existing per-specification run.lock path. Its context manager releases the native lock on return or exception. Acquisition remains blocking. This fixes the direct Unix-only import on Windows while retaining macOS support.

A lock only coordinates local writers to that path. It is not a Git collaboration lock, and it does not protect every shared data/type file. Do not manually remove a lock while a process could hold it.

[The CI workflow](../.github/workflows/portability.yml) runs disposable tests and CLI import checks on Windows and macOS after changes are shared. It skips LFS downloads and never launches estimations. Check GitHub Actions for its current status; no CI result was evaluated in the original local validation.

## Estimation is a separate step

Existing v2/v3 estimators, v4 batch execution, validate_results.py, and report generators can write tracked outputs. They were not run in this setup. --force can overwrite saved fits; --tag does not isolate shared demographic type files. Follow [the collaboration workflow](COLLABORATION.md) and isolate all new-run outputs before executing research runs.

## LaTeX

On Yifan's Windows machine, consult `D:\dev\Documents\.env\TeX` for LaTeX compilation. Collaborators should use their own local TeX installation.
