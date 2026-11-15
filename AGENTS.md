# Project instructions

Read README.md, docs/README.md, docs/STATUS.md, docs/WORKPLAN.md, and the latest dated handoff before substantive changes. Follow docs/COLLABORATION.md. Read the original Chinese baseline for research context.

- Use `uv` for Python environments, dependencies, and script execution; follow docs/SETUP.md.
- For LaTeX on Yifan's machine, consult `D:\dev\Documents\.env\TeX`. This is a local tool location, not a portable project dependency.
- Use `uv sync --locked` and `uv run --locked`; pyproject.toml, .python-version, and uv.lock define the shared environment. Do not commit .venv, .uv-cache, .uv-python, or .local.
- v4 uses FileLock for Windows/macOS compatibility. Windows runtime checks passed; record actual Mac evidence before claiming Mac runtime verification.
- For safe verification, run `uv run --locked python scripts/check_environment.py`. It uses disposable lock tests, read-only preparation, and saved-parameter prediction; it does not estimate models.
- Preserve original data, reference PDFs, and historical estimation outputs, including failed and exploratory fits.
- Archive/ps3_v1 contains active inputs, including the cleaned panel and UPC table. It is not disposable.
- Keep existing data/analysis paths unless a task requires migration and updates dependent paths and Git LFS attributes.
- Preparation validation is read-only by default; --write-artifacts overwrites preparation artifacts. Inspect other scripts: validators and estimation scripts may still write tracked outputs. Batch runs may retry expensive failed fits.
- For new research runs, isolate all outputs first. --tag does not isolate shared demographic type files. Preserve baseline results and record the run ID and environment.
- Convergence, negative price coefficients, and instrument strength do not establish identification. Current models are exploratory; supply-side/merger work is unfinished.
- Maintain docs/STATUS.md and docs/WORKPLAN.md in place. Add a dated handoff, consequential decisions, and validation evidence for meaningful rounds; update indexes and docs/CHANGELOG.md. Templates are in docs/templates/.
- Record collaborator/account, actual branch/base commit, changed paths, checks, unresolved work, and sharing state. Repository records must stand alone without access to either account's chats.
- Use repository-relative links and paths in shared documentation and code.
