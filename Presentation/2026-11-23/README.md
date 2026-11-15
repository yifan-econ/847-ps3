# November 23 presentation draft

This is the preserved first draft. Use [revision 02](revision_02/README.md) for the current talk, feedback response and rehearsal plan. Sharing statements below describe the first draft's original state.

Editable source: [main.tex](main.tex). Rendered slides: [presentation.pdf](presentation.pdf). [Speaker notes and storyboard](SPEAKER_NOTES.md) map all required assignment parts and allocate thirty minutes. Speaking roles are proposals, not accepted assignments. This is a first complete draft for collaborator review.

The six figures cover manufacturer package shares, a typical market, a Scott price/quantity series, first stages, merger-price sensitivity and Scott-single cost failures. Each has PDF/PNG exports and CSV values in `figures/`; [build_figures.py](build_figures.py) is editable. [Summary statistics](summary_statistics.json) and [matched assumption comparison](assumption_comparison.csv) give the underlying definitions and values. Curves and counts summarize saved outputs only; no demand fitting or equilibrium solving occurs.

## Build

From this directory, use a local TeX Live installation:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex
```

On Yifan's machine follow the TeX alias instructions in the local setup guide identified by AGENTS.md. The deck itself contains no machine-specific paths. After successful visual review copy `build/main.pdf` to `presentation.pdf`.

Figure generation uses the project uv environment plus an isolated plotting dependency, leaving pyproject.toml and uv.lock unchanged:

```sh
uv run --locked --with matplotlib==3.10.8 python Presentation/2026-11-23/build_figures.py
```

Run that command from the repository root in a new copied presentation directory: the script refuses to overwrite an existing `figures/` directory. Keep the directory at the same depth. `main_results.tex` records generated row values; the displayed table in main.tex uses the same rounded values and should be updated with them if source results change. Research source results are frozen for this talk.

## Remaining work

Collaborators review the narrative and industry context, confirm speaking roles, rehearse with a timer and check classroom legibility. No additional estimation is planned. An aggregation exercise is optional only after a reviewed full draft and rehearsal, with an explicit question and sufficient time. Current recommendation: omit it before this deadline.

The PDF was compiled and all slides visually inspected on Windows. No native Mac build or human rehearsal is claimed. See the [delivery validation](../../docs/validation/2026-11-15-presentation-draft.md) for exact scope. All changes remain local/uncommitted/unpushed.
