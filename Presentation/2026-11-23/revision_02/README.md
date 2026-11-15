# Revised presentation for November 23

Current [PDF](presentation.pdf), [editable Beamer source](main.tex), and [speaker notes / source map](SPEAKER_NOTES.md). Fifteen main slides target 25.5 minutes, leaving discussion time; three backup slides cover retailer margins, mixed logit and welfare. [First draft](../README.md) remains preserved.

This revision responds to [Fable's supplied review](fable_feedback.txt). It adds demand estimates and first stages with standard errors, pack-size elasticities, the worked Scott cost example, calendar dates, price-variation summary, and an explicit link between price predictions and cost failures. It simplifies classroom wording and proposes an earlier rough rehearsal. Current preview sheets in `previews/` are generated from this PDF.

Build from this folder with `latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex`. Follow the local TeX setup named in AGENTS.md on Yifan's machine. No local installation path is required by the source.

For a new reproduction directory at the same depth, run from the repository root:

```sh
uv run --locked --with matplotlib==3.10.8 python Presentation/2026-11-23/revision_02/build_figures.py
uv run --locked python Presentation/2026-11-23/revision_02/prepare_tables.py
```

These extraction scripts refuse existing output paths. The optional `--offline` flag uses an already cached plotting environment. Existing outputs stay isolated; pyproject.toml and uv.lock are unchanged. Chart CSVs and exact table values accompany the source. OLS was not refitted; no demand model or equilibrium was re-estimated. The original first draft and all historical research outputs remain preserved.

The current round is prepared for the user-authorized local commit on `codex/deliv-001-beamer`; the user will push. Historical manifests describe their own earlier sharing state. Collaborator review, speaking allocation and timed rehearsal remain pending.
